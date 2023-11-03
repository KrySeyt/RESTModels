from typing import Union
from datetime import datetime, date, time, timedelta
from decimal import Decimal

import pytest

from RESTModels.parsers.type_alias_parsers import TypeAliasParser


def test_parse_str():
    type_alias_parser = TypeAliasParser()

    data = "text"
    expected_type = str

    expected_result = "text"

    assert type_alias_parser(data, expected_type) == expected_result


def test_parse_bytes():
    type_alias_parser = TypeAliasParser()

    data = "text"
    expected_type = bytes

    expected_result = b"text"

    assert type_alias_parser(data, expected_type) == expected_result


def test_parse_int():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        "5",
        5,
    )
    expected_type = int

    expected_result = 5

    for data in input_datas:
        assert type_alias_parser(data, expected_type) == expected_result


def test_parse_float():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        "5",
        5,
        5.0,
    )
    expected_type = float

    expected_result = 5

    for data in input_datas:
        assert type_alias_parser(data, expected_type) == expected_result


def test_parse_bool():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        "text",
        5,
        0,
        1,
        True,
        False,
        []
    )
    expected_type = bool

    expected_results = (True, True, False, True, True, False, False)

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result


def test_parse_decimal():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        "5",
        5,
        5.0
    )
    expected_type = Decimal

    expected_results = (5, 5, 5)

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result


def test_parse_datetime():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        "2023-10-22T19:50:29.182993",
        "2023-10-22T19:50:29.182993Z",
    )
    expected_type = datetime

    expected_results = (
        datetime.fromisoformat("2023-10-22T19:50:29.182993"),
        datetime.fromisoformat("2023-10-22T19:50:29.182993Z"),
    )

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result


def test_parse_date():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        "2023-10-22",
    )
    expected_type = date

    expected_results = (
        date.fromisoformat("2023-10-22"),
    )

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result


def test_parse_time():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        "19:50:29.182993",
        "19:50:29.182993Z",
        23,
        time(15),
    )
    expected_type = time

    expected_results = (
        time.fromisoformat("19:50:29.182993"),
        time.fromisoformat("19:50:29.182993Z"),
        time(23),
        time(15),
    )

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result


def test_parse_timedelta():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        23,
        timedelta(15),
    )
    expected_type = timedelta

    expected_results = (
        timedelta(23),
        timedelta(15),
    )

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result


def test_parse_none():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        23,
        timedelta(15),
        5.0,
        Decimal("13.567"),
        [],
        {},
    )
    expected_type = None

    expected_results = (None,) * 6

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result


def test_simple_parse_tuple():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        [1, 2],
        ["ez"],
    )
    expected_type = tuple

    for result in (type_alias_parser(data, expected_type) for data in input_datas):
        assert isinstance(result, expected_type)


def test_simple_parse_list():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        (1, 2),
        ("ez",),
    )
    expected_type = list

    for result in (type_alias_parser(data, expected_type) for data in input_datas):
        assert isinstance(result, expected_type)


def test_simple_parse_set():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        (1, 2),
        ("ez",),
    )
    expected_type = set

    expected_results = ({1, 2}, {"ez"})

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result


def test_simple_parse_frozenset():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        (1, 2),
        ("ez",),
        "test"

    )
    expected_type = frozenset

    expected_results = (frozenset((1, 2)), frozenset(("ez",)), frozenset("test"))

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result


def test_parse_tuple_with_nested():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        ["1"],
        {5},
    )
    expected_type = tuple[int]

    expected_results = (
        (1,),
        (5,),
    )

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result

    dt = datetime.fromisoformat("2023-10-22T19:50:29.182993")
    input_datas = (
        [dt, "5"],
        ["2023-10-22T19:50:29.182993", "5"],
    )
    expected_type = tuple[datetime, int]

    expected_results = (
        (dt, 5),
        (dt, 5),
    )

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result

    with pytest.raises(ValueError):
        type_alias_parser([5, "str"], tuple[str, int])


def test_parse_list_with_nested():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        ["1"],
        ["1", "2", "3"],
        (5, 6.0, "10"),
    )
    expected_type = list[int]

    expected_results = (
        [1],
        [1, 2, 3],
        [5, 6, 10],
    )

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result

    input_data = [[1, 2], ["3", "4"]]
    expected_type = list[list[int]]

    expected_result = [
        [1, 2],
        [3, 4],
    ]

    assert type_alias_parser(input_data, expected_type) == expected_result


def test_parse_set_with_nested():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        ["1"],
        ["1", "2", "3"],
        (5, 6.0, "10"),
    )
    expected_type = set[int]

    expected_results = (
        {1},
        {1, 2, 3},
        {5, 6, 10},
    )

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result

    input_data = [[1, 2], ["3", "4"]]
    expected_type = list[set[int]]

    expected_result = [
        {1, 2},
        {3, 4},
    ]

    assert type_alias_parser(input_data, expected_type) == expected_result


def test_parse_frozenset_with_nested():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        ["1"],
        ["1", "2", "3"],
        (5, 6.0, "10"),
    )
    expected_type = frozenset[int]

    expected_results = (
        frozenset((1,)),
        frozenset((1, 2, 3)),
        frozenset((5, 6, 10),),
    )

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result

    input_data = [[1, 2], ["3", "4"]]
    expected_type = list[set[int]]

    expected_result = [
        frozenset((1, 2)),
        frozenset((3, 4)),
    ]

    assert type_alias_parser(input_data, expected_type) == expected_result


def test_parse_nested_collections():
    type_alias_parser = TypeAliasParser()

    input_data = [
        [
            [
                5, 10,
            ]
        ],
        [
            15,
        ]
    ]
    expected_type = tuple[tuple[tuple[str, str]], tuple[str]]

    expected_result = (
        (
            (
                "5", "10",
            ),
        ),
        (
          "15",
        ),
    )

    assert type_alias_parser(input_data, expected_type) == expected_result


def test_parse_old_union():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        "test",
        15,
        6.3,

    )
    expected_type = Union[int, str, float]

    expected_results = (
        "test",
        15,
        6,
    )

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result


def test_parse_new_union():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        "test",
        15,
        6.3,

    )
    expected_type = int | str | float

    expected_results = (
        "test",
        15,
        6,
    )

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result
