import builtins
import time
from typing import Any

from .decorators import check_params
from .terminal.ansi import ANSIColorCode


@check_params()
def print(
    *values: Any, sep: str = " ", delay_ms: int = 100, end: str = "\n"
) -> None:
    r"""
    Prints `values` separated by `sep` character for character with the given
      `delay_ms` between each character.

    Args:
        *values: The objects to print.
        sep: The seperator used to join objects together.
          Default: `" "`
        delay_ms: The delay between each printed character in milliseconds.
          Default: `100` (0.01 seconds)
        end: What to print at the end.
          Default: `"\n"`

    Note:
        Overrides the default `print()` function (`builtins.print`) if imported
          directly and without using `as`
    """

    if not values:
        return builtins.print(end, end="")

    for char in sep.join(map(str, values)):
        print(char, end="", flush=True)
        time.sleep(delay_ms)

    print(end, end="")


@check_params()
def input(prompt: Any = "", delay_ms: int = 100) -> str:
    r"""
    Gets an input in a stylistic way.

    Prints the given `prompt` character for character with the given `delay_ms`
      before getting and returning the user's input.

    Args:
        prompt: The prompt to print before waiting for user input.
          Default: `""`
        delay_ms: The delay between each printed character in milliseconds.
          Default: `100` (0.01 seconds)

    Returns:
        The user's input as a string.

    Note:
        Overrides the default `input()` function (`builtins.input`) if imported
          directly and without using `as`
    """

    if prompt:
        print(prompt, end="", delay_ms=delay_ms)

    return builtins.input()


@check_params()
def color_input(
    prompt: Any = "",
    delay_ms: int = 100,
    input_color: ANSIColorCode = ANSIColorCode(36),
    text_after_color: ANSIColorCode = ANSIColorCode(0),
) -> str:
    """
    Gets an input in a stylistic and colorful way.

    Prints the given `prompt` character for character with the given `delay_ms`
      before setting the text color for the user's input to `input_color` and
      then getting the user's input before setting the text color for all
      following text to `text_after_color`.

    Args:
        prompt: The prompt to print before changing the text color and waiting
          for user input.
          Default: `""`
        delay_ms: The delay between each printed character in milliseconds.
          Default: `100` (0.01 seconds)
        input_color: The color the user's input text should be.
          Default: `.terminal.colors.FG_CYAN`
        text_after_color: The color to set after getting the input.
          Default: `.terminal.colors.RESET`

    Returns:
        The user's input as a string.
    """

    if prompt:
        print(prompt, end="", delay_ms=delay_ms)

    input_color()
    user_input = builtins.input()
    text_after_color()

    return user_input
