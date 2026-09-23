#!/usr/bin/env python3

import os
import sys

if __package__ is None or __package__ == "":
    sys.path.insert(
        0, os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    )

from my_pgp.core import Core
from my_pgp.input_parser import input_parser, read_message


def main():
    try:
        args = input_parser()
        message = read_message(args)
        Core(args, message).run()
    except KeyboardInterrupt:
        sys.exit(84)
    return message


if __name__ == "__main__":
    main()
