"""
Returns the state of a bit from a HEX string
"""

__author__ = 'Cesar'


def getBitState(String, bitNum):
    Byte = int(String, 16)
    if bitNum == 7:
        mask = 128
        if Byte & mask:
            return '1'
        else:
            return '0'
    elif bitNum == 6:
        mask = 64
        if Byte & mask:
            return '1'
        else:
            return '0'
    elif bitNum == 5:
        mask = 32
        if Byte & mask:
            return '1'
        else:
            return '0'
    elif bitNum == 4:
        mask = 16
        if Byte & mask:
            return '1'
        else:
            return '0'
    elif bitNum == 3:
        mask = 8
        if Byte & mask:
            return '1'
        else:
            return '0'
    elif bitNum == 2:
        mask = 4
        if Byte & mask:
            return '1'
        else:
            return '0'
    elif bitNum == 1:
        mask = 2
        if Byte & mask:
            return '1'
        else:
            return '0'
    elif bitNum == 0:
        mask = 1
        if Byte & mask:
            return '1'
        else:
            return '0'
    else:
        return '0'