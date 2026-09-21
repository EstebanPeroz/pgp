from abc import ABC, abstractmethod


class Cipher(ABC):
    """
    Symmetric or asymmetric encryption algorithm.

    Implementations receive their key in ``__init__``
    """

    @abstractmethod
    def encrypt(self, message: bytes) -> bytes:
        """Encrypt ``message`` and return the ciphertext."""
        ...

    @abstractmethod
    def decrypt(self, message: bytes) -> bytes:
        """Decrypt ``message`` and return the original text."""
        ...
