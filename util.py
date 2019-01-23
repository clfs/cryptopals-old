import itertools


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def xor_c(a, b: int):
    return bytes(x ^ y for x, y in zip(a, itertools.repeat(b)))
