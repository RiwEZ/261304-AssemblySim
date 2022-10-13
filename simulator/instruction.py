from simulator.int32 import int32
import warnings
warnings.filterwarnings("ignore")

def get_opcode(machinecode: int):
    """get opcode, type format, instruction name from machinecode

    Args:
        machinecode (int): machinecode from assembler

    Returns:
        opcode (int): opcode (bits 22-24)
        t_format (str): type format of instruction
        ins (str): name of instruction
    """
    t_format = '-'
    ins = '-'
    opcode = (machinecode >> 22) & 0b0111       # bits 22-24
    if opcode == 0:
        t_format = 'r'
        ins = 'add'
    elif opcode == 1:
        t_format = 'r'
        ins = 'nand'
    elif opcode == 2:
        t_format = 'i'
        ins = 'lw'
    elif opcode == 3:
        t_format = 'i'
        ins = 'sw'
    elif opcode == 4:
        t_format = 'i'
        ins = 'beq'
    elif opcode == 5:
        t_format = 'j'
        ins = 'jalr'
    elif opcode == 6:
        t_format = 'o'
        ins = 'halt' 
    elif opcode == 7:
        t_format = 'o'
        ins = 'noop'
    return opcode, t_format, ins

def execute_instruction(state):
    machinecode = state.mem[state.pc]
    opcode, t, ins = get_opcode(machinecode)
    if ins == 'halt':
        return False

    reg_a = (machinecode >> 19) & 0b0111    # bits 19-21
    reg_b = (machinecode >> 16) & 0b0111    # bits 16-18

    match t:
        case 'r':        
            dest_reg = machinecode & 0b0111         # bits 0-2
            execute_r_type(state, reg_a, reg_b, dest_reg, ins)
        case 'i':
            offset_field = machinecode & 0x0FFFF     # bits 0-15
            execute_i_type(state, reg_a, reg_b, offset_field, ins)
        case 'j':
            execute_j_type(state, reg_a, reg_b, ins)

    return True

def execute_r_type(state, reg_a, reg_b, dest_reg, ins):
    if dest_reg == 0: return

    reg = state.reg
    if ins == 'add':
        reg[dest_reg] = int32(reg[reg_a]) + int32(reg[reg_b])
    elif ins == 'nand':
        reg[dest_reg] = ~(int32(reg[reg_a]) & int32(reg[reg_b]))

def execute_i_type(state, reg_a, reg_b, offset_field, ins):
    mem = state.mem
    reg = state.reg
    offset_field = sign_extend(offset_field)
    mem_addr = int32(offset_field) + int32(reg[reg_a])

    if ins == 'lw':
        if reg_b == 0: return

        reg[reg_b] = int32(mem[mem_addr])
    elif ins == 'sw':
        mem[mem_addr] = int32(reg[reg_b])
    elif ins == 'beq':
        if reg[reg_a] == reg[reg_b]:
            state.pc = state.pc + int32(offset_field)

def execute_j_type(state, reg_a, reg_b, ins):
    reg = state.reg

    if ins == 'jalr':
        if reg_b == 0: return

        reg[reg_b] = state.pc + int32(1)
        if reg_a == reg_b:
            state.pc = state.pc + int32(1)
        else:
            state.pc = reg[reg_a] - int32(1)

def sign_extend(num: int):
    # convert a 16-bit number into a 32-bit integer 
    if num & (1 << 15):
         num -= (1 << 16)
    return num