"""Module for error handling."""


class CategoriesDivNotFoundError(Exception):
    """Exception raised when the categories div container is not found."""

    def __init__(self: classmethod, message: str = "Categories div container has not been found") -> None:
        self.message = message
        super().__init__(self.message)


class RequestError(Exception):
    """Exception raised when there's an issue with request."""

    def __init__(self: classmethod, message: str = "Request issue has occured:") -> None:
        self.message = message
        super().__init__(self.message)


class UnknownError(Exception):
    """Exception raised when there's an unknown issue."""

    def __init__(self, message: str = "Unknown issue has occurred.") -> None:
        super().__init__(message)
