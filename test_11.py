import test_08
import util


def junk():
    return util.rbytes(util.rint(5, 10))  # 5-10 random bytes.


def encrypt(pt):
    pt = junk() + pt + junk()
    k, iv = util.rbytes(16), util.rbytes(16)
    if util.rbool():
        return "ECB", util.AesEcbCipher(k).encrypt(pt)
    else:
        return "CBC", util.AesCbcCipher(k, iv).encrypt(pt)


def detect_mode(ct):
    return "ECB" if test_08.is_aes_ecb_ct(ct) else "CBC"


def test_solve():
    pt = bytes(100)
    for _ in range(10):
        mode, ct = encrypt(pt)
        assert detect_mode(ct) == mode
