# UPDATE 0.1.4

## CHANGED

+ `Terminal.color.foreground.random` -> `Terminal.color.foreground.random()`
    - before:
        ```python
        random = random.choice(colorList)
        ```
    - now:
        ```python
        def random():
            colorList = Terminal.color.foreground.colorList
            return random.choice(colorList)
        ```

+ `Terminal.color.background.random` -> `Terminal.color.background.random()`
    - before:
        ```python
        random = random.choice(colorList)
        ```
    - now:
        ```python
        def random():
            colorList = Terminal.color.background.colorList
            return random.choice(colorList)
        ```