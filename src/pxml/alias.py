"""Type Alias"""
# pylint: disable=C

from typing import List, Tuple, Union


BooleanAttribute = str
ValueAttribute = Tuple[str, Union[int, str]]
Attribute = Union[BooleanAttribute, ValueAttribute]

Attributes = List[Attribute]
FormattedAttributes = List[str]
