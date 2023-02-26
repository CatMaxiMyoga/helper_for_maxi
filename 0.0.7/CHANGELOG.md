# UPDATE 0.0.7

## CHANGED

+ changed the way the BetterPrint function works
    - before:
        ```python
        sys.stdout.write(char)
        sys.stdout.flush()```
    - now:
        ```python
        print(char, end='', flush=True)```
+ changed the default value for `delay` of the BetterPrint function
    - before: `.1`
    - now: `.01`