import util


def is_aes_ecb_ct(m):
    blocks = util.blocks(m, 16)
    return len(blocks) > len(set(blocks))


def find_aes_ecb_ct(cts):
    for ct in cts:
        if is_aes_ecb_ct(ct):
            return ct
    raise RuntimeError("no ciphertext found")


def test_solve():
    with open("files/08.txt") as f:
        cts = [bytes.fromhex(line) for line in f]
    ct = "d880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a"
    assert find_aes_ecb_ct(cts).hex() == ct
