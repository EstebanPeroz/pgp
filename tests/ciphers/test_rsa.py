import pytest

from my_pgp.ciphers.rsa import RSA

PUBLIC_KEY = "0101-19bb"
PRIVATE_KEY = "9d5b-19bb"

BIG_P = "4b1da73924978f2e9c1f04170e46820d648edbee12ccf4d4462af89b080c86e1"
BIG_Q = "bb3ca1e126f7c8751bd81bc8daa226494efb3d128f72ed9f6cacbe96e14166cb"
BIG_N = (
    "c9f91a9ff3bd6d84005b9cc8448296330bd23480f8cf8b36fd4edd0a8cd925de"
    "139a0076b962f4d57f50d6f9e64e7c41587784488f923dd60136c763fd602fb3"
)
BIG_D = (
    "81b08f4eb6dd8a4dd21728e5194dfc4e349829c9991c8b5e44b31e6ceee1e56a"
    "11d66ef23389be92ef7a4178470693f509c90b86d4a1e1831056ca0757f3e209"
)


def test_from_hex_reads_little_endian():
    assert RSA.from_hex("67452301") == 0x1234567


def test_from_hex_reads_even_length():
    assert RSA.from_hex("d3") == 0xD3
    assert RSA.from_hex("bb19") == 0x19BB


def test_from_hex_pads_odd_length():
    assert RSA.from_hex("d") == 0xD
    assert RSA.from_hex("abc") == 0xBC0A


def test_from_hex_rejects_non_hex():
    with pytest.raises(ValueError):
        RSA.from_hex("not-hexadecimal")


def test_to_hex_matches_subject_example():
    assert RSA.to_hex(0x1234567) == "67452301"


def test_to_hex_reverts_from_hex():
    assert RSA.to_hex(RSA.from_hex("19bb")) == "19bb"


def test_to_bytes_keeps_one_byte_for_zero():
    assert RSA.to_bytes(0) == b"\x00"


def test_generate_keys_matches_subject_example():
    assert RSA.generate_keys(0xD3, 0xE3) == (PUBLIC_KEY, PRIVATE_KEY)


def test_generate_keys_matches_subject_large_example():
    p, q = RSA.from_hex(BIG_P), RSA.from_hex(BIG_Q)
    assert RSA.generate_keys(p, q) == (
        f"010001-{BIG_N}",
        f"{BIG_D}-{BIG_N}",
    )


def test_generate_keys_picks_the_biggest_valid_fermat_prime():
    public, _ = RSA.generate_keys(0xD3, 0xE3)
    assert public.split("-")[0] == RSA.to_hex(257)


def test_generate_keys_without_valid_fermat_prime_raises():
    with pytest.raises(ValueError):
        RSA.generate_keys(3, 3)


def test_encrypt_matches_subject_example():
    assert RSA(PUBLIC_KEY).encrypt(b"WF") == bytes.fromhex("8f84")


def test_decrypt_matches_subject_example():
    assert RSA(PRIVATE_KEY).decrypt(bytes.fromhex("8f84")) == b"WF"


def test_decrypt_reverts_encrypt():
    ciphered = RSA(PUBLIC_KEY).encrypt(b"WF")
    assert RSA(PRIVATE_KEY).decrypt(ciphered) == b"WF"


def test_empty_key_is_rejected():
    with pytest.raises(ValueError):
        RSA("")


def test_malformed_key_is_rejected():
    with pytest.raises(ValueError):
        RSA("0101")


def test_message_larger_than_modulus_is_rejected():
    with pytest.raises(ValueError):
        RSA(PUBLIC_KEY).encrypt(b"much too long for this tiny key")
