# UPDATE 0.0.8

## CHANGED

+ updated `color_input.py` to be able to use the `terminal.py` module correctly
    - before:
        ```python
        from terminal import Terminal```
    - now:
        ```python
        from .terminal import Terminal```