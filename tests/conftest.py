"""Fixtures"""

from pathlib import Path

import pytest

import pyhtml


@pytest.fixture
def attr():
    """The static method attr."""
    return pyhtml.attr

@pytest.fixture
def doctypes():
    """Doctype declarations dictionary."""
    return pyhtml.PyHTML.DOCTYPES

@pytest.fixture
def expect_file():
    """Read the file containing expected output."""
    def _read(filename):
        with open(Path(__file__).parent.joinpath(filename), "r") as f:
            return f.read()
    return _read

@pytest.fixture
def pon():
    """New instance of PyHTML with auto spacing enabled."""
    return pyhtml.new(auto_spacing=True)

@pytest.fixture
def poff():
    """New instance of PyHTML with auto spacing disabled."""
    return pyhtml.new(auto_spacing=False)

@pytest.fixture
def pdoc():
    """New instance of PyHTML with the specified doctype."""
    def _new(doctype):
        return pyhtml.new(auto_spacing=False, doctype=doctype)
    return _new
