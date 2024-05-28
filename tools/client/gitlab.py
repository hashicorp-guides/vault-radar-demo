from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional

import json

from .auth import BearerAuth
from .client import Client


@dataclass
class GitLabClient(Client):
    _namespace_id: Optional[int] = None

    def _get_namespace_id(self, data_source_name: str) -> int:
        if not self._namespace_id:
            base_url = f'https://gitlab.com'
            if self.connection_url:
                base_url = self.connection_url

            response = self.session.get(
                f'{base_url}/api/v4/groups/{data_source_name}',
                auth=BearerAuth(self.auth_token)
            )

            self._namespace_id = json.loads(response.content.decode('utf-8')).get('id')
        return self._namespace_id

    def create_resource(self, data_source_name: str, resource_name: str) -> None:
        """Makes API request to third-party provider to create a resource"""
        if not self.session:
            self.set_session()

        namespace_id = self._get_namespace_id(data_source_name=data_source_name)

        # https://docs.gitlab.com/ee/api/projects.html#create-project
        base_url = f'https://gitlab.com'
        if self.connection_url:
            base_url = self.connection_url

        response = self.session.post(
            f'{base_url}/api/v4/projects?name={resource_name}&namespace_id={namespace_id}',
            auth=BearerAuth(self.auth_token)
        )

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)
