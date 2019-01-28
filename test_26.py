import test_16
import util

# Very similar to Challenge 16 - only a few lines change.


class TokenManager:
    """Token format is Nonce || CT."""

    def __init__(self):
        self.key = util.rbytes(16)

    def create_token(self, userdata: str) -> bytes:
        if ";" in userdata or "=" in userdata:
            raise ValueError("invalid userdata")
        s = f"comment1=cooking%20MCs;userdata={userdata};comment2=%20like%20a%20pound%20of%20bacon"
        nonce = util.rbytes(8)
        return nonce + util.AesCtrCipher(self.key, nonce).crypt(s.encode())

    def is_admin(self, token: bytes):
        nonce, ct = token[:8], token[8:]
        return b";admin=true;" in util.AesCtrCipher(self.key, nonce).crypt(ct)


def create_admin_token(manager):
    ref = manager.create_token("\x00" * len(";admin=true;"))
    nonce, ct = ref[:8], ref[8:]
    offset = len("comment1=cooking%20MCs;userdata=")
    return nonce + test_16.xor_offset(ct, b";admin=true;", offset)


def test_solve():
    manager = TokenManager()
    token = create_admin_token(manager)
    assert manager.is_admin(token)
