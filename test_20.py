import base64

import test_06
import util


def create_cts(s):
    pts = [base64.b64decode(line) for line in s.split()]
    k, n = util.rbytes(16), util.rbytes(8)
    return [util.AesCtrCipher(k, n).crypt(pt) for pt in pts]


def find_keystream(cts):
    bound = min(map(len, cts))
    chunk = b"".join(ct[:bound] for ct in cts)
    return test_06.find_key(chunk)


def test_solve():
    """Test always passes; check STDOUT instead."""
    with open("files/20.txt") as f:
        cts = create_cts(f.read())
    ks = find_keystream(cts)
    for ct in cts:
        print(util.xor(ct, ks))
    assert True
