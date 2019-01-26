import base64
import functools
import math

import util

INPUT = """
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK
"""


class Oracle:
    def __init__(self):
        self.ecb = util.AesEcbCipher(util.rbytes(16))
        self.suffix = base64.b64decode(INPUT)

    def response(self, query):
        return self.ecb.encrypt(query + self.suffix)


def recover_suffix(oracle):
    def find_block_size():
        """Largest possible size is 128 bytes (Threefish)."""
        cts = (oracle.response(bytes(n)) for n in range(128))
        return functools.reduce(math.gcd, map(len, cts))

    def is_ecb_oracle(bs):
        b = util.blocks(oracle.response(bytes(bs * 2)), bs)
        return len(b) > len(set(b))  # Any repeats?

    def find_suffix_len(bs):
        reflen = len(oracle.response(b""))
        for qlen in range(1, bs + 1):
            rlen = len(oracle.response(bytes(qlen)))
            if rlen > reflen:
                return reflen - qlen
        raise RuntimeError("suffix length not found")

    bs = find_block_size()
    assert is_ecb_oracle(bs)
    slen = find_suffix_len(bs)

    ans = b""
    for _ in range(slen):
        pad = bytes(bs - (len(ans) % bs) - 1)
        ref = oracle.response(pad)
        for b in util.brange(256):
            q = pad + ans + b
            r = oracle.response(q)
            if r[: len(q)] == ref[: len(q)]:
                ans += b
                break
    return ans


def test_solve():
    oracle = Oracle()
    assert recover_suffix(oracle) == oracle.suffix
