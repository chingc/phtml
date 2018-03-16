"""Type Hints"""
# pylint: disable=C

from typing import Generator, List, Tuple, Union


BooleanAttribute = str
ValueAttribute = Tuple[str, Union[int, str]]
Attribute = Union[BooleanAttribute, ValueAttribute]

FormattedElements = List[str]

Wrapper = Generator
