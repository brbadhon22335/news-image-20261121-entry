import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(outdir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
