from enum import Enum

from .clients import Client


class ResourceModel:
    def __init__(self, client: Client) -> None:
        self.client = client


class BodyType(Enum):
    EMBEDDED = "EMBEDDED"
    FLAT = "FLAT"
