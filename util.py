import itertools

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Util.strxor import strxor


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


class AesCbcCipher:
    """Fun fact: CBC decryption is parallelizable, but encryption isn't."""

    def __init__(self, k, iv):
        self.ecb = AES.new(k, AES.MODE_ECB)
        self.iv = iv

    def encrypt(self, pt):
        p, c = blocks(pad(pt, 16), 16), [self.iv]
        for pi, ci in zip(p, c):
            c.append(self.ecb.encrypt(strxor(pi, ci)))
        return b"".join(c[1:])

    def decrypt(self, ct):
        c = [self.iv] + blocks(ct, 16)
        p = [strxor(c[i - 1], self.ecb.decrypt(c[i])) for i in range(1, len(c))]
        return unpad(b"".join(p), 16)
