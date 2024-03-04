import sys
from typing import TextIO


def get_last_lines(file: TextIO, n: int = 10) -> list[str]:
    return list(file)[-n:]


def print_last_lines(file: TextIO, n: int = 10) -> None:
    print("".join(get_last_lines(file, n)), end="")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_last_lines(sys.stdin, 17)
        sys.exit(0)

    for i, path in enumerate(sys.argv[1:]):
        try:
            f = open(path)
        except FileNotFoundError:
            print(
                f"{sys.argv[0]}: cannot open '{path}' for reading: No such file or directory"
            )
        else:
            # Check tail formatting implementation
            if len(sys.argv) > 2:
                file_title_newline = '\n' if i != 0 else ''
                print(f"{file_title_newline}==> {path} <==")
            with f:
                print_last_lines(f)
