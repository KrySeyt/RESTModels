from typing import Any, Type, TypeVar, get_origin, Protocol, cast
from datetime import datetime
from collections import ChainMap
from types import GenericAlias
from itertools import zip_longest


class TypeAliasParseError(ValueError):
    def __init__(self, value_for_parse: Any, expected_type: type, *args: Any, **kwargs: Any) -> None:
        super().__init__(
            f"Can't parse {value_for_parse} with type {type(value_for_parse)} to {expected_type}",
            *args,
            *kwargs
        )


T = TypeVar("T")


class TypeParserProtocol(Protocol):
    def __call__(
            self,
            value: Any,
            alias: GenericAlias,
            alias_parser: "TypeAliasParser",
    ) -> Any:  # TODO: Type it correctly!

        raise NotImplementedError


class TypeAliasParser:
    general_types_parsers: dict[Any, TypeParserProtocol] = {}

    def __init__(self) -> None:
        self.types_parsers: dict[Any, TypeParserProtocol] = {}

    def register_type_parser(self, expected_type: Any, parser: TypeParserProtocol) -> None:  # TODO: Type it correctly!
        self.types_parsers[expected_type] = parser

    # TODO: Type it correctly!
    @classmethod
    def register_general_type_parser(cls, expected_type: Any, parser: TypeParserProtocol) -> None:
        cls.general_types_parsers[expected_type] = parser

    def __call__(self, value: Any, expected_type: Type[T]) -> T:
        parsers = ChainMap(self.types_parsers, self.general_types_parsers)
        type_ = get_origin(expected_type) or expected_type

        if type_ not in parsers:
            raise TypeError(
                f"Has not type parser (TypeParser) for type {expected_type}. "
                f"Perhaps you forgot {self}.register(expected_type, type_parser)?"
            )

        type_alias = cast(GenericAlias, expected_type)
        parser = parsers[type_]
        return parser(value, alias=type_alias, alias_parser=self)  # type: ignore[no-any-return]


# TODO: Types, types, types!
def str_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> Any:
    return str(value)


def int_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> Any:
    return int(value)


def float_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> Any:
    return float(value)


def bytes_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> Any:
    if isinstance(value, str):
        return value.encode(encoding="utf-8")
    raise TypeAliasParseError(value, bytes)


def datetime_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> Any:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    raise TypeAliasParseError(value, datetime)


def tuple_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> Any:
    if hasattr(alias, "__args__"):
        values = []
        for elem, elem_type in zip_longest(value, alias.__args__):
            if (elem is None or elem_type is None) and type(elem) != elem_type:
                raise TypeAliasParseError(value, tuple)
            values.append(alias_parser(elem, elem_type))
        return tuple(values)

    return tuple(value)


def list_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> Any:
    if hasattr(alias, "__args__"):
        origin_type_alias = alias.__args__[0]
        return [alias_parser(elem, origin_type_alias) for elem in value]

    return list(value)


def set_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> Any:
    if hasattr(alias, "__args__"):
        origin_type_alias = alias.__args__[0]
        return {alias_parser(elem, origin_type_alias) for elem in value}

    return set(value)
