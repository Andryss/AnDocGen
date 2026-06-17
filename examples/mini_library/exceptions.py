"""Domain exceptions for mini_library."""


class MiniLibraryError(Exception):
    """Base error for the library."""


class NotFoundError(MiniLibraryError):
    """Raised when a requested entity does not exist."""


class ValidationError(MiniLibraryError):
    """Raised when input data is invalid."""
