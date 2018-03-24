# pylint: skip-file

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE.parent.joinpath("src")))

from phtml.phtml import PHTML


def _read(filename):
    with open(HERE.joinpath(filename), "r") as f:
        return f.read()


@pytest.fixture
def phtml():
    return PHTML()


class TestDunder():
    def test_dunder(self, phtml):
        assert not len(phtml)
        phtml.append("a")
        assert "a" in phtml
        assert len(phtml) == 2  # + 1 due to newline
        assert str(phtml) == repr(phtml) == phtml == PHTML().append("a") == "a\n"


class TestAttribute():
    bad_in = [None, True, 1, [], {}, (), ("a",), ("a", "b", "c")]  # non-strings and len(tuple) != 2
    good_in = [["a"], ["a", "b"], [("a", 1)], [("a", 1), ("b", "2")], ["a", ("b", 2)], [("a", 1), "b"]]
    good_out = ["a", "a b", 'a="1"', 'a="1" b="2"', 'a b="2"', 'a="1" b', 1]

    def test_empty_input(self):
        assert PHTML.attr() == ""

    @pytest.mark.parametrize("test_input, expected", list(zip(good_in, good_out)))
    def test_good_input(self, test_input, expected):
        assert PHTML.attr(*test_input) == expected

    @pytest.mark.parametrize("bad", bad_in)
    def test_bad_input(self, bad):
        with pytest.raises(ValueError):
            PHTML.attr(bad)


class TestAppend():
    @pytest.mark.parametrize("repeat", range(4))
    def test_with_newline(self, phtml, repeat):
        for _ in range(repeat):
            phtml.append("a")
        assert phtml == "a\n" * repeat

    @pytest.mark.parametrize("repeat", range(4))
    def test_without_newline(self, phtml, repeat):
        phtml.oneline = True
        for _ in range(repeat):
            phtml.append("a")
        assert phtml == "a" * repeat

    @pytest.mark.parametrize("bad", [None, True, 1])
    def test_non_string_type(self, phtml, bad):
        with pytest.raises(ValueError):
            phtml.append(bad)


class TestIndent():
    @pytest.mark.parametrize("spaces", range(4))
    @pytest.mark.parametrize("depth", range(4))
    def test_depth(self, phtml, spaces, depth):
        phtml.spaces = spaces
        phtml.depth = depth
        assert phtml.indent() == " " * phtml.spaces * phtml.depth


class TestNewline():
    @pytest.mark.parametrize("depth", range(2))
    def test_depth_does_not_indent(self, phtml, depth):
        phtml.depth = depth
        phtml.newline().newline()
        assert phtml == "\n\n"
        phtml.newline().newline()
        assert " " not in phtml


class TestVoidElement():
    def test_without_attribute(self, phtml):
        phtml.vwrap("br")
        assert phtml == "<br>\n"

    def test_with_attribute(self, phtml):
        phtml.vwrap("img", PHTML.attr("abc", ("x", 1), ("y", 2), ("z", 3)))
        assert phtml == '<img abc x="1" y="2" z="3">\n'

    @pytest.mark.parametrize("bad", ["a", "b", "c"])
    def test_non_void_element(self, phtml, bad):
        with pytest.raises(ValueError):
            phtml.vwrap(bad)


class TestOneline():
    def test_single(self, phtml):
        with phtml.owrap("a"):
            phtml.append("1")
        assert phtml == "<a>1</a>"

    def test_nested(self, phtml):
        with phtml.owrap("a"), phtml.owrap("b"):
            phtml.append("1 2")
        assert phtml == "<a><b>1 2</b></a>"

    def test_double_nested(self, phtml):
        with phtml.owrap("a"), phtml.owrap("b"), phtml.owrap("c"):
            phtml.append("1 2 3")
        assert phtml == "<a><b><c>1 2 3</c></b></a>"

    def test_side_by_side(self, phtml):
        with phtml.owrap("a"):
            phtml.append("1")
        with phtml.owrap("b"):
            phtml.append("2")
        assert phtml == "<a>1</a><b>2</b>"

    def test_nested_side_by_side(self, phtml):
        with phtml.owrap("a"):
            with phtml.owrap("b"):
                phtml.append("2")
            with phtml.owrap("c"):
                phtml.append("3")
        assert phtml == "<a><b>2</b><c>3</c></a>"


class TestWrap():
    def test_single(self, phtml):
        with phtml.wrap("a"):
            phtml.append("1")
        assert phtml == _read("expected_single.txt")

    def test_nested(self, phtml):
        with phtml.wrap("a"), phtml.wrap("b"):
            phtml.append("1 2")
        assert phtml == _read("expected_nested.txt")

    def test_double_nested(self, phtml):
        with phtml.wrap("a"), phtml.wrap("b"), phtml.wrap("c"):
            phtml.append("1 2 3")
        assert phtml == _read("expected_double_nested.txt")

    def test_side_by_side(self, phtml):
        with phtml.wrap("a"):
            phtml.append("1")
        with phtml.wrap("b"):
            phtml.append("2")
        assert phtml == _read("expected_side_by_side.txt")

    def test_nested_side_by_side(self, phtml):
        with phtml.wrap("a"):
            with phtml.wrap("b"):
                phtml.append("2")
            with phtml.wrap("c"):
                phtml.append("3")
        assert phtml == _read("expected_nested_side_by_side.txt")

    def test_nested_oneline(self, phtml):
        with phtml.wrap("a"):
            with phtml.owrap("b"):
                phtml.append("2")
        assert phtml == _read("expected_nested_oneline.txt")

    def test_nested_oneline_side_by_side(self, phtml):
        with phtml.wrap("a"):
            with phtml.owrap("b", newline=True):
                phtml.append("2")
            with phtml.owrap("c"):
                phtml.append("3")
        assert phtml == _read("expected_nested_oneline_side_by_side.txt")

    def test_complex(self, phtml):
        with phtml.wrap("a"):
            phtml.append("1")
            phtml.newline()
            with phtml.wrap("b"):
                phtml.append("2")
            phtml.newline()
            with phtml.owrap("c", newline=True):
                phtml.append("3")
            with phtml.owrap("d"):
                phtml.append("4")
            phtml.newline()
            with phtml.wrap("e"):
                phtml.append("5")
                phtml.newline()
            with phtml.owrap("f"):
                phtml.append("6")
            phtml.newline()
            with phtml.wrap("g"):
                with phtml.wrap("h"):
                    phtml.append("8")
                    with phtml.owrap("i"):
                        phtml.append("9")
                    with phtml.owrap("j", newline=True):
                        phtml.append("10")
                    phtml.newline()
                    with phtml.owrap("k", newline=True), phtml.owrap("l"):
                        phtml.append("11 12")
                phtml.append("7")
        assert phtml == _read("expected_complex.txt")
