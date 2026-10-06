import pytest

from my_pgp.ciphers.aes import Aes
from my_pgp.ciphers.factory import CipherFactory
from my_pgp.ciphers.xor import Xor


def test_build_returns_matching_cipher():
    cipher = CipherFactory.build("xor", b"key")
    assert isinstance(cipher, Xor)


def test_build_returns_aes():
    cipher = CipherFactory.build("aes", bytes(16))
    assert isinstance(cipher, Aes)


def test_build_unknown_system_raises():
    with pytest.raises(NotImplementedError):
        CipherFactory.build("pgp-aes", b"key")
