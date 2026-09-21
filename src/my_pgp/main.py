#!/usr/bin/env python3
from input_parser import input_parser, read_message
import sys

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
