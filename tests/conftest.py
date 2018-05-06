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
def phtml():
    """New instance of PHTML."""
    return PHTML()
