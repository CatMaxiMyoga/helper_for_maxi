# UPDATE 1.2.3

## ADDED
- ANSI codes in `Terminal.color.foreground`
  - `STRIKETHROUGH`, `FGRESET`
- ANSI codes in `Terminal.color.background`
  - `BGRESET`
- `Terminal.Cursor`
  - Allows manipulation of the terminal cursor, such as movement and visibility of it.
- `Terminal.Manager`
  - Currently only contains methods for clearing the terminal in specific ways.
- `inputColor` parameter to `betterColorInput` and `colorInput`

## CHANGED
- Made `_utils.ANSICodeBase` use `outputStdout` instead of `print`
- Added the `@checkParams` decorator to most functions
- some string parameters to `*args` parameters, adding the `sep` parameter to seperate objects 
  in the `*args` parameter

## FIXED
- Made the `@checkParams` decorator work. Now works with:
  - annotated `*args` parameters
  - annotated `**kwargs` parameters
    - Note that this only checks for the annotated types in the values given and does not, like 
      the `KWArgsHandler`, validate the keys and check for the specific type in the value for 
      the given key.
  - hopefully any type I'll ever use. If not, it throws a useful `NotImplementedError` showing 
    useful information for implementing it.

---------------
# UPDATE 1.2.2

## FIXED
- Added the missing imports for the ANSI codes to the `Terminal/color/foreground/__init__.py` file
- Fixed a mistake with redundant underscores before `ANSICodeBase` in `isinstance()` checks in 
  `_utils/_ansi_code_base.py`

---------------
# UPDATE 1.2.1

## CHANGED
- Switched from using an Enum for `Terminal.color.*.*` to using class-instances with `__repr__` 
  functions and a `value` property for backwards compatibility.

---------------
# UPDATE 1.2.0

## CHANGED
- Added parameter `returnLine` to `ChoiceInterface`
  - changes return type to `tuple[int, str]` if `True`