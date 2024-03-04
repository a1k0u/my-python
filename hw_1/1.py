import sys
from typing import TextIO


def print_files_with_numbered_lines(file: TextIO) -> None:
    for i, line in enumerate(file):
        print(f"{i + 1:6d}\t{line}", end="")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_files_with_numbered_lines(sys.stdin)
        sys.exit(0)

    path = sys.argv[1]
    try:
        f = open(path)
    except FileNotFoundError:
        print(f"{sys.argv[0]}: {path}: No such file or directory")
    else:
        with f:
            print_files_with_numbered_lines(f)
