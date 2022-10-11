import unittest
from assembler.tokenizer import Tokenizer

# Testing codes
class TestParser(unittest.TestCase):
    def test_tokenizer(self):
        with open("tests/files/t1.s") as f:
            lines = f.read().splitlines()
            tk = Tokenizer(lines)
        
        self.assertEqual(tk.line, 0)
        arr = []
        for _ in range(10):
            arr.append(tk.consume())
        
        self.assertEqual(arr, ['lw', '0', '1', 'five', 'load', 'reg1', 'with', '5', '(uses', 'symbolic'])
        return 0

if __name__ == '__main__':
    unittest.main()