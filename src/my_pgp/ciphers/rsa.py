import math
from typing import override

from my_pgp.ciphers.base import Cipher


class RSA(Cipher):
    FERMAT_PRIMES = (65537, 257, 17, 5, 3)

    _exp: int
    _n: int

    def __init__(self, key: str) -> None:
        if not key:
            raise ValueError("Cipher key is needed.")
        try:
            exponent, modulus = key.split("-")
            self._exp = self.from_hex(exponent)
            self._n = self.from_hex(modulus)
        except ValueError as err:
            raise ValueError(f"invalid RSA key: {key}") from err

    @staticmethod
    def from_hex(value: str) -> int:
        if len(value) % 2 != 0:
            value = "0" + value
        return int.from_bytes(bytes.fromhex(value), "little")

    @staticmethod
    def to_bytes(value: int) -> bytes:
        return value.to_bytes(max(1, (value.bit_length() + 7) // 8), "little")

    @classmethod
    def to_hex(cls, value: int) -> str:
        return cls.to_bytes(value).hex()

    @classmethod
    def generate_keys(cls, p: int, q: int) -> tuple[str, str]:
        n = p * q
        lam = math.lcm(p - 1, q - 1)
        e = next(
            (f for f in cls.FERMAT_PRIMES if f < lam and math.gcd(f, lam) == 1),
            None,
        )
        if e is None:
            raise ValueError("no valid Fermat prime for these primes")
        d = pow(e, -1, lam)
        modulus = cls.to_hex(n)
        return f"{cls.to_hex(e)}-{modulus}", f"{cls.to_hex(d)}-{modulus}"

    def __apply(self, value: int) -> int:
        if value >= self._n:
            raise ValueError("message too large for this key")
        return pow(value, self._exp, self._n)

    @override
    def encrypt(self, message: bytes) -> bytes:
        return self.to_bytes(self.__apply(int.from_bytes(message, "little")))

    @override
    def decrypt(self, message: bytes) -> bytes:
        return self.to_bytes(self.__apply(int.from_bytes(message, "little")))
