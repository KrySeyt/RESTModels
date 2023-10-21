from http import HTTPMethod
from abc import ABC, abstractmethod
from typing import Any

import requests


class Client(ABC):
    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    def request(
            self,
            endpoint_path: str,
            method: HTTPMethod,
            params: dict[str, Any],
            body: dict[str, Any] | str = ""
    ) -> Any:

        match method:
            case HTTPMethod.GET:
                return self.get(endpoint_path, params)
            case HTTPMethod.POST:
                return self.post(endpoint_path, params, body)
            case HTTPMethod.DELETE:
                return self.delete(endpoint_path, params, body)
            case HTTPMethod.PUT:
                return self.put(endpoint_path, params, body)
            case HTTPMethod.PATCH:
                return self.patch(endpoint_path, params, body)

    @abstractmethod
    def get(self, endpoint_path: str, params: dict[str, Any]) -> Any:
        raise NotImplementedError

    @abstractmethod
    def post(self, endpoint_path: str, params: dict[str, Any], body: dict[str, Any] | str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def delete(self, endpoint_path: str, params: dict[str, Any], body: dict[str, Any] | str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def put(self, endpoint_path: str, params: dict[str, Any], body: dict[str, Any] | str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def patch(self, endpoint_path: str, params: dict[str, Any], body: dict[str, Any] | str) -> Any:
        raise NotImplementedError


class SyncClient(Client):
    def get(self, endpoint_path: str, params: dict[str, Any]) -> Any:
        response = requests.get(self.api_url + endpoint_path, params=params)
        return response.json()

    def post(self, endpoint_path: str, params: dict[str, Any], body: dict[str, Any] | str) -> Any:
        response = requests.post(self.api_url + endpoint_path, params=params, json=body)
        return response.json()

    def delete(self, endpoint_path: str, params: dict[str, Any], body: dict[str, Any] | str) -> Any:
        response = requests.delete(self.api_url + endpoint_path, params=params, json=body)
        return response.json()

    def put(self, endpoint_path: str, params: dict[str, Any], body: dict[str, Any] | str) -> Any:
        response = requests.put(self.api_url + endpoint_path, params=params, json=body)
        return response.json()

    def patch(self, endpoint_path: str, params: dict[str, Any], body: dict[str, Any] | str) -> Any:
        response = requests.patch(self.api_url + endpoint_path, params=params, json=body)
        return response.json()
