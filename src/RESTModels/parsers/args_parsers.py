from typing import Iterable, Sequence, Any, Mapping


def get_args_dict(
        function_args_names: Iterable[str],
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
) -> dict[str, Any]:

    params = {**kwargs}
    for i, param in enumerate(function_args_names):
        params[param] = args[i]
    return params
