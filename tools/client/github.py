from dataclasses import dataclass
from http import HTTPStatus

from .auth import BearerAuth
from .client import Client


@dataclass
class GitHubClient(Client):
    def create_resource(self, data_source_name: str, resource_name: str) -> None:
        """Makes API request to third-party provider to create a resource"""
        if not self.session:
            self.set_session()

        # https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#create-an-organization-repository
        base_url = 'https://api.github.com'
        if self.connection_url:
            base_url = self.connection_url + '/api/v3'

        response = self.session.post(
            f'{base_url}/orgs/{data_source_name}/repos',
            json={'name': resource_name},
            auth=BearerAuth(self.auth_token)
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)
