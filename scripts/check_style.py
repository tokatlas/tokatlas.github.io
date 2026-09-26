#!/usr/bin/env python3
"""Style gate: no em dashes (U+2014) in authored or generated repo files.

Data blobs under data/ (records.csv, records.json, sources.json, raw/,
reference/) may carry em dashes verbatim from their sources;
everything else the project writes may not. Exits non-zero on any violation.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EM_DASH = "\u2014"
SKIP_DIRS = {".git", ".cache"}
SKIP_DATA_FILES = {"records.csv", "records.json", "sources.json"}


def main() -> int:
    bad = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            rel = os.path.relpath(os.path.join(root, fn), ROOT)
            parts = rel.split(os.sep)
            in_data = parts[0] == "data"
            skip = in_data and (
                (len(parts) == 2 and fn in SKIP_DATA_FILES)
                or (len(parts) > 2 and parts[1] in ("raw", "reference")))
            if skip:
                continue
            try:
                t = open(os.path.join(root, fn), encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            if EM_DASH in t:
                bad.append((rel, t.count(EM_DASH)))
    if bad:
        for rel, n in sorted(bad):
            print("em dash x%d: %s" % (n, rel))
        print("FAIL: %d files contain em dashes" % len(bad))
        return 1
    print("OK: no em dashes in authored/generated files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
