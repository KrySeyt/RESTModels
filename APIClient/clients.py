from abc import ABC, abstractmethod
from typing import Any

import requests


class Client(ABC):
    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    @abstractmethod
    def get(self, endpoint_path: str, params: dict[str, Any]) -> Any:
        raise NotImplementedError

    @abstractmethod
    def post(self, endpoint_path: str, params: dict[str, Any], body: dict[str, Any]) -> Any:
        raise NotImplementedError


class SyncClient(Client):
    def get(self, endpoint_path: str, params: dict[str, Any]) -> Any:
        response = requests.get(self.api_url + endpoint_path, params=params)
        return response.json()

    def post(self, endpoint_path: str, params: dict[str, Any], body: dict[str, Any] | str) -> Any:
        response = requests.post(self.api_url + endpoint_path, params=params, json=body)
        return response.json()
