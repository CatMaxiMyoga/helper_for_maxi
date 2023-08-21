# UPDATE 1.0.0

## CHANGED

+ Changed the case used in the `__init__.py` to export all the functions
    - Changed from Pascal Case to Camel Case
        - PascalCase: Every word's first letter is uppercase
        - camelCase: The same as Pascal Case, with the first letter being an exception
        - updated the `README.md` accordingly
    - Classes stay in PascalCase

+ `better_color_input.py`
    - added `end=""` the `print()` function used to reset the color to `beforeColor` after getting the input.
    - switched from a default of `None` for `beforeColor` to a default of `terminal/Terminal.color.RESET`.
    - switched the type of `beforeColor` from `Terminal.color.foreground` to `Optional[Terminal.color.foreground]` to allow None to be given.
    - switched positions of `delay` and `beforeColor`
    - Updated the `README.md` accordingly

+ `better_input.py`
    - removed the `end` argument, since it is not needed.
    - Updated the `README.md` accordingly

+ `color_input.py`
    - applied the first 3 changes of of `better_color_input.py`
    - updated the `README.md` accordingly

+ `output.py`
    - renamed to `output_stdout.py`
    - changed function name and export accordingly
        - `ouput` -> `outputStdout`
    - updated the `README.md` accordingly