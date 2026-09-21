#!/usr/bin/env python3
from input_parser import input_parser
import sys

from input_parser import read_message


def main():
    try:
        args = input_parser()
        message = read_message(args)
    except KeyboardInterrupt:
        sys.exit(84)
    print("Hello World!")
    return message


if __name__ == "__main__":
    main()
