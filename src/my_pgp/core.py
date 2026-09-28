import sys

from my_pgp.ciphers.asymmetric import KeyPair
from my_pgp.ciphers.base import Cipher
from my_pgp.ciphers.factory import CipherFactory
from my_pgp.ciphers.rsa import RSA
from my_pgp.ciphers.x25519 import X25519


class Core:
    _cipher: Cipher
    _message: bytes

    def __init__(self, args, message: bytes | None) -> None:
        if not args:
            raise ValueError("Arguments are needed.")

        self._args = args
        if args.g is not None:
            return
        if message is None:
            raise ValueError("Arguments are needed.")
        self._message = message
        self._cipher = CipherFactory.build(
            self._args.crypto_system, self._args.key
        )

    def _generate_keys(self) -> None:
        system = self._args.crypto_system
        if system == "rsa":
            p, q = (RSA.from_hex(number) for number in self._args.g)
            public, private = RSA.generate_keys(p, q)
            print(f"public key: {public}")
            print(f"private key: {private}")
        elif system == "x25519":
            key_pair: KeyPair = X25519.generate_keys(*self._args.g)
            print(f"public key: {key_pair.public_key.hex()}")
            print(f"private key: {key_pair.private_key.hex()}")
        else:
            raise ValueError(f"{system} does not support key generation.")

    def _encrypt(self) -> str:
        message: bytes = self._cipher.encrypt(self._message)
        return message.hex()

    def _decrypt(self) -> bytes:
        return self._cipher.decrypt(self._message)

    def run(self) -> None:
        if self._args.g is not None:
            self._generate_keys()
            return
        if self._args.c:
            print(self._encrypt())
        elif self._args.d:
            sys.stdout.buffer.write(self._decrypt())
            sys.stdout.buffer.write(b"\n")
