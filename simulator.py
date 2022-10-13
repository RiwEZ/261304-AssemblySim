from simulator.simulator import Simulator
import argparse
import os
import sys

def main():
    arg_parser = argparse.ArgumentParser(description='')
    arg_parser.add_argument('path', metavar='path', type=str, help='the path to machine code file *.bin file')
    
    args = arg_parser.parse_args()
    path = args.path
    
    if not os.path.exists(path):
        print('The path specified does not exist')
        sys.exit()
    
    com = Simulator()
    com.run_sim(path)
    
    return
        

if __name__ == "__main__":
    main()