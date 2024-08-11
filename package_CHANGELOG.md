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