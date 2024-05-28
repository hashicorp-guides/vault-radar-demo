from dataclasses import dataclass
from http import HTTPStatus


from .auth import BasicAuth
from .client import Client


@dataclass
class BitbucketClient(Client):

    def create_resource(self, data_source_name: str, resource_name: str) -> None:
        """Makes API request to third-party provider to create a resource"""
        if not self.session:
            self.set_session()

        # https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/#api-repositories-workspace-repo-slug-post
        base_url = f'https://api.bitbucket.org/2.0/repositories/{data_source_name}/{resource_name}'
        body = {'scm': 'git'}
        if self.connection_url:
            # https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-rest.html#idm8287395680
            base_url = self.connection_url + f'/rest/api/1.0/projects/{data_source_name}/repos'
            body = {'name': resource_name, 'scmId': 'git'}

        response = self.session.post(
            base_url, json=body, auth=BasicAuth(self.auth_token)
        )

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)
