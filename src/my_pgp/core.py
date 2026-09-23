class Core:
    def __init__(self, args, message) -> None:
        if not args or not message:
            raise ValueError("Arguments are needed.")
        self._args = args
        self._message = message

    def _generate_keys(self) -> None:
        raise NotImplementedError("Key generation is not implemented yet.")

    def _encrypt(self) -> None:
        raise NotImplementedError("Encryption is not implemented yet.")

    def _decrypt(self) -> None:
        raise NotImplementedError("Decryption is not implemented yet.")

    def run(self) -> None:
        if self._args.g:
            self._generate_keys()
            return
        if self._args.c:
            self._encrypt()
        elif self._args.d:
            self._decrypt()
