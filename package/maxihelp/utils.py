from collections.abc import Callable
from inspect import signature
from types import UnionType
from typing import Any, Literal, TypeAliasType, Union, get_args, get_origin


def compare_types(type1: type[Any], type2: type[Any]) -> bool:
    def inner_compare_types(itype1: type[Any], itype2: type[Any]) -> bool:
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
                inner_compare_types(a1, a2) for a1, a2 in zip(iargs1, iargs2)
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


def validate_type(value: Any, annot: type[Any] | UnionType) -> bool:
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
            and (isinstance(args[0], UnionType) or get_origin(args[0]) is Union)
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
        k_check: bool = all(validate_type(k, args[0]) for k in d_value.keys())
        v_check: bool = all(validate_type(v, args[1]) for v in d_value.values())

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
        f"Make sure to include this information as written:\n"
        f"Annotation:   {str(annot)}\n"
        f"Type:         {str(type(annot))}\n"
        f"Type Name:    {str(type(annot).__name__)}\n"
        f"Origin:       {str(origin)}\n"
        f"Args:         {str(args)}\n"
        f"Value:        {str(value)}\n"
    )


__all__ = ["compare_types", "validate_type"]
