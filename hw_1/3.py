import sys
from typing import TextIO


def get_word_count(file: TextIO) -> tuple[int, int, int]:
    n, w, b = 0, 0, 0
    for line in file:
        n += 1
        w += len(line.split())
        b += len(line.encode())
    return n, w, b


def print_word_count(n: int, w: int, b: int, title: str) -> None:
    print(f"{n:4d} {w:4d} {b:4d} {title}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        n, w, b = get_word_count(sys.stdin)
        print_word_count(n, w, b, "")
        sys.exit(0)

    newlines, words, byte = 0, 0, 0
    for path in sys.argv[1:]:
        try:
            f = open(path)
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {path}: No such file or directory")
        else:
            with f:
                n, w, b = get_word_count(f)
                newlines += n
                words += w
                byte += b
                print_word_count(n, w, b, path)
    if len(sys.argv) > 2:
        print_word_count(newlines, words, byte, "total")
