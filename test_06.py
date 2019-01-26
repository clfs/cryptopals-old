import base64

from Cryptodome.Util.strxor import strxor

import test_03
import test_05
import util


def hamming(a, b):
    return sum(bin(v).count("1") for v in strxor(a, b))


def find_key_size(ct):
    def heuristic(ks):
        pairs = util.pairs(util.blocks(ct, ks))
        return sum(hamming(x, y) for x, y in pairs if len(x) == len(y))

    return min(range(2, 61), key=heuristic)  # Bumped up to 60 for later.


def find_key(ct):
    ks = find_key_size(ct)
    return bytes(test_03.find_key(ct[offset::ks]) for offset in range(ks))


def decrypt(ct):
    return test_05.repeating_xor(ct, find_key(ct))


def test_hamming():
    a = b"this is a test"
    b = b"wokka wokka!!!"
    assert hamming(a, b) == 37


def test_solve():
    with open("files/06.txt") as f:
        ct = base64.b64decode(f.read())
    with open("files/play_that_funky_music.txt") as f:
        pt = f.read()
    assert decrypt(ct).decode() == pt
