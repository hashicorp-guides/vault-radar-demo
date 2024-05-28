from dataclasses import dataclass
from http import HTTPStatus


from .auth import BasicAuth
from .client import Client


@dataclass
class AzureDevOpsClient(Client):

    def create_resource(self, data_source_name: str, resource_name: str) -> None:
        """Makes API request to third-party provider to create a resource"""
        if not self.session:
            self.set_session()

        # https://learn.microsoft.com/en-us/rest/api/azure/devops/git/repositories/create?view=azure-devops-rest-7.1&tabs=HTTP
        if self.connection_url:
            raise Exception('No self-managed Azure DevOps available')

        response = self.session.post(
            f'https://dev.azure.com/{data_source_name}/_apis/git/repositories?api-version=7.1-preview.1',
            json={'name': resource_name},
            auth=BasicAuth(self.auth_token),
        )

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)
