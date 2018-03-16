# pylint: skip-file

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE.parent.joinpath("src")))

from pxml.pxml import PXML


def _read(filename):
    with open(HERE.joinpath(filename), "r") as f:
        return f.read()


@pytest.fixture
def pxml():
    return PXML()


class TestDunder():
    def test_dunder(self, pxml):
        assert not len(pxml)
        pxml.append("a")
        assert "a" in pxml
        assert len(pxml) == 2  # + 1 due to newline
        assert str(pxml) == repr(pxml) == pxml == PXML().append("a") == "a\n"


class TestAttribute():
    bad_in = [None, True, 1, [], {}, (), ("a",), ("a", "b", "c")]  # non-strings and len(tuple) != 2
    good_in = [["a"], ["a", "b"], [("a", 1)], [("a", 1), ("b", "2")], ["a", ("b", 2)], [("a", 1), "b"]]
    good_out = ["a", "a b", 'a="1"', 'a="1" b="2"', 'a b="2"', 'a="1" b', 1]

    def test_empty_input(self):
        assert PXML.attr() == ""

    @pytest.mark.parametrize("test_input, expected", list(zip(good_in, good_out)))
    def test_good_input(self, test_input, expected):
        assert PXML.attr(*test_input) == expected

    @pytest.mark.parametrize("bad", bad_in)
    def test_bad_input(self, bad):
        with pytest.raises(ValueError):
            PXML.attr(bad)


class TestAppend():
    @pytest.mark.parametrize("repeat", range(4))
    def test_with_newline(self, pxml, repeat):
        for _ in range(repeat):
            pxml.append("a")
        assert pxml == "a\n" * repeat

    @pytest.mark.parametrize("repeat", range(4))
    def test_without_newline(self, pxml, repeat):
        pxml.oneline = True
        for _ in range(repeat):
            pxml.append("a")
        assert pxml == "a" * repeat

    @pytest.mark.parametrize("bad", [None, True, 1])
    def test_non_string_type(self, pxml, bad):
        with pytest.raises(ValueError):
            pxml.append(bad)


class TestIndent():
    @pytest.mark.parametrize("spaces", range(4))
    @pytest.mark.parametrize("depth", range(4))
    def test_depth(self, pxml, spaces, depth):
        pxml.spaces = spaces
        pxml.depth = depth
        assert pxml.indent() == " " * pxml.spaces * pxml.depth


class TestNewline():
    @pytest.mark.parametrize("depth", range(2))
    def test_depth_does_not_indent(self, pxml, depth):
        pxml.depth = depth
        pxml.newline().newline()
        assert pxml == "\n\n"
        pxml.newline().newline()
        assert " " not in pxml


class TestVoidElement():
    def test_without_attribute(self, pxml):
        pxml.vwrap("br")
        assert pxml == "<br>\n"

    def test_with_attribute(self, pxml):
        pxml.vwrap("img", PXML.attr("abc", ("x", 1), ("y", 2), ("z", 3)))
        assert pxml == '<img abc x="1" y="2" z="3">\n'

    @pytest.mark.parametrize("bad", ["a", "b", "c"])
    def test_non_void_element(self, pxml, bad):
        with pytest.raises(ValueError):
            pxml.vwrap(bad)


class TestOneline():
    def test_single(self, pxml):
        with pxml.owrap("a"):
            pxml.append("1")
        assert pxml == "<a>1</a>"

    def test_nested(self, pxml):
        with pxml.owrap("a"), pxml.owrap("b"):
            pxml.append("1 2")
        assert pxml == "<a><b>1 2</b></a>"

    def test_double_nested(self, pxml):
        with pxml.owrap("a"), pxml.owrap("b"), pxml.owrap("c"):
            pxml.append("1 2 3")
        assert pxml == "<a><b><c>1 2 3</c></b></a>"

    def test_side_by_side(self, pxml):
        with pxml.owrap("a"):
            pxml.append("1")
        with pxml.owrap("b"):
            pxml.append("2")
        assert pxml == "<a>1</a><b>2</b>"

    def test_nested_side_by_side(self, pxml):
        with pxml.owrap("a"):
            with pxml.owrap("b"):
                pxml.append("2")
            with pxml.owrap("c"):
                pxml.append("3")
        assert pxml == "<a><b>2</b><c>3</c></a>"


class TestWrap():
    def test_single(self, pxml):
        with pxml.wrap("a"):
            pxml.append("1")
        assert pxml == _read("expected_single.txt")

    def test_nested(self, pxml):
        with pxml.wrap("a"), pxml.wrap("b"):
            pxml.append("1 2")
        assert pxml == _read("expected_nested.txt")

    def test_double_nested(self, pxml):
        with pxml.wrap("a"), pxml.wrap("b"), pxml.wrap("c"):
            pxml.append("1 2 3")
        assert pxml == _read("expected_double_nested.txt")

    def test_side_by_side(self, pxml):
        with pxml.wrap("a"):
            pxml.append("1")
        with pxml.wrap("b"):
            pxml.append("2")
        assert pxml == _read("expected_side_by_side.txt")

    def test_nested_side_by_side(self, pxml):
        with pxml.wrap("a"):
            with pxml.wrap("b"):
                pxml.append("2")
            with pxml.wrap("c"):
                pxml.append("3")
        assert pxml == _read("expected_nested_side_by_side.txt")

    def test_nested_oneline(self, pxml):
        with pxml.wrap("a"):
            with pxml.owrap("b"):
                pxml.append("2")
        assert pxml == _read("expected_nested_oneline.txt")

    def test_nested_oneline_side_by_side(self, pxml):
        with pxml.wrap("a"):
            with pxml.owrap("b", newline=True):
                pxml.append("2")
            with pxml.owrap("c"):
                pxml.append("3")
        assert pxml == _read("expected_nested_oneline_side_by_side.txt")

    def test_complex(self, pxml):
        with pxml.wrap("a"):
            pxml.append("1")
            pxml.newline()
            with pxml.wrap("b"):
                pxml.append("2")
            pxml.newline()
            with pxml.owrap("c", newline=True):
                pxml.append("3")
            with pxml.owrap("d"):
                pxml.append("4")
            pxml.newline()
            with pxml.wrap("e"):
                pxml.append("5")
                pxml.newline()
            with pxml.owrap("f"):
                pxml.append("6")
            pxml.newline()
            with pxml.wrap("g"):
                with pxml.wrap("h"):
                    pxml.append("8")
                    with pxml.owrap("i"):
                        pxml.append("9")
                    with pxml.owrap("j", newline=True):
                        pxml.append("10")
                    pxml.newline()
                    with pxml.owrap("k", newline=True), pxml.owrap("l"):
                        pxml.append("11 12")
                pxml.append("7")
        assert pxml == _read("expected_complex.txt")
