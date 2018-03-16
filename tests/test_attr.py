"""Tests"""

import sys
from pathlib import Path
from typing import no_type_check

import pytest

HERE = Path(__file__).resolve()
sys.path.append(str(HERE.parent.parent.joinpath("src")))

from pxml.attr import attr  # pylint: disable=C, E


BAD_IN = [None, True, 1, [], {}, (), ("a",), ("a", "b", "c")]  # non-strings and len(tuple) != 2
GOOD_IN = [["a"], ["a", "b"], [("a", 1)], [("a", 1), ("b", "2")], ["a", ("b", 2)], [("a", 1), "b"]]
GOOD_OUT = ["a", "a b", 'a="1"', 'a="1" b="2"', 'a b="2"', 'a="1" b', 1]

@no_type_check
def test_empty():
    """Zero attributes returns an empty string."""
    assert attr() == ""

@no_type_check
@pytest.mark.parametrize("test_input, expected", list(zip(GOOD_IN, GOOD_OUT)))
def test_good_input(test_input, expected):
    """Valid input returns the expected string."""
    assert attr(*test_input) == expected

@no_type_check
@pytest.mark.parametrize("bad_in", BAD_IN)
def test_bad_input(bad_in):
    """Invalid input raises an exception."""
    with pytest.raises(ValueError):
        attr(bad_in)
