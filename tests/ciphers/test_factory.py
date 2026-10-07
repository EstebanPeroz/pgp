import pytest

from my_pgp.ciphers.aes import Aes
from my_pgp.ciphers.factory import CipherFactory
from my_pgp.ciphers.pgp import PgpAes, PgpXor
from my_pgp.ciphers.xor import Xor

RSA_KEY = "0101-19bb"


def test_build_returns_matching_cipher():
    cipher = CipherFactory.build("xor", b"key")
    assert isinstance(cipher, Xor)


def test_build_returns_aes():
    cipher = CipherFactory.build("aes", bytes(16))
    assert isinstance(cipher, Aes)


def test_build_returns_pgp_xor():
    cipher = CipherFactory.build("pgp-xor", f"11:{RSA_KEY}")
    assert isinstance(cipher, PgpXor)


def test_build_returns_pgp_aes():
    cipher = CipherFactory.build("pgp-aes", f"{'11' * 16}:{RSA_KEY}")
    assert isinstance(cipher, PgpAes)


def test_build_unknown_system_raises():
    with pytest.raises(NotImplementedError):
        CipherFactory.build("pgp-foo", b"key")
