import util


def find_pt(cts):
    pts = (util.xor_c(ct, k) for ct in cts for k in range(256))
    heuristic = lambda pt: sum(b in b" etaoin" for b in pt)
    return max(pts, key=heuristic)


def test_solve():
    with open("files/04.txt") as f:
        cts = [bytes.fromhex(line) for line in f]
    assert find_pt(cts) == b"Now that the party is jumping\n"
