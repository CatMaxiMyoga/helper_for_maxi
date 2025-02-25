import re
from typing import Any, Protocol

class Validator(Protocol):
    error_message: str
    allowed_types: list[type[Any]]

    def validate(self, name: str, value: Any) -> str | None: ...

class RegexValidator(Validator):
    error_message: str
    allowed_types: list[type[Any]]

    def __init__(self, regex: str, flags: re._FlagsType = 0) -> None: ...
    def validate(self, name: str, value: str) -> str | None: ...

class IntRangeValidator(Validator):
    error_message: str
    allowed_types: list[type[Any]]

    def __init__(self, min: int, max: int) -> None: ...
    def validate(self, name: str, value: str) -> str | None: ...

class FloatRangeValidator(Validator):
    error_message: str
    allowed_types: list[type[Any]]

    def __init__(
        self,
        min: float,
        max: float,
        inclusive: tuple[bool, bool] = (True, True),
    ) -> None: ...
    def validate(self, name: str, value: str) -> str | None: ...
