import pytest

from my_pgp.ciphers.xor import Xor

MESSAGE = b"You know nothing, Jon Snow"
KEY = bytes.fromhex("576861742069732064656164206d6179206e6576657220646965")
CIPHERTEXT = bytes.fromhex(
    "20070f2700071c6a4449060a490515164e4e12190b190011063c"
)


def test_encrypt():
    assert Xor(KEY).encrypt(MESSAGE) == CIPHERTEXT


def test_decrypt():
    assert Xor(KEY).decrypt(CIPHERTEXT) == MESSAGE


def test_decrypt_reverts_encrypt():
    cipher = Xor(KEY)
    assert cipher.decrypt(cipher.encrypt(MESSAGE)) == MESSAGE


def test_encrypt_pads_last_block_with_zeros():
    key = b"\x01\x02\x03"
    message = b"\x40\x30\x20\x10"
    assert Xor(key).encrypt(message) == b"\x11\x22\x33\x41\x02\x03"


def test_empty_key_is_rejected():
    with pytest.raises(ValueError):
        Xor(b"")


def test_encrypt_message_shorter_than_key():
    assert Xor(b"\x01\x02\x03").encrypt(b"\x10") == b"\x11\x02\x03"


def test_encrypt_repeats_key_on_each_block():
    message = b"\x60\x50\x40\x30\x20\x10"
    expected = b"\x11\x22\x33\x41\x52\x63"
    assert Xor(b"\x01\x02\x03").encrypt(message) == expected


def test_decrypt_keeps_padding_zeros():
    ciphertext = b"\x11\x22\x33\x41\x02\x03"
    expected = b"\x00\x00\x40\x30\x20\x10"
    assert Xor(b"\x01\x02\x03").decrypt(ciphertext) == expected
