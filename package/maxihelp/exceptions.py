r"""Contains all the package's Exceptions"""


class MissingAnnotationsError(Exception):
    pass


class ValidationError(Exception):
    pass


class InvalidValidatorError(Exception):
    pass


__all__ = ["MissingAnnotationsError"]
