"""PyHTML"""

from contextlib import contextmanager
from typing import Generator, List, Tuple, Union


class PyHTML():
    """Create HTML Elements."""
    Attribute = Union[str, Tuple[str, Union[int, str]]]

    @staticmethod
    def _close_tag(elem: str) -> str:
        return f"</{elem}>"

    @staticmethod
    def _is_void(elem: str) -> bool:
        # http://w3c.github.io/html/syntax.html#void-elements
        return elem in ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"]

    @staticmethod
    def _open_tag(elem: str, attrs: str = "") -> str:
        return f"<{elem}{'' if not attrs else f' {attrs}'}>"

    @staticmethod
    def attr(*attrs: Attribute) -> str:
        """Return a string formatted as HTML attributes.

        Can take multiple strings and 2-tuples.  Strings are treated as boolean attributes and
        2-tuples are treated as value attributes.  Tuples take the form (str, str) or (str, int).

        For example, to create the attributes in the element:
        <video src="videofile.webm" autoplay width="800" height="600"></video>

        `attr(("src", "videofile.webm"), autoplay, ("width", 800), ("height", 600))`
        """
        formatted = []
        for attr_ in attrs:
            if isinstance(attr_, str):
                formatted.append(attr_)
            elif isinstance(attr_, tuple) and len(attr_) == 2:
                formatted.append(f'{attr_[0]}="{attr_[1]}"')
            else:
                raise ValueError(f"Bad attribute: {attr_}")
        return " ".join(formatted)

    def __init__(self, auto_spacing: bool = True, spaces: int = 4) -> None:
        self.auto_spacing = auto_spacing
        self.depth = 0
        self.elems: List[str] = []
        self.spaces = spaces

    def __contains__(self, item: object) -> bool:
        return str(item) in str(self)

    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)

    def __len__(self) -> int:
        return len(str(self))

    def __repr__(self) -> str:
        return "".join(self.elems)

    def __str__(self) -> str:
        return "".join(self.elems)

    def append(self, string: str) -> "PyHTML":
        """Add a string."""
        if isinstance(string, str):
            if self.auto_spacing:
                self.indent()
            self.elems.append(string)
            if self.auto_spacing:
                self.newline()
        else:
            raise ValueError("Value being appended must be a string type")
        return self

    def indent(self) -> "PyHTML":
        """Add indentation."""
        self.elems.append(" " * self.spaces * self.depth)
        return self

    def newline(self) -> "PyHTML":
        """Add a newline."""
        self.elems.append("\n")
        return self

    def vwrap(self, elem: str, attrs: str = "") -> "PyHTML":
        """Add a void element."""
        if not self._is_void(elem):
            raise ValueError(f"Use the wrap context manager for non-void elements like {elem}")
        self.append(self._open_tag(elem, attrs))
        return self

    @contextmanager
    def wrap(self, elem: str, attrs: str = "") -> Generator:
        """Add an element."""
        if self._is_void(elem):
            raise ValueError(f"Use the vwrap method for void elements like {elem}")
        self.append(self._open_tag(elem, attrs))
        self.depth += 1
        yield
        self.depth -= 1
        self.append(self._close_tag(elem))
