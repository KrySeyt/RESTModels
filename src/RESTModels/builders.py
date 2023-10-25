import re
from typing import Any, Collection

from .resources import BodyType


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
