from typing import Callable, Any
from datetime import datetime


TypeParser = Callable[[Any], Any]  # TODO: Type it correctly!


class TypeParseError(ValueError):
    def __init__(self, value_for_parse: Any, expected_type: type, *args: Any, **kwargs: Any) -> None:
        super().__init__(
            f"Can't parse {value_for_parse} with type {type(value_for_parse)} to {expected_type}",
            *args,
            *kwargs
        )


def bytes_parser(value: Any) -> bytes:
    if isinstance(value, str):
        return value.encode(encoding="utf-8")
    raise TypeParseError(value, bytes)


def datetime_parser(value: Any) -> datetime:
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    raise TypeParseError(value, bytes)
