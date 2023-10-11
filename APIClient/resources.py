import re
from enum import Enum
from inspect import signature
from typing import Callable, TypeVar, Any, get_type_hints, Sequence, Iterable, ParamSpec, Mapping
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

    pattern = re.compile(r"\{\w+}")
    matches = re.findall(pattern, composed_path)
    for match in matches:
        param = params.pop(match[1:-1]) if exclude_params else params[match[1:-1]]
        composed_path = composed_path.replace(match, str(param))

    return composed_path


def build_body(
        body_params: Iterable[str],
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

        case BodyType.FLAT:
            param_name = next(iter(body_params))
            param = params.pop(param_name) if exclude_params else params[param_name]
            return str(param)


ArgsType = ParamSpec("ArgsType")
ReturnType = TypeVar("ReturnType")


def get(endpoint_path: str) -> Callable[
    [
        Callable[ArgsType, ReturnType]
    ],
    Callable[ArgsType, ReturnType]
]:

    def request_decorator(func: Callable[ArgsType, ReturnType]) -> Callable[ArgsType, ReturnType]:
        def request(*args: ArgsType.args, **kwargs: ArgsType.kwargs) -> ReturnType:
            params = get_args_dict(signature(func).parameters.keys(), args, kwargs)
            path = build_path(endpoint_path, params, exclude_params=True)
            model = params.pop("self")

            data = model.client.get(path, params)

            if not isinstance(data, get_type_hints(func)["return"]):
                raise ValueError

            return data  # type: ignore

        return request

    return request_decorator


def post(endpoint_path: str, body: Sequence[str], body_type: BodyType = BodyType.EMBEDDED) -> Callable[
    [
        Callable[ArgsType, ReturnType]
    ],
    Callable[ArgsType, ReturnType]
]:

    if len(body) > 1 and body_type is BodyType.FLAT:
        raise ValueError("BodyType.RAW cannot be set with more than one body param")

    def request_decorator(func: Callable[ArgsType, ReturnType]) -> Callable[ArgsType, ReturnType]:
        def request(*args: ArgsType.args, **kwargs: ArgsType.kwargs) -> ReturnType:
            params = get_args_dict(signature(func).parameters.keys(), args, kwargs)
            path = build_path(endpoint_path, params, exclude_params=True)
            model = params.pop("self")
            request_body = build_body(body, params, body_type, exclude_params=True)

            data = model.client.post(path, params, request_body)

            if not isinstance(data, get_type_hints(func)["return"]):
                raise ValueError

            return data  # type: ignore

        return request

    return request_decorator