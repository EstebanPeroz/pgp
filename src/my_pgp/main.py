#!/usr/bin/env python3

import sys

from core import Core
from input_parser import input_parser, read_message


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
