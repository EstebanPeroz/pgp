import argparse
import sys

class MyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"{self.prog}: error: {message}\n")
        sys.exit(84)

def input_parser():
    description_text = """DESCRIPTION
Cipher or decipher MESSAGE using a given CRYPTO_SYSTEM. The MESSAGE is read from the standard input.
..."""

    parser = MyArgumentParser(
        usage="USAGE\n\t./my_pgp CRYPTO_SYSTEM MODE [OPTIONS] [key]",
        description=description_text,
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-h", action="help", help="Show this help message and exit"
    )
    parser.add_argument(
        "crypto_system",
        choices=["xor", "aes", "rsa", "pgp-xor", "pgp-aes"],
        help="Crypto system choice",
    )
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "-c",
        action="store_true",
        help="MESSAGE is clear and we want to cipher it",
    )
    mode_group.add_argument(
        "-d",
        action="store_true",
        help="MESSAGE is ciphered and we want to decipher it",
    )
    mode_group.add_argument(
        "-g",
        nargs=2,
        metavar=("P", "Q"),
        help="Generate keys using prime numbers P and Q",
    )
    
    parser.add_argument(
        "-b",
        action="store_true",
        help="Block mode for XOR, AES, and PGP",
    )
    
    parser.add_argument(
        "key",
        nargs="?",
        default=None,
        help="Key used to cipher/decipher MESSAGE",
    )
     
    args, unknown = parser.parse_known_args()

    if unknown:
        if len(unknown) == 1 and args.key is None:
            args.key = unknown[0]
        else:
            parser.error(f"unrecognized arguments: {' '.join(unknown)}")

    if args.g and args.key is not None:
        parser.error("The 'key' argument is incompatible with the -g MODE.")
        
    if not args.g and args.key is None:
        parser.error("A key must be provided unless the -g mode is used.")

    if args.b:
        if sys.stdin.isatty():
            sys.stderr.write("Error: No message provided on standard input.\n")
            sys.exit(84)
        message = sys.stdin.read().rstrip('\n')
        active_key = args.key.split(":")[0] if "pgp" in args.crypto_system else args.key
        
        if len(active_key) != len(message):
            sys.stderr.write("when b flag, key and message must be the same size.\n")
            sys.exit(84)

    return args