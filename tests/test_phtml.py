# pylint: disable=C0111,C0301

import pytest


class TestDunder():
    def test_contains(self, poff):
        assert "a" not in poff
        poff.append("a")
        assert "a" in poff

    def test_eq_repr_str(self, poff):
        assert repr(poff) == str(poff) == poff == ""
        poff.append("a")
        assert repr(poff) == str(poff) == poff == "a"

    def test_len(self, poff):
        assert not poff
        poff.append("a")
        assert len(poff) == 1


class TestAttribute():
    bad_in = [None, True, 1, [], {}, (), ("a",), ("a", "b", "c")]  # non-strings and len(tuple) != 2
    good_in = [["a"], ["a", "b"], [("a", 1)], [("a", 1), ("b", "2")], ["a", ("b", 2)], [("a", 1), "b"]]
    good_out = ["a", "a b", 'a="1"', 'a="1" b="2"', 'a b="2"', 'a="1" b', 1]

    def test_empty_input(self, attr):
        assert attr() == ""

    @pytest.mark.parametrize("test_input, expected", list(zip(good_in, good_out)))
    def test_good_input(self, attr, test_input, expected):
        assert attr(*test_input) == expected

    @pytest.mark.parametrize("bad", bad_in)
    def test_bad_input(self, attr, bad):
        with pytest.raises(ValueError):
            attr(bad)


class TestAppend():
    @pytest.mark.parametrize("repeat", range(4))
    def test_with_newline(self, pon, repeat):
        for _ in range(repeat):
            pon.append("a")
        assert pon == "a\n" * repeat

    @pytest.mark.parametrize("repeat", range(4))
    def test_without_newline(self, poff, repeat):
        for _ in range(repeat):
            poff.append("a")
        assert poff == "a" * repeat

    @pytest.mark.parametrize("bad", [None, True, 1])
    def test_non_string_type(self, poff, bad):
        with pytest.raises(ValueError):
            poff.append(bad)


class TestIndent():
    @pytest.mark.parametrize("spaces", range(4))
    @pytest.mark.parametrize("depth", range(4))
    def test_depth(self, poff, spaces, depth):
        poff.depth = depth
        poff.spaces = spaces
        assert poff.indent() == " " * poff.spaces * poff.depth


class TestNewline():
    @pytest.mark.parametrize("depth", range(2))
    def test_depth_does_not_indent(self, poff, depth):
        poff.depth = depth
        poff.newline().newline()
        assert poff == "\n\n"
        poff.newline().newline()
        assert " " not in poff


class TestVoidWrap():
    def test_without_attribute(self, poff):
        poff.vwrap("br")
        assert poff == "<br>"

    def test_with_attribute(self, attr, poff):
        poff.vwrap("img", attr("abc", ("x", 1), ("y", 2), ("z", 3)))
        assert poff == '<img abc x="1" y="2" z="3">'

    @pytest.mark.parametrize("bad", ["a", "b", "c"])
    def test_non_void_element(self, poff, bad):
        with pytest.raises(ValueError):
            poff.vwrap(bad)


class TestWrapAutoSpacingOff():
    def test_single(self, poff):
        with poff.wrap("a"):
            poff.append("1")
        assert poff == "<a>1</a>"

    def test_nested(self, poff):
        with poff.wrap("a"), poff.wrap("b"):
            poff.append("1 2")
        assert poff == "<a><b>1 2</b></a>"

    def test_double_nested(self, poff):
        with poff.wrap("a"), poff.wrap("b"), poff.wrap("c"):
            poff.append("1 2 3")
        assert poff == "<a><b><c>1 2 3</c></b></a>"

    def test_sibling(self, poff):
        with poff.wrap("a"):
            poff.append("1")
        with poff.wrap("b"):
            poff.append("2")
        assert poff == "<a>1</a><b>2</b>"

    def test_nested_sibling(self, poff):
        with poff.wrap("a"):
            with poff.wrap("b"):
                poff.append("2")
            with poff.wrap("c"):
                poff.append("3")
        assert poff == "<a><b>2</b><c>3</c></a>"


class TestWrapAutoSpacingOn():
    def test_single(self, pon, expect_file):
        with pon.wrap("a"):
            pon.append("1")
        assert pon == expect_file("expected_single.txt")

    def test_nested(self, pon, expect_file):
        with pon.wrap("a"), pon.wrap("b"):
            pon.append("1 2")
        assert pon == expect_file("expected_nested.txt")

    def test_double_nested(self, pon, expect_file):
        with pon.wrap("a"), pon.wrap("b"), pon.wrap("c"):
            pon.append("1 2 3")
        assert pon == expect_file("expected_double_nested.txt")

    def test_sibling(self, pon, expect_file):
        with pon.wrap("a"):
            pon.append("1")
        with pon.wrap("b"):
            pon.append("2")
        assert pon == expect_file("expected_sibling.txt")

    def test_nested_sibling(self, pon, expect_file):
        with pon.wrap("a"):
            with pon.wrap("b"):
                pon.append("2")
            with pon.wrap("c"):
                pon.append("3")
        assert pon == expect_file("expected_nested_sibling.txt")


class TestWrapAutoSpacingMixed():
    def test_nested_oneline(self, pon, expect_file):
        with pon.wrap("a"):
            pon.auto_spacing = False
            pon.indent()
            with pon.wrap("b"):
                pon.append("2")
            pon.auto_spacing = True
            pon.newline()
        assert pon == expect_file("expected_nested_oneline.txt")

    def test_nested_oneline_sibling(self, pon, expect_file):
        with pon.wrap("a"):
            pon.auto_spacing = False
            pon.indent()
            with pon.wrap("b"):
                pon.append("2")
            pon.newline().indent()
            with pon.wrap("c"):
                pon.append("3")
            pon.newline()
            pon.auto_spacing = True
        assert pon == expect_file("expected_nested_oneline_sibling.txt")

    def test_complex(self, pon, expect_file):
        with pon.wrap("a"):
            pon.append("1")
            pon.newline()
            with pon.wrap("b"):
                pon.append("2")
            pon.newline()
            pon.auto_spacing = False
            pon.indent()
            with pon.wrap("c"):
                pon.append("3")
            pon.newline().indent()
            with pon.wrap("d"):
                pon.append("4")
            pon.newline().newline()
            pon.auto_spacing = True
            with pon.wrap("e"):
                pon.append("5")
                pon.newline()
            pon.auto_spacing = False
            pon.indent()
            with pon.wrap("f"):
                pon.append("6")
            pon.newline().newline()
            pon.auto_spacing = True
            with pon.wrap("g"):
                with pon.wrap("h"):
                    pon.append("8")
                    pon.auto_spacing = False
                    pon.indent()
                    with pon.wrap("i"):
                        pon.append("9")
                    with pon.wrap("j"):
                        pon.append("10")
                    pon.newline().newline().indent()
                    with pon.wrap("k"), pon.wrap("l"):
                        pon.append("11 12")
                    pon.newline()
                    pon.auto_spacing = True
                pon.append("7")
        assert pon == expect_file("expected_complex.txt")
