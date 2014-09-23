import unittest
import interpreter

class TestParse(unittest.TestCase):
    def test_it_tokenizes_expressions(self):
        self.assertEquals(interpreter.tokenize('(1 2 32)'), ["(", "1", "2", "32", ")"])
        self.assertEquals(interpreter.tokenize('(+ 2 32)'), ["(", "+", "2", "32", ")"])

    def test_it_parses_lists(self):
        self.assertEquals(interpreter.read('(1 2 3)'), ["1", "2", "3"])

    def test_it_parses_single_atoms(self):
        self.assertEquals(interpreter.read('1'), "1")

    def test_it_parses_application(self):
        self.assertEquals(interpreter.read('(+ 1 2)'), ["+", "1", "2"])

    def test_it_parses_nested_lists(self):
        self.assertEquals(interpreter.read('(1 2 (23 hello (another list 43)))'), ["1", "2", ["23", "hello", ["another", "list", "43"]]])

    def test_it_adds(self):
        self.assertEquals(interpreter.eval(['+', '4', '3']), 7)
        self.assertEquals(interpreter.eval(['-', '4', '3', '2']), -1)
        self.assertEquals(interpreter.eval(['-', '4']), -4)
        with self.assertRaises(TypeError):
            interpreter.eval(['-'])

    def test_define(self):
        self.assertEquals(interpreter.eval_read('(define a 1)'), None)
        self.assertEquals(interpreter.eval_read('a'), 1)


if __name__ == "__main__":
    unittest.main()
