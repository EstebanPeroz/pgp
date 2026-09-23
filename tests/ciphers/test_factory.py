import pytest

from my_pgp.ciphers.factory import CipherFactory
from my_pgp.ciphers.xor import Xor


def test_build_returns_matching_cipher():
    cipher = CipherFactory.build("xor", b"key")
    assert isinstance(cipher, Xor)


def test_build_unknown_system_raises():
    with pytest.raises(NotImplementedError):
        CipherFactory.build("aes", b"key")
