import base64

from Cryptodome.Util.Padding import pad, unpad

import util

INPUT = """
MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93
"""


class Oracle:
    def __init__(self):
        self.key = util.rbytes(16)
        self.secrets = [base64.b64decode(s) for s in INPUT.split()]

    def create_token(self):
        iv, pt = util.rbytes(16), util.rchoice(self.secrets)
        return iv + util.AesCbcCipher(self.key, iv).encrypt(pt)

    def is_padding_ok(self, token):
        iv, ct = token[:16], token[16:]
        try:
            _ = util.AesCbcCipher(self.key, iv).decrypt(ct)
        except ValueError:
            return False
        else:
            return True


def xor(a, b, c) -> bytearray:
    return bytearray(x ^ y ^ z for x, y, z in zip(a, b, c))


def recover_token(oracle):
    token = oracle.create_token()
    ans = bytearray()

    for c1, c2 in util.pairs(util.blocks(token, 16)):
        p2 = bytearray(16)
        for i in reversed(range(16)):
            padding = pad(bytes(i), 16)
            for guess in range(256):
                p2[i] = guess
                c1_alt = xor(c1, p2, padding)
                if i == 15:  # Ugly hack; prevent creating new valid padding.
                    c1_alt[14] = 0
                if oracle.is_padding_ok(bytes(c1_alt + c2)):
                    break
        ans += p2

    return bytes(unpad(ans, 16))


def test_solve():
    for _ in range(5):  # Repeat for different keys and different tokens.
        oracle = Oracle()
        assert recover_token(oracle) in oracle.secrets
