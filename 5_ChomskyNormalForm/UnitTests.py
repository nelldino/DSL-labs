from Grammar import Grammar
import unittest

class TestGrammarMethods(unittest.TestCase):
    def setUp(self):
        self.non_terminals = ['S', 'A', 'B', 'C', 'D', 'X']
        self.terminals = ['a', 'b']
        self.grammar_rules = {
            'S': ['A'],
            'A': ['aX', 'bX'],
            'X': ['BX', 'ε', 'b'],
            'B': ['AD'],
            'D': ['aD'],
            'C': ['Ca']
        }
        self.grammar = Grammar(self.non_terminals, self.terminals, self.grammar_rules)

    def test_eliminate_empty_string(self):
        self.grammar.eliminate_empty_string()
        expected = {
            'S': ['A'],
            'A': ['aX', 'bX', 'a', 'b'],
            'X': ['BX', 'b', 'B'],
            'B': ['AD'],
            'D': ['aD'],
            'C': ['Ca']
        }
        self.assertEqual(self.grammar.eliminate_empty_string(), expected)

    def test_eliminate_renaming(self):
        self.grammar.eliminate_empty_string()
        self.grammar.eliminate_renaming()
        expected = {
            'S': ['aX', 'bX', 'a', 'b'],
            'A': ['aX', 'bX', 'a', 'b'],
            'X': ['BX', 'b', 'AD'],
            'B': ['AD'],
            'D': ['aD'],
            'C': ['Ca']
        }
        self.assertEqual(self.grammar.eliminate_renaming(), expected)

    def test_eliminate_inaccessible(self):
        self.grammar.eliminate_empty_string()
        self.grammar.eliminate_renaming()
        self.grammar.eliminate_inaccessible()
        expected = {
            'S': ['aX', 'bX', 'a', 'b'],
            'A': ['aX', 'bX', 'a', 'b'],
            'X': ['BX', 'b', 'AD'],
            'B': ['AD'],
            'D': ['aD'],
        }
        self.assertEqual(self.grammar.eliminate_inaccessible(), expected)

    def test_eliminate_nonproductive(self):
        self.grammar.eliminate_empty_string()
        self.grammar.eliminate_renaming()
        self.grammar.eliminate_inaccessible()
        self.grammar.eliminate_nonproductive()
        expected = {
            'S': ['aX', 'bX', 'a', 'b'],
            'A': ['aX', 'bX', 'a', 'b'],
            'X': ['b'],
        }
        self.assertEqual(self.grammar.eliminate_nonproductive(), expected)

    def test_to_cnf(self):
        self.grammar.eliminate_empty_string()
        self.grammar.eliminate_renaming()
        self.grammar.eliminate_inaccessible()
        self.grammar.eliminate_nonproductive()
        self.grammar.to_cnf()
        expected = {
            'S': {'a', '0X', '1X', 'b'},
            'A': {'a', '0X', '1X', 'b'},
            'X': {'b'},
            '0': {'a'},
            '1': {'b'},
        }
        self.assertEqual(self.grammar.to_cnf(), expected)

if __name__ == '__main__':
    unittest.main()
