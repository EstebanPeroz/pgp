from my_pgp.ciphers.base import Cipher
from my_pgp.ciphers.factory import CipherFactory


class Core:
    _cipher: Cipher

    def __init__(self, args, message) -> None:
        if not args or not message:
            raise ValueError("Arguments are needed.")

        self._args = args
        self._message = message
        self._cipher = CipherFactory.build(
            self._args.crypto_system, self._args.key
        )

    def _generate_keys(self) -> None:
        raise NotImplementedError("Key generation is not implemented yet.")

    def _encrypt(self) -> str:
        message: bytes = self._cipher.encrypt(self._message)
        return message.hex()

    def _decrypt(self) -> str:
        message: bytes = self._cipher.decrypt(self._message)
        return message.decode("utf-8")

    def run(self) -> None:
        if self._args.g:
            self._generate_keys()
            return
        if self._args.c:
            print(self._encrypt())
        elif self._args.d:
            print(self._decrypt())
