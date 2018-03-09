"""Tests"""

import pytest


def test_write(PXML):
    pxml = PXML()
    pxml.depth = 0
    pxml.write("a")
    assert str(pxml) == "a\n"

    pxml = PXML()
    pxml.depth = 1
    pxml.write("a")
    assert str(pxml) == "    a\n"


def test_vwrap(PXML):
    """test"""
    pxml = PXML()
    pxml.vwrap("br")
    assert str(pxml) == "<br>\n"

    pxml = PXML()
    pxml.vwrap("img", [("src", "/world.png"), ("width", "640"), ("height", "480")])
    assert str(pxml) == '<img src="/world.png" width="640" height="480">\n'


@pytest.mark.parametrize("spaces", range(5))
@pytest.mark.parametrize("depth", range(5))
def test_indent(PXML, spaces, depth):
    """test"""
    pxml = PXML(spaces)
    pxml.depth = depth
    pxml.indent()
    assert str(pxml) == " " * pxml.spaces * pxml.depth


def test_newline(PXML):
    """test"""
    pxml = PXML()
    pxml.newline()
    assert str(pxml) == "\n"
    pxml.newline()
    assert str(pxml) == "\n\n"


def test_owrap(PXML):
    """test"""
    pxml = PXML()
    with pxml.owrap("b"):
        pxml.write("HelloWorld")
    assert str(pxml) == "<b>HelloWorld</b>"

    pxml = PXML()
    with pxml.owrap("b"):
        with pxml.owrap("i"):
            pxml.write("HelloWorld")
    assert str(pxml) == "<b><i>HelloWorld</i></b>"

    pxml = PXML()
    with pxml.owrap("b"):
        with pxml.owrap("i"):
            with pxml.owrap("u"):
                pxml.write("HelloWorld")
    assert str(pxml) == "<b><i><u>HelloWorld</u></i></b>"

    pxml = PXML()
    with pxml.owrap("b"):
        pxml.write("Hello")
    with pxml.owrap("b"):
        pxml.write("World")
    assert str(pxml) == "<b>Hello</b><b>World</b>"

    pxml = PXML()
    with pxml.owrap("span", [("id", "Hello")]):
        pxml.write("Hello")
    assert str(pxml) == '<span id="Hello">Hello</span>'

    pxml = PXML()
    with pxml.owrap("span", [("id", "Hello")]):
        with pxml.owrap("span", [("id", "World")]):
            pxml.write("HelloWorld")
    assert str(pxml) == '<span id="Hello"><span id="World">HelloWorld</span></span>'


def test_wrap(PXML):
    """
    <b>
        HelloWorld
    </b>
    """
    pxml = PXML(4)
    with pxml.wrap("b"):
        pxml.write("HelloWorld")
    assert str(pxml) == "<b>\n    HelloWorld\n</b>\n"

    """
    <b>
        <i>
            HelloWorld
        </i>
    </b>
    """
    pxml = PXML(4)
    with pxml.wrap("b"):
        with pxml.wrap("i"):
            pxml.write("HelloWorld")
    assert str(pxml) == "<b>\n    <i>\n        HelloWorld\n    </i>\n</b>\n"

    """
    <b>
        <i>
            <u>
                HelloWorld
            </u>
        </i>
    </b>
    """
    pxml = PXML(4)
    with pxml.wrap("b"):
        with pxml.wrap("i"):
            with pxml.wrap("u"):
                pxml.write("HelloWorld")
    assert str(pxml) == "<b>\n    <i>\n        <u>\n            HelloWorld\n        </u>\n    </i>\n</b>\n"

    """
    <b>
        Hello
    </b>
    <b>
        World
    </b>
    """
    pxml = PXML(4)
    with pxml.wrap("b"):
        pxml.write("Hello")
    with pxml.wrap("b"):
        pxml.write("World")
    assert str(pxml) == "<b>\n    Hello\n</b>\n<b>\n    World\n</b>\n"

    """
    <span id="Hello">
        Hello
    </span>
    """
    pxml = PXML(4)
    with pxml.wrap("span", [("id", "Hello")]):
        pxml.write("Hello")
    assert str(pxml) == '<span id="Hello">\n    Hello\n</span>\n'

    """
    <span id="Hello">
        <span id="World">
            HelloWorld
        </span>
    </span>
    """
    pxml = PXML(4)
    with pxml.wrap("span", [("id", "Hello")]):
        with pxml.wrap("span", [("id", "World")]):
            pxml.write("HelloWorld")
    assert str(pxml) == '<span id="Hello">\n    <span id="World">\n        HelloWorld\n    </span>\n</span>\n'
