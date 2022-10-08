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