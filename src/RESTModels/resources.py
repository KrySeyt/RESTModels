import re
from functools import partial
from http import HTTPMethod
from enum import Enum
from inspect import signature
from typing import (
    Callable,
    TypeVar,
    Any,
    Sequence,
    Iterable,
    ParamSpec,
    Mapping,
    Collection,
    NoReturn,
    Type,
    get_type_hints
)

from .clients import Client


class ResourceModel:
    def __init__(self, client: Client) -> None:
        self.client = client


class BodyType(Enum):
    EMBEDDED = "EMBEDDED"
    FLAT = "FLAT"


def get_args_dict(
        function_args_names: Iterable[str],
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
) -> dict[str, Any]:
    params = {**kwargs}
    for i, param in enumerate(function_args_names):
        params[param] = args[i]
    return params


def build_path(path_pattern: str, params: dict[str, Any], exclude_params: bool = False) -> str:
    composed_path = path_pattern

    matches = re.findall(r"\{\w+}", composed_path)
    for match in matches:
        param = params.pop(match[1:-1]) if exclude_params else params[match[1:-1]]
        composed_path = composed_path.replace(match, str(param))

    return composed_path


def build_body(  # type: ignore[return]
        body_params: Collection[str],
        params: dict[str, Any],
        body_type: BodyType,
        exclude_params: bool = False
) -> dict[str, Any] | str:
    match body_type:
        case BodyType.EMBEDDED:
            body: dict[str, Any] = {}
            for body_param_name in body_params:
                body[body_param_name] = params.pop(body_param_name) if exclude_params else params[body_param_name]
            return body

        case BodyType.FLAT if len(body_params) <= 1:
            param_name = next(iter(body_params))
            param = params.pop(param_name) if exclude_params else params[param_name]
            return str(param)

        case BodyType.FLAT if len(body_params) > 1:
            raise ValueError(f"{body_type} cannot be set with more than one body param")

        case _:
            raise ValueError(f"Can't build body with type {body_type}")


ExpectedType = TypeVar("ExpectedType")


def try_parse_response_content(  # TODO: mb protocol?
        response_content: Any,
        expected_type: Callable[..., ExpectedType]
) -> ExpectedType | NoReturn:

    try:
        return expected_type(response_content)
    except TypeError:
        pass

    if isinstance(response_content, Mapping):
        try:
            return expected_type(**response_content)
        except TypeError:
            pass

    if isinstance(response_content, Iterable):
        try:
            return expected_type(*response_content)
        except TypeError:
            pass

    raise TypeError(f"Can't convert value {response_content} with "
                    f"type {type(response_content)} to expected {expected_type}")


ArgsType = ParamSpec("ArgsType")
ReturnType = TypeVar("ReturnType")


def create_request_decorator(
        endpoint_path: str,
        request_type: HTTPMethod,
        body: Sequence[str] = tuple(),
        body_type: BodyType = BodyType.EMBEDDED,
) -> Callable[
    [
        Callable[ArgsType, ReturnType]
    ],
    Callable[ArgsType, ReturnType]
]:

    def decorator(func: Callable[ArgsType, ReturnType]) -> Callable[ArgsType, ReturnType]:
        def request(*args: ArgsType.args, **kwargs: ArgsType.kwargs) -> ReturnType:
            params = get_args_dict(signature(func).parameters.keys(), args, kwargs)
            path = build_path(endpoint_path, params, exclude_params=True)
            model = params.pop("self")
            request_body = build_body(body, params, body_type, exclude_params=True)

            data = model.client.request(path, request_type, params, request_body)
            expected_type: Type[ReturnType] = get_type_hints(func)["return"]

            return try_parse_response_content(data, expected_type)

        return request

    return decorator


get = partial(create_request_decorator, request_type=HTTPMethod.GET)
post = partial(create_request_decorator, request_type=HTTPMethod.POST)
delete = partial(create_request_decorator, request_type=HTTPMethod.DELETE)
put = partial(create_request_decorator, request_type=HTTPMethod.PUT)
patch = partial(create_request_decorator, request_type=HTTPMethod.PATCH)
