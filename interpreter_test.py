import unittest
import interpreter

class TestParse(unittest.TestCase):
    def setUp(self):
        self.env = (interpreter.default_scope.copy(),)

    def assertEvalsTo(self, exp, expected):
        self.assertEquals(interpreter.eval_read(exp, self.env), expected)

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
        self.assertEvalsTo('(+ 4 3)', 7)
        self.assertEvalsTo('(- 4 3 2 1)', -2)
        self.assertEvalsTo('(- 4)', -4)
        with self.assertRaises(TypeError):
            interpreter.eval_one('(-)')

    def test_define(self):
        self.assertEvalsTo('(define a 1)', None)
        self.assertEvalsTo('a', 1)

    def test_lambda(self):
        self.assertEvalsTo('((lambda (x) x) 1)', 1)
        self.assertEvalsTo('((lambda (x) (+ x 1)) 2)', 3)
        self.assertEvalsTo('((lambda (x) (+ 4 (+ x 1))) 2)', 7)
        self.assertEquals(self.env, (interpreter.default_scope.copy(),))

    def test_let(self):
        self.assertEvalsTo('(let ((a 1)) (+ a a))', 2)
        with self.assertRaises(NameError):
            self.assertEvalsTo('(+ (let ((a 1)) (+ a a)) a)', None)


if __name__ == "__main__":
    unittest.main()
