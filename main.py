#!/usr/bin/env python3
"""make.fun entrypoint for news-image-20261120.

Standard library only. Copies the pre-composed front page
(assets/entry.png, drawn by compose.py) to the output entry.png,
byte for byte, so repeated runs always produce identical bytes.

Output directory: $MAKEFUN_OUTPUT_DIR when set, else /output.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    src = Path(__file__).resolve().parent / "assets" / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
