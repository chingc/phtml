"""Tests"""

import pytest


def test_check_str(PXML, types):
    """test"""
    # pass: string
    for element in [t for t in types if isinstance(t, str)]:
        assert PXML.check_str(element) is None

    # fail: non-string
    for element in [t for t in types if not isinstance(t, str)]:
        with pytest.raises(TypeError):
            PXML.check_str(element)


def test_etag(PXML):
    """test"""
    pxml = PXML()
    pxml.etag("br")
    assert pxml.raw == ["<br />"]
    assert str(pxml) == "<br />"

    pxml = PXML()
    pxml.etag("img", [("src", "/world.png"), ("width", "640"), ("height", "480")])
    assert pxml.raw == ['<img src="/world.png" width="640" height="480" />']
    assert str(pxml) == '<img src="/world.png" width="640" height="480" />'


def test_indent(PXML):
    """test"""
    pxml = PXML()
    pxml.indent()
    assert pxml.raw == []
    assert str(pxml) == ""

    pxml = PXML(4)
    pxml.depth = 1
    pxml.indent(5)
    assert pxml.raw == [" " * pxml.spaces] * 5
    assert str(pxml) == " " * pxml.spaces * 5

    for spaces in range(1, 5):
        for depth in range(1, 5):
            pxml = PXML(spaces)
            pxml.depth = depth
            pxml.indent()
            assert pxml.raw == [" " * spaces * depth]
            assert str(pxml) == " " * spaces * depth


def test_insert(PXML):
    """test"""
    pxml = PXML(4)
    pxml.insert("Hello")
    assert pxml.raw == ["Hello"]
    assert str(pxml) == "Hello"

    pxml.insert("World")
    assert pxml.raw == ["Hello", "World"]
    assert str(pxml) == "HelloWorld"

    pxml.depth = 1
    pxml.indent().insert("One")
    one = " " * pxml.spaces * pxml.depth
    assert pxml.raw == ["Hello", "World", one, "One"]
    assert str(pxml) == "HelloWorld{}One".format(one)

    pxml.depth = 2
    pxml.indent().insert("Two")
    two = " " * pxml.spaces * pxml.depth
    assert pxml.raw == ["Hello", "World", one, "One", two, "Two"]
    assert str(pxml) == "HelloWorld{}One{}Two".format(one, two)

    pxml.depth = 3
    pxml.indent().insert("Three")
    three = " " * pxml.spaces * pxml.depth
    assert pxml.raw == ["Hello", "World", one, "One", two, "Two", three, "Three"]
    assert str(pxml) == "HelloWorld{}One{}Two{}Three".format(one, two, three)

    pxml.insert("Bye").insert("Bye")
    assert pxml.raw == ["Hello", "World", one, "One", two, "Two", three, "Three", "Bye", "Bye"]
    assert str(pxml) == "HelloWorld{}One{}Two{}ThreeByeBye".format(one, two, three)


def test_newline(PXML):
    """test"""
    pxml = PXML()
    pxml.newline()
    assert pxml.raw == ["\n"]
    assert str(pxml) == "\n"

    pxml.newline()
    assert pxml.raw == ["\n", "\n"]
    assert str(pxml) == "\n\n"

    pxml.newline().newline()
    assert pxml.raw == ["\n", "\n", "\n", "\n"]
    assert str(pxml) == "\n\n\n\n"

    pxml.newline(3)
    assert pxml.raw == ["\n", "\n", "\n", "\n", "\n", "\n", "\n"]
    assert str(pxml) == "\n\n\n\n\n\n\n"


def test_itag(PXML):
    """test"""
    pxml = PXML()
    with pxml.itag("b"):
        pxml.insert("HelloWorld")
    assert pxml.raw == ["<b>", "HelloWorld", "</b>"]
    assert str(pxml) == "<b>HelloWorld</b>"

    pxml = PXML()
    with pxml.itag("b"):
        with pxml.itag("i"):
            pxml.insert("HelloWorld")
    assert pxml.raw == ["<b>", "<i>", "HelloWorld", "</i>", "</b>"]
    assert str(pxml) == "<b><i>HelloWorld</i></b>"

    pxml = PXML()
    with pxml.itag("b"):
        with pxml.itag("i"):
            with pxml.itag("u"):
                pxml.insert("HelloWorld")
    assert pxml.raw == ["<b>", "<i>", "<u>", "HelloWorld", "</u>", "</i>", "</b>"]
    assert str(pxml) == "<b><i><u>HelloWorld</u></i></b>"

    pxml = PXML()
    with pxml.itag("b"):
        pxml.insert("Hello")
    with pxml.itag("b"):
        pxml.insert("World")
    assert pxml.raw == ["<b>", "Hello", "</b>", "<b>", "World", "</b>"]
    assert str(pxml) == "<b>Hello</b><b>World</b>"

    pxml = PXML()
    with pxml.itag("span", [("id", "Hello")]):
        pxml.insert("Hello")
    assert pxml.raw == ['<span id="Hello">', "Hello", "</span>"]
    assert str(pxml) == '<span id="Hello">Hello</span>'

    pxml = PXML()
    with pxml.itag("span", [("id", "Hello")]):
        with pxml.itag("span", [("id", "World")]):
            pxml.insert("HelloWorld")
    assert pxml.raw == ['<span id="Hello">', '<span id="World">', "HelloWorld", "</span>", "</span>"]
    assert str(pxml) == '<span id="Hello"><span id="World">HelloWorld</span></span>'


def test_tag(PXML):
    """
    <b>
        HelloWorld
    </b>
    """
    pxml = PXML(4)
    with pxml.tag("b"):
        pxml.indent().insert("HelloWorld").newline()
    assert pxml.raw == ["<b>", "\n", "    ", "HelloWorld", "\n", "</b>", "\n"]
    assert str(pxml) == "<b>\n    HelloWorld\n</b>\n"

    """
    <b>
        <i>
            HelloWorld
        </i>
    </b>
    """
    pxml = PXML(4)
    with pxml.tag("b"):
        with pxml.tag("i"):
            pxml.indent().insert("HelloWorld").newline()
    assert pxml.raw == ["<b>", "\n", "    ", "<i>", "\n", "        ", "HelloWorld", "\n", "    ", "</i>", "\n", "</b>", "\n"]
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
    with pxml.tag("b"):
        with pxml.tag("i"):
            with pxml.tag("u"):
                pxml.indent().insert("HelloWorld").newline()
    assert pxml.raw == ["<b>", "\n", "    ", "<i>", "\n", "        ", "<u>", "\n", "            ", "HelloWorld", "\n", "        ", "</u>", "\n", "    ", "</i>", "\n", "</b>", "\n"]
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
    with pxml.tag("b"):
        pxml.indent().insert("Hello").newline()
    with pxml.tag("b"):
        pxml.indent().insert("World").newline()
    assert pxml.raw == ["<b>", "\n", "    ", "Hello", "\n", "</b>", "\n", "<b>", "\n", "    ", "World", "\n", "</b>", "\n"]
    assert str(pxml) == "<b>\n    Hello\n</b>\n<b>\n    World\n</b>\n"

    """
    <span id="Hello">
        Hello
    </span>
    """
    pxml = PXML(4)
    with pxml.tag("span", [("id", "Hello")]):
        pxml.indent().insert("Hello").newline()
    assert pxml.raw == ['<span id="Hello">', "\n", "    ", "Hello", "\n", "</span>", "\n"]
    assert str(pxml) == '<span id="Hello">\n    Hello\n</span>\n'

    """
    <span id="Hello">
        <span id="World">
            HelloWorld
        </span>
    </span>
    """
    pxml = PXML(4)
    with pxml.tag("span", [("id", "Hello")]):
        with pxml.tag("span", [("id", "World")]):
            pxml.indent().insert("HelloWorld").newline()
    assert pxml.raw == ['<span id="Hello">', "\n", "    ", '<span id="World">', "\n", "        ", "HelloWorld", "\n", "    ", "</span>", "\n", "</span>", "\n"]
    assert str(pxml) == '<span id="Hello">\n    <span id="World">\n        HelloWorld\n    </span>\n</span>\n'
