import io
from sys import stdout
import unittest
import unittest.mock

from simulator.simulator import Simulator

'''
    UnitTests for Simulator
    asserting equal between the console output and the expected output
    regardless of whitespaces
    use `python -m unittest discover` command at root to run tests
'''
# use python -m unittest discover at root to run tests
class TestSimulator(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, path, expected_output, mock_stdout):
        com = Simulator()
        com.run_sim(path)
        stdout = ''.join(mock_stdout.getvalue().split())
        expected_output = ''.join(expected_output.split())        
        self.assertEqual(stdout, expected_output)

    def read_file(self, path):
        with open(path) as f:
            return f.read()

    def test_example(self):
        expected_output = 'tests/files/output_sim_example.txt'
        self.maxDiff = None
        self.assert_stdout('tests/files/test_sim_example.bin', self.read_file(expected_output))