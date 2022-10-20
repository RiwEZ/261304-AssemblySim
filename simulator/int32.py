"""Signed Int32 Simulator

This script converts from 64-bit int to 32-bit signed int.
It simulates overflow and underflow of 32-bit signed int.
"""

def int32(x: int):
    """Convert from 64-bit signed int to 32-bit signed int. 
    Returns fake underflow/overflow

    Args:
        x (int): Integer to convert (simulate)

    Returns:
        x represented in 32-bit signed int
    """

    x = int(x)
    if x > 0xFFFFFFFF:
        raise OverflowError
    if x > 0x7FFFFFFF:
        x = int(0x100000000 - x)
        if x < 2147483648:
            return -x
        else:
            return -2147483648
    return x