r"""
Contains all the package's decorators
"""

from collections.abc import Callable
from functools import wraps
from inspect import Parameter, signature
from types import UnionType
from typing import (
    Any,
    Literal,
    Type,
    TypeAliasType,
    Union,
    get_args,
    get_origin,
)

from .exceptions import MissingAnnotationsError


def check_params[R](func: Callable[..., R]) -> Callable[..., R]:
    r"""
    Checks that all given parameters and the return value are the expected type.

    Goes through the function signature to ensure that all the parameters
    passed when calling this function adhere to them, as well as the function's
    return value.

    Args:
        func: The function to be wrapped.

    Returns:
        `collections.abc.Callable[..., R]`: The wrapped function.

    Raises:
        `TypeError`: Parameter's value does not match the expected type.
        `TypeError`: Keyword argument given for function without ** parameter.
        `TypeError`: Function returned wrong type.
        `.exceptions.MissingAnnotationsError`: Function missing annotations

    Note:
        You have to annotate your function fully when using this decorator
          with the exception of `*args` and `**kwargs`!
    """

    def check_for_annotations() -> int:
        sig = signature(func)
        params = sig.parameters
        ret = 0

        for param in params.values():
            if param.kind in {param.VAR_POSITIONAL, param.VAR_KEYWORD}:
                continue

            if param.annotation is Parameter.empty:
                ret += 0b10

        if sig.return_annotation is Parameter.empty:
            ret += 0b01

        return ret

    def compare_types(type1: Type[Any], type2: Type[Any]) -> bool:
        def inner_compare_types(itype1: Type[Any], itype2: Type[Any]) -> bool:
            iorigin1, iargs1 = get_origin(itype1), get_args(itype1)
            iorigin2, iargs2 = get_origin(itype2), get_args(itype2)

            if iorigin1 is None and iorigin2 is None:
                return itype1 == itype2

            if iorigin1 is not None and iorigin2 is not None:
                if iorigin1 != iorigin2:
                    return False

                if not iargs1 and not iargs2:
                    return True

                if len(iargs1) != len(iargs2):
                    return False

                return all(
                    inner_compare_types(a1, a2)
                    for a1, a2 in zip(iargs1, iargs2)
                )

            return False

        def compare_literals(
            literals1: tuple[Any, ...], literals2: tuple[Any, ...]
        ) -> bool:
            return set(literals1) == set(literals2)

        if isinstance(type1, TypeAliasType):
            type1 = type1.__value__
        if isinstance(type2, TypeAliasType):
            type2 = type2.__value__

        origin1, args1 = get_origin(type1), get_args(type1)
        origin2, args2 = get_origin(type2), get_args(type2)

        if origin1 is Literal and origin2 is Literal:
            return compare_literals(args1, args2)

        return inner_compare_types(type1, type2)

    def validate_type(value: Any, annot: Type[Any] | UnionType) -> bool:
        if isinstance(annot, TypeAliasType):
            annot = annot.__value__

        origin, args = get_origin(annot), get_args(annot)

        if origin is None:
            return isinstance(value, annot)

        elif origin is tuple:
            if not isinstance(value, tuple):
                return False

            if not args:
                return True

            t_value: tuple[Any, ...] = value

            if len(args) != len(t_value) and not (
                len(args) == 2
                and args[1] is Ellipsis
                and (
                    isinstance(args[0], UnionType)
                    or get_origin(args[0]) is Union
                )
            ):
                return False

            elif len(args) == 2 and args[1] is Ellipsis:
                if get_origin(args[0]) is Union:
                    return all(validate_type(v, args[0]) for v in t_value)

                elif isinstance(args[0], UnionType):
                    return any(validate_type(v, args[0]) for v in t_value)

                else:
                    return all(validate_type(v, args[0]) for v in t_value)

            elif len(args) != len(t_value):
                return False

            return all(validate_type(v, args[i]) for v, i in enumerate(t_value))

        elif origin is list:
            if not isinstance(value, list):
                return False

            if not args:
                return True

            l_value: list[Any] = value
            return all(validate_type(v, args[0]) for v in l_value)

        elif origin is set:
            if not isinstance(value, set):
                return False

            if not args:
                return True

            s_value: set[Any] = value
            return all(validate_type(v, args[0]) for v in s_value)

        elif origin is dict:
            if not isinstance(value, dict):
                return False

            if not args:
                return True

            d_value: dict[Any, Any] = value
            k_check: bool = all(
                validate_type(k, args[0]) for k in d_value.keys()
            )
            v_check: bool = all(
                validate_type(v, args[1]) for v in d_value.values()
            )

            return k_check and v_check

        elif origin is Callable:
            if not callable(value):
                return False

            if not args or args in [(Ellipsis, Any), (Ellipsis, object)]:
                return True

            c_value: Callable[..., Any] = value
            c_sig = signature(c_value)
            c_params = c_sig.parameters
            c_annots = [param.annotation for param in c_params.values()]
            c_return = c_sig.return_annotation
            expected_param_types = args[0]
            expected_return_type = args[1]

            if expected_param_types is not Ellipsis:
                if len(c_params) != len(expected_param_types):
                    return False

                if not all(
                    compare_types(v, t)
                    for v, t in zip(c_annots, expected_param_types)
                ):
                    return False

            if (
                expected_return_type is not Ellipsis
                and expected_return_type is not object
            ):
                if not compare_types(c_return, expected_return_type):
                    return False

            return True

        elif origin is Literal:
            return value in args

        elif origin is Union or origin is UnionType:
            return any(validate_type(value, arg) for arg in args)

        raise NotImplementedError(
            f"You've stumbled upon an unimplemented type!\n"
            f"(or something somehow went very wrong)\n"
            f"Please create an issue on the package's GitHub page.\n"
            f"Make sure to include this information:\n"
            f"Annotation:   {str(annot)}\n"
            f"Type:         {str(type(annot))}\n"
            f"Type Name:    {str(type(annot).__name__)}\n"
            f"Origin:       {str(origin)}\n"
            f"Args:         {str(args)}\n"
            f"Value:        {str(value)}\n"
            f"Signature:    {str(signature(func))}"
        )

    @wraps(func)
    def decorator(*args: Any, **kwargs: Any) -> R:
        annotation_check = check_for_annotations()

        if annotation_check != 0:
            missing: list[str] = []

            if annotation_check & 0b10:
                missing.append("parameters")

            if annotation_check & 0b01:
                missing.append("the return value")

            raise MissingAnnotationsError(
                f"Missing annotations for {
                    missing[0] if len(missing) == 1 else " and ".join(missing)
                }"
            )

        params = signature(func).parameters

        for arg, param in zip(args, params.values()):
            annot = param.annotation

            if annot != Parameter.empty and not validate_type(arg, annot):
                pname = str(param.name)
                gtype = type(arg)
                gtypename = str(
                    gtype.__name__ if hasattr(gtype, "__name__") else gtype
                )
                raise TypeError(
                    f"Invalid type for parameter {pname}: "
                    f"{gtypename}. Expected: {annot}."
                )

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
                        gtype.__name__ if hasattr(gtype, "__name__") else gtype
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

        ignore_return_names: list[str] = ["__init__"]

        if hasattr(func, "__name__") and func.__name__ in ignore_return_names:
            return func_return

        return_annot = signature(func).return_annotation

        if return_annot is Parameter.empty:
            return func_return

        if validate_type(func_return, return_annot):
            return func_return

        gtype = type(func_return)
        gtypename = str(gtype.__name__ if hasattr(gtype, "__name__") else gtype)
        raise TypeError(
            f"Return of function {func.__name__} has invalid type: "
            f"{gtypename}. Expected: {return_annot}"
        )

    return decorator


__all__ = ["check_params"]
