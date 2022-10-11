import unittest

from assembler.asm_ast import *

# Testing codes
class TestParser(unittest.TestCase):
    def test_O_ins(self):      
        var_map = {}
        self.assertEqual(O_ins('noop').evaluate(var_map), 29360128)
        self.assertEqual(O_ins('halt').evaluate(var_map), 25165824)

    def test_J_ins(self):
        var_map = {}
        self.assertEqual(J_ins(1, 2).evaluate(var_map), 0b101001010 << 16)
        self.assertEqual(J_ins(2, 4).evaluate(var_map), 0b101010100 << 16)

    def test_I_ins(self):
        var_map = {}
        self.assertEqual(I_ins('beq', 0, 1, 2).evaluate(var_map), 16842754)
        self.assertEqual(I_ins('beq', 0, 0, -3).evaluate(var_map), 16842749)
        self.assertEqual(I_ins('lw', 0, 1, 5).evaluate(var_map), 8454149)

    def test_R_ins(self):
        var_map = {}
        self.assertEqual(R_ins('add', 1, 2, 1).evaluate(var_map), 655361)
        self.assertEqual(R_ins('nand', 0, 0, 0).evaluate(var_map), 0b001 << 22)