import unittest
from itertools import permutations

from pxml import PXML


class TestPXML(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_str(self):
        types = [None, True, 1, "", "string", [], (), {}]

        # pass: string
        for element in [t for t in types if isinstance(t, str)]:
            self.assertIsNone(PXML.check_str(element))

        # fail: non-string
        for element in [t for t in types if not isinstance(t, str)]:
            with self.assertRaises(TypeError):
                PXML.check_str(element)

    def test_check_attr(self):
        types = [None, True, 1, "", "string", [], (), {}]

        # pass: empty list
        self.assertIsNone(PXML.check_attr([]))

        # pass: list of 2-tuple (tuple elements are strings)
        for element in permutations([t for t in types if isinstance(t, str)], 2):
            self.assertIsNone(PXML.check_attr([element]))

        # fail: non-list
        for element in [t for t in types if not isinstance(t, list)]:
            with self.assertRaises(TypeError):
                PXML.check_attr(element)

        # fail: 1 element list (element is not a 2-tuple of strings)
        for element in permutations(types, 1):
            with self.assertRaises(TypeError):
                PXML.check_attr(list(element))

        # fail: 2 element list (elements are not a 2-tuple of strings)
        for element in permutations(types, 2):
            with self.assertRaises(TypeError):
                PXML.check_attr(list(element))

        # fail: 3 element list (elements are not a 2-tuple of strings)
        for element in permutations(types, 3):
            with self.assertRaises(TypeError):
                PXML.check_attr(list(element))

        # fail: list of 1-tuple
        for element in permutations(types, 1):
            with self.assertRaises(TypeError):
                PXML.check_attr([element])

        # fail: list of 2-tuple (tuple elements are non-strings)
        for element in permutations([t for t in types if not isinstance(t, str)], 2):
            with self.assertRaises(TypeError):
                PXML.check_attr([element])

        # fail: list of 3-tuple
        for element in permutations(types, 3):
            with self.assertRaises(TypeError):
                PXML.check_attr([element])

    def test_attributes(self):
        self.assertEqual("", PXML.attributes([]))
        self.assertEqual(' hello="world"', PXML.attributes([("hello", "world")]))
        self.assertEqual(' a="1" b="2"', PXML.attributes([("a", "1"), ("b", "2")]))
        self.assertEqual(' a="1" b="2" c="3"', PXML.attributes([("a", "1"), ("b", "2"), ("c", "3")]))

    def test_indent(self):
        pxml = PXML()
        pxml.indent()
        self.assertEqual([], pxml.raw)
        self.assertEqual("", str(pxml))

        pxml = PXML(4)
        pxml.depth = 1
        pxml.indent(5)
        self.assertEqual([" " * pxml.spaces] * 5, pxml.raw)
        self.assertEqual(" " * pxml.spaces * 5, str(pxml))

        for spaces in range(1, 5):
            for depth in range(1, 5):
                pxml = PXML(spaces)
                pxml.depth = depth
                pxml.indent()
                self.assertEqual([" " * spaces * depth], pxml.raw)
                self.assertEqual(" " * spaces * depth, str(pxml))

    def test_insert(self):
        pxml = PXML(4)
        pxml.insert("Hello")
        self.assertEqual(["Hello"], pxml.raw)
        self.assertEqual("Hello", str(pxml))

        pxml.insert("World")
        self.assertEqual(["Hello", "World"], pxml.raw)
        self.assertEqual("HelloWorld", str(pxml))

        pxml.depth = 1
        pxml.indent().insert("One")
        one = " " * pxml.spaces * pxml.depth
        self.assertEqual(["Hello", "World", one, "One"], pxml.raw)
        self.assertEqual("HelloWorld{}One".format(one), str(pxml))

        pxml.depth = 2
        pxml.indent().insert("Two")
        two = " " * pxml.spaces * pxml.depth
        self.assertEqual(["Hello", "World", one, "One", two, "Two"], pxml.raw)
        self.assertEqual("HelloWorld{}One{}Two".format(one, two), str(pxml))

        pxml.depth = 3
        pxml.indent().insert("Three")
        three = " " * pxml.spaces * pxml.depth
        self.assertEqual(["Hello", "World", one, "One", two, "Two", three, "Three"], pxml.raw)
        self.assertEqual("HelloWorld{}One{}Two{}Three".format(one, two, three), str(pxml))

        pxml.insert("Bye").insert("Bye")
        self.assertEqual(["Hello", "World", one, "One", two, "Two", three, "Three", "Bye", "Bye"], pxml.raw)
        self.assertEqual("HelloWorld{}One{}Two{}ThreeByeBye".format(one, two, three), str(pxml))

    def test_newline(self):
        pxml = PXML()
        pxml.newline()
        self.assertEqual(["\n"], pxml.raw)
        self.assertEqual("\n", str(pxml))

        pxml.newline()
        self.assertEqual(["\n", "\n"], pxml.raw)
        self.assertEqual("\n\n", str(pxml))

        pxml.newline().newline()
        self.assertEqual(["\n", "\n", "\n", "\n"], pxml.raw)
        self.assertEqual("\n\n\n\n", str(pxml))

        pxml.newline(3)
        self.assertEqual(["\n", "\n", "\n", "\n", "\n", "\n", "\n"], pxml.raw)
        self.assertEqual("\n\n\n\n\n\n\n", str(pxml))

    def test_itag(self):
        pxml = PXML()
        with pxml.itag("b"):
            pxml.insert("HelloWorld")
        self.assertEqual(["<b>", "HelloWorld", "</b>"], pxml.raw)
        self.assertEqual("<b>HelloWorld</b>", str(pxml))

        pxml = PXML()
        with pxml.itag("b"):
            with pxml.itag("i"):
                pxml.insert("HelloWorld")
        self.assertEqual(["<b>", "<i>", "HelloWorld", "</i>", "</b>"], pxml.raw)
        self.assertEqual("<b><i>HelloWorld</i></b>", str(pxml))

        pxml = PXML()
        with pxml.itag("b"):
            with pxml.itag("i"):
                with pxml.itag("u"):
                    pxml.insert("HelloWorld")
        self.assertEqual(["<b>", "<i>", "<u>","HelloWorld", "</u>", "</i>", "</b>"], pxml.raw)
        self.assertEqual("<b><i><u>HelloWorld</u></i></b>", str(pxml))

        pxml = PXML()
        with pxml.itag("b"):
            pxml.insert("Hello")
        with pxml.itag("b"):
            pxml.insert("World")
        self.assertEqual(["<b>", "Hello", "</b>", "<b>", "World", "</b>"], pxml.raw)
        self.assertEqual("<b>Hello</b><b>World</b>", str(pxml))

        pxml = PXML()
        with pxml.itag("span", [("id", "Hello")]):
            pxml.insert("Hello")
        self.assertEqual(['<span id="Hello">', "Hello", "</span>"], pxml.raw)
        self.assertEqual('<span id="Hello">Hello</span>', str(pxml))

        pxml = PXML()
        with pxml.itag("span", [("id", "Hello")]):
            with pxml.itag("span", [("id", "World")]):
                pxml.insert("HelloWorld")
        self.assertEqual(['<span id="Hello">', '<span id="World">', "HelloWorld", "</span>", "</span>"], pxml.raw)
        self.assertEqual('<span id="Hello"><span id="World">HelloWorld</span></span>', str(pxml))

    def test_tag(self):
        """
        <b>
            HelloWorld
        </b>
        """
        pxml = PXML(4)
        with pxml.tag("b"):
            pxml.indent().insert("HelloWorld").newline()
        self.assertEqual(["<b>", "\n", "    ", "HelloWorld", "\n", "</b>", "\n"], pxml.raw)
        self.assertEqual("<b>\n    HelloWorld\n</b>\n", str(pxml))

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
        self.assertEqual(["<b>", "\n", "    ", "<i>", "\n", "        ", "HelloWorld", "\n", "    ", "</i>", "\n", "</b>", "\n"], pxml.raw)
        self.assertEqual("<b>\n    <i>\n        HelloWorld\n    </i>\n</b>\n", str(pxml))

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
        self.assertEqual(["<b>", "\n", "    ", "<i>", "\n", "        ", "<u>", "\n", "            ", "HelloWorld", "\n", "        ", "</u>", "\n", "    ", "</i>", "\n", "</b>", "\n"], pxml.raw)
        self.assertEqual("<b>\n    <i>\n        <u>\n            HelloWorld\n        </u>\n    </i>\n</b>\n", str(pxml))

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
        self.assertEqual(["<b>", "\n", "    ", "Hello", "\n", "</b>", "\n", "<b>", "\n", "    ", "World", "\n", "</b>", "\n"], pxml.raw)
        self.assertEqual("<b>\n    Hello\n</b>\n<b>\n    World\n</b>\n", str(pxml))

        """
        <span id="Hello">
            Hello
        </span>
        """
        pxml = PXML(4)
        with pxml.tag("span", [("id", "Hello")]):
            pxml.indent().insert("Hello").newline()
        self.assertEqual(['<span id="Hello">', "\n", "    ", "Hello", "\n", "</span>", "\n"], pxml.raw)
        self.assertEqual('<span id="Hello">\n    Hello\n</span>\n', str(pxml))

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
        self.assertEqual(['<span id="Hello">', "\n", "    ", '<span id="World">', "\n", "        ", "HelloWorld", "\n", "    ", "</span>", "\n", "</span>", "\n"], pxml.raw)
        self.assertEqual('<span id="Hello">\n    <span id="World">\n        HelloWorld\n    </span>\n</span>\n', str(pxml))


if __name__ == "__main__":
    unittest.main()
