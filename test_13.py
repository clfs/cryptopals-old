from Cryptodome.Util.Padding import pad

import util


class ProfileManager:
    def __init__(self):
        self.ecb = util.AesEcbCipher(util.rbytes(16))

    def create_profile(self, email: str) -> bytes:
        if "&" in email or "=" in email:
            raise ValueError("invalid email address")
        return self.ecb.encrypt(f"email={email}&uid=10&role=user".encode())

    def get_role(self, profile: bytes) -> str:
        return kvparse(self.ecb.decrypt(profile).decode())["role"]


def kvparse(s):
    result = {}
    for pair in s.split("&"):
        left, right = pair.split("=")
        result[left] = right
    return result


def create_admin_profile(manager):
    """Assume attacker knows AES encryption is used."""
    magic_block = pad(b"admin", 16).decode()
    email1 = "A" * (16 - len("email=")) + magic_block
    email2 = "A" * (32 - len("email=" + "&uid=10&role="))
    profile1 = manager.create_profile(email1)
    profile2 = manager.create_profile(email2)

    # This is the cut-and-paste step.
    return profile2[:-16] + profile1[16:32]


def test_solve():
    manager = ProfileManager()
    profile = create_admin_profile(manager)
    assert manager.get_role(profile) == "admin"
