from __future__ import annotations

import argparse
import os
import requests

from dotenv import load_dotenv
from enum import StrEnum
from random import choices
from time import sleep
from typing import Type

from tools.client import AzureDevOpsClient, BitbucketClient, Client, ConfluenceClient, GitHubClient, GitLabClient

load_dotenv()


NUM_RESOURCES = os.environ.get('NUM_RESOURCES') or '100'        # How many resources to generate on the provider
DATA_SOURCE_NAME = os.environ.get('DATA_SOURCE_NAME')
DATA_SOURCE_TYPE = os.environ.get('DATA_SOURCE_TYPE')
CONNECTION_URL = os.environ.get('CONNECTION_URL')

AUTH_TOKEN = os.environ.get('AUTH_TOKEN')


class DataSourceType(StrEnum):
    GITHUB_CLOUD = 'github_cloud', 'GitHub Cloud', 'cloud', GitHubClient
    GITHUB_ENTERPRISE = 'github_enterprise', 'GitHub Enterprise Server', 'self_managed', GitHubClient
    BITBUCKET_CLOUD = 'bitbucket_cloud', 'Bitbucket Cloud', 'cloud', BitbucketClient
    BITBUCKET_SERVER = 'bitbucket_server', 'Bitbucket Server', 'self_managed', BitbucketClient
    GITLAB_CLOUD = 'gitlab_cloud', 'GitLab Cloud', 'cloud', GitLabClient
    GITLAB_ONPREM = 'gitlab_onprem', 'GitLab Self-managed Server', 'self_managed', GitLabClient
    AZURE_DEVOPS_CLOUD = 'azure_devops_cloud', 'Azure DevOps Cloud', 'cloud', AzureDevOpsClient
    # GERRIT_SERVER = 'gerrit_server', 'Gerrit Server', 'self_managed'
    CONFLUENCE_CLOUD = 'confluence_cloud', 'Confluence Cloud', 'cloud', ConfluenceClient
    # CONFLUENCE_SERVER = 'confluence_server', 'Confluence Server', 'self_managed'

    def __new__(cls, value: str, readable_name: str, server_type: str, client: Type[Client]) -> DataSourceType:
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.readable_name = readable_name
        obj.server_type = server_type
        obj.client = client
        return obj

    def is_self_managed(self) -> bool:
        return self.server_type.casefold() == 'self_managed'


if __name__ == '__main__':
    """
    Generates resources on the data source provider, i.e. repositories on GitHub, spaces on Confluence, etc
    
    Please set the following environment variables (or manually update the script's default values)
    * NUM_RESOURCES - number of resources to generate on the provider
    * DATA_SOURCE_NAME - the name of the data source i.e. organization on GitHub, the workspace on Bitbucket, etc
    * DATA_SOURCE_TYPE - the type of the data source, i.e. github_cloud, github_enterprise, etc.
    * CONNECTION_URL - the domain of the self-managed instance if the data source type is self-managed
        (i.e. github.acme.com for a GitHub Enterprise Server instance)
    * AUTH_TOKEN - token in the format that the provider will accept, i.e. PAT for GitHub
    
    Variables that are not set but required you may be prompted for
    Run `python3 -m tools.generate` with Python 3.11+ to execute this script
    
    Make sure you have requests installed - https://pypi.org/project/requests/ 
      as well as python-dotenv - https://pypi.org/project/python-dotenv/
    """
    parser = argparse.ArgumentParser()

    data_source_type = DataSourceType(DATA_SOURCE_TYPE) if DATA_SOURCE_TYPE else None
    if not data_source_type:
        for i, data_source_type in enumerate(list(DataSourceType)):
            print(f'{i + 1}. {data_source_type.readable_name}')

        index = input('Choose your data source type: ')
        while not index.isdigit() or int(index) not in range(1, len(DataSourceType) + 1):
            index = input(f'Please pick a data source type from 1 - {len(DataSourceType)}: ')

        data_source_type = list(DataSourceType)[int(index) - 1]

    data_source_name = DATA_SOURCE_NAME
    if not DATA_SOURCE_NAME:
        data_source_name = input('Input your data source name: ')

    connection_url = CONNECTION_URL or ''
    if data_source_type.is_self_managed():
        if not connection_url:
            connection_url = input('Input your connection url (i.e. github.acme.com): ')

        connection_url = 'https://' + connection_url

    auth_token = AUTH_TOKEN
    if not auth_token:
        auth_token = input('Input your auth token: ')

    num_resources = int(NUM_RESOURCES)

    print(
        f'Proceeding with data source type: {data_source_type}, '
        f'data source name: {data_source_name}, '
        f'connection URL: {connection_url}, and auth token: {auth_token[:3]}***. '
        f'Generating {num_resources} resources on the provider for this data source. '
    )

    words_txt = requests.get('https://www.mit.edu/~ecprice/wordlist.10000')
    words = words_txt.content.decode('utf-8').splitlines()

    client = data_source_type.client(connection_url=connection_url, auth_token=auth_token)
    client.set_session()
    for i in range(num_resources):
        resource_name = '-'.join(choices(words, k=4))
        print(f'[{i}/{NUM_RESOURCES}] Creating resource with name: {resource_name}')
        client.create_resource(data_source_name=data_source_name, resource_name=resource_name)

        sleep(1)

    print(f'Completed generating {NUM_RESOURCES} resources')
