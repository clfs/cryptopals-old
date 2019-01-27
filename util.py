import itertools
import operator
import secrets
from struct import Struct

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Util.strxor import strxor


def xor(a, b):
    # If len(a) == len(b), use `strxor`.
    return bytes(x ^ y for x, y in zip(a, b))


def brange(*args):
    return (bytes([n]) for n in range(*args))


def rbytes(n):
    """rbytes(0) -> b""."""
    return secrets.token_bytes(n)


def rbool():
    return bool(secrets.randbits(1))


def rint(a, b):
    """a <= rint(a, b) <= b."""
    return a + secrets.randbelow(b - a + 1)


def rchoice(seq):
    return secrets.choice(seq)


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
        p = [strxor(cur, self.ecb.decrypt(nxt)) for cur, nxt in pairs(c)]
        return unpad(b"".join(p), 16)


class AesCtrCipher:
    """8-byte nonce || 8-byte counter."""

    def __init__(self, key, nonce):
        self.ecb = AES.new(key, AES.MODE_ECB)
        self.nonce = nonce

    def _keystream(self):
        to8bytes = Struct("<Q").pack  # optimization
        for c in itertools.count():
            for n in self.ecb.encrypt(self.nonce + to8bytes(c)):
                yield n

    def crypt(self, m):
        return xor(m, self._keystream())
