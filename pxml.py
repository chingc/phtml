"""Programmatic XML: Generate XML Programmatically."""

from contextlib import contextmanager


class PXML():
    def __init__(self, spaces=4):
        self.spaces = spaces
        self.depth = 0
        self.raw = []

    def __str__(self):
        return "".join(self.raw)

    @staticmethod
    def _verify_str_(obj):
        """Raise a TypeError if the given object is not a string."""
        if not isinstance(obj, str):
            raise TypeError("Type must be a string, but got {}".format(obj))

    @staticmethod
    def _verify_attr_(obj):
        """Raise a TypeError if the given object is not a list of 2-tuple strings."""
        if not isinstance(obj, list):
            raise TypeError("Type must be a list of 2-tuple strings, but got {}".format(obj))
        for element in obj:
            if not isinstance(element, tuple) or len(element) != 2:
                raise TypeError("Type must be a list of 2-tuple strings, but got {}".format(obj))
        for first, second in obj:
            if not isinstance(first, str) or not isinstance(second, str):
                raise TypeError("Type must be a list of 2-tuple strings, but got {}".format(obj))

    @staticmethod
    def attributes(attr):
        """Return the attribute list as a string."""
        to_string = ""
        for name, value in attr:
            to_string += ' {}="{}"'.format(name, value)
        return to_string

    @staticmethod
    def indent(spaces, depth):
        """Return the indentation."""
        return " " * spaces * depth

    @contextmanager
    def tag(self, name, attr=None):
        if attr is None:
            attr = []
        PXML._verify_str_(name)
        PXML._verify_attr_(attr)
        indent = PXML.indent(self.spaces, self.depth)
        self.raw.append("{}<{}{}>\n".format(indent, name, PXML.attributes(attr)))
        self.depth += 1
        yield
        self.depth -= 1
        self.raw.append("{}</{}>\n".format(indent, name))
        return self

    @contextmanager
    def itag(self, name, attr=None, indent=True):
        if attr is None:
            attr = []
        PXML._verify_str_(name)
        PXML._verify_attr_(attr)
        indent = PXML.indent(self.spaces, self.depth) if indent else ""
        self.raw.append("{}<{}{}>".format(indent, name, PXML.attributes(attr)))
        yield
        self.raw.append("</{}>".format(name))
        return self

    def insert(self, string, indent=True):
        self._verify_str_(string)
        indent = PXML.indent(self.spaces, self.depth) if indent else ""
        self.raw.append("{}{}".format(indent, string))
        return self

    def newline(self):
        self.raw.append("\n")
        return self
