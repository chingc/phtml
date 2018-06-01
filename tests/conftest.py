"""Fixtures"""

from typing import Callable

import pytest

import env
from pyhtml.pyhtml import PyHTML


@pytest.fixture
def attr() -> "PyHTML":
    """The static method attr."""
    return PyHTML.attr

@pytest.fixture
def expect_file() -> Callable[[str], str]:
    """Read the file containing expected output."""
    def _read(filename: str) -> str:
        with open(env.HERE.joinpath(filename), "r") as _file:
            return _file.read()
    return _read

@pytest.fixture
def pon() -> "PyHTML":
    """New instance of PyHTML with auto spacing enabled."""
    return PyHTML(auto_spacing=True)

@pytest.fixture
def poff() -> "PyHTML":
    """New instance of PyHTML with auto spacing disabled."""
    return PyHTML(auto_spacing=False)
