from typing import Any

from .terminal.ansi import ANSIColorCode

def print(
    *values: Any, sep: str = " ", delay_ms: int = 100, end: str = "\n"
) -> None: ...
def input(prompt: Any = "", delay_ms: int = 100) -> str: ...
def color_input(
    prompt: Any = "",
    delay_ms: int = 100,
    input_color: ANSIColorCode = ANSIColorCode(36),
    text_after_color: ANSIColorCode = ANSIColorCode(0),
) -> str: ...
