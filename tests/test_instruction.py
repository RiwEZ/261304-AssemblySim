import unittest

from simulator.instruction import execute_instruction, sign_extend
from simulator.simulator import State

class TestInstruction(unittest.TestCase):
    def test_add(self):
        # add 1 2 3
        output = State(8, 1)
        expected = State(8, 1)

        expected.mem[0] = 655363
        expected.reg[1] = 1
        expected.reg[2] = 6
        
        expected.reg[3] = 7

        output.mem[0] = 655363
        output.reg[1] = 1
        output.reg[2] = 6
        
        execute_instruction(output)
        self.assertEqual(output, expected)

    def test_nand(self):
        # nand 1 2 3
        output = State(8, 1)
        expected = State(8, 1)

        expected.mem[0] = 4849667
        expected.reg[1] = -1
        expected.reg[2] = -1
        
        expected.reg[3] = 0

        output.mem[0] = 4849667
        output.reg[1] = -1
        output.reg[2] = -1

        execute_instruction(output)
        self.assertEqual(output, expected)
    
    def test_lw(self):
        # lw 0 1 max
        # max .fill 2147483647
        output = State(8, 2)
        expected = State(8, 2)

        expected.mem[0] = 8454145
        expected.mem[1] = 2147483647
        
        expected.reg[1] = 2147483647

        output.mem[0] = 8454145
        output.mem[1] = 2147483647

        execute_instruction(output)
        self.assertEqual(output, expected)
    
    def test_sw(self):
        # sw 1 2 32767
        output = State(8, 65536)
        expected = State(8, 65536)

        expected.mem[0] = 13271039
        expected.reg[1] = 32768
        expected.reg[2] = 2147483647
        
        expected.mem[65535] = 2147483647

        output.mem[0] = 13271039
        output.reg[1] = 32768
        output.reg[2] = 2147483647

        execute_instruction(output)
        self.assertEqual(output, expected)

    def test_beq(self):
        # beq 0 0 -32768
        # pc at 60000
        output = State(8, 65536)
        output.pc = 60000
        expected = State(8, 65536)
        expected.pc = 60000

        expected.mem[60000] = 16809984
        expected.pc = 27232

        output.mem[60000] = 16809984

        execute_instruction(output)
        self.assertEqual(output, expected)

    def test_sign_extend_32767(self):
        output = sign_extend(0x7FFF)
        expected = 32767
        self.assertEqual(output, expected)

    def test_sign_extend_neg1(self):
        output = sign_extend(0xFFFF)
        expected = -1
        self.assertEqual(output, expected)