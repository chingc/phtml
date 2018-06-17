"""Test fixtures."""

from pathlib import Path

import pytest

from pyhtml import PyHTML


@pytest.fixture
def attr():
    """The static method attr."""
    return PyHTML.attr

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
    return PyHTML(auto_spacing=True)

@pytest.fixture
def poff():
    """New instance of PyHTML with auto spacing disabled."""
    return PyHTML(auto_spacing=False)
