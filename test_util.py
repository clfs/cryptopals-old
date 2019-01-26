import util


def test_aes_ecb_cipher():
    cipher = util.AesEcbCipher(bytes(16))
    for n in range(1, 33):
        pt = bytes(n)
        assert cipher.decrypt(cipher.encrypt(pt)) == pt


def test_aes_cbc_cipher():
    cipher = util.AesCbcCipher(bytes(16), bytes(16))
    for n in range(1, 33):
        pt = bytes(n)
        assert cipher.decrypt(cipher.encrypt(pt)) == pt
