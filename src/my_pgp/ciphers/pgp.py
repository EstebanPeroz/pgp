from typing import ClassVar, override

from my_pgp.ciphers.aes import Aes
from my_pgp.ciphers.base import Cipher
from my_pgp.ciphers.rsa import RSA
from my_pgp.ciphers.xor import Xor


class Pgp(Cipher):
    _symmetric_cls: ClassVar[type[Cipher]]
    _symmetric_part: bytes
    _rsa: RSA

    def __init__(self, key: str) -> None:
        try:
            symmetric_part, rsa_key = key.split(":", 1)
        except ValueError as err:
            raise ValueError(f"invalid PGP key: {key}") from err
        self._symmetric_part = bytes.fromhex(symmetric_part)
        self._rsa = RSA(rsa_key)

    @override
    def encrypt(self, message: bytes) -> bytes:
        ciphered_message = self._symmetric_cls(self._symmetric_part).encrypt(
            message
        )
        ciphered_key = self._rsa.encrypt(self._symmetric_part)
        return (
            ciphered_key.hex().encode()
            + b"\n"
            + ciphered_message.hex().encode()
        )

    @override
    def decrypt(self, message: bytes) -> bytes:
        symmetric_key = self._rsa.decrypt(self._symmetric_part)
        return self._symmetric_cls(symmetric_key).decrypt(message)


class PgpXor(Pgp):
    _symmetric_cls = Xor


class PgpAes(Pgp):
    _symmetric_cls = Aes
