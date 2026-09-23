# from my_pgp.main import main


# def test_main_prints_hello(capsys):
#     main()
#     assert capsys.readouterr().out == "Hello World!\n"

import sys
from unittest.mock import patch

import pytest

from src.my_pgp.input_parser import input_parser

key: str = "576861742069732064656164206d6179206e6576657220646965"


def test_input_parser_valid_args():
    test_args = ["my_pgp", "xor", "-c", key]
    with patch.object(sys, "argv", test_args):
        args = input_parser()
        assert args.crypto_system == "xor"
        assert args.c is True
        assert args.d is False
        assert args.key.hex() == key


def test_input_parser_non_hex_key_exits():
    test_args = ["my_pgp", "xor", "-c", "not-hexadecimal"]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as exc_info:
            input_parser()
        assert exc_info.value.code == 84


def test_input_parser_odd_length_hex_key_exits():
    test_args = ["my_pgp", "xor", "-c", "abc"]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as exc_info:
            input_parser()
        assert exc_info.value.code == 84


def test_input_parser_non_hex_key_prints_error(capsys):
    test_args = ["my_pgp", "xor", "-c", "not-hexadecimal"]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            input_parser()
        assert "hexadecimal" in capsys.readouterr().err
