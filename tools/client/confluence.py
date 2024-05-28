from dataclasses import dataclass
from http import HTTPStatus

from .auth import BasicAuth, BearerAuth
from .client import Client


@dataclass
class ConfluenceClient(Client):
    def create_resource(self, data_source_name: str, resource_name: str) -> None:
        """Makes API request to third-party provider to create a resource"""
        if not self.session:
            self.set_session()

        # https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-space/#api-wiki-rest-api-space-post
        base_url = f'https://{data_source_name}.atlassian.net/wiki'
        auth = BasicAuth(self.auth_token)
        if self.connection_url:
            # https://docs.atlassian.com/ConfluenceServer/rest/8.7.2/#api/space-createSpace
            base_url = self.connection_url
            auth = BearerAuth(self.auth_token)

        resource_key = resource_name.title().replace('-', '')
        response = self.session.post(
            f'{base_url}/rest/api/space', json={'key': resource_key, 'name': resource_name}, auth=auth
        )

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)
