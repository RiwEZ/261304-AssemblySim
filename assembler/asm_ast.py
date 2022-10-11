from abc import ABC, abstractmethod

class Statement(ABC):
    @abstractmethod
    def evaluate(self, var_map: dict[str, int]):
        return 0

class Fill(Statement):
    def __init__(self, val):
        self.val = val # str | int
    
    def evaluate(self, var_map: dict[str, int]):
        if type(self.val) == int:
            return self.val
        elif type(self.val) == str:
            return var_map[self.val]
        else:
            raise Exception(f"Something wrong on: .fill {self.v}")


class R_ins(Statement):
    def __init__(self, op: str, rs: int, rt: int, rd: int):
        self.op = op
        self.rs = rs
        self.rt = rt
        self.rd = rd

    def evaluate(self, var_map: dict[str, int]):
        b = self.rs << 19
        c = self.rt << 16
        d = self.rd

        if self.op == 'add':
            a = 0b000 << 22
        elif self.op == 'nand':
            a = 0b001 << 22
        else: raise Exception('R_ins op should be either add or nand')

        return a | b | c | d

class I_ins(Statement):
    def __init__(self, op: str, rs: int, rt: int, var):
        self.op = op
        self.rs = rs
        self.rt = rt    
        self.var = var # str | int
    
    def evaluate(self, var_map: dict[str, int]):
        b = self.rs << 19
        c = self.rt << 16
        
        if type(self.var) == str and self.var in var_map.keys():
            imm = var_map[self.var]
        elif type(self.var) == int:
            imm = self.var
        else: 
            if type(self.var) != int: raise Exception('I_ins immediate is not int')
            else: raise Exception('I_ins label cannot be found')

        
        if imm < 0:
            # convert to sign imm
            temp = list(bin(imm).removeprefix('-0b'))
            for i, w in enumerate(temp):
                if w == '1': temp[i] = '0'
                else: temp[i] = '1'
            while len(temp) < 16:
                temp.insert(0, '1')
            temp = ''.join(temp)
            d = int(temp, 2) + 1
        else: 
            d = imm
        
        if self.op == 'lw':
            a = 0b010 << 22
        elif self.op == 'sw':
            a = 0b011 << 22
        elif self.op == 'beq':
            a = 0b100 << 22
        else: raise Exception('I_ins op invalid')

        return a | b | c | d

class J_ins(Statement):
    def __init__(self, rs: int, rd: int):
        self.rs = rs
        self.rd = rd

    def evaluate(self, var_map: dict[str, int]):
        a = 0b101 << 22
        b = self.rs << 19
        c = self.rd << 16
        return a | b | c

class O_ins(Statement):
    def __init__(self, op: str):
        self.op = op

    def evaluate(self, var_map: dict[str, int]):
        if self.op == 'noop':
            return 0b111 << 22
        elif self.op == 'halt':
            return 0b110 << 22
        else: raise Exception('O_ins op should be either noop or halt')