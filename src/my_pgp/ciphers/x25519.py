import os
from typing import override

from my_pgp.ciphers.asymmetric import AsymmetricCipher, KeyPair


class X25519(AsymmetricCipher):
    _key: bytes

    def __init__(self, key) -> None:
        if not key:
            raise ValueError("Cipher key is needed.")
        self._key = key

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
            seed = os.usrandom(32)
            print(seed)
