import os
from typing import override

from my_pgp.ciphers.asymmetric import AsymmetricCipher, KeyPair


class X25519(AsymmetricCipher):
    _key: bytes

    def __init__(self, key) -> None:
        self._key = key

    @classmethod
    def _generate_private_key(cls, seed: bytes) -> bytes:
        private_key = bytearray(seed)
        private_key[0] &= 0b11111000
        private_key[31] &= 0b01111111
        private_key[31] |= 0b01000000
        return bytes(private_key)

    @classmethod
    @override
    def generate_keys(cls, *args: str) -> KeyPair:
        if len(args) > 1:
            raise ValueError("X25519 -g takes at most one argument (seed)")
        if args:
            seed = bytes.fromhex(args[0])
            if len(seed) != 32:
                raise ValueError("seed must be 32 bytes (64 hex chars)")
        else:
            seed = os.urandom(32)
        private_key = cls._generate_private_key(seed)
        print(f"Private key: {private_key.hex()}")

    @override
    def encrypt(self, message: bytes) -> bytes:
        raise NotImplementedError("X25519 is not an encryption algorithm.")

    @override
    def decrypt(self, message: bytes) -> bytes:
        raise NotImplementedError("X25519 is not an encryption algorithm.")
