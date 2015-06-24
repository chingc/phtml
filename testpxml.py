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
        self.assertEqual('', PXML.attributes([]))
        self.assertEqual(' hello="world"', PXML.attributes([("hello", "world")]))
        self.assertEqual(' a="1" b="2"', PXML.attributes([("a", "1"), ("b", "2")]))
        self.assertEqual(' a="1" b="2" c="3"', PXML.attributes([("a", "1"), ("b", "2"), ("c", "3")]))

    def test_indent(self):
        pxml = PXML()

        for spaces in range(5):
            pxml.spaces = spaces
            for depth in range(5):
                pxml.depth = depth
                self.assertEqual(" " * spaces * depth, pxml.indent())

    def test_insert(self):
        pxml = PXML()

        pxml.insert("Hello")
        self.assertEqual(["Hello"], pxml.raw)
        self.assertEqual("Hello", str(pxml))

        pxml.insert("World")
        self.assertEqual(["Hello", "World"], pxml.raw)
        self.assertEqual("HelloWorld", str(pxml))

        pxml.depth = 1
        pxml.insert("One")
        one = pxml.indent()
        self.assertEqual(["Hello", "World", one + "One"], pxml.raw)
        self.assertEqual("HelloWorld{}One".format(one), str(pxml))

        pxml.depth = 2
        pxml.insert("Two")
        two = pxml.indent()
        self.assertEqual(["Hello", "World", one + "One", two + "Two"], pxml.raw)
        self.assertEqual("HelloWorld{}One{}Two".format(one, two), str(pxml))

        pxml.depth = 3
        pxml.insert("Three")
        three = pxml.indent()
        self.assertEqual(["Hello", "World", one + "One", two + "Two", three + "Three"], pxml.raw)
        self.assertEqual("HelloWorld{}One{}Two{}Three".format(one, two, three), str(pxml))

        pxml.depth = 0
        pxml.insert("Bye").insert("Bye")
        self.assertEqual(["Hello", "World", one + "One", two + "Two", three + "Three", "Bye", "Bye"], pxml.raw)
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

    def test_itag(self):
        # <b>HelloWorld</b>
        # <b><i>HelloWorld</i></b>
        # <b><i><u>HelloWorld</u></i></b>
        # <b>Hello</b><b>World</b>
        # <span id="Hello">Hello</span>
        # <span id="Hello"><span id="World">HelloWorld</span></span>
        # <span>Hello</span><span>World</span>
        pass


if __name__ == "__main__":
    unittest.main()
