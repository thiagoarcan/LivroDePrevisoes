#!/usr/bin/env python3
"""Create a deterministic JAR from Kotlin/Java compiler output."""
from pathlib import Path
import sys
import zipfile
root = Path(sys.argv[1])
with zipfile.ZipFile(sys.argv[2], 'w') as package:
    for path in sorted(root.rglob('*')):
        if path.is_file():
            entry = zipfile.ZipInfo(path.relative_to(root).as_posix(), date_time=(2020, 1, 1, 0, 0, 0))
            entry.external_attr = 0o644 << 16
            package.writestr(entry, path.read_bytes())
