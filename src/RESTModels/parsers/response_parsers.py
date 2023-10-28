from typing import TypeVar, Type, Any

from .type_alias_parsers import TypeAliasParser


T = TypeVar("T")


class ResponseParser:
    def __init__(self, type_aliases_parser: TypeAliasParser) -> None:
        self.type_aliases_parser = type_aliases_parser

    def __call__(self, response: Any, expected_type: Type[T]) -> T:  # TODO: Type it correctly!
        if isinstance(expected_type, type) and isinstance(response, expected_type):
            return response

        try:
            return self.type_aliases_parser(response, expected_type)

        except (TypeError, ValueError) as error:
            raise ValueError(
                f"Can't convert value {response} with "
                f"type {type(response)} to expected {expected_type}"
            ) from error
