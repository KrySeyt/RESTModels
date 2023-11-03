from typing import TypeVar, Type, Any, cast
from types import GenericAlias

from .type_alias_parsers import TypeAliasParser


T = TypeVar("T")


class ResponseParser:
    def __init__(self, type_alias_parser: TypeAliasParser) -> None:
        self.type_alias_parser = type_alias_parser

    def __call__(self, response: Any, expected_type: Type[T]) -> T:
        if isinstance(expected_type, type) and isinstance(response, expected_type):
            return response

        try:
            type_alias = cast(GenericAlias, expected_type)
            return self.type_alias_parser(response, type_alias)  # type: ignore[no-any-return]

        except ValueError as error:
            raise ValueError(
                f"Can't convert response {response} with "
                f"type {type(response)} to expected {expected_type}"
            ) from error
