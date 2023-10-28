import datetime

import pytest

from RESTModels.parsers.type_alias_parsers import TypeAliasParser


def test_parse_str():
    type_alias_parser = TypeAliasParser()

    data = "text"
    expected_type = str

    expected_result = "text"

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
    expected_type = int

    expected_result = 5

    for data in input_datas:
        assert type_alias_parser(data, expected_type) == expected_result


def test_parse_datetime():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        "2023-10-22T19:50:29.182993",
        "2023-10-22T19:50:29.182993Z",
    )
    expected_type = datetime.datetime

    expected_results = (
        datetime.datetime.fromisoformat("2023-10-22T19:50:29.182993"),
        datetime.datetime.fromisoformat("2023-10-22T19:50:29.182993Z"),
    )

    for data, expected_result in zip(input_datas, expected_results):
        assert type_alias_parser(data, expected_type) == expected_result


def test_parse_tuple():
    type_alias_parser = TypeAliasParser()

    input_datas = (
        [1, 2],
        ["ez"],
    )
    expected_type = tuple

    for result in (type_alias_parser(data, expected_type) for data in input_datas):
        assert type(result) == expected_type


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

    dt = datetime.datetime.fromisoformat("2023-10-22T19:50:29.182993")
    input_datas = (
        [dt, "5"],
        ["2023-10-22T19:50:29.182993", "5"],
    )
    expected_type = tuple[datetime.datetime, int]

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


def test_parse_nested_collections():
    type_alias_parser = TypeAliasParser()

    input_data = [
        [
            [
                "test", "nested",
            ]
        ],
        [
            "another",
        ]
    ]
    expected_type = tuple[tuple[tuple[str, str]], tuple[str]]

    expected_result = (
        (
            (
                "test", "nested",
            ),
        ),
        (
          "another",
        ),
    )

    assert type_alias_parser(input_data, expected_type) == expected_result
