"""PyHTML"""

from contextlib import contextmanager


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
    def _close_tag(elem):
        return f"</{elem}>"

    @staticmethod
    def _open_tag(elem, attrs=""):
        return f"<{elem}{'' if not attrs else f' {attrs}'}>"

    @staticmethod
    def attr(*attrs):
        """Stringify HTML attributes.

        attrs: str, (str, str), or (str, int) -- attributes to stringify
        -> str
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

    def __init__(self, auto_spacing=True, spaces=4, doctype=""):
        """Create a new instance of PyHTML.

        auto_spacing: bool -- automatic indentation and newlines (default: True)
        spaces: int -- number of spaces used for indentation (default: 4)
        doctype: str -- doctype declaration (default: "")
        """
        self.auto_spacing = auto_spacing
        self.depth = 0
        self.elems = []
        self.spaces = spaces
        if doctype:
            if doctype in PyHTML.DOCTYPES:
                self.append(PyHTML.DOCTYPES[doctype])
            else:
                raise ValueError(f"Unknown doctype declaration: '{doctype}'")

    def __contains__(self, item):
        return str(item) in str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __len__(self):
        return len(str(self))

    def __repr__(self):
        return "".join(self.elems)

    def __str__(self):
        return "".join(self.elems)

    def append(self, string):
        """Add a string.

        string: str -- arbitrary text to add to the HTML
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

    def indent(self):
        """Add indentation.

        -> self
        """
        self.elems.append(" " * self.spaces * self.depth)
        return self

    def newline(self):
        """Add a newline.

        -> self
        """
        self.elems.append("\n")
        return self

    def vwrap(self, elem, attrs=""):
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
    def wrap(self, elem, attrs=""):
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


# these convenience functions will allow one to simply use
# `import pyhtml` instead of `from pyhtml import PyHTML`

def attr(*attrs):
    """Stringify HTML attributes.

    attrs: str, (str, str), or (str, int) -- attributes to stringify
    -> str
    """
    return PyHTML.attr(*attrs)

def new(auto_spacing=True, spaces=4, doctype=""):
    """Create a new instance of PyHTML.

    auto_spacing: bool -- automatic indentation and newlines (default: True)
    spaces: int -- number of spaces used for indentation (default: 4)
    doctype: str -- doctype declaration (default: "")
    """
    return PyHTML(auto_spacing, spaces, doctype)
