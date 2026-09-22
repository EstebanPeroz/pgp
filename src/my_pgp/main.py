#!/usr/bin/env python3

import sys

from input_parser import input_parser, read_message


def main():
    print("Hello World!")
    try:
        args = input_parser()
        message = read_message(args)
    except KeyboardInterrupt:
        sys.exit(84)
    return message


if __name__ == "__main__":
    main()
