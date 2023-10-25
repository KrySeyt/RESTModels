from collections import ChainMap
from typing import TypeVar, Type, Any

from .types_parsers import TypeParser


T = TypeVar("T")


class ResponseParser:
    general_types_parsers: dict[Any, TypeParser] = {}  # TODO: Type it correctly!

    def __init__(self) -> None:
        self.types_parsers: dict[Any, TypeParser] = {}  # TODO: Type it correctly!

    def register_type_parser(self, expected_type: Any, parser: TypeParser) -> None:  # TODO: Type it correctly!
        self.types_parsers[expected_type] = parser

    @classmethod
    def register_general_type_parser(cls, expected_type: Any, parser: TypeParser) -> None:  # TODO: Type it correctly!
        cls.general_types_parsers[expected_type] = parser

    # TODO: Type it correctly!
    def __call__(self, response: Any, expected_type: Type[T]) -> T:
        if isinstance(response, expected_type):
            return response

        try:
            parsers = ChainMap(self.types_parsers, self.general_types_parsers)

            if expected_type not in parsers:
                raise TypeError(
                    f"Has not type parser (TypeParser) for type {expected_type}. "
                    f"Perhaps you forgot {self}.register(expected_type, type_parser)?"
                )

            parser = parsers[expected_type]
            return parser(response)  # type: ignore[no-any-return]

        except TypeError as error:
            raise TypeError(
                f"Can't convert value {response} with "
                f"type {type(response)} to expected {expected_type}"
            ) from error
