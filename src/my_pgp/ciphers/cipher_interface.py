from abc import ABC, abstractmethod


class CipherInterface(ABC):
    @abstractmethod
    def cipher(self: CipherInterface, message: str) -> str:
        pass

    @abstractmethod
    def decipher(self: CipherInterface, message: str) -> str:
        pass
