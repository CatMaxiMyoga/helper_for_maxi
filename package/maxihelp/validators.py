r"""Contains all Validators usable in `.decorators.check_params()`"""

from collections.abc import Callable
import re
from typing import Any, Protocol


class Validator(Protocol):
    error_message: str
    allowed_types: list[type[Any]]

    def validate(self, name: str, value: Any) -> str | None: ...


class CustomValidator[T]:
    r"""
    Uses `callback` to validate parameters.

    Attrubutes:
        error_message: The message the Validator returns if validation failed.
        allowed_types: The types of parameters allowed to use this validator.
    """

    error_message = "Validation for Parameter {} failed."
    allowed_types = [Any]

    def __init__(self, callback: Callable[[T], bool]) -> None:
        self.callback = callback

    def validate(self, name: str, value: T) -> str | None:
        valid = self.callback(value)

        if valid:
            return None

        return self.error_message.format(repr(name))


class LengthValidator:
    r"""
    Validates the length of a string or list.

    Attrubutes:
        error_message: The message the Validator returns if validation failed.
        allowed_types: The types of parameters allowed to use this validator.
    """

    error_message = "Parameter {} has invalid length."
    allowed_types = [str, list]

    def __init__(self, length: int | tuple[int, int]) -> None:
        self.length = length if isinstance(length, tuple) else (length, length)

    def validate(self, name: str, value: str | list[Any]) -> str | None:
        valid = self.length[0] <= len(value) <= self.length[1]

        if valid:
            return None

        return self.error_message.format(repr(name))


class RegexValidator:
    r"""
    Uses `re.fullmatch()` to validate parameters.

    Attributes:
        error_message: The message the Validator returns if validation failed.
        allowed_types: The types of parameters allowed to use this Validator.
    """

    error_message = "Parameter {} does not match specified regex pattern!"
    allowed_types = [str]

    def __init__(self, regex: str, flags: int = 0) -> None:
        r"""
        Initializes the Validator.

        Args:
            regex: The regex to match the parameter with.
            flags: The flags passed to `re.fullmatch()`
        """
        self.regex = regex
        self.flags = flags

    def validate(self, name: str, value: str) -> str | None:
        valid = re.fullmatch(self.regex, value, self.flags)

        if valid:
            return None

        return self.error_message.format(repr(name))


class DateRangeValidator:
    r"""
    Checks if the parameter is in the given range

    Attributes:
        error_message: The message the Validator returns if validation failed.
        allowed_types: The types of parameters allowed to use this Validator.
    """


class IntRangeValidator:
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


class FloatRangeValidator:
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
        valid = all(
            [
                value >= self.min if self.inclusive[0] else value > self.min,
                value <= self.max if self.inclusive[1] else value < self.max,
            ]
        )

        if valid:
            return None

        def get_num_str(num: float) -> str:
            if 0.01 <= abs(num) < 1000:
                return str(num)

            return f"{num:.3e}"

        num_range = (
            f"{"[" if self.inclusive[0] else "]"}{get_num_str(self.min)};"
            f"{get_num_str(self.max)}{"]" if self.inclusive[1] else "["}"
        )

        return self.error_message.format(repr(name), num_range)


__all__ = [
    "Validator",
    "CustomValidator",
    "LengthValidator",
    "RegexValidator",
    "IntRangeValidator",
    "FloatRangeValidator",
]
