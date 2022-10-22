from re import L
from assembler.asm_ast import *
from assembler.tokenizer import Tokenizer

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
    return w not in reserve and w[0].isnumeric() == False and is_int(w) == False

def is_int(w: str):
    try:
        int(w)
        return True
    except ValueError:
        return False

def is_reg(w: str):
    if is_int(w):
        v = int(w)
        return v >= 0 and v <= 7
    return False

def add_var_count(label: str, var_count: dict[str, int]):
    if label in var_count:
        var_count[label] += 1
    else:
        var_count[label] = 1

class Program():
    """
    AST class

    Attributes
    -------
    statement : list[Statement]
        list of statements

    var_map: dict[str, int]
        variable map for fill instruction and label

    Methods
    -------
    append(statement: Statement)
        Add a new statement to the tree

    execute()
        Evaluates nodes. Returns  a list of machine code
    """

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
    """
    Parser for the input assembly code.

    Attributes
    -------
    tk: Tokenizer    
        A tokenizer with lines of assembly code as input
    
    var_map: dict[str, int]
        variable map for fill instruction and label

    Method
    -------
    parse()
        Parses the assembly code. Returns an AST of the assembly code.

    """

    def __init__(self, lines: list[str]):
        """
        Args: 
            lines (list[str]): list of assembly code lines
        """

        self.tk = Tokenizer(lines)
        self.var_map: dict[str, int] = {}
        self.var_count: dict[str, int] = dict()

    def err_info(self, w):
        return 'at' + self.tk.get_info(w)

    # program -> statement+
    def parse(self):
        if not self.tk.has_next(): raise Exception("at least 1 statement needed")
        program = Program(self.var_map)
        top = self.tk.peek()
        while (is_label(top) or is_instruction(top) or top == '.fill') and self.tk.has_next():
            program.append(self.parse_statement())

        if self.tk.has_next():
            raise Exception(f"Something went wrong {self.err_info(self.tk.peek())}")

        label_not_used = False
        for k, v in self.var_count.items():
            if v == 1:
                label_not_used = True
                print(f"Label \x1b[0;30;43m {k} \x1b[0m is not used.")
        if label_not_used:
            print("-----------------------------")
        

        return program

    # statement -> label cmd [*]'\n'
    # label -> <label> | ε
    # cmd -> ins | '.fill' <label> | <number>
    def parse_statement(self):
        curr_line = self.tk.line

        if is_label(self.tk.peek()): 
            label = self.tk.consume()
            if len(label) > 6: raise Exception(f'Label length should not exceeds 6 {self.err_info(label)}')
            if label in self.var_map.keys(): raise Exception(f"Duplicated label {self.err_info(label)}")
            self.var_map[label] = curr_line # pre set label value for cmd label
            add_var_count(label, self.var_count)   

        if self.tk.peek() == '.fill':
            self.tk.consume()
            v = self.tk.consume()
            if is_int(v):
                v = int(v)
            elif is_label(v):
                add_var_count(v, self.var_count)   
            else: 
                raise Exception(f".fill should be followed by <label> or <int> {self.err_info(v)}")

            if self.tk.line == curr_line: self.tk.consume_line() # ignore comment
            return Fill(v)

        if is_instruction(self.tk.peek()):
            statement = self.parse_ins()
            if self.tk.line == curr_line: self.tk.consume_line() # ignore comment
            return statement
        else:
            raise Exception(f'Instruction expected {self.err_info(self.tk.peek())}')

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
        else: raise Exception(f'Something went wrong! {self.err_info(top)}')

    # R -> Rcmd <reg> <reg> <reg>
    # Rcmd -> add | nand
    def parse_R(self):
        op = self.tk.consume()
        # maybe we can check if it's int or not first
        rs = self.tk.consume()
        if not is_reg(rs): raise Exception(f'Invalid register {self.err_info(rs)}')
        rt = self.tk.consume()
        if not is_reg(rt): raise Exception(f'Invalid register {self.err_info(rt)}')
        rd = self.tk.consume()
        if not is_reg(rd): raise Exception(f'Invalid register {self.err_info(rd)}')
        return R_ins(op, int(rs), int(rt), int(rd))
    
    # I -> Icmd <reg> <reg> var
    # Icmd -> lw | sw | beq
    # var -> <label> | <number>
    def parse_I(self):
        curr_line = self.tk.line
        op = self.tk.consume()
        rs = self.tk.consume()
        if not is_reg(rs): raise Exception(f'Invalid register {self.err_info(rs)}')
        rt = self.tk.consume()
        if not is_reg(rt): raise Exception(f'Invalid register {self.err_info(rt)}')
    
        var = self.tk.consume() 
        
        if is_label(var):
            add_var_count(var, self.var_count)   
            return I_ins(op, int(rs), int(rt), var, curr_line)
        elif is_int(var):
            v = int(var)
            if v >= -32768 and v <= 32767:
                offset = v
                return I_ins(op, int(rs), int(rt), offset, curr_line)
            else: raise Exception(f'Offset field exceed limit {self.err_info(var)}')
        else:
            raise Exception(f'Somethine went wrong {self.err_info(var)}, invalid label')

    # J -> jalr <reg> <reg>
    def parse_J(self):
        self.tk.consume() # consume jalr
        rs = self.tk.consume()
        if not is_reg(rs): raise Exception(f'Invalid register {self.err_info(rs)}') 
        rd = self.tk.consume()
        if not is_reg(rd): raise Exception(f'Invalid register {self.err_info(rd)}') 
        return J_ins(int(rs), int(rd))
    
