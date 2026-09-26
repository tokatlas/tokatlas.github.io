#!/usr/bin/env python3
"""Static link check: every internal href in the built site must resolve.

Walks the committed site (repo root), extracts href/src from all .html
files, resolves relative links against the page that contains them, and
verifies the target exists as a file or as <dir>/index.html.
Exits non-zero on any broken internal link.
"""
import os
import re
import sys
from urllib.parse import urljoin, urldefrag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".cache", "scripts", ".github"}
HREF_RE = re.compile(r'(?:href|src)="([^"]+)"')


def main() -> int:
    broken = []
    checked = 0
    pages = 0
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.endswith(".html"):
                continue
            pages += 1
            page_path = os.path.relpath(os.path.join(root, fn), ROOT)
            if fn == "index.html":
                # served as a directory: /hardware/index.html lives at /hardware/
                page_url = "https://tokatlas.github.io/" + os.path.dirname(
                    page_path) + "/"
            else:
                page_url = "https://tokatlas.github.io/" + page_path
            text = open(os.path.join(root, fn), encoding="utf-8").read()
            for m in HREF_RE.finditer(text):
                raw = m.group(1)
                if raw.startswith(("http://", "https://", "mailto:",
                                   "data:", "javascript:", "#", "'")):
                    continue
                target, _frag = urldefrag(urljoin(page_url, raw))
                target = target.split("tokatlas.github.io", 1)[-1]
                if not target.startswith("/"):
                    continue
                rel = target.lstrip("/").split("?")[0]
                if not rel:
                    continue
                checked += 1
                base = os.path.join(ROOT, rel)
                if os.path.isfile(base) or os.path.isfile(base + "/index.html"):
                    continue
                broken.append((page_path, target))
    if broken:
        for page, target in broken:
            print("broken: %s -> %s" % (page, target))
        print("FAIL: %d broken internal links" % len(broken))
        return 1
    print("OK: %d internal links across %d pages" % (checked, pages))
    return 0


if __name__ == "__main__":
    sys.exit(main())
