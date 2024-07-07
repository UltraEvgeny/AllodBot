# https://stackoverflow.com/questions/54761638/what-is-the-difference-between-pytesseract-and-tesserocr/56387215#56387215

# from __future__ import annotations
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from screen_scanner.ScreenScanner import ScreenScanner


def run_scanner_server(scanner: ScreenScanner):
    scanner.start()


def main():
    scanner = ScreenScanner(need_location=False)
    if __name__ == '__main__':
        scanner.allocate_memory()
    run_scanner_server(scanner=scanner)


if __name__ == '__main__':
    main()
