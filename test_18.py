import base64

import util


def test_solve() -> None:
    key, nonce = b"YELLOW SUBMARINE", bytes(8)
    ct = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    pt = b"Yo, VIP Let's kick it Ice, Ice, baby Ice, Ice, baby "
    assert util.AesCtrCipher(key, nonce).crypt(base64.b64decode(ct)) == pt
