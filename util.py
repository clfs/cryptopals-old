import itertools

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def xor_c(a, b: int):
    return bytes(x ^ y for x, y in zip(a, itertools.repeat(b)))


def pairs(it):
    # pairs('cats') -> ('c', 'a'), ('a', 't'), ('t', 's')
    a, b = itertools.tee(it)
    next(b, None)
    return zip(a, b)


def blocks(x, n):
    # blocks('goats', 2) -> ['go', 'at', 's']
    return [x[i : i + n] for i in range(0, len(x), n)]


class AesEcbCipher:
    def __init__(self, k):
        self.ecb = AES.new(k, AES.MODE_ECB)

    def encrypt(self, pt):
        return self.ecb.encrypt(pad(pt, 16))

    def decrypt(self, ct):
        return unpad(self.ecb.decrypt(ct), 16)
