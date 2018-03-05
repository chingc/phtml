"""Tests"""

import sys
from pathlib import Path
from typing import no_type_check

import pytest

HERE = Path(__file__).resolve()
sys.path.append(str(HERE.parent.parent.joinpath("src")))

from pxml.attr import Attr  # pylint: disable=C, E


BAD_IN = [None, True, 1, [], {}, (), ("a",), ("a", "b", "c")]  # non-strings and len(tuple) != 2
GOOD_IN = [["a"], ["a", "b"], [("a", 1)], [("a", 1), ("b", "2")], ["a", ("b", 2)], [("a", 1), "b"]]
GOOD_OUT = ["a", "a b", 'a="1"', 'a="1" b="2"', 'a b="2"', 'a="1" b', 1]

@no_type_check
@pytest.mark.parametrize("test_input, expected", list(zip(GOOD_IN, GOOD_OUT)))
def test_init(test_input, expected):
    """The given attribute produces the expected attribute string."""
    assert Attr(*test_input) == expected

@no_type_check
@pytest.mark.parametrize("test_input", GOOD_IN)
def test_repr(test_input):
    """The expression `eval(repr(Attr(x)) == Attr(x)` is true."""
    assert eval(repr(Attr(*test_input))) == Attr(*test_input)  # pylint: disable=W

@no_type_check
def test_empty():
    """No attribute results in an empty string."""
    assert Attr() == ""

@no_type_check
def test_pop():
    """Attributes can be removed."""
    attr = Attr()
    flattened = [x for xs in GOOD_IN for x in xs]
    for value in flattened:
        attr.append(value)
    while attr.attrs:
        assert isinstance(attr.pop(), str)
    with pytest.raises(IndexError):
        attr.pop()

@no_type_check
def test_append_good():
    """Good input increases the attribute list by 1."""
    attr = Attr()
    flattened = [x for xs in GOOD_IN for x in xs]
    for value in flattened:
        attr.append(value)
    assert len(attr.attrs) == len(flattened)

@no_type_check
def test_append_bad():
    """Bad input does not increase the attribute list."""
    attr = Attr()
    for value in BAD_IN:
        attr.append(value)
    assert not attr.attrs
