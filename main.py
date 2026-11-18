#!/usr/bin/env python3
"""Copy the pre-rendered front page to the harness output directory.

The newspaper image is drawn ahead of time by render.py (Pillow is only
needed for drawing); this entrypoint runs on the standard library alone,
so it works in the sandbox with nothing installed. It verifies the copy
by comparing SHA-256 digests before reporting success.
"""

import hashlib
import os
import sys


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    with open(source, "rb") as src, open(target, "wb") as dst:
        dst.write(src.read())
    if sha256_of(source) != sha256_of(target):
        print("copy mismatch", file=sys.stderr)
        raise SystemExit(1)
    print("wrote", target)


if __name__ == "__main__":
    main()
