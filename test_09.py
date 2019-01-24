from Cryptodome.Util.Padding import pad


def test_solve():
    assert pad(b"YELLOW SUBMARINE", 20) == b"YELLOW SUBMARINE\x04\x04\x04\x04"
