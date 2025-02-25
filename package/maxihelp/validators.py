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
        allowed_types: The types of parameters allowed to use this Validator.
    """

    error_message = "Parameter {} does not match specified regex pattern!"
    allowed_types = [str]

    def __init__(self, regex: str, flags: re._FlagsType = 0) -> None:
        r"""
        Initializes the Validator.

        Args:
            regex: The regex to match the parameter with.
            flags: The flags passed to `re.fullmatch()`
        """
        self.regex = regex
        self.flags = flags

    def validate(self, name: str, value: str) -> str | None:
        valid = re.match(self.regex, value, self.flags)

        if valid:
            return None

        return self.error_message.format(repr(name))


class IntRangeValidator(Validator):
    r"""
    Checks if the parameter is in the given range

    Attributes:
        error_message: The message the Validator returns if validation failed.
        allowed_types: The types of parameters allowed to use this Validator.
    """

    error_message = "Parameter {} is out of range ({};{})"
    allowed_types = [int]

    def __init__(self, min: int, max: int) -> None:
        r"""
        Initializes the Validator.

        Args:
            min: The minimum of the range. Inclusive
            max: The maximum of the range. Inclusive
        """
        self.min = min
        self.max = max

    def validate(self, name: str, value: int) -> str | None:
        valid = self.min <= value <= self.max

        if valid:
            return None

        return self.error_message.format(repr(name), self.min, self.max)


class FloatRangeValidator(Validator):
    r"""
    Checks if the parameter is in the given range

    Attributes:
        error_message: The message the Validator returns if validation failed.
        allowed_types: The types of parameters allowed to use this Validator.
    """

    error_message = "Parameter {} is out of range {}"
    allowed_types = [float]

    def __init__(
        self,
        min: float,
        max: float,
        inclusive: tuple[bool, bool] = (True, True),
    ) -> None:
        r"""
        Initializes the validator.

        Args:
            min: The minimum of the range
            max: The maximum of the range
            inclusive: Whether or not `min` and `max` are inclusive or
              exclusive. First item is `min`, second item is `max`.
        """

        self.min = min
        self.max = max
        self.inclusive = inclusive

    def validate(self, name: str, value: float) -> str | None:
        valid = (
            value >= self.min if self.inclusive[0] else value > self.min
        ) and (value <= self.max if self.inclusive[1] else value < self.max)

        if valid:
            return None

        num_range = (
            f"{"[" if self.inclusive[0] else "]"}{self.min:.2f};"
            f"{self.max:.2f}{"]" if self.inclusive[1] else "["}"
        )

        return self.error_message.format(repr(name), num_range)


class DictValidator(Validator):
    r"""
    Checks if the parameter's keys and values fit the given structure.

    Attributes:
        error_message: The message the Validator returns if validation failed.
        allowed_types: The types of parameters allowed to use this Validator.
    """

    error_message = "Parameter {} does not fit the given validation structure."
    allowed_types = [dict]
    __structure_type = dict[str, type[Any] | tuple[type[Any], None] | "__structure_type"]

    def __init__(self, structure: __structure_type) -> None:


__all__ = [
    "Validator",
    "RegexValidator",
    "IntRangeValidator",
    "FloatRangeValidator",
]
