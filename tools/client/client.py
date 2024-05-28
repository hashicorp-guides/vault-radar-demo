from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import requests


@dataclass
class Client(ABC):
    connection_url: str
    auth_token: str

    session: Optional[requests.Session] = None

    def set_session(self):
        self.session = requests.Session()

    @abstractmethod
    def create_resource(self, data_source_name: str, resource_name: str) -> None:
        """Makes API request to third-party provider to create a resource"""
        pass

