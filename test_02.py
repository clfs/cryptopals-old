import util


def xor_hex(a, b):
    return util.xor(bytes.fromhex(a), bytes.fromhex(b)).hex()


def test_solve():
    a = "1c0111001f010100061a024b53535009181c"
    b = "686974207468652062756c6c277320657965"
    c = "746865206b696420646f6e277420706c6179"
    assert xor_hex(a, b) == c
