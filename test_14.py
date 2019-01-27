import base64
import functools
import math
import statistics

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
        self.prefix = util.rbytes(util.rint(1, 50))
        self.suffix = base64.b64decode(INPUT)

    def response(self, query):
        return self.ecb.encrypt(self.prefix + query + self.suffix)


def recover_suffix(oracle):
    def find_block_size():
        # Largest possible size is 128 bytes (Threefish).
        cts = (oracle.response(bytes(n)) for n in range(128))
        return functools.reduce(math.gcd, map(len, cts))

    def is_ecb_oracle(bs):
        b = util.blocks(oracle.response(bytes(bs * 3)), bs)
        return len(b) > len(set(b))  # Any repeats?

    def find_prefix_len(bs):
        # Create a "magic" block that decrypts to 16 null bytes. Submit queries
        # until the magic block appears, then compute the prefix length.
        r = oracle.response(bytes(bs * 3))
        magic_block = statistics.mode(util.blocks(r, bs))
        for qlen in range(bs, bs * 2):
            blocks = util.blocks(oracle.response(bytes(qlen)), bs)
            try:
                return (blocks.index(magic_block) + 1) * 16 - qlen
            except ValueError:
                continue
        raise RuntimeError("prefix length not found")

    def find_suffix_len(bs, plen):
        reflen = len(oracle.response(b""))
        for qlen in range(1, bs + 1):
            rlen = len(oracle.response(bytes(qlen)))
            if rlen > reflen:
                return reflen - plen - qlen
        raise RuntimeError("suffix length not found")

    bs = find_block_size()
    assert is_ecb_oracle(bs)
    plen = find_prefix_len(bs)
    slen = find_suffix_len(bs, plen)

    ans = b""
    for _ in range(slen):
        pad = bytes(bs - ((len(ans) + plen) % bs) - 1)
        ref = oracle.response(pad)
        for b in util.brange(256):
            q = pad + ans + b
            r = oracle.response(q)
            if r[: plen + len(q)] == ref[: plen + len(q)]:
                ans += b
                break
    return ans


def test_solve():
    for _ in range(5):  # Repeat for different prefix lengths.
        oracle = Oracle()
        assert recover_suffix(oracle) == oracle.suffix
