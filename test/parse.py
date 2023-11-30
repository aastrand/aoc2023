import unittest

from utils.parse import ints


class TestMath(unittest.TestCase):
    def test_ints(self):
        self.assertEqual([], ints(""))
        self.assertEqual([321, 19, 123], ints(
            "jag heter ape 321 och det är 19 fåglar här ååh kaffe är 123"))


if __name__ == "__main__":
    unittest.main()
