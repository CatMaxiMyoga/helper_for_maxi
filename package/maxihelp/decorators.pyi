from collections.abc import Callable
from typing import Any, Optional

from .validators import Validator

def check_params(
    special_validation: Optional[dict[str, Validator]],
    *,
    force_annotations: bool = True,
    validate_return: bool = True,
    **kwargs: Validator,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...
