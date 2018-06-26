"""Fixtures"""

from pathlib import Path

import pytest

import pyhtml.main as pyhtml


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
        with open(Path(__file__).parent.joinpath(filename), "r") as lines:
            return lines.read()
    return _read

@pytest.fixture
def pon():
    """New instance of PyHTML with auto spacing enabled."""
    return pyhtml.new()

@pytest.fixture
def poff():
    """New instance of PyHTML with auto spacing disabled."""
    html = pyhtml.new()
    html.auto_spacing = False
    return html

@pytest.fixture
def pdoc():
    """New instance of PyHTML with the specified doctype."""
    def _new(doctype):
        return pyhtml.new(doctype)
    return _new
