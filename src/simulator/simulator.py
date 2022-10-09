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
from dataclasses import dataclass
from instruction import *

class Simulator:
    NUMMEMORY = 65536
    NUMREGS = 8
    MAXLINELENGTH = 1000
    
    @dataclass
    class State:
        reg: list[int]
        mem: list[int]
        pc: int
        numMemory: int

        def __init__(self, NUMREGS, NUMMEMORY):
            self.reg = [0] * NUMREGS
            self.mem = [0] * NUMMEMORY
            self.pc = 0
            self.numMemory = 0
        

    def __init__(self):
        self.state = self.State(self.NUMREGS, self.NUMMEMORY)
        self.ins_executed = 0
        
    def print_state(self):
        print('\n@@@\nstate:')
        print('\tpc %d' % self.state.pc)
        print('\tmemory:')
        for i in range(0, self.state.numMemory, 1):
            print('\t\tmem[ %d ] %d' % (i, self.state.mem[i]))
        print('\tregisters:')
        for i in range(0, self.NUMREGS, 1):
            print('\t\treg[ %d ] %d' % (i, self.state.reg[i]))
        print('end state')
        
    def read_machinecode(self,path):
        with open(path) as f:
            lines = f.readlines()
        for line in lines:
            self.state.mem[self.state.numMemory] = int(line)
            print('memory[%d]=%d' % (self.state.numMemory, self.state.mem[self.state.numMemory]))
            self.state.numMemory += 1
        print()
        f.close()
        
    def run_program(self):
        isRunning = True
        while(isRunning):
            self.print_state()
            isRunning = execute_instruction(self.state)
            self.state.pc += 1
            self.ins_executed += 1
        print('machine halted\ntotal of %d instructions executed\nfinal state of machine:' % self.ins_executed)
        self.print_state()
    
    
    
# testing
if __name__ == '__main__':
    com = Simulator()
    com.read_machinecode('tests/test.bin')
    com.run_program()