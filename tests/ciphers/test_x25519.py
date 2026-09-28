import pytest

from my_pgp.ciphers.x25519 import X25519

BOB_PRIVATE_KEY = (
    "5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb"
)
BOB_PUBLIC_KEY = (
    "de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f"
)

ALICE_PRIVATE_KEY = (
    "77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a"
)
ALICE_PUBLIC_KEY = (
    "8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a"
)

message = b"Hello, world!"
tricky_message = (
    b"Hey sir.\nHello madam.\nHow are you?\nI am fine.\nThank you.\n"
)


def test_generating_bob_public_key_from_private_key():
    key_pair = X25519.generate_keys(BOB_PRIVATE_KEY)
    assert key_pair.public_key.hex() == BOB_PUBLIC_KEY


def test_generating_alice_public_key_from_private_key():
    key_pair = X25519.generate_keys(ALICE_PRIVATE_KEY)
    assert key_pair.public_key.hex() == ALICE_PUBLIC_KEY


def test_shared_secret_between_alice_and_bob():
    bob_crypted = X25519(bytes.fromhex(ALICE_PUBLIC_KEY)).encrypt(message)
    alice_decrypted = X25519(bytes.fromhex(ALICE_PRIVATE_KEY)).decrypt(
        bob_crypted
    )
    assert alice_decrypted == message


def test_shared_secret_between_bob_and_alice():
    alice_crypted = X25519(bytes.fromhex(BOB_PUBLIC_KEY)).encrypt(message)
    bob_decrypted = X25519(bytes.fromhex(BOB_PRIVATE_KEY)).decrypt(
        alice_crypted
    )
    assert bob_decrypted == message


def test_shared_secret_no_precompute_key():
    bob_key_pair = X25519.generate_keys()
    alice_crypted = X25519(bob_key_pair.public_key).encrypt(message)
    bob_decrypted = X25519(bob_key_pair.private_key).decrypt(alice_crypted)
    assert bob_decrypted == message


def test_shared_secret_with_tricky_message():
    bob_key_pair = X25519.generate_keys()
    alice_crypted = X25519(bob_key_pair.public_key).encrypt(tricky_message)
    bob_decrypted = X25519(bob_key_pair.private_key).decrypt(alice_crypted)
    assert bob_decrypted == tricky_message


def test_generate_keys_rejects_more_than_one_argument():
    with pytest.raises(ValueError):
        X25519.generate_keys(BOB_PRIVATE_KEY, ALICE_PRIVATE_KEY)


def test_generate_keys_rejects_seed_shorter_than_32_bytes():
    with pytest.raises(ValueError):
        X25519.generate_keys(BOB_PRIVATE_KEY[:-2])


def test_generate_keys_rejects_seed_longer_than_32_bytes():
    with pytest.raises(ValueError):
        X25519.generate_keys(BOB_PRIVATE_KEY + "00")


def test_generate_keys_with_seed_is_deterministic():
    first = X25519.generate_keys(BOB_PRIVATE_KEY)
    second = X25519.generate_keys(BOB_PRIVATE_KEY)
    assert first == second


def test_generate_keys_without_seed_are_32_bytes_each():
    key_pair = X25519.generate_keys()
    assert len(key_pair.public_key) == 32
    assert len(key_pair.private_key) == 32


def test_generate_keys_without_seed_is_random():
    first = X25519.generate_keys()
    second = X25519.generate_keys()
    assert first != second


def test_clamping_clears_the_low_three_bits_of_the_first_byte():
    private_key = X25519._generate_private_key(b"\xff" * 32)
    assert private_key[0] == 0b11111000


def test_clamping_clears_the_high_bit_of_the_last_byte():
    private_key = X25519._generate_private_key(b"\xff" * 32)
    assert private_key[31] & 0b10000000 == 0


def test_clamping_sets_the_second_high_bit_of_the_last_byte():
    private_key = X25519._generate_private_key(b"\x00" * 32)
    assert private_key[31] == 0b01000000
