from typing import (
    ParamSpec,
    TypeVar,
    Sequence,
    Callable,
    Type,
    get_type_hints
)
from http import HTTPMethod
from inspect import signature
from functools import partial

from .resources import BodyType
from .parsers.args_parsers import get_args_dict
from .parsers.response_parsers import ResponseParser
from .builders import build_body, build_path


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

            response = model.client.request(path, request_type, params, request_body)
            expected_type: Type[ReturnType] = get_type_hints(func)["return"]  # mb get from inspect.signature?
            response_parser = ResponseParser()

            return response_parser(response, expected_type)

        return request

    return decorator


get = partial(create_request_decorator, request_type=HTTPMethod.GET)
post = partial(create_request_decorator, request_type=HTTPMethod.POST)
delete = partial(create_request_decorator, request_type=HTTPMethod.DELETE)
put = partial(create_request_decorator, request_type=HTTPMethod.PUT)
patch = partial(create_request_decorator, request_type=HTTPMethod.PATCH)
