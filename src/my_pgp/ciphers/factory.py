from my_pgp.ciphers.base import Cipher
from my_pgp.ciphers.rsa import RSA
from my_pgp.ciphers.x25519 import X25519
from my_pgp.ciphers.xor import Xor


class CipherFactory:
    _ciphers: dict[str, type[Cipher]] = {
        "xor": Xor,
        "rsa": RSA,
        "x25519": X25519,
    }

    @classmethod
    def build(cls, algorithm: str, key: bytes) -> Cipher:
        try:
            cipher_cls = cls._ciphers[algorithm]
        except KeyError:
            raise NotImplementedError(
                f"{algorithm} is not implemented yet."
            ) from None
        return cipher_cls(key)
