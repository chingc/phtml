"""Fixtures"""

import pytest

import env
from phtml.phtml import PHTML  # pylint: disable=E0401


@pytest.fixture
def attr():
    """The static method attr."""
    return PHTML.attr

@pytest.fixture
def expect_file():
    """Read the file containing expected output."""
    def _read(filename):
        with open(env.HERE.joinpath(filename), "r") as _file:
            return _file.read()
    return _read

@pytest.fixture
def pon():
    """New instance of PHTML with auto spacing enabled."""
    return PHTML(auto_spacing=True)

@pytest.fixture
def poff():
    """New instance of PHTML with auto spacing disabled."""
    return PHTML(auto_spacing=False)
