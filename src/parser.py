import unittest

reserve = set('add', 'nand', 'lw', 'sw', 'beq')

def is_R(w: str):
    return w == 'add' or w == 'nand'

def is_I(w: str):
    return w == 'lw' or w == 'sw' or w == 'beq'

def is_instruction(w: str):
    return is_R(w) or is_I(w)

def is_label(w: str):
    return w not in reserve and len(w) <= 6


class Tokens():
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
      
    def peek(self):
        return self.tokens[0]
    
    def consume(self):
        temp = self.tokens.pop(0)
        return temp


class Parser():
    def __init__(self, program: list[str]):
        self.tokens = Tokens(program)
        self.var_map = {}

    # program -> cmd+ | misc+ 
    def parse():
        return 0

    def parse_cmd(self):
        cmd = [] # CMD class?
        if is_label(self.tokens.peek()):
            v = self.tokens.consume() # do something with this

        if is_instruction(self.tokens.peek()):
            a = self.parse_ins()
    
    def parse_ins():
        return 0
    
    
class TestParser(unittest.TestCase):
    def test_parser(self):
        parser = Parser(['lw', '0', '1', '3'])
        self.assertEqual(parser.parse(), 9043971)


if __name__ == '__main__':
    unittest.main()