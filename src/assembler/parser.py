import unittest
from asm_ast import *
from tokenizer import Tokenizer

reserve = set(['add', 'nand', 'lw', 'sw', 'beq', 'jalr', 'noop', 'halt', '.fill'])

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
    return w not in reserve and not w[0].isnumeric()

def is_reg(w: str):
    if w.isnumeric():
        v = int(w)
        return v >= 0 and v <= 7
    return False

class Program():
    def __init__(self, var_map: dict[str, int]):
        self.statement: list[Statement] = []
        self.var_map = var_map
    
    def append(self, statement: Statement):
        self.statement.append(statement)

    def execute(self):
        res = [0] * len(self.statement)
        for i, node in enumerate(self.statement):
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
        while (is_label(top) or is_instruction(top) or top == '.fill') and self.tk.has_next():
            program.append(self.parse_statement())

        if self.tk.has_next():
            raise Exception(f"Something went wrong {self.err_info()}")
        return program

    # statement -> label cmd [*]'\n'
    # label -> <label> | ε
    # cmd -> ins | '.fill' <label> | <number>
    def parse_statement(self):
        curr_line = self.tk.line

        if is_label(self.tk.peek()): 
            label = self.tk.consume()
            if len(label) > 6: raise Exception(f'Label length should not exceeds 6 {self.err_info()}')
            if label in self.var_map.keys(): raise Exception(f"Duplicated label {self.err_info()}")
            self.var_map[label] = curr_line # pre set label value for cmd label
   
        if self.tk.peek() == '.fill':
            self.tk.consume()
            v = self.tk.consume()
            if v.isnumeric() or (v[0] == '-' and v[1:len(v)].isnumeric()):
                v = int(v)             
            elif not is_label(v): 
                raise Exception(f".fill should be followed by <label> or <number> {self.err_info()}")

            if self.tk.line == curr_line: self.tk.consume_line() # ignore comment
            return Fill(v)

        if is_instruction(self.tk.peek()):
            statement = self.parse_ins()
            if self.tk.line == curr_line: self.tk.consume_line() # ignore comment
            return statement
        else:
            raise Exception(f'Instruction expected {self.err_info()}')

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
        else: raise Exception(f'Something went wrong! {self.err_info()}')

    # R -> Rcmd <reg> <reg> <reg>
    # Rcmd -> add | nand
    def parse_R(self):
        op = self.tk.consume()
        # maybe we can check if it's int or not first
        rs = self.tk.consume()
        if not is_reg(rs): raise Exception(f'Invalid register {self.err_info()}')
        rt = self.tk.consume()
        if not is_reg(rt): raise Exception(f'Invalid register {self.err_info()}')
        rd = self.tk.consume()
        if not is_reg(rd): raise Exception(f'Invalid register {self.err_info()}')
        return R_ins(op, int(rs), int(rt), int(rd))
    
    # I -> Icmd <reg> <reg> var
    # Icmd -> lw | sw | beq
    # var -> <label> | <number>
    def parse_I(self):
        op = self.tk.consume()
        rs = self.tk.consume()
        if not is_reg(rs): raise Exception(f'Invalid register {self.err_info()}')
        rt = self.tk.consume()
        if not is_reg(rt): raise Exception(f'Invalid register {self.err_info()}')

        var = self.tk.consume()
        if op == 'beq' and var in self.var_map: # pre set label value
            imm = self.var_map[var] - self.tk.line - 1 # TODO maybe -1 is not necessary 
            return I_ins(op, int(rs), int(rt), imm)
        
        if var.isnumeric():
            v = int(var)
            if v >= -32768 and v <= 32767:
                imm = v
                return I_ins(op, int(rs), int(rt), imm)
            else: raise Exception(f'Offset field exceed limit {self.err_info()}')

        return I_ins(op, int(rs), int(rt), var)


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
        res = p.execute()
        self.assertEqual(res, [8454151, 9043971, 655361, 16842754, 16842749, 29360128, 25165824, 5, -1, 2])
    
    def test_parser_err(self):
        with open("tests/t2.s") as f:
            lines = f.read().splitlines()
            parser = Parser(lines)

        with self.assertRaisesRegex(Exception, 'Invalid register'):
            parser.parse()

    def test_parser_instruction(self):
        # This test may cause memory leak !!!
        with open("tests/t3.s") as f:
            lines = f.read().splitlines()
            parser = Parser(lines)
        with self.assertRaisesRegex(Exception, 'Instruction expected'):
            parser.parse()

    def test_parser_label(self):
        # Label should not be number and instruction should exception when argument not match

        with open("tests/t4.s") as f:
            lines = f.read().splitlines()
            parser = Parser(lines)
        with self.assertRaisesRegex(Exception, 'Something went wrong'):
            parser.parse()

    def test_parser_fill(self):
        # Instruction expected rise when no label
        # fill should be able to get label
        with open("tests/t5.s") as f:
            lines = f.read().splitlines()
            parser = Parser(lines)
            parser.parse()

if __name__ == '__main__':
    unittest.main(verbosity=2)
