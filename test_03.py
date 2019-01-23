import util


def find_key(ct):
    heuristic = lambda k: sum(b in b" etaoin" for b in util.xor_c(ct, k))
    return max(range(256), key=heuristic)


def decrypt(ct):
    return util.xor_c(ct, find_key(ct))


def test_solve():
    ct = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    assert decrypt(bytes.fromhex(ct)) == b"Cooking MC's like a pound of bacon"
