r"""Contains all the package's decorators"""

from collections.abc import Callable
from functools import wraps
from inspect import Parameter, signature
from typing import Any, Optional, get_origin

from . import exceptions
from .utils import validate_type
from .validators import Validator


def check_params(
    validation_options: (
        Optional[dict[str, Validator]] | Callable[..., Any]
    ) = None,
    *,
    force_annotations: bool = True,
    validate_return: bool = True,
    **kwargs: Validator,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    r"""
    Checks that all given parameters and the return value are the expected type.

    Goes through the function signature to ensure that all the parameters
    passed when calling this function adhere to them, as well as the function's
    return value.

    Args:
        validation_options: `"parameter_name": rules` Custom Validators used
          for specified parameters. Can also use **kwargs parameter instead or
          combine both.
        force_annotations: Whether or not to throw an error for missing
          function annotations.
        validate_return: Whether or not to validate the wrapped `func`'s
          return value's type.
        **kwargs: Same as `validation_options`

    Returns:
        `collections.abc.Callable[..., R]`: The wrapped `func`.

    Raises:
        `TypeError`: Parameter's value does not match the expected type.
        `TypeError`: Keyword argument given for function without ** parameter.
        `TypeError`: Function returned wrong type.
        `.exceptions.MissingAnnotationsError`: Function missing annotations
        `.excpetions.InvalidValidatorError`: Validator does not fit parameter's
          annotated type.
        `ValueError`: `special_validation` or `**kwargs` entry specified for
          unannotated parameter.
    """

    if callable(validation_options):
        return check_params()(validation_options)

    if validation_options is None:
        validation_options = {}

    if set(validation_options.keys()) & set(kwargs.keys()):
        raise ValueError(
            "Don't specify the same keys in "
            "`special_validation` and `**kwargs`"
        )

    validation_options.update(kwargs)

    def _check_params[R](func: Callable[..., R]) -> Callable[..., R]:
        def check_for_annotations() -> int:
            sig = signature(func)
            params = sig.parameters
            ret = 0

            for param in params.values():
                if param.kind in {param.VAR_POSITIONAL, param.VAR_KEYWORD}:
                    continue

                if param.name == "self":
                    continue

                if param.annotation is Parameter.empty:
                    ret += 0b10

            if sig.return_annotation is Parameter.empty:
                ret += 0b01

            return ret

        @wraps(func)
        def decorator(*args: Any, **kwargs: Any) -> R:
            annotation_check: int = 0

            if force_annotations:
                annotation_check = check_for_annotations()

            if annotation_check != 0:
                missing: list[str] = []

                if annotation_check & 0b10:
                    missing.append("parameters")

                if annotation_check & 0b01:
                    missing.append("the return value")

                raise exceptions.MissingAnnotationsError(
                    f"Missing annotations for {
                        missing[0]
                        if len(missing) == 1
                        else " and ".join(missing)
                    }"
                )

            params = signature(func).parameters

            for arg, param in zip(args, params.values()):
                annot = param.annotation
                validation_result = validate_type(arg, annot)

                if (
                    annot == Parameter.empty
                    and param.name in validation_options.keys()
                ):
                    raise ValueError(
                        "Specified key in `special_validation` or `**kwargs` "
                        f"for unannotated parameter {repr(param.name)}."
                    )
                elif annot == Parameter.empty:
                    continue
                elif not validation_result:
                    pname = str(param.name)
                    gtype = type(arg)
                    gtypename = str(
                        gtype.__name__ if hasattr(gtype, "__name__") else gtype
                    )
                    raise TypeError(
                        f"Invalid type for parameter {pname}: "
                        f"{gtypename}. Expected: {annot}."
                    )
                elif param.name in validation_options.keys():
                    name = param.name
                    validator = validation_options[name]

                    if get_origin(
                        annot
                    ) not in validator.allowed_types and validator.allowed_types != [
                        Any
                    ]:
                        raise exceptions.InvalidValidatorError(
                            f"Validator {validator.__class__.__name__} not "
                            f"allowed on type {
                                get_origin(annot).__class__.__name__
                            }."
                        )

                    validator_result = validator.validate(name, arg)

                    if validator_result is None:
                        continue

                    raise exceptions.ValidationError(validator_result)

            kwargs_param: Parameter | None = None
            for param in params.values():
                if param.kind == param.VAR_KEYWORD:
                    kwargs_param = param
                    break

            for k, v in kwargs.items():
                if k not in params:
                    if kwargs_param is None:
                        raise TypeError(
                            f"{func.__name__}() got an unexpected keyword "
                            f"argument {k}={str(v)}"
                        )

                    if kwargs_param.annotation is Parameter.empty:
                        continue

                    if not validate_type(v, annot := kwargs_param.annotation):
                        pname = str(kwargs_param.name)
                        gtype = type(v)
                        gtypename = str(
                            gtype.__name__
                            if hasattr(gtype, "__name__")
                            else gtype
                        )
                        raise TypeError(
                            f"Invalid type for keyword {pname}: "
                            f"{gtypename}. Expected: {annot}."
                        )

                    continue

                annot = params[k].annotation

                if annot is not Parameter.empty and not validate_type(v, annot):
                    pname = str(params[k].name)
                    gtype = type(v)
                    gtypename = str(
                        gtype.__name__ if hasattr(gtype, "__name__") else gtype
                    )
                    raise TypeError(
                        f"Invalid type for parameter {pname}: "
                        f"{gtypename}. Expected: {annot}."
                    )

            func_return: R = func(*args, **kwargs)

            if not validate_return:
                return func_return

            ignore_return_names: list[str] = ["__init__"]

            if (
                hasattr(func, "__name__")
                and func.__name__ in ignore_return_names
            ):
                return func_return

            return_annot = signature(func).return_annotation

            if return_annot is Parameter.empty:
                return func_return

            if validate_type(func_return, return_annot):
                return func_return

            gtype = type(func_return)
            gtypename = str(
                gtype.__name__ if hasattr(gtype, "__name__") else gtype
            )
            raise TypeError(
                f"Return of function {func.__name__} has invalid type: "
                f"{gtypename}. Expected: {return_annot}"
            )

        return decorator

    return _check_params


__all__ = ["check_params"]
