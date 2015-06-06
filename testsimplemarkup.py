import unittest

import simplemarkup


class TestSimpleMarkup(unittest.TestCase):

    def setUp(self):
        self.sm = simplemarkup.SimpleMarkup()

    def tearDown(self):
        del self.sm

    def test_type_check(self):
        types = [None, True, 1, 0.1, 1j, "Hi", "", [], (), {}]

        ### test _verify_str_ ###

        # no strings
        with self.assertRaises(TypeError):
            for element in [x for x in types if not isinstance(x, str)]:
                self.sm._verify_str_(element)

        # only strings
        for element in [x for x in types if isinstance(x, str)]:
            self.assertIsNone(self.sm._verify_str_(element))

        ### test _verify_attr_ ###

        # no lists
        with self.assertRaises(TypeError):
            for element in [x for x in types if not isinstance(x, list)]:
                self.sm._verify_attr_(element)

        # empty list
        self.assertIsNone(self.sm._verify_attr_([]))

        # 1 element lists
        with self.assertRaises(TypeError):
            for element in [[x] for x in types]:
                self.sm._verify_attr_(element)

        # 2 element lists
        with self.assertRaises(TypeError):
            for element in [[x, y] for x in types for y in types]:
                self.sm._verify_attr_(element)

        # 3 element lists
        with self.assertRaises(TypeError):
            for element in [[x, y, z] for x in types for y in types for z in types]:
                self.sm._verify_attr_(element)

        # 1-tuple lists
        with self.assertRaises(TypeError):
            for element in [[(x,)] for x in types]:
                self.sm._verify_attr_(element)

        # 2-tuple lists, no strings
        with self.assertRaises(TypeError):
            for element in [[(x, y)] for x in types if not isinstance(x, str) for y in types if not isinstance(y, str)]:
                self.sm._verify_attr_(element)

        # 3-tuple lists
        with self.assertRaises(TypeError):
            for element in [[(x, y, z)] for x in types for y in types for z in types]:
                self.sm._verify_attr_(element)

        # 2-tuple lists, only strings
        for element in [[(x, y)] for x in types if isinstance(x, str) for y in types if isinstance(y, str)]:
            self.assertIsNone(self.sm._verify_attr_(element))

    def test_expand_attr(self):
        self.assertEqual('', self.sm._expand_attr_([]))
        self.assertEqual(' hello="world"', self.sm._expand_attr_([("hello", "world")]))
        self.assertEqual(' a="1" b="2"', self.sm._expand_attr_([("a", "1"), ("b", "2")]))
        self.assertEqual(' a="1" b="2" c="3"', self.sm._expand_attr_([("a", "1"), ("b", "2"), ("c", "3")]))

    def test_insert(self):
        self.sm.insert("Hello")
        self.assertEqual(self.sm.raw, ["Hello"])
        self.assertEqual(self.sm.out(), "Hello")

        self.sm.insert("World")
        self.assertEqual(self.sm.raw, ["Hello", "World"])
        self.assertEqual(self.sm.out(), "HelloWorld")

        self.sm.depth = 1
        self.sm.insert("One")
        one = self.sm.indent * self.sm.depth
        self.assertEqual(self.sm.raw, ["Hello", "World", one + "One"])
        self.assertEqual(self.sm.out(), "HelloWorld{}One".format(one))

        self.sm.depth = 2
        self.sm.insert("Two")
        two = self.sm.indent * self.sm.depth
        self.assertEqual(self.sm.raw, ["Hello", "World", one + "One", two + "Two"])
        self.assertEqual(self.sm.out(), "HelloWorld{}One{}Two".format(one, two))

        self.sm.depth = 3
        self.sm.insert("Three")
        three = self.sm.indent * self.sm.depth
        self.assertEqual(self.sm.raw, ["Hello", "World", one + "One", two + "Two", three + "Three"])
        self.assertEqual(self.sm.out(), "HelloWorld{}One{}Two{}Three".format(one, two, three))

        self.sm.depth = 0
        self.sm.insert("Bye").insert("Bye")
        self.assertEqual(self.sm.raw, ["Hello", "World", one + "One", two + "Two", three + "Three", "Bye", "Bye"])
        self.assertEqual(self.sm.out(), "HelloWorld{}One{}Two{}ThreeByeBye".format(one, two, three))

    def test_newline(self):
        self.sm.newline()
        self.assertEqual(self.sm.raw, ["\n"])
        self.assertEqual(self.sm.out(), "\n")

        self.sm.newline()
        self.assertEqual(self.sm.raw, ["\n", "\n"])
        self.assertEqual(self.sm.out(), "\n\n")

        self.sm.depth = 1
        self.sm.newline()
        self.assertEqual(self.sm.raw, ["\n", "\n", "\n"])
        self.assertEqual(self.sm.out(), "\n\n\n")

        self.sm.depth = 2
        self.sm.newline()
        self.assertEqual(self.sm.raw, ["\n", "\n", "\n", "\n"])
        self.assertEqual(self.sm.out(), "\n\n\n\n")

        self.sm.depth = 3
        self.sm.newline()
        self.assertEqual(self.sm.raw, ["\n", "\n", "\n", "\n", "\n"])
        self.assertEqual(self.sm.out(), "\n\n\n\n\n")

        self.sm.depth = 0
        self.sm.newline().newline()
        self.assertEqual(self.sm.raw, ["\n", "\n", "\n", "\n", "\n", "\n", "\n"])
        self.assertEqual(self.sm.out(), "\n\n\n\n\n\n\n")


if __name__ == "__main__":
    unittest.main()
