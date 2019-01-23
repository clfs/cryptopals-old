import base64

import util


def test_solve():
    with open("files/07.txt") as f:
        ct = base64.b64decode(f.read())
    with open("files/play_that_funky_music.txt") as f:
        pt = f.read()
    assert util.AesEcbCipher(b"YELLOW SUBMARINE").decrypt(ct).decode() == pt
