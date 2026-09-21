#!/usr/bin/env python3
from input_parser import *

def main():
    try:
        args = input_parser()
        message = read_message(args)
        # check_block(args, message)
    except KeyboardInterrupt:
        sys.exit(84)
    print("Hello World!")


if __name__ == "__main__":
    main()
