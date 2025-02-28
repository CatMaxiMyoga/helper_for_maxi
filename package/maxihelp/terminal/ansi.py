r"""Contains Utility Classes"""

from __future__ import annotations
import sys
from typing import override

from ..decorators import check_params


class ANSICode:
    r"""
    Represents an ANSI code

    Holds an ANSI code value you can print to the terminal or combine with
    strings.

    Attributes:
        value: The actual ANSI code
    """

    @check_params()
    def __init__(self, value: str) -> None:
        r"""
        Initializes the ANSICode object

        Args:
            value: The ANSI code following the escape character.

        Raises:
            `ValueError`: `value` string is empty
            `TypeError`: Invalid type for `value`
        """

        if not value:
            name = self.__class__.__name__
            raise ValueError(
                f"{name} cannot be initialized with a falsy `value`."
            )

        self.__value = "\033[" + value

    @property
    def value(self) -> str:
        return self.__value

    def __repr__(self) -> str:
        return self.value

    def __call__(self) -> None:
        sys.stdout.write(self.value)
        sys.stdout.flush()


class ANSIColorCode(ANSICode):
    r"""
    Represents an ANSI color code

    Holds an ANSI color code value you can print to the terminal or combine
    with other strings, as well as other ANSIColorCode instances.

    Attributes:
        value: The actual ANSI code
        codes: List of all ANSI color code integers.
        is_RGB: Whether or not the represented color code is an RGB color code.
    """

    @check_params
    def __init__(self, *codes: int) -> None:
        r"""
        Initializes the ANSIColorCode object

        Args:
            *codes: The colon-separated color codes as integers

        Raises:
            `ValueError`: No values given for `codes` or invalid
            `TypeError`: Items of `codes` have invalid types
        """

        if not codes:
            name = self.__class__.__name__
            raise ValueError(
                f"{name} cannot be initialized without values for '*codes'"
            )

        if not self._validate_codes(*codes):
            raise ValueError(
                "Invalid ANSI Color / Graphics mode codes given for '*codes'"
            )

        self.__codes: list[int] = list(codes)
        self.__isrgb: bool = (
            True if codes[0] in [48, 38] and codes[1] == 2 else False
        )

    @check_params
    @staticmethod
    def _validate_codes(*codes: int) -> bool:
        code = ";".join(map(str, codes))

        if code.startswith("38;2") or code.startswith("48;2"):
            if len(codes) != 5 or not all(0 <= x <= 255 for x in codes[2:]):
                return False
            return True

        for c in codes:
            if not (
                0 <= c <= 7
                or 30 <= c <= 37
                or 40 <= c <= 47
                or 90 <= c <= 97
                or 100 <= c <= 107
                or (c == 38 or c == 48)
            ):
                return False

        return True

    @property
    @override
    def value(self) -> str:
        return f"\033[{";".join(map(str, self.__codes))}m"

    @property
    def codes(self) -> list[int]:
        return self.__codes

    @property
    def is_RGB(self) -> bool:
        return self.__isrgb

    def __add__(self, other: str | "ANSIColorCode") -> str | "ANSIColorCode":
        if isinstance(other, str):
            return other + self.value

        elif isinstance(other, ANSIColorCode):
            if self.is_RGB or other.is_RGB:
                raise ValueError(
                    "Combining of RGB ANSI Color Codes not supported!\n"
                    "Validation only supports ANSI color codes OR rgb codes!"
                )

            return ANSIColorCode(*(other.codes + self.codes))

        raise TypeError(
            f"Cannot add value of type {str(type(other).__name__)} to an "
            f"ANSIColorCode object!"
        )

    def __radd__(self, other: str | "ANSIColorCode") -> str | "ANSIColorCode":
        if isinstance(other, str):
            return self.value + other

        elif isinstance(other, ANSIColorCode):
            if self.is_RGB or other.is_RGB:
                raise ValueError(
                    "Combining of RGB ANSI Color Codes not supported!\n"
                    "Validation only supports ANSI color codes OR rgb codes!"
                )

            return ANSIColorCode(*(self.codes + other.codes))

        raise TypeError(
            f"Cannot add value of type {str(type(other).__name__)} to an "
            f"ANSIColorCode object!"
        )


__all__ = ["ANSICode", "ANSIColorCode"]
