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
        key_pair: KeyPair = KeyPair(
            public_key=b"public_key", private_key=b"private"
        )
        return key_pair
