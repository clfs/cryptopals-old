import pytest  # type: ignore

from Cryptodome.Util.Padding import unpad


def test_valid_input():
    assert unpad(b"ICE ICE BABY\x04\x04\x04\x04", 16) == b"ICE ICE BABY"


def test_invalid_input():
    cases = [b"ICE ICE BABY\x05\x05\x05\x05", b"ICE ICE BABY\x01\x02\x03\x04"]
    for x in cases:
        with pytest.raises(ValueError):
            _ = unpad(x, 16)
