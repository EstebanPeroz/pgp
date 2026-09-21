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
    parser.add_argument("crypto_system",
                        choices=["xor", "aes", "rsa", "pgp-xor", "pgp-aes"])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("-c", action="store_true")
    mode.add_argument("-d", action="store_true")
    mode.add_argument("-g", nargs=2, metavar=("P", "Q"))
    parser.add_argument("-b", action="store_true")
    parser.add_argument("key", nargs="?", default=None)
    args = parser.parse_intermixed_args()
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
    return data

def check_block(args, message):
    if not args.b or args.crypto_system == "rsa":
        return
    sym_key = args.key.split(":")[0] if "pgp" in args.crypto_system else args.key
    if len(sym_key) // 2 != len(message): 
        sys.stderr.write("with -b, key and message must be the same size\n")
        sys.exit(84)