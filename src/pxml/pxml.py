"""Programmatic XML: Write XML Programmatically"""

from contextlib import contextmanager

from .attr import Attr  # pylint: disable=E
from .error import NonVoidError, VoidError  # pylint: disable=E
from .typehint import FormattedElements, Wrapper  # pylint: disable=E


class PXML():
    """Create HTML Elements.
    """
    @staticmethod
    def _open_tag(name: str, attr: Attr = None) -> str:
        return f"<{name}{'' if attr is None else f' {Attr(*attr)}'}>"

    @staticmethod
    def _close_tag(name: str) -> str:
        return f"</{name}>"

    @staticmethod
    def _is_void(name: str) -> bool:
        # http://w3c.github.io/html/syntax.html#void-elements
        return name in ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"]  # pylint: disable=C

    def __init__(self, spaces: int = 4) -> None:
        self.depth: int = 0
        self.elems: FormattedElements = []
        self.oneline: bool = False
        self.spaces: int = spaces

    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)

    def __repr__(self) -> str:
        # TODO: REPR
        pass

    def __str__(self) -> str:
        return "".join(self.elems)

    def write(self, string: str) -> "PXML":
        """doc"""  # TODO: Doc
        if string:
            if not self.oneline:
                self.indent()
            self.elems.append(string)
            if not self.oneline:
                self.newline()
        return self

    def newline(self) -> "PXML":
        """Add a newline."""
        self.elems.append("\n")
        return self

    def indent(self) -> "PXML":
        """Add indentation."""
        self.elems.append(" " * self.spaces * self.depth)
        return self

    def vwrap(self, name: str, attr: Attr = None) -> "PXML":
        """Add a void element."""
        if not self._is_void(name):
            raise NonVoidError(name)
        self.write(self._open_tag(name, attr))
        return self

    @contextmanager
    def owrap(self, name: str, attr: Attr = None) -> Wrapper:
        """Add an HTML element (oneliner)."""
        if self._is_void(name):
            raise VoidError(name)
        self.oneline = True
        self.write(self._open_tag(name, attr))
        yield
        self.write(self._close_tag(name))

    @contextmanager
    def wrap(self, name: str, attr: Attr = None) -> Wrapper:
        """Add an HTML element."""
        if self._is_void(name):
            raise VoidError(name)
        self.oneline = False
        self.write(self._open_tag(name, attr))
        self.depth += 1
        yield
        self.depth -= 1
        self.write(self._close_tag(name))
