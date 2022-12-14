import argparse
import os
import sys
from assembler.asm_parser import Parser
from simulator.simulator import Simulator

"""
Main class.
Compiles the assembly code and Executes the machine code
using both Assembler and Simulator modules
"""

def main():
    arg_parser = argparse.ArgumentParser(description='')
    arg_parser.add_argument('path', metavar='path', type=str, help='the path to assembly *.s file')

    args = arg_parser.parse_args()
    path = args.path

    if not os.path.exists(path):
        print('The path specified does not exist')
        sys.exit()
    
    head_tail = os.path.split(path)
    compiled_path = os.path.join(head_tail[0], 'compiled', head_tail[1].replace('.s','.bin'))
    # check compiled directory exists or not
    isExist = os.path.exists(os.path.join(head_tail[0], 'compiled'))
    # create compiled directory for save machine code file
    if not isExist:
        os.makedirs(os.path.join(head_tail[0], 'compiled'))
    # assembly to machine code
    with open(path, 'r') as f, open(compiled_path, 'w') as f_compiled:
        lines = f.read().splitlines()
        p = Parser(lines).parse()
        for item in p.execute():
            if item != p.execute()[-1]:
                f_compiled.write(str(item)+'\n')
            else:
                f_compiled.write(str(item))
    f.close()
    f_compiled.close()
    # run machine code with simulator
    com = Simulator()
    com.run_sim(compiled_path)
    return

if __name__ == '__main__':
    main()