import pytest

from my_pgp.ciphers.pgp import PgpAes, PgpXor

SYMMETRIC_KEY = "57696e74657220697320636f6d696e67"

BIG_N = (
    "c9f91a9ff3bd6d84005b9cc8448296330bd23480f8cf8b36fd4edd0a8cd925de"
    "139a0076b962f4d57f50d6f9e64e7c41587784488f923dd60136c763fd602fb3"
)
BIG_D = (
    "81b08f4eb6dd8a4dd21728e5194dfc4e349829c9991c8b5e44b31e6ceee1e56a"
    "11d66ef23389be92ef7a4178470693f509c90b86d4a1e1831056ca0757f3e209"
)
PUBLIC_KEY = f"010001-{BIG_N}"
PRIVATE_KEY = f"{BIG_D}-{BIG_N}"

MESSAGE = b"All men must die"

CIPHERED_KEY = (
    "97f2af4c1b712008c1e46935f446756443a8a700f20581d138e4e6916afe5c5f"
    "9b9d6eaa0a870374b686f1a024f9bbb88c23c766654579339caf55afd149d41d"
)
CIPHERED_MESSAGE = "744ce22c385958348f0df26eceb62eef"


def test_encrypt_matches_subject_example():
    cipher = PgpAes(f"{SYMMETRIC_KEY}:{PUBLIC_KEY}")
    assert cipher.encrypt(MESSAGE) == (
        CIPHERED_KEY.encode() + b"\n" + CIPHERED_MESSAGE.encode()
    )


def test_decrypt_matches_subject_example():
    cipher = PgpAes(f"{CIPHERED_KEY}:{PRIVATE_KEY}")
    assert cipher.decrypt(bytes.fromhex(CIPHERED_MESSAGE)) == MESSAGE


def test_pgp_aes_decrypt_reverts_encrypt():
    encrypted = PgpAes(f"{SYMMETRIC_KEY}:{PUBLIC_KEY}").encrypt(MESSAGE)
    ciphered_key, ciphered_message = encrypted.split(b"\n")
    cipher = PgpAes(f"{ciphered_key.decode()}:{PRIVATE_KEY}")
    assert cipher.decrypt(bytes.fromhex(ciphered_message.decode())) == MESSAGE


def test_pgp_xor_decrypt_reverts_encrypt():
    message = b"You know nothing"
    encrypted = PgpXor(f"{SYMMETRIC_KEY}:{PUBLIC_KEY}").encrypt(message)
    ciphered_key, ciphered_message = encrypted.split(b"\n")
    cipher = PgpXor(f"{ciphered_key.decode()}:{PRIVATE_KEY}")
    assert cipher.decrypt(bytes.fromhex(ciphered_message.decode())) == message


def test_malformed_key_is_rejected():
    with pytest.raises(ValueError):
        PgpAes(SYMMETRIC_KEY)
