"""Errors crossing the provider boundary contain no native binding values."""


class GPUError(Exception):
    pass


class QueryError(GPUError):
    pass


class FatalQueryError(QueryError):
    pass


class CombinedError(GPUError):
    def __init__(self, errors: list[Exception]):
        self.errors = tuple(errors)
        super().__init__("\n".join(str(error) for error in errors))


def combine(*errors: Exception | None) -> Exception | None:
    present = [error for error in errors if error is not None]
    if not present:
        return None
    return present[0] if len(present) == 1 else CombinedError(present)
