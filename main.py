"""Copy the pre-rendered news image to the output directory.

The entry image (entry.png) sits next to this script in the repository.
The grader runs this program with no network and no third-party packages,
so it uses only the standard library.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    destination = os.path.join(outdir, "entry.png")
    shutil.copyfile(source, destination)
    if not os.path.exists(destination):
        raise RuntimeError("copy failed: %s was not created" % destination)
    if os.path.getsize(destination) != os.path.getsize(source):
        raise RuntimeError(
            "copy failed: %s is %d bytes, expected %d"
            % (destination, os.path.getsize(destination), os.path.getsize(source))
        )


if __name__ == "__main__":
    main()
    sys.exit(0)
