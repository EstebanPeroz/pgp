import sys

from my_pgp.ciphers.base import Cipher
from my_pgp.ciphers.factory import CipherFactory
from my_pgp.ciphers.rsa import RSA


class Core:
    _cipher: Cipher

    def __init__(self, args, message) -> None:
        if not args or (message is None and not args.g):
            raise ValueError("Arguments are needed.")

        self._args = args
        self._message = message
        if args.g:
            return
        self._cipher = CipherFactory.build(
            self._args.crypto_system, self._args.key
        )

    def _generate_keys(self) -> None:
        p, q = (RSA.from_hex(number) for number in self._args.g)
        public, private = RSA.generate_keys(p, q)
        print(f"public key: {public}")
        print(f"private key: {private}")

    def _encrypt(self) -> str:
        message: bytes = self._cipher.encrypt(self._message)
        return message.hex()

    def _decrypt(self) -> bytes:
        return self._cipher.decrypt(self._message)

    def run(self) -> None:
        if self._args.g:
            self._generate_keys()
            return
        if self._args.c:
            print(self._encrypt())
        elif self._args.d:
            sys.stdout.buffer.write(self._decrypt())
            sys.stdout.buffer.write(b"\n")
