import base64
import itertools
from struct import Struct

from Cryptodome.Cipher import AES

import util

# Most solutions brute-force the plaintext byte-by-byte. Instead, it's possible
# to recover the plaintext by calling `edit` once. For what it's worth, I made
# the same mistake at first.


class AesCtrEditingCipher:
    """8-byte nonce || 8-byte counter."""

    def __init__(self, key, nonce):
        self.ecb = AES.new(key, AES.MODE_ECB)
        self.nonce = nonce

    def _keystream(self, offset: int = 0):
        to8bytes = Struct("<Q").pack  # optimization

        c = offset // 16
        for i, n in enumerate(self.ecb.encrypt(self.nonce + to8bytes(c))):
            if i >= offset % 16:
                yield n

        for c in itertools.count(offset // 16 + 1):
            for n in self.ecb.encrypt(self.nonce + to8bytes(c)):
                yield n

    def crypt(self, m):
        return util.xor(m, self._keystream())

    def edit(self, ct, pt, offset):
        tmp = bytearray(ct)
        tmp[offset : offset + len(pt)] = util.xor(pt, self._keystream(offset))
        return bytes(tmp)


def recover_pt(cipher, ct):
    return cipher.edit(ct, ct, 0)  # Wow!


def test_solve():
    ecb = util.AesEcbCipher(b"YELLOW SUBMARINE")
    ctr = AesCtrEditingCipher(util.rbytes(16), util.rbytes(8))
    with open("files/25.txt") as f:
        pt = ecb.decrypt(base64.b64decode(f.read()))
    assert recover_pt(ctr, ctr.crypt(pt)) == pt
