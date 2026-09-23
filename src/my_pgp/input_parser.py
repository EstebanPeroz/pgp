import argparse
import sys


class MyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"{self.prog}: error: {message}\n")
        sys.exit(84)


def input_parser():
    parser = MyArgumentParser(
        usage="USAGE\n\t./my_pgp CRYPTO_SYSTEM MODE [OPTIONS] [key]",
        description="DESCRIPTION\n...",
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-h", action="help")
    parser.add_argument(
        "crypto_system", choices=["xor", "aes", "rsa", "pgp-xor", "pgp-aes"]
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("-c", action="store_true")
    mode.add_argument("-d", action="store_true")
    mode.add_argument("-g", nargs=2, metavar=("P", "Q"))
    parser.add_argument("-b", action="store_true")
    parser.add_argument("key", nargs="?", default=None)
    args = parser.parse_intermixed_args()
    if args.key is not None:
        try:
            args.key = bytearray.fromhex(args.key)
        except ValueError:
            parser.error("the key must be a valid hexadecimal string")
    if args.g and args.key is not None:
        parser.error("the key argument is incompatible with -g")
    if not args.g and args.key is None:
        parser.error("a key must be provided unless -g is used")
    return args


def read_message(args):
    if args.g:
        return None
    data = sys.stdin.buffer.read()
    if data.endswith(b"\n"):
        data = data[:-1]
    if args.d:
        try:
            data = bytes.fromhex(data.decode().strip())
        except ValueError:
            sys.stderr.write("invalid hexadecimal input\n")
            sys.exit(84)
    if args.b:
        if len(args.key) >= len(data):
            args.key = args.key[: len(data)]
        else:
            data = data[: len(args.key)]
    return data
