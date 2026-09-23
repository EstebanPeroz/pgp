from typing import override

from my_pgp.ciphers.base import Cipher


class Xor(Cipher):
    _key: bytes

    def __init__(self, key) -> None:
        if not key:
            raise ValueError("Cipher key is needed.")
        self._key = key

    def __xor(self, message: bytes) -> bytes:
        key_size = len(self._key)
        remainder = len(message) % key_size
        if remainder != 0:
            message = message + bytes(key_size - remainder)
        result = bytearray(len(message))

        for i in range(len(message)):
            key_byte = self._key[i % key_size]
            result[i] = message[i] ^ key_byte
        return bytes(result)

    @override
    def encrypt(self, message: bytes) -> bytes:
        return self.__xor(message[::-1])

    @override
    def decrypt(self, message: bytes) -> bytes:
        return self.__xor(message)[::-1]
