# UPDATE 1.1.6

## ADDED
- `_kwargs_handler.py`
  - Added `__getitem__` to allow for retrieval of values per KWArgsHandler[key]
- `_check_params_decorator.py`
  - A decorator that raises a `TypeError` if a parameter is not of the annotated type

## CHANGED
- `_kwargs_handler.py`
  - Made the `*allowedKeywords` parameter take tuples that don't necessarily contain a third item (default value)
