#!/usr/bin/env python3
"""Check local showcase documentation links and its source layout."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MD_LINKS = re.compile(r"\]\(([^\s)]+)(?:\s+[^)]*)?\)")
HTML_LINKS = re.compile(r'\b(?:href|src)="([^"]+)"')

REQUIRED = (
    "events/2026-ossdevcon/README.md",
    "events/2026-builder-season4/01-validation/README.md",
    "projects/cubrid-lab/intro-video/README.md",
    "projects/cubrid-python-ecosystem/press-kit/README.md",
    "templates/README.md",
    "presentation/slides.md",
)
REMOVED = ("contests", "demo-videos", "press-kit", "programs")


def main() -> int:
    failures: list[str] = []

    for item in REQUIRED:
        if not (ROOT / item).is_file():
            failures.append(f"Missing source: {item}")
    for item in REMOVED:
        if (ROOT / item).exists():
            failures.append(f"Legacy top-level directory remains: {item}")

    checks = 0
    for document in sorted(ROOT.rglob("*.md")):
        if ".git" in document.parts or "node_modules" in document.parts:
            continue
        text = document.read_text(encoding="utf-8")
        for match in (*MD_LINKS.finditer(text), *HTML_LINKS.finditer(text)):
            url = match.group(1)
            parsed = urlsplit(url)
            if (parsed.scheme or parsed.netloc or not parsed.path
                    or parsed.path.startswith("/")):
                continue
            local_path = (document.parent / unquote(parsed.path)).resolve()
            checks += 1
            if not local_path.is_relative_to(ROOT):
                failures.append(f"{document.relative_to(ROOT)}: link escapes repo: {url}")
            elif not local_path.exists():
                failures.append(f"{document.relative_to(ROOT)}: broken link: {url}")

    site = (ROOT / "scripts/build_site.mjs").read_text(encoding="utf-8")
    index = (ROOT / "presentation/site.html").read_text(encoding="utf-8")
    routes = (
        "contests/2026-ossdevcon",
        "events/2026-builder-season4/01-validation/ko",
        "events/2026-builder-season4/01-validation/en",
    )
    for route in routes:
        if route not in site or route not in index:
            failures.append(f"Published route changed: {route}")

    for failure in failures:
        print(f"ERROR: {failure}")
    print(f"Checked {checks} local links in Markdown; {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
