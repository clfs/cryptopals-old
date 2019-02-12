from Cryptodome.Util.strxor import strxor

import util


class TokenManager:
    """Token format is IV || CT."""

    def __init__(self):
        self.key = util.rbytes(16)
        self.cbc = util.AesCbcCipher(self.key, self.key)

    def create_token(self, userdata: str) -> bytes:
        if ";" in userdata or "=" in userdata:
            raise ValueError("invalid userdata")
        s = f"comment1=cooking%20MCs;userdata={userdata};comment2=%20like%20a%20pound%20of%20bacon"
        return self.cbc.encrypt(s.encode())

    def is_admin(self, token: bytes):
        pt = self.cbc.decrypt(token)
        try:
            s = pt.decode()
        except UnicodeDecodeError as e:
            raise RuntimeError(pt.hex()) from e
        return ";admin=true;" in s


def recover_key(manager):
    pt = "A" * 100
    ct = manager.create_token(pt)

    ct = ct[:16] + bytes(16) + ct[:16] + ct[48:]
    try:
        _ = manager.is_admin(ct)
    except RuntimeError as e:
        pt = bytes.fromhex(e.args[0])

    return strxor(pt[:16], pt[32:48])


def test_solve():
    manager = TokenManager()
    assert recover_key(manager) == manager.key
