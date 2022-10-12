from assembler.asm_parser import Parser
import argparse
import os
import sys

def main():
    arg_parser = argparse.ArgumentParser(description='')
    arg_parser.add_argument('path', metavar='path', type=str, help='the path to assembly *.s file')

    args = arg_parser.parse_args()
    path = args.path

    if not os.path.exists(path):
        print('The path specified does not exist')
        sys.exit()

    with open(path) as f:
        lines = f.read().splitlines()
        p = Parser(lines).parse()
        for item in p.execute():
            print(item)
    return

if __name__ == "__main__":
    main()
