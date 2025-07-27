import sys
from . import __version__


def main():
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"cleaningbox version {__version__}")
    else:
        print("Use --version to check version.")


if __name__ == "__main__":
    main()
