#!/usr/bin/env python3
"""Reject incomplete OSSDevCon PDF/PPTX exports.

Usage (from presentation/, after the export commands):
    python3 scripts/verify_exports.py [--entry slides.md]
        [--pdf exports/ossdevcon.pdf] [--pptx exports/ossdevcon.pptx]

Requires pypdf (pinned in the README and the export workflow) and Node with
the presentation's node_modules installed.

The expected slide count is not hard-coded. It is read with @slidev/parser,
the same parser the Slidev exporter uses for its page total
(`options.data.slides.length`), so it follows edits to the deck.

A Slidev export can exit 0 while its print page still shows the
"Loading slide..." placeholder (or nothing at all) for slides whose
components had not rendered yet. Every real slide in this deck has text, so
the PDF check fails on pages that contain the placeholder or no text.
The PPTX holds one screenshot per slide, so only its structure and slide
count can be checked here.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import zipfile
from pathlib import Path

from pypdf import PdfReader

PRESENTATION_DIR = Path(__file__).resolve().parent.parent
PLACEHOLDER = "Loading slide"
SLIDE_XML = re.compile(r"ppt/slides/slide\d+\.xml")
COUNT_SLIDES_JS = (
    "const { load } = await import('@slidev/parser/fs');"
    "const data = await load(process.cwd(), process.argv[1]);"
    "console.log(data.slides.length);"
)


def expected_slide_count(entry: str) -> int:
    result = subprocess.run(
        ["node", "--input-type=module", "-e", COUNT_SLIDES_JS, entry],
        cwd=PRESENTATION_DIR,
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def check_pdf(path: Path, expected: int) -> list[str]:
    errors = []
    pages = PdfReader(path).pages
    if len(pages) != expected:
        errors.append(f"{path}: {len(pages)} pages, expected {expected}")
    for number, page in enumerate(pages, 1):
        text = (page.extract_text() or "").strip()
        if not text:
            errors.append(f"{path}: page {number} has no text (blank render)")
        elif PLACEHOLDER in text:
            errors.append(f"{path}: page {number} shows the '{PLACEHOLDER}' placeholder")
    return errors


def check_pptx(path: Path, expected: int) -> list[str]:
    try:
        with zipfile.ZipFile(path) as archive:
            bad_member = archive.testzip()
            slides = [name for name in archive.namelist() if SLIDE_XML.fullmatch(name)]
    except zipfile.BadZipFile as exc:
        return [f"{path}: not a valid zip ({exc})"]
    errors = []
    if bad_member is not None:
        errors.append(f"{path}: corrupt zip member {bad_member}")
    if len(slides) != expected:
        errors.append(f"{path}: {len(slides)} slides, expected {expected}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--entry", default="slides.md")
    parser.add_argument("--pdf", default="exports/ossdevcon.pdf")
    parser.add_argument("--pptx", default="exports/ossdevcon.pptx")
    args = parser.parse_args()

    expected = expected_slide_count(args.entry)
    pdf = PRESENTATION_DIR / args.pdf
    pptx = PRESENTATION_DIR / args.pptx
    errors = check_pdf(pdf, expected) + check_pptx(pptx, expected)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"OK: {args.entry} has {expected} slides; {pdf.name} and {pptx.name} match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
