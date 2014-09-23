import unittest
import interpreter

class TestParse(unittest.TestCase):
	def test_it_tokenizes_expressions(self):
		self.assertEquals(interpreter.tokenize('(1 2 32)'), ["(", "1", "2", "32", ")"])

	def test_it_parses_lists(self):
		self.assertEquals(interpreter.read('(1 2 3)'), ["1", "2", "3"])

	def test_it_parses_nested_lists(self):
		self.assertEquals(interpreter.read('(1 2 (23 hello (another list 43)))'), ["1", "2", ["23", "hello", ["another", "list", "43"]]])

	def test_it_adds(self):
		self.assertEquals(interpreter.eval('(+ 4 3)'), 7)

if __name__ == "__main__":
	unittest.main()
