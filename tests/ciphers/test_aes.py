import pytest

from my_pgp.ciphers.aes import Aes, _swap_words

# Example from the subject, in block mode.
KEY = bytes.fromhex("57696e74657220697320636f6d696e67")
MESSAGE = b"All men must die"
CIPHERTEXT = bytes.fromhex("744ce22c385958348f0df26eceb62eef")

# Appendix C of FIPS-197, as (key, plaintext, ciphertext).
FIPS_VECTORS = [
    (
        "000102030405060708090a0b0c0d0e0f",
        "00112233445566778899aabbccddeeff",
        "69c4e0d86a7b0430d8cdb78070b4c55a",
    ),
    (
        "000102030405060708090a0b0c0d0e0f1011121314151617",
        "00112233445566778899aabbccddeeff",
        "dda97ca4864cdfe06eaf70a0ec0d7191",
    ),
    (
        "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
        "00112233445566778899aabbccddeeff",
        "8ea2b7ca516745bfeafc49904b496089",
    ),
]


def test_encrypt():
    assert Aes(KEY).encrypt(MESSAGE) == CIPHERTEXT


def test_decrypt():
    assert Aes(KEY).decrypt(CIPHERTEXT) == MESSAGE


def test_decrypt_reverts_encrypt():
    cipher = Aes(KEY)
    assert cipher.decrypt(cipher.encrypt(MESSAGE)) == MESSAGE


@pytest.mark.parametrize(("key", "plain", "ciphered"), FIPS_VECTORS)
def test_block_cipher_matches_fips_197(key, plain, ciphered):
    # the key is byte swapped word by word by the constructor, so feed it
    # an already swapped key to get the raw FIPS one internally
    cipher = Aes(_swap_words(bytes.fromhex(key)))
    assert cipher._cipher_block(bytes.fromhex(plain)).hex() == ciphered


@pytest.mark.parametrize(("key", "plain", "ciphered"), FIPS_VECTORS)
def test_block_decipher_matches_fips_197(key, plain, ciphered):
    cipher = Aes(_swap_words(bytes.fromhex(key)))
    assert cipher._decipher_block(bytes.fromhex(ciphered)).hex() == plain


def test_key_expansion_matches_fips_197():
    cipher = Aes(_swap_words(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")))
    last = cipher._round_keys[-1]
    flat = bytes(last[row][col] for col in range(4) for row in range(4))
    assert flat.hex() == "d014f9a8c9ee2589e13f0cc8b6630ca6"


@pytest.mark.parametrize(("size", "rounds"), [(16, 10), (24, 12), (32, 14)])
def test_round_count_depends_on_key_size(size, rounds):
    cipher = Aes(bytes(size))
    assert cipher._nr == rounds
    assert len(cipher._round_keys) == rounds + 1


@pytest.mark.parametrize("size", [0, 1, 15, 17, 24 + 1, 33])
def test_invalid_key_size_is_rejected(size):
    with pytest.raises(ValueError):
        Aes(bytes(size))


def test_encrypt_pads_last_block_with_zeros():
    cipher = Aes(KEY)
    short = b"Winter"
    assert cipher.encrypt(short) == cipher.encrypt(short + bytes(10))


def test_encrypt_works_on_several_blocks():
    cipher = Aes(KEY)
    message = b"The night is dark and full of terrors"
    ciphered = cipher.encrypt(message)
    assert len(ciphered) == 48
    assert cipher.decrypt(ciphered) == message + bytes(48 - len(message))


def test_encrypt_is_block_by_block():
    cipher = Aes(KEY)
    other = b"Valar morghulis "
    assert cipher.encrypt(MESSAGE + other) == cipher.encrypt(
        MESSAGE
    ) + cipher.encrypt(other)


def test_empty_message():
    assert Aes(KEY).encrypt(b"") == b""


@pytest.mark.parametrize("size", [16, 24, 32])
def test_round_trip_on_every_key_size(size):
    cipher = Aes(bytes(range(size)))
    message = b"A lion still has claws"
    assert cipher.decrypt(cipher.encrypt(message)).startswith(message)


def test_swap_words_is_its_own_inverse():
    data = bytes.fromhex("0011223344556677")
    assert _swap_words(_swap_words(data)) == data
    assert _swap_words(data).hex() == "3322110077665544"
