import unittest

from pxml import PXML


class TestPXML(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_type_check(self):
        types = [None, True, 1, 0.1, 1j, "Hi", "", [], (), {}]

        ### test _verify_str_ ###

        # no strings
        with self.assertRaises(TypeError):
            for element in [x for x in types if not isinstance(x, str)]:
                PXML._verify_str_(element)

        # only strings
        for element in [x for x in types if isinstance(x, str)]:
            self.assertIsNone(PXML._verify_str_(element))

        ### test _verify_attr_ ###

        # no lists
        with self.assertRaises(TypeError):
            for element in [x for x in types if not isinstance(x, list)]:
                PXML._verify_attr_(element)

        # empty list
        self.assertIsNone(PXML._verify_attr_([]))

        # 1 element lists
        with self.assertRaises(TypeError):
            for element in [[x] for x in types]:
                PXML._verify_attr_(element)

        # 2 element lists
        with self.assertRaises(TypeError):
            for element in [[x, y] for x in types for y in types]:
                PXML._verify_attr_(element)

        # 3 element lists
        with self.assertRaises(TypeError):
            for element in [[x, y, z] for x in types for y in types for z in types]:
                PXML._verify_attr_(element)

        # 1-tuple lists
        with self.assertRaises(TypeError):
            for element in [[(x,)] for x in types]:
                PXML._verify_attr_(element)

        # 2-tuple lists, no strings
        with self.assertRaises(TypeError):
            for element in [[(x, y)] for x in types if not isinstance(x, str) for y in types if not isinstance(y, str)]:
                PXML._verify_attr_(element)

        # 3-tuple lists
        with self.assertRaises(TypeError):
            for element in [[(x, y, z)] for x in types for y in types for z in types]:
                PXML._verify_attr_(element)

        # 2-tuple lists, only strings
        for element in [[(x, y)] for x in types if isinstance(x, str) for y in types if isinstance(y, str)]:
            self.assertIsNone(PXML._verify_attr_(element))

    def test_attributes(self):
        self.assertEqual('', PXML.attributes([]))
        self.assertEqual(' hello="world"', PXML.attributes([("hello", "world")]))
        self.assertEqual(' a="1" b="2"', PXML.attributes([("a", "1"), ("b", "2")]))
        self.assertEqual(' a="1" b="2" c="3"', PXML.attributes([("a", "1"), ("b", "2"), ("c", "3")]))

    def test_indent(self):
        for spaces in range(5):
            for depth in range(5):
                self.assertEqual(" " * spaces * depth, PXML.indent(spaces, depth))

    def test_insert(self):
        pxml = PXML()

        pxml.insert("Hello")
        self.assertEqual(pxml.raw, ["Hello"])
        self.assertEqual(str(pxml), "Hello")

        pxml.insert("World")
        self.assertEqual(pxml.raw, ["Hello", "World"])
        self.assertEqual(str(pxml), "HelloWorld")

        pxml.depth = 1
        pxml.insert("One")
        one = PXML.indent(pxml.spaces, pxml.depth)
        self.assertEqual(pxml.raw, ["Hello", "World", one + "One"])
        self.assertEqual(str(pxml), "HelloWorld{}One".format(one))

        pxml.depth = 2
        pxml.insert("Two")
        two = PXML.indent(pxml.spaces, pxml.depth)
        self.assertEqual(pxml.raw, ["Hello", "World", one + "One", two + "Two"])
        self.assertEqual(str(pxml), "HelloWorld{}One{}Two".format(one, two))

        pxml.depth = 3
        pxml.insert("Three")
        three = PXML.indent(pxml.spaces, pxml.depth)
        self.assertEqual(pxml.raw, ["Hello", "World", one + "One", two + "Two", three + "Three"])
        self.assertEqual(str(pxml), "HelloWorld{}One{}Two{}Three".format(one, two, three))

        pxml.depth = 0
        pxml.insert("Bye").insert("Bye")
        self.assertEqual(pxml.raw, ["Hello", "World", one + "One", two + "Two", three + "Three", "Bye", "Bye"])
        self.assertEqual(str(pxml), "HelloWorld{}One{}Two{}ThreeByeBye".format(one, two, three))

    def test_newline(self):
        pxml = PXML()

        pxml.newline()
        self.assertEqual(pxml.raw, ["\n"])
        self.assertEqual(str(pxml), "\n")

        pxml.newline()
        self.assertEqual(pxml.raw, ["\n", "\n"])
        self.assertEqual(str(pxml), "\n\n")

        pxml.depth = 1
        pxml.newline()
        self.assertEqual(pxml.raw, ["\n", "\n", "\n"])
        self.assertEqual(str(pxml), "\n\n\n")

        pxml.depth = 2
        pxml.newline()
        self.assertEqual(pxml.raw, ["\n", "\n", "\n", "\n"])
        self.assertEqual(str(pxml), "\n\n\n\n")

        pxml.depth = 3
        pxml.newline()
        self.assertEqual(pxml.raw, ["\n", "\n", "\n", "\n", "\n"])
        self.assertEqual(str(pxml), "\n\n\n\n\n")

        pxml.depth = 0
        pxml.newline().newline()
        self.assertEqual(pxml.raw, ["\n", "\n", "\n", "\n", "\n", "\n", "\n"])
        self.assertEqual(str(pxml), "\n\n\n\n\n\n\n")


if __name__ == "__main__":
    unittest.main()
