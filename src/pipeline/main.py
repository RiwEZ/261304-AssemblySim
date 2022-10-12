import opcode
import re


class Programcounter:
    pc = 0
    def __init__(self) -> None:
        pass
    def set_counter(pc):
        pass

# class Instruction_register:
    # memory = []
    # def __init__(self ) -> None:
    #     # self.memory = code
    #     pass
    
    # @classmethod
    # def inint(cls , code):
    #     cls.memory = code
    # @classmethod
    # def summary(cls):
    #     print(cls.memory)


class Register:
    regis = [0] * 32

    def __init__(self , name) -> None:
        self.name = name 
 
    def get(self, index):
        return self.regis[ (32 - index)-1]

    def set(self, index, value):
        self.regis[(32 - index)-1] = value

    def test(self):
        for id in range(len(self.regis)):
            self.regis[id] = 1
        print(self.regis)
        print(Register.regis)
    @classmethod
    def summary(cls):
        print(cls.regis)
        pass
        # print " tes".format(cls.r)


class Memory:
    memory = []
    def __init__(self ,code ) -> None:
        self.memory = code
     
    def summary(self):
        print(self.memory)



class Alu:
    def __init__(self) -> None:
        pass

class Control:
    
    Opcode = '01001000010010000010000110011101'

    # print(len(opcode))
    def __init__(self) -> None:
        pass
    

    def test():
        print("test_work")
        a = Control.Opcode[25:32]
        print(str(a))

class Gate:
    def __init__(self) -> None:
        pass

    @staticmethod
    def adder(val1, val2):
        max_len = max(len(val1), len(val2))
        val1 = val1.zfill(max_len)
        val2 = val2.zfill(max_len)

        # Initialize the result
        result = ''
        # Initialize the carry
        carry = 0
        # Traverse the string
        for i in range(max_len - 1, -1, -1):
            r = carry
            r += 1 if val1[i] == '1' else 0
            r += 1 if val2[i] == '1' else 0
            result = ('1' if r % 2 == 1 else '0') + result

            # Compute the carry.
            carry = 0 if r < 2 else 1

            if carry != 0:
                result = '1' + result
        
        return result.zfill(max_len)

    @staticmethod
    def Mux(sel, val1, val2):
        if sel == 0:
            return val1
        elif sel == 1:
            return val2


def main():
    f = open("src\\testcode.txt", "r")
    raw = f.read()
    code = raw.split("\n")

    print(code)
    reg = Register('A1')
    mem = Memory(code)
    
    mem.summary()    
    reg.summary()
    print("test")
    reg.test()
    reg.summary()
    print(reg.get(8))
    Register.set(reg,8,2)
    print(reg.get(8))
    reg.summary()
    Register.summary()
    return


if __name__ == "__main__":
    main()
