'''
    Rules ของ project description
    1) (assembler) outputting the machine-code file.
    2) (assembler) Call exit(1) ถ้า มี errors ใน assembly-language program. Call exit(0) ถ้าทำเสร็จโดยไม่มี errors.
    3) (simulator) อย่าแก้ printState หรือ stateStruct
    4) (simulator) Call printState 1 ครั้ง ก่อน instruction executes และ 1 ครั้ง  ก่อน simulator exits.  อย่า call printState ที่อื่น.
    5) (simulator) อย่า print "@@@" ที่ใดยกเว้นใน printState.
    6) (simulator) state.numMemory ต้อง เท่ากับ จำนวนบรรทัด ใน machine-code file.
    7) (simulator) Initialize ทุก registers ให้เป็น 0.
    8) (multiplication) เก็บ ผลลัพธ์ ใน register 1.
    9) (multiplication) labeled "mcand" และ "mplier" (lower-case) เป็นที่ที่ ตัวเลข 2 ตัว อยู่
   10) (combination) ควรจะรับค่า n และ r จาก Memory ที่ location ที่มี Label เป็น n และ r และ ผลลัพธ์ควรจะเก็บที่  register 3
'''
import os

class Simulator:
    NUMMEMORY = 65536
    NUMREGS = 8
    MAXLINELENGTH = 1000
    
    def __init__(self):
        self.reg = [0] * self.NUMREGS
        self.mem = [0] * self.NUMMEMORY
        self.numMemory = 0
        self.pc = 0
        
    def print_state(self):
        print('\n@@@\nstate:\n')
        print('\tpc %d\n' % self.pc)
        print('\tmemory:\n')
        for i in range(0, self.numMemory, 1):
            print('\t\tmem[ %d ] %d\n' % (i, self.mem[i]))
        print('\tregisters:\n')
        for i in range(0, self.NUMREGS, 1):
            print('\t\treg[ %d ] %d\n' % (i, self.reg[i]))
        print('end state\n')
        
    def read_machinecode(self,path):
        with open(path) as f:
            lines = f.readlines()
        for line in lines:
            self.mem[self.numMemory] = int(line)
            print('memory[%d]=%d\n' % (self.numMemory, self.mem[self.numMemory]))
            self.numMemory += 1
        f.close()
        
    def run_program(self):
        pass
    
    
    
    
if __name__ == '__main__':
    com = Simulator()
    com.read_machinecode('tests/test.bin')
    com.print_state()