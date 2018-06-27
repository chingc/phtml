"""Fixtures"""

from pathlib import Path

import pytest

import pyhtml.main as pyhtml


@pytest.fixture
def attr():
    return pyhtml.attr

@pytest.fixture
def doctypes():
    return pyhtml.PyHTML.DOCTYPES

@pytest.fixture
def read_file():
    def _read(file):
        with open(Path(__file__).parent / "test_files" / file, "r") as lines:
            return lines.read()
    return _read

@pytest.fixture
def pon():
    return pyhtml.new()

@pytest.fixture
def poff():
    html = pyhtml.new()
    html.auto_spacing = False
    return html

@pytest.fixture
def pdoc():
    def _new(doctype):
        return pyhtml.new(doctype)
    return _new
