from collections.abc import Callable


def check_params[R](func: Callable[..., R]) -> Callable[..., R]: ...
