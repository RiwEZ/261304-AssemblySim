import unittest
from asm_ast import *
from tokenizer import Tokenizer

reserve = set(['add', 'nand', 'lw', 'sw', 'beq', 'jalr', 'noop', 'halt'])

def is_O(w: str):
    return w == 'noop' or w == 'halt'

def is_J(w: str):
    return w == 'jalr'

def is_R(w: str):
    return w == 'add' or w == 'nand'

def is_I(w: str):
    return w == 'lw' or w == 'sw' or w == 'beq'

def is_instruction(w: str):
    return is_R(w) or is_I(w) or is_J(w) or is_O(w)

def is_label(w: str):
    return w not in reserve

class Program():
    def __init__(self, var_map: dict[str, int]):
        self.statement: list[Statement] = []
        self.assignments: list[Statement] = []
        self.var_map = var_map
    
    def append(self, statement: Statement):
        self.statement.append(statement)
        if isinstance(statement, Assignment):
            self.assignments.append(statement)

    def execute(self):
        for s in self.assignments:
           s.evaluate(self.var_map)
        
        res = []
        for s in self.statement:
            res.append(s.evaluate(self.var_map))
        return s

class Parser():
    def __init__(self, lines: list[str]):
        self.tk = Tokenizer(lines)
        self.var_map: dict[str, int] = {}

    # program -> statement+
    def parse(self):
        if not self.tk.has_next(): raise Exception("at least 1 statement needed")
        program = Program(self.var_map)
        top = self.tk.peek()
        while (is_label(top) or is_instruction(top)) and self.tk.has_next():
            program.append(self.parse_statement())

        return program

    # statement -> cmd | assignment
    def parse_statement(self):
        if is_label(self.tk.peek()): 
            label = self.tk.consume()
            if len(label) > 6: raise Exception("label length should not exceeds 6")
            if label in self.var_map.keys(): raise Exception(f"duplicated label {label}")

            # assignment -> <label> .fill <number>
            if self.tk.peek() == '.fill':
                self.tk.consume()
                v = self.tk.consume()
                if is_label(v) and v in self.var_map.keys():
                    v = self.var_map[v]
                else:
                    v = int(v) # maybe we can check for error if this is not int
                return Assignment(label, v)
            
            # cmd_l -> <label> | ε
            self.var_map[label] = self.tk.line # pre set label value for cmd label

        # cmd -> cmd_l ins
        if is_instruction(self.tk.peek()):
            return self.parse_ins()

    # ins -> R | I | J | O
    def parse_ins(self):
        top = self.tk.peek()
        if is_R(top):
            return self.parse_R()
        elif is_I(top):
            return self.parse_I()
        elif is_J(top):
            return self.parse_J()
        elif is_O(top):
            return O_ins(self.tk.consume())
        else: raise Exception("Something wrong!")

    # R -> Rcmd <number> <number> <number>
    # Rcmd -> add | nand
    def parse_R(self):
        op = self.tk.consume()
        # maybe we can check if it's int or not first
        rd = int(self.tk.consume())
        rs1 = int(self.tk.consume())
        rs2 = int(self.tk.consume())
        return R_ins(op, rd, rs1, rs2)
    
    # I -> Icmd <number> <number> var
    # Icmd -> lw | sw | beq
    # var -> <label> | <number>
    def parse_I(self):
        op = self.tk.consume()
        rd = int(self.tk.consume())
        rs1 = int(self.tk.consume())
        imm = int(self.tk.consume()) if self.tk.peek().isnumeric() else self.tk.consume()
        return I_ins(op, rd, rs1, imm)

    # J -> jalr <number> <number>
    def parse_J(self):
        self.tk.consume() # consume jalr
        rd = int(self.tk.consume())
        rs1 = int(self.tk.consume())
        return J_ins(rd, rs1)
    
class TestParser(unittest.TestCase):
    def test_parser(self):
        with open("tests/t1.s") as f:
            lines = f.read().splitlines()
            parser = Parser(lines)

        p = parser.parse()
        print(p.var_map)
        p.execute()
        print(p.var_map)


if __name__ == '__main__':
    unittest.main()