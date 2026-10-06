from typing import override

from my_pgp.ciphers.base import Cipher

# fmt: off
S_BOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
    0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
    0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC,
    0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A,
    0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
    0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B,
    0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85,
    0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
    0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17,
    0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88,
    0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
    0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9,
    0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6,
    0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
    0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94,
    0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68,
    0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]
# fmt: on

# The S-Box is a permutation of the 256 byte values, so its inverse is
# simply the position of each value inside it.
INV_S_BOX = [S_BOX.index(value) for value in range(256)]

RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

# Polynomial used by MixColumns and its inverse, as a 4x4 matrix.
# fmt: off
MIX_MATRIX = (
    (0x02, 0x03, 0x01, 0x01),
    (0x01, 0x02, 0x03, 0x01),
    (0x01, 0x01, 0x02, 0x03),
    (0x03, 0x01, 0x01, 0x02),
)

INV_MIX_MATRIX = (
    (0x0E, 0x0B, 0x0D, 0x09),
    (0x09, 0x0E, 0x0B, 0x0D),
    (0x0D, 0x09, 0x0E, 0x0B),
    (0x0B, 0x0D, 0x09, 0x0E),
)
# fmt: on

BLOCK_SIZE = 16

WORD_SIZE = 4

NB_COLUMNS = 4

# Key length in bytes -> (words in the key, number of rounds).
KEY_SIZES = {16: (4, 10), 24: (6, 12), 32: (8, 14)}

State = list[list[int]]


def _xtime(byte: int) -> int:
    """Multiply ``byte`` by 2 in GF(2^8)."""
    shifted = byte << 1
    if shifted & 0x100:
        return (shifted ^ 0x1B) & 0xFF
    return shifted


def _gmul(left: int, right: int) -> int:
    """Multiply two bytes in GF(2^8)."""
    result = 0
    while right:
        if right & 1:
            result ^= left
        left = _xtime(left)
        right >>= 1
    return result


def _swap_words(data: bytes) -> bytes:
    """
    Reverse the bytes of every 32-bit word of ``data``.

    The subject represents numbers as little endian 32-bit words, and for
    AES both the key and the ciphered message are numbers. Converting
    between that representation and the byte sequences the algorithm works
    on therefore means swapping the bytes of each word.
    """
    return b"".join(
        bytes(data[i : i + WORD_SIZE][::-1])
        for i in range(0, len(data), WORD_SIZE)
    )


class Aes(Cipher):
    """
    AES-128, AES-192 and AES-256 in block mode.

    ``nk`` is the number of 32-bit words of the key and ``nr`` the number
    of rounds, the last one leaving out the MixColumns step.
    """

    _nk: int
    _nr: int
    _round_keys: list[State]

    def __init__(self, key: bytes) -> None:
        if len(key) not in KEY_SIZES:
            raise ValueError("AES key must be 16, 24 or 32 bytes long.")
        self._nk, self._nr = KEY_SIZES[len(key)]
        self._key = _swap_words(bytes(key))
        self._round_keys = self._key_expansion()

    @staticmethod
    def _rot_word(word: list[int]) -> list[int]:
        """Cyclic left shift of a word: [b0, b1, b2, b3] -> [b1, b2, b3, b0]."""
        return word[1:] + word[:1]

    @staticmethod
    def _sub_word(word: list[int]) -> list[int]:
        """Pass each byte of the word through the S-Box."""
        return [S_BOX[byte] for byte in word]

    def _key_expansion(self) -> list[State]:
        """Derive the ``nr + 1`` round keys, as 4x4 matrices, from the key."""
        words = [
            list(self._key[i * WORD_SIZE : (i + 1) * WORD_SIZE])
            for i in range(self._nk)
        ]
        for i in range(self._nk, NB_COLUMNS * (self._nr + 1)):
            temp = words[i - 1].copy()
            if i % self._nk == 0:
                temp = self._sub_word(self._rot_word(temp))
                temp[0] ^= RCON[i // self._nk]
            elif self._nk > 6 and i % self._nk == WORD_SIZE:
                temp = self._sub_word(temp)
            previous = words[i - self._nk]
            words.append([previous[j] ^ temp[j] for j in range(WORD_SIZE)])
        return [
            [
                [
                    words[rnd * NB_COLUMNS + col][row]
                    for col in range(NB_COLUMNS)
                ]
                for row in range(WORD_SIZE)
            ]
            for rnd in range(self._nr + 1)
        ]

    @staticmethod
    def _to_state(block: bytes) -> State:
        """Load a block into a 4x4 matrix, column by column."""
        return [
            [block[col * WORD_SIZE + row] for col in range(NB_COLUMNS)]
            for row in range(WORD_SIZE)
        ]

    @staticmethod
    def _from_state(state: State) -> bytes:
        """Read a 4x4 matrix back into a block, column by column."""
        return bytes(
            state[row][col]
            for col in range(NB_COLUMNS)
            for row in range(WORD_SIZE)
        )

    @staticmethod
    def _sub_bytes(state: State, box: list[int]) -> State:
        """Substitute every byte of the state through ``box``."""
        return [[box[byte] for byte in row] for row in state]

    @staticmethod
    def _shift_rows(state: State) -> State:
        """Rotate row ``i`` of the state ``i`` bytes to the left."""
        return [row[i:] + row[:i] for i, row in enumerate(state)]

    @staticmethod
    def _inv_shift_rows(state: State) -> State:
        """Rotate row ``i`` of the state ``i`` bytes to the right."""
        return [
            row[NB_COLUMNS - i :] + row[: NB_COLUMNS - i]
            for i, row in enumerate(state)
        ]

    @staticmethod
    def _mix_columns(
        state: State, matrix: tuple[tuple[int, ...], ...]
    ) -> State:
        """Multiply each column of the state by ``matrix`` in GF(2^8)."""
        mixed = [[0] * NB_COLUMNS for _ in range(WORD_SIZE)]
        for col in range(NB_COLUMNS):
            for row in range(WORD_SIZE):
                for i in range(WORD_SIZE):
                    mixed[row][col] ^= _gmul(matrix[row][i], state[i][col])
        return mixed

    @staticmethod
    def _add_round_key(state: State, round_key: State) -> State:
        """XOR the state with a round key."""
        return [
            [state[row][col] ^ round_key[row][col] for col in range(NB_COLUMNS)]
            for row in range(WORD_SIZE)
        ]

    @staticmethod
    def _blocks(message: bytes) -> list[bytes]:
        """Split ``message`` into blocks, padding the last one with zeros."""
        remainder = len(message) % BLOCK_SIZE
        if remainder:
            message = bytes(message) + bytes(BLOCK_SIZE - remainder)
        return [
            message[i : i + BLOCK_SIZE]
            for i in range(0, len(message), BLOCK_SIZE)
        ]

    def _cipher_block(self, block: bytes) -> bytes:
        """Cipher a single block."""
        state = self._add_round_key(self._to_state(block), self._round_keys[0])
        for rnd in range(1, self._nr + 1):
            state = self._sub_bytes(state, S_BOX)
            state = self._shift_rows(state)
            if rnd != self._nr:
                state = self._mix_columns(state, MIX_MATRIX)
            state = self._add_round_key(state, self._round_keys[rnd])
        return self._from_state(state)

    def _decipher_block(self, block: bytes) -> bytes:
        """Decipher a single block, running the rounds backwards."""
        state = self._to_state(block)
        state = self._add_round_key(state, self._round_keys[self._nr])
        for rnd in range(self._nr - 1, -1, -1):
            state = self._inv_shift_rows(state)
            state = self._sub_bytes(state, INV_S_BOX)
            state = self._add_round_key(state, self._round_keys[rnd])
            if rnd:
                state = self._mix_columns(state, INV_MIX_MATRIX)
        return self._from_state(state)

    @override
    def encrypt(self, message: bytes) -> bytes:
        return b"".join(
            _swap_words(self._cipher_block(block))
            for block in self._blocks(message)
        )

    @override
    def decrypt(self, message: bytes) -> bytes:
        return b"".join(
            self._decipher_block(_swap_words(block))
            for block in self._blocks(message)
        )
