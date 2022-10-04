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

def is_reg(w: str):
    if w.isnumeric():
        v = int(w)
        return v >= 0 and v <= 7
    return False

class Program():
    def __init__(self, var_map: dict[str, int]):
        self.statement: list[Statement] = []
        self.priority: set[int] = set()
        self.var_map = var_map
    
    def append(self, statement: Statement):
        self.statement.append(statement)
        if isinstance(statement, Assignment):
            self.priority.add(len(self.statement) - 1)

    def execute(self):
        res = [0] * len(self.statement)
        
        for i in self.priority:
            res[i] = self.statement[i].evaluate(self.var_map)

        for i, node in enumerate(self.statement):
            if i in self.priority: pass
            res[i] = node.evaluate(self.var_map)
            
        return res

class Parser():
    def __init__(self, lines: list[str]):
        self.tk = Tokenizer(lines)
        self.var_map: dict[str, int] = {}

    def err_info(self):
        return 'at' + self.tk.get_info() 

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
            if len(label) > 6: raise Exception(f'Label length should not exceeds 6 {self.err_info()}')
            if label in self.var_map.keys(): raise Exception(f"duplicated label {self.err_info()}")

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
        else: raise Exception(f'Something wrong! {self.err_info()}')

    # R -> Rcmd <reg> <reg> <reg>
    # Rcmd -> add | nand
    def parse_R(self):
        op = self.tk.consume()
        # maybe we can check if it's int or not first
        rd = self.tk.consume()
        if not is_reg(rd): raise Exception(f'Invalid register {self.err_info()}')
        rs1 = self.tk.consume()
        if not is_reg(rs1): raise Exception(f'Invalid register {self.err_info()}')
        rs2 = self.tk.consume()
        if not is_reg(rs2): raise Exception(f'Invalid register {self.err_info()}')
        return R_ins(op, int(rd), int(rs1), int(rs2))
    
    # I -> Icmd <reg> <reg> var
    # Icmd -> lw | sw | beq
    # var -> <label> | <number>
    def parse_I(self):
        op = self.tk.consume()
        rd = self.tk.consume()
        if not is_reg(rd): raise Exception(f'Invalid register {self.err_info()}')
        rs1 = self.tk.consume()
        if not is_reg(rs1): raise Exception(f'Invalid register {self.err_info()}')
        imm = int(self.tk.consume()) if self.tk.peek().isnumeric() else self.tk.consume()
        return I_ins(op, int(rd), int(rs1), imm)

    # J -> jalr <reg> <reg>
    def parse_J(self):
        self.tk.consume() # consume jalr
        rs = self.tk.consume()
        if not is_reg(rs): raise Exception(f'Invalid register {self.err_info()}') 
        rd = self.tk.consume()
        if not is_reg(rd): raise Exception(f'Invalid register {self.err_info()}') 
        return J_ins(int(rs), int(rd))
    

class TestParser(unittest.TestCase):
    def test_parser(self):
        with open("tests/t1.s") as f:
            lines = f.read().splitlines()
            parser = Parser(lines)

        p = parser.parse()
        print(p.var_map)
        p.execute()
        print(p.var_map)
    
    def test_parser_err(self):
        with open("tests/t2.s") as f:
            lines = f.read().splitlines()
            parser = Parser(lines)

        with self.assertRaisesRegex(Exception, 'Invalid register'):
            parser.parse()
        


if __name__ == '__main__':
    unittest.main()