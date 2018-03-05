"""Fixtures"""

import sys
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def PXML():
    """Locate and import PXML."""
    here = Path(__file__).resolve()
    sys.path.append(str(here.parent.parent.joinpath("src")))
    from pxml.pxml import PXML as p  # pylint: disable=E
    return p

@pytest.fixture()
def types():
    """Types to check."""
    return [None, True, 1, "", "string", [], (), {}]
