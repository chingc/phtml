"""PyHTML"""

from contextlib import contextmanager


class PyHTML():
    """Write and format HTML manually."""

    @staticmethod
    def _close_tag(elem):
        return f"</{elem}>"

    @staticmethod
    def _is_void(elem):
        # http://w3c.github.io/html/syntax.html#void-elements
        return elem in ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"]

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

    def __init__(self, auto_spacing=True, spaces=4):
        """Constructor.

        auto_spacing: bool -- automatic indentation and newlines (default: True)
        spaces: int -- number of spaces used for indentation (default: 4)
        """
        self.auto_spacing = auto_spacing
        self.depth = 0
        self.elems = []
        self.spaces = spaces

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
            raise ValueError("Value being appended must be a string type")
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
        if not self._is_void(elem):
            raise ValueError(f"Use the wrap context manager for non-void elements like {elem}")
        self.append(self._open_tag(elem, attrs))
        return self

    @contextmanager
    def wrap(self, elem, attrs=""):
        """Add an element.

        elem: str -- an HTML element
        attrs: str -- element attributes (default: "")
        """
        if self._is_void(elem):
            raise ValueError(f"Use the vwrap method for void elements like {elem}")
        self.append(self._open_tag(elem, attrs))
        self.depth += 1
        yield
        self.depth -= 1
        self.append(self._close_tag(elem))
