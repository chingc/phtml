"""Attribute"""

from .typehint import Attribute  # pylint: disable=E


def attr(*attrs: Attribute) -> str:
    """Return a string formatted as HTML attributes.

    This function can take multiple strings and 2-tuples.  They are treated as boolean attributes
    and value attributes, respectively.  The tuples should be in the form (str, str) or (str, int).

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
