import itertools


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def xor_c(a, b: int):
    return bytes(x ^ y for x, y in zip(a, itertools.repeat(b)))


def pairs(it):
    # pairs('goats') -> 'go', 'oa', 'at', 'ts'
    a, b = itertools.tee(it)
    next(b, None)
    return zip(a, b)


def blocks(x, n):
    # blocks('goats', 2) -> 'go', 'at', 's'
    return [x[i : i + n] for i in range(0, len(x), n)]
