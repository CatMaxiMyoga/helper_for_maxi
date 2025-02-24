class MissingAnnotationsError(Exception):
    pass


class ValidationError(Exception):
    pass


class InvalidValidatorError(Exception):
    pass


__all__ = ["MissingAnnotationsError"]
