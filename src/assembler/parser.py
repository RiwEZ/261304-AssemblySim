import unittest
from assembler.ast import Assignment
from tokenizer import Tokenizer
from ast import *

reserve = set('add', 'nand', 'lw', 'sw', 'beq', 'jalr', 'noop', 'halt')

def is_O(w: str):
    return w == 'noop' or w == 'halt'

def is_R(w: str):
    return w == 'add' or w == 'nand'

def is_I(w: str):
    return w == 'lw' or w == 'sw' or w == 'beq'

def is_instruction(w: str):
    return is_R(w) or is_I(w) or w == 'jalr' or is_O(w)

def is_label(w: str):
    return w not in reserve

class Parser():
    def __init__(self, lines: list[str]):
        self.tk = Tokenizer(lines)
        self.var_map: dict[str, int] = {}

    # program -> statement+
    def parse(self):
        if not self.tk.has_next(): raise Exception("at least 1 statement needed")
        program = []
        top = self.tk.peek()
        while is_label(top) or is_instruction(top):
            program.append(self.parse_statement())

        return 0

    # statement -> cmd | assignment
    def parse_statement(self):
        if is_label(self.tk.peek()): 
            label = self.tk.consume()
            if len(label) > 6: raise Exception("label length should not exceeds 6")
            if label in self.var_map.keys(): raise Exception("duplicated label")

            # assignment -> <label> .fill <number>
            if self.tk.peek() == '.fill':
                self.tk.consume()
                v = int(self.tk.consume()) # maybe we can check for error if this is not int
                return Assignment(label, v)
            
            # cmd_l -> <label> | ε
            self.var_map[label] = self.tk.line # pre set label value for cmd label

        # cmd -> cmd_l ins
        if is_instruction(self.tk.peek()):
            ins = self.parse_ins()

    # ins -> R | I | J | O
    def parse_ins(self):
        top = self.tk.peek()
        if is_R(top):
            return self.parse_R()
            
        return 0

    # R -> Rcmd <number> <number> <number>
    # Rcmd -> add | nand
    def parse_R(self):
        op = self.tk.consume()
        # maybe we can check if it's int or not first
        rd = int(self.tk.consume())
        rs1 = int(self.tk.consume())
        rs2 = int(self.tk.consume())
        return R_ins(op, rd, rs1, rs2)

    
class TestParser(unittest.TestCase):
    def test_parser(self):
        parser = Parser(['lw', '0', '1', '3'])
        self.assertEqual(parser.parse(), 9043971)

if __name__ == '__main__':
    unittest.main()