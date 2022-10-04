from abc import ABC, abstractmethod

class Statement(ABC):
    @abstractmethod
    def evalulate(self, var_map: dict[str, int]):
        pass

class Assignment(Statement):
    def __init__(self, var: str, val: int):
        self.var = var
        self.val = val
    
    def evaluate(self, var_map: dict[str, int]):
        var_map[self.var] = self.val
        return self.val

class R_ins(Statement):
    def __init__(self, op: str, rd: int, rs1: int, rs2: int):
        self.op = op
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2

    def evalulate(self, var_map: dict[str, int]):
        return 0