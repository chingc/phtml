"""Programmatic XML: Write XML Programmatically"""

from contextlib import contextmanager

from pxml.attr import Attr  # pylint: disable=E


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


    def etag(self, name, attr=None):
        """Add empty tag content.

        name -- The name of the tag.
        attr -- A list of 2-tuple strings.  Default: None

        => self
        """
        self.insert(f"<{name} />" if attr is None else f"<{name} {Attr(*attr)} />")
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
    def tag(self, name, attr=None, oneline=False):
        """Add tag content.

        name -- The name of the tag.
        attr -- A list of 2-tuple strings.  Default: None

        => self
        """
        attributes = "" if attr is None else f" {Attr(*attr)}"
        # self.indent().insert(f"<{name}>" if attr is None else f"<{name} {Attr(*attr)}>").newline()
        self.indent().insert(f"<{name}{attributes}>").newline()
        self.depth += 1
        yield
        self.depth -= 1
        self.indent().insert(f"</{name}>").newline()
        return self


    @contextmanager
    def itag(self, name, attr=None):
        """Add inline tag content.

        name -- The name of the tag.
        attr -- A list of 2-tuple strings.  Default: None

        => self
        """
        self.insert(f"<{name}>" if attr is None else f"<{name} {Attr(*attr)}>")
        yield
        self.insert(f"</{name}>")
        return self
