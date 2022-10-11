import unittest

from assembler.asm_parser import Parser

class TestParser(unittest.TestCase):
    def test_parser(self):
        with open("tests/files/t1.s") as f:
            lines = f.read().splitlines()
            parser = Parser(lines)

        p = parser.parse()
        res = p.execute()
        self.assertEqual(res, [8454151, 9043971, 655361, 16842754, 16842749, 29360128, 25165824, 5, -1, 2])
    
    def test_parser_err(self):
        with open("tests/files/t2.s") as f:
            lines = f.read().splitlines()
            parser = Parser(lines)

        with self.assertRaisesRegex(Exception, 'Invalid register'):
            parser.parse()

    def test_parser_instruction(self):
        # This test may cause memory leak !!!
        with open("tests/files/t3.s") as f:
            lines = f.read().splitlines()
            parser = Parser(lines)
        with self.assertRaisesRegex(Exception, 'Instruction expected'):
            parser.parse()

    def test_parser_label(self):
        # Label should not be number and instruction should exception when argument not match

        with open("tests/files/t4.s") as f:
            lines = f.read().splitlines()
            parser = Parser(lines)
        with self.assertRaisesRegex(Exception, 'Something went wrong'):
            parser.parse()

    def test_parser_fill(self):
        # Instruction expected rise when no label
        # fill should be able to get label
        with open("tests/files/t5.s") as f:
            lines = f.read().splitlines()
            parser = Parser(lines)
            parser.parse()

if __name__ == '__main__':
    unittest.main(verbosity=2)
