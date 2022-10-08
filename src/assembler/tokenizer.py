import unittest

class Tokenizer():
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.line = 0
        self.pos = 0
        self.next = ''
        self.compute_next()
    
    def get_info(self):
        if len(self.lines) == 0: return ''
        elif self.line < len(self.lines):
            return ':' + str(self.line) + '\n\t' + self.lines[self.line] + '\n\t' + (self.pos - 1) * ' ' + '^'
        return ':unknown'

    def compute_next(self):
        if len(self.lines) == 0: return
        if self.line > len(self.lines) - 1:
            self.next = ''
            return

        curr_line = self.lines[self.line]
        self.next = ''

        while self.pos >= len(curr_line) or curr_line[self.pos] == ' ':
            self.pos += 1
            if self.pos >= len(curr_line):
                if self.line == len(self.lines) - 1: return
                self.line += 1
                curr_line = self.lines[self.line]
                self.pos = 0
        
        while self.pos < len(curr_line) and curr_line[self.pos] != ' ':
            self.next += curr_line[self.pos]
            self.pos += 1

        return

    def has_next(self):
        return self.next != ''
    
    def peek(self):
        return self.next
    
    def consume(self):
        temp = self.next
        self.compute_next()
        return temp

    def consume_line(self):
        self.pos = 0
        self.line += 1
        self.compute_next()
    
 
# Testing codes
class TestParser(unittest.TestCase):
    def test_tokenizer(self):
        with open("tests/t1.s") as f:
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