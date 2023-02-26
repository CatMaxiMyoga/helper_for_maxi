# UPDATE 0.0.8

## CHANGED

+ Updated the colorList values in `Terminal.color.foreground` and `Terminal.color.background`
    - removed `SWAPCOLOR` from both
    - removed `UNDERLINE` and `BOLD` from `_.foreground`
+ Updated the description of `color_input.py\color_input()`
    - before:
        ```txt
        Prints the given text in cyan and changes the color back to beforeColor
        ```
    - after:
        ```txt
        executes the input() function in cyan and changes the color back to beforeColor if given
        ```