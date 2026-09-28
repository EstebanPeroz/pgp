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
