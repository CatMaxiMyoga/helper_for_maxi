r"""Contains all Validators usable in `.decorators.check_params()`"""

import re
from typing import Any, Protocol


class Validator(Protocol):
    error_message: str
    allowed_types: list[type[Any]]

    def validate(self, name: str, value: Any) -> str | None: ...


class RegexValidator(Validator):
    r"""
    Uses `re.fullmatch()` to validate parameters.

    Attributes:
        error_message: The message the Validator returns if validation failed.
    """

    error_message = "Parameter {} does not match specified regex pattern!"
    allowed_types = [str]

    def __init__(self, regex: str, flags: re._FlagsType = 0) -> None:
        self.regex = regex
        self.flags = flags

    def validate(self, name: str, value: str) -> str | None:
        valid = re.match(self.regex, value, self.flags)

        if valid:
            return None

        return self.error_message.format(repr(name))


__all__ = ["Validator", "RegexValidator"]
