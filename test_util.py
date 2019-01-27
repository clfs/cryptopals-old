import util


def test_aes_ecb_cipher():
    for n in range(1, 33):
        k, pt = util.rbytes(16), util.rbytes(n)
        cipher = util.AesEcbCipher(k)
        assert cipher.decrypt(cipher.encrypt(pt)) == pt


def test_aes_cbc_cipher():
    for n in range(1, 33):
        k, iv, pt = util.rbytes(16), util.rbytes(16), util.rbytes(n)
        cipher = util.AesCbcCipher(k, iv)
        assert cipher.decrypt(cipher.encrypt(pt)) == pt


def test_aes_ctr_cipher():
    for n in range(1, 33):
        k, n, pt = util.rbytes(16), util.rbytes(8), util.rbytes(n)
        cipher = util.AesCtrCipher(k, n)
        assert cipher.crypt(cipher.crypt(pt)) == pt
