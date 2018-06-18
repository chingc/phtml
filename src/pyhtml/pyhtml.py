"""PyHTML"""

from contextlib import contextmanager
from typing import Generator, Tuple, Union


Attribute = Union[str, Tuple[str, Union[int, str]]]


class PyHTML():
    """Write and format HTML manually."""

    # https://www.w3.org/QA/2002/04/valid-dtd-list.html
    DOCTYPES = {
        "html5": "<!DOCTYPE html>",
        "html4.01s": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">',
        "html4.01t": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">',
        "html4.01f": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">',
        "xhtml1.1": '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">',
        "xhtml1.0s": '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">',
        "xhtml1.0t": '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">',
        "xhtml1.0f": '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">'
    }

    # http://w3c.github.io/html/syntax.html#void-elements
    VOID_ELEMENTS = ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"]

    @staticmethod
    def _close_tag(elem: str) -> str:
        return f"</{elem}>"

    @staticmethod
    def _open_tag(elem: str, attrs: str = "") -> str:
        return f"<{elem}{'' if not attrs else f' {attrs}'}>"

    @staticmethod
    def attr(*attrs: Attribute) -> str:
        """Strings and tuples are stringified into HTML attribute form.

        attrs -- attributes to stringify
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

    def __init__(self, doctype: str = "", spaces: int = 4) -> None:
        """Create a new instance of PyHTML.

        doctype: str -- doctype declaration (default: "")
        spaces: int -- number of spaces used for indentation (default: 4)
        """
        self.auto_spacing = True
        self.depth = 0
        self.spaces = spaces
        if doctype in PyHTML.DOCTYPES:
            self.elems = [PyHTML.DOCTYPES[doctype]]
        elif not doctype:
            self.elems = []
        else:
            raise ValueError(f"Unknown doctype declaration: '{doctype}'")

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
        """Add a string.

        string: str -- add arbitrary text to the HTML
        -> self
        """
        if isinstance(string, str):
            if self.auto_spacing:
                self.indent()
            self.elems.append(string)
            if self.auto_spacing:
                self.newline()
        else:
            raise ValueError("Value being appended must be a string")
        return self

    def indent(self) -> "PyHTML":
        """Add indentation.

        -> self
        """
        self.elems.append(" " * self.spaces * self.depth)
        return self

    def newline(self) -> "PyHTML":
        """Add a newline.

        -> self
        """
        self.elems.append("\n")
        return self

    def vwrap(self, elem: str, attrs: str = "") -> "PyHTML":
        """Add a void element.

        elem: str -- an HTML void element
        attrs: str -- element attributes (default: "")
        -> self
        """
        if elem not in PyHTML.VOID_ELEMENTS:
            raise ValueError(f"Use `wrap` for non-void element: {elem}")
        self.append(self._open_tag(elem, attrs))
        return self

    @contextmanager
    def wrap(self, elem: str, attrs: str = "") -> Generator:
        """Add an element.

        elem: str -- an HTML element
        attrs: str -- element attributes (default: "")
        """
        if elem in PyHTML.VOID_ELEMENTS:
            raise ValueError(f"Use `vwrap` for void element: {elem}")
        self.append(self._open_tag(elem, attrs))
        self.depth += 1
        yield
        self.depth -= 1
        self.append(self._close_tag(elem))

    @contextmanager
    def manual_spacing(self) -> Generator:
        """Disable automatic indentation and newlines."""
        self.auto_spacing = False
        yield
        self.auto_spacing = True


# these convenience functions will allow one to simply use
# `import pyhtml` instead of `from pyhtml import PyHTML`

def attr(*attrs: Attribute) -> str:
    """Stringify HTML attributes.

    attrs: str, (str, str), or (str, int) -- attributes to stringify
    -> str
    """
    return PyHTML.attr(*attrs)

def new(doctype: str = "", spaces: int = 4) -> "PyHTML":
    """Create a new instance of PyHTML.

    doctype: str -- doctype declaration (default: "")
    spaces: int -- number of spaces used for indentation (default: 4)
    """
    return PyHTML(doctype, spaces)
