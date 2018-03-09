"""Attribute"""

from .typehint import Attributes, FormattedAttributes, Attribute, ValueAttribute  # pylint: disable=E


class Attr():
    """Create HTML Attributes.

    Attr can take multiple strings or 2-tuples and return a string formatted as HTML attributes.
    Strings and 2-tuples are treated as boolean attributes and value attributes, respectively.
    Tuples should be in the form (str, str) or (str, int).

    For example, to create the attributes in the element:
    <video src="videofile.webm" autoplay width="800" height="600"></video>

    `Attr(("src", "videofile.webm"), autoplay, ("width", 800), ("height", 600))`

    Methods to append and pop attributes are available, and work the same way as their Python
    list equivalents.  Attributes can be compared and are equal if their string representation
    are the same.
    """
    @staticmethod
    def _decode(_: str) -> ValueAttribute:
        values = _.replace('"', "").split("=")
        return values[0], values[1]

    @staticmethod
    def _encode(_: ValueAttribute) -> str:
        return f'{_[0]}="{_[1]}"'

    def __init__(self, *attrs: Attribute) -> None:
        self.attrs: FormattedAttributes = []
        self.append(*attrs)

    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)

    def __repr__(self) -> str:
        output: Attributes = []
        for attr in self.attrs:
            if "=" in attr:
                output.append(self._decode(attr))
            else:
                output.append(attr)
        return f"{type(self).__name__}{tuple(output)}"

    def __str__(self) -> str:
        return " ".join(self.attrs)

    def append(self, *attrs: Attribute) -> None:
        """Add an attribute."""
        for attr in attrs:
            if isinstance(attr, str):
                self.attrs.append(attr)
            elif isinstance(attr, tuple):
                if len(attr) == 2:
                    self.attrs.append(self._encode(attr))
            else:
                pass

    def pop(self, index: int = -1) -> str:
        """Remove an attribute."""
        return str(self.attrs.pop(index))
