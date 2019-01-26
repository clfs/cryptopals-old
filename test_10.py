import base64

import util


def test_solve():
    with open("files/10.txt") as f:
        ct = base64.b64decode(f.read())
    with open("files/play_that_funky_music.txt") as f:
        pt = f.read()
    k, iv = b"YELLOW SUBMARINE", bytes(16)
    assert util.AesCbcCipher(k, iv).decrypt(ct).decode() == pt
