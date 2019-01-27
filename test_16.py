import util


class TokenManager:
    """Token format is IV || CT."""

    def __init__(self):
        self.key = util.rbytes(16)

    def create_token(self, userdata: str) -> bytes:
        if ";" in userdata or "=" in userdata:
            raise ValueError("invalid userdata")
        s = f"comment1=cooking%20MCs;userdata={userdata};comment2=%20like%20a%20pound%20of%20bacon"
        iv = util.rbytes(16)
        return iv + util.AesCbcCipher(self.key, iv).encrypt(s.encode())

    def is_admin(self, token: bytes):
        iv, ct = token[:16], token[16:]
        return b";admin=true;" in util.AesCbcCipher(self.key, iv).decrypt(ct)


def xor_offset(a, b, n):
    tmp = bytearray(a)
    for i, v in enumerate(b):
        tmp[i + n] ^= v
    return bytes(tmp)


def create_admin_token(manager):
    token = manager.create_token("\x00" * 16)
    iv, ct = token[:16], token[16:]
    offset = len("comment1=cooking%20MCs;userdata=") - 16
    return iv + xor_offset(ct, b";admin=true;", offset)


def test_solve():
    manager = TokenManager()
    token = create_admin_token(manager)
    assert manager.is_admin(token)
