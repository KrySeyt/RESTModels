from .requests import (
    get,
    post,
    delete,
    put,
    patch
)
from .resources import ResourceModel
from .clients import SyncClient
from .parsers.type_alias_parsers import TypeAliasParser

__all__ = [
    "get",
    "post",
    "delete",
    "put",
    "patch",
    "ResourceModel",
    "SyncClient",
    "register_general_type_parser",
]

register_general_type_parser = TypeAliasParser.register_general_type_parser
