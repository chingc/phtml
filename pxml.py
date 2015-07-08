"""Programmatic XML: Generate XML Programmatically"""

from contextlib import contextmanager


class PXML():
    def __init__(self, spaces=4):
        self.spaces = spaces
        self.depth = 0
        self.raw = []

    def __str__(self):
        return "".join(self.raw)

    @staticmethod
    def check_str(obj):
        """Raise a TypeError if the given object is not a string."""
        if not isinstance(obj, str):
            raise TypeError("Expected {}, but got {}".format(type(""), type(obj)))

    @staticmethod
    def check_attr(obj):
        """Raise a TypeError if the given object is not a list of 2-tuple strings."""
        if not isinstance(obj, list):
            raise TypeError("Expected {}, but got {}".format(type([]), type(obj)))
        for element in obj:
            if not isinstance(element, tuple):
                raise TypeError("Expected {}, but got {}".format(type(()), type(element)))
            if len(element) != 2:
                raise TypeError("Expected tuple length to be 2, but got {}".format(len(element)))
            if not (isinstance(element[0], str) and isinstance(element[1], str)):
                raise TypeError("Expected all tuple elements to be {}".format(type("")))

    @staticmethod
    def attributes(attr):
        """Return the attribute list as a string.

        attr: A list of 2-tuple strings.
        """
        PXML.check_attr(attr)
        to_string = ""
        for name, value in attr:
            to_string += ' {}="{}"'.format(name, value)
        return to_string

    def etag(self, name, attr=None):
        """Add empty tag content.

        name: Name of the tag.
        attr: (Optional) A list of 2-tuple strings.
        """
        if attr is None:
            attr = []
        self.insert("<{}{} />".format(name, PXML.attributes(attr)))
        return self

    def indent(self, repeat=1):
        """Add indentation.

        repeat: (Optional) The number of times to indent.  Default: 1
        """
        for i in range(repeat):
            self.insert(" " * self.spaces * self.depth)
        return self

    def insert(self, string):
        """Add a string."""
        self.check_str(string)
        if len(string) > 0:
            self.raw.append(string)
        return self

    def newline(self, repeat=1):
        """Add a newline.

        repeat: (Optional) The number of newlines to add.  Default: 1
        """
        for i in range(repeat):
            self.insert("\n")
        return self

    @contextmanager
    def tag(self, name, attr=None):
        """Add tag content.

        name: Name of the tag.
        attr: (Optional) A list of 2-tuple strings.
        """
        if attr is None:
            attr = []
        self.indent().insert("<{}{}>".format(name, PXML.attributes(attr))).newline()
        self.depth += 1
        yield
        self.depth -= 1
        self.indent().insert("</{}>".format(name)).newline()
        return self

    @contextmanager
    def itag(self, name, attr=None):
        """Add inline tag content.

        name: Name of the tag.
        attr: (Optional) A list of 2-tuple strings.
        """
        if attr is None:
            attr = []
        self.insert("<{}{}>".format(name, PXML.attributes(attr)))
        yield
        self.insert("</{}>".format(name))
        return self
