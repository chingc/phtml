"""Programmatic XML: Write XML Programmatically"""

from contextlib import contextmanager


class PXML():
    """Main class."""
    def __init__(self, spaces=4):
        self.spaces = spaces
        self.depth = 0
        self.raw = []


    def __str__(self):
        return "".join(self.raw)


    @staticmethod
    def check_str(obj):
        """Check if an object is a string.

        obj -- The object to check.

        Success => None
        Failure => Raise TypeError
        """
        if not isinstance(obj, str):
            raise TypeError("Expected {}, but got {}".format(type(""), type(obj)))


    @staticmethod
    def check_attr(obj):
        """Check if an object is a list of 2-tuple strings.

        obj -- The object to check.

        Success => None
        Failure => Raise TypeError
        """
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
        """Stringify an attribute list.

        attr -- A list of 2-tuple strings.

        => The string representation of attr.
        """
        PXML.check_attr(attr)
        to_string = ""
        for name, value in attr:
            to_string += ' {}="{}"'.format(name, value)
        return to_string


    def etag(self, name, attr=None):
        """Add empty tag content.

        name -- The name of the tag.
        attr -- A list of 2-tuple strings.  Default: None

        => self
        """
        if attr is None:
            attr = []
        self.insert("<{}{} />".format(name, PXML.attributes(attr)))
        return self


    def indent(self, repeat=1):
        """Add indentation.

        repeat -- The number of times to indent.  Default: 1

        => self
        """
        for _ in range(repeat):
            self.insert(" " * self.spaces * self.depth)
        return self


    def insert(self, string):
        """Add a string.

        string -- The string to add.

        => self
        """
        self.check_str(string)
        if string:
            self.raw.append(string)
        return self


    def newline(self, repeat=1):
        """Add a newline.

        repeat -- The number of newlines to add.  Default: 1

        => self
        """
        for _ in range(repeat):
            self.insert("\n")
        return self


    @contextmanager
    def tag(self, name, attr=None):
        """Add tag content.

        name -- The name of the tag.
        attr -- A list of 2-tuple strings.  Default: None

        => self
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

        name -- The name of the tag.
        attr -- A list of 2-tuple strings.  Default: None

        => self
        """
        if attr is None:
            attr = []
        self.insert("<{}{}>".format(name, PXML.attributes(attr)))
        yield
        self.insert("</{}>".format(name))
        return self
