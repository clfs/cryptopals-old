import itertools
import time

from Cryptodome.Util.strxor import strxor
import numpy as np  # type: ignore

import util

# Part 1 - Known plaintext attack.


class MtCipher:
    """Uses NumPy's MT-RNG for speed-up."""

    def __init__(self, seed: int):
        self.seed = seed

    def crypt(self, m):
        np.random.seed(self.seed)  # Reset PRNG.
        return strxor(m, np.random.bytes(len(m)))


def create_ct(known_pt):
    seed = util.rint(0, 0xFFFF)
    pt = util.rbytes(util.rint(1, 20)) + known_pt
    return seed, MtCipher(seed).crypt(pt)


def recover_seed(ct, known_pt) -> int:
    for seed in range(0xFFFF + 1):
        if MtCipher(seed).crypt(ct).endswith(known_pt):
            return seed
    raise RuntimeError("no seed found")


def test_kpa():
    known_pt = b"A" * 16
    seed, ct = create_ct(known_pt)
    assert recover_seed(ct, known_pt) == seed


# Part 2 - Time-seeded token detection.


def create_token():
    # Mock a delay by pretending the token is from 10 seconds ago.
    np.random.seed(int(time.time() - 10))
    return np.random.bytes(16)


def is_time_seeded(token):
    # Check the last 100 seconds.
    ts = int(time.time())
    for seed in range(ts, ts - 100, -1):
        np.random.seed(seed)
        if np.random.bytes(16) == token:
            return True
    return False


def test_token_detection():
    assert is_time_seeded(create_token())
