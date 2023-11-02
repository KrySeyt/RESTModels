from inspect import get_annotations
from decimal import Decimal
from typing import Any, Type, TypeVar, get_origin, Protocol, cast
from datetime import datetime, date, time, timedelta
from collections import ChainMap
from types import GenericAlias
from itertools import zip_longest


class TypeAliasParseError(ValueError):
    def __init__(self, value_for_parse: Any, expected_type: type, *args: Any, **kwargs: Any) -> None:
        super().__init__(
            f"Can't parse {value_for_parse} with type {type(value_for_parse)} to {expected_type}",
            *args,
            **kwargs
        )


T = TypeVar("T")


class TypeParserProtocol(Protocol):
    def __call__(
            self,
            value: Any,
            alias: GenericAlias,
            alias_parser: "TypeAliasParser",
    ) -> Any:
        """
        :param value: response body as json.loads(request.body)
        :param alias: GenericAlias that describes expected result type
        :param alias_parser: TypeAliasParser object that called your type parser
        :return:
        """

        raise NotImplementedError


class TypeAliasParser:
    general_types_parsers: dict[type, TypeParserProtocol] = {}

    def __init__(self) -> None:
        self.types_parsers: dict[type, TypeParserProtocol] = {}

    def register_type_parser(self, parser: TypeParserProtocol) -> None:
        expected_type_alias = get_annotations(parser)["return"]
        expected_type = get_origin(expected_type_alias) or expected_type_alias
        self.types_parsers[expected_type] = parser

    @classmethod
    def register_general_type_parser(cls, parser: TypeParserProtocol) -> None:
        expected_type_alias = get_annotations(parser)["return"]
        expected_type = get_origin(expected_type_alias) or expected_type_alias
        cls.general_types_parsers[expected_type] = parser

    def __call__(self, value: Any, expected_type: Type[T]) -> T:
        parsers = ChainMap(self.types_parsers, self.general_types_parsers)

        type_alias = cast(GenericAlias, expected_type)
        most_general_type = get_origin(type_alias) or expected_type

        if most_general_type not in parsers:
            raise ValueError(
                f"Has not type parser (TypeParser) for type {type_alias}. "
                f"Perhaps you forgot {self}.register(expected_type, type_parser)?"
            )

        parser = parsers[most_general_type]
        return parser(value, alias=type_alias, alias_parser=self)  # type: ignore[no-any-return]


@TypeAliasParser.register_general_type_parser
def str_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> str:
    return str(value)


@TypeAliasParser.register_general_type_parser
def int_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> int:
    return int(value)


@TypeAliasParser.register_general_type_parser
def bool_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> bool:
    return bool(value)


@TypeAliasParser.register_general_type_parser
def float_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> float:
    return float(value)


@TypeAliasParser.register_general_type_parser
def decimal_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> Decimal:
    return Decimal(value)


@TypeAliasParser.register_general_type_parser
def bytes_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> bytes:
    if isinstance(value, str):
        return value.encode(encoding="utf-8")
    raise TypeAliasParseError(value, bytes)


@TypeAliasParser.register_general_type_parser
def datetime_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    raise TypeAliasParseError(value, datetime)


@TypeAliasParser.register_general_type_parser
def date_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> date:
    if isinstance(value, str):
        return date.fromisoformat(value)
    raise TypeAliasParseError(value, date)


@TypeAliasParser.register_general_type_parser
def time_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> time:
    if isinstance(value, str):
        return time.fromisoformat(value)
    return time(value)


@TypeAliasParser.register_general_type_parser
def timedelta_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> timedelta:
    return timedelta(value)


@TypeAliasParser.register_general_type_parser
def tuple_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> tuple[Any, ...]:
    if hasattr(alias, "__args__"):
        values = []
        for elem, elem_type in zip_longest(value, alias.__args__):
            if (elem is None or elem_type is None) and not isinstance(elem, elem_type):
                raise TypeAliasParseError(value, tuple)
            values.append(alias_parser(elem, elem_type))
        return tuple(values)

    return tuple(value)


@TypeAliasParser.register_general_type_parser
def list_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> list[Any]:
    if hasattr(alias, "__args__"):
        origin_type_alias = alias.__args__[0]
        return [alias_parser(elem, origin_type_alias) for elem in value]

    return list(value)


@TypeAliasParser.register_general_type_parser
def set_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> set[Any]:
    if hasattr(alias, "__args__"):
        origin_type_alias = alias.__args__[0]
        return {alias_parser(elem, origin_type_alias) for elem in value}

    return set(value)


@TypeAliasParser.register_general_type_parser
def frozenset_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> frozenset[Any]:
    if hasattr(alias, "__args__"):
        origin_type_alias = alias.__args__[0]
        return frozenset(alias_parser(elem, origin_type_alias) for elem in value)

    return frozenset(value)


@TypeAliasParser.register_general_type_parser
def none_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> None:
    return
