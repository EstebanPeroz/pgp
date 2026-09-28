import os
from typing import override

from my_pgp.ciphers.asymmetric import AsymmetricCipher, KeyPair


class X25519(AsymmetricCipher):
    P = 9
    A = 486662
    PRIME = pow(2, 255) - 19

    _key: bytes

    def __init__(self, key) -> None:
        self._key = key

    @classmethod
    def _swap(cls, a: int, b: int, bit: int) -> tuple[int, int]:
        mask = -bit

        inverter = mask & (a ^ b)
        a = a ^ inverter
        b = b ^ inverter
        return a, b

    @classmethod
    def _compute_ladder_step(
        cls,
        X0: int,
        Z0: int,
        X1: int,
        Z1: int,
        byte: int,
        bit_num: int,
        base_point: int,
    ) -> tuple[int, int, int, int]:
        new_X0, new_Z0, new_X1, new_Z1 = 0, 0, 0, 0
        bit = (byte >> bit_num) & 1
        X0, X1 = cls._swap(X0, X1, bit)
        Z0, Z1 = cls._swap(Z0, Z1, bit)

        new_X0 = pow(
            (pow(X0, 2, cls.PRIME) - pow(Z0, 2, cls.PRIME)), 2, cls.PRIME
        )
        new_Z0 = (
            4
            * X0
            * Z0
            * (pow(X0, 2, cls.PRIME) + cls.A * X0 * Z0 + pow(Z0, 2, cls.PRIME))
        ) % cls.PRIME
        new_X1 = pow(X0 * X1 - Z0 * Z1, 2, cls.PRIME)
        new_Z1 = (base_point * pow(X0 * Z1 - X1 * Z0, 2, cls.PRIME)) % cls.PRIME

        X0, X1 = cls._swap(new_X0, new_X1, bit)
        Z0, Z1 = cls._swap(new_Z0, new_Z1, bit)
        return X0, Z0, X1, Z1

    @classmethod
    def _generate_private_key(cls, seed: bytes) -> bytes:
        private_key = bytearray(seed)
        private_key[0] &= 0b11111000
        private_key[31] &= 0b01111111
        private_key[31] |= 0b01000000
        return bytes(private_key)

    @classmethod
    def _scalar_mult(cls, private_key: bytes, base_point: int) -> bytes:
        private_key = cls._generate_private_key(private_key)

        # Defines P0 (x coordinate), which is infinity by default
        X0 = 1
        Z0 = 0
        # Defines P1 (x coordinate), which is the base point by default
        X1 = base_point
        Z1 = 1

        for byte in reversed(private_key):
            for bit in reversed(range(8)):
                X0, Z0, X1, Z1 = cls._compute_ladder_step(
                    X0, Z0, X1, Z1, byte, bit, base_point
                )

        # Multiply X0 with the modular inverse of Z0 to get the affine
        # x coordinate
        public_key = (X0 * pow(Z0, cls.PRIME - 2, cls.PRIME)) % cls.PRIME
        return public_key.to_bytes(32, "little")

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
        private_key = seed
        public_key = cls._scalar_mult(private_key, cls.P)
        return KeyPair(public_key=public_key, private_key=private_key)

    @override
    def encrypt(self, message: bytes) -> bytes:
        raise NotImplementedError("X25519 is not an encryption algorithm.")

    @override
    def decrypt(self, message: bytes) -> bytes:
        raise NotImplementedError("X25519 is not an encryption algorithm.")
