# UPDATE 1.1.2

## CHANGED
- `_repr_iterable.py`
	- changed return type of main function from `Tuple[str|None, None|Exception]` to `str`
	- if a RecursionError occurs, the main function now returns `""`