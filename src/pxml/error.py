"""Errors"""


class Error(Exception):
    """Base class for exceptions."""
    pass

class NonVoidError(Error):
    """Raise when an element is not a void element."""
    def __init__(self, element: str) -> None:  # pylint: disable=W
        self.message = f"Use the wrap or owrap method for non-void elements like {element}"

class VoidError(Error):
    """Raise when an element is a void element."""
    def __init__(self, element: str) -> None:  # pylint: disable=W
        self.message = f"Use the vwrap method for void elements like {element}"
