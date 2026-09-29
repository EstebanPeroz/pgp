from abc import ABC, abstractmethod
from typing import NamedTuple

from my_pgp.ciphers.base import Cipher


class KeyPair(NamedTuple):
    public_key: bytes
    private_key: bytes


class AsymmetricCipher(Cipher, ABC):
    """
    Asymmetric encryption algorithm.
    """

    @classmethod
    @abstractmethod
    def generate_keys(cls, *args: str) -> KeyPair:
        """Generate a public and private key pair."""
        ...
