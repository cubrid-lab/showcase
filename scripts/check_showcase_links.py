#!/usr/bin/env python3
"""Check local showcase documentation links and its source layout."""

from __future__ import annotations

import json
import re
import subprocess
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
    "presentation/2026-ossdevcon.md",
    "presentation/decks/2026-ossdevcon/slides.md",
)
REMOVED = ("contests", "demo-videos", "press-kit", "programs")
PUBLISHED_ROUTES = (
    "contests/2026-ossdevcon",
    "events/2026-builder-season4/01-validation/ko",
    "events/2026-builder-season4/01-validation/en",
)

# Local agent runtime state; ignored in .gitignore and never committed.
RUNTIME_STATE_DIRS = (".omc",)
# Regenerable build output and release media (README.md, "Generated files").
# They go to CI artifacts or GitHub Releases, never into Git.
BUILD_OUTPUT_DIRS = ("node_modules", "out", "exports", "dist", "site-dist", ".slidev")
RELEASE_MEDIA = (".pdf", ".pptx", ".mp4", ".mov", ".webm", ".wav")

PRESENTATION = ROOT / "presentation"
# Rules from presentation/README.md ("Where deck sources live").
ENTRY_NAME = re.compile(r"\d{4}-[a-z0-9-]+(?:\.[a-z]{2})?\.md")
SOURCE_PATH = re.compile(r"decks/\d{4}-[a-z0-9-]+/(?:[a-z0-9-]+/)?slides(?:\.[a-z]{2})?\.md")
ENTRY = re.compile(r"---\n(?P<head>.*?\n)---\s*", re.S)
SRC = re.compile(r"^src:\s*\./(\S+)\s*$", re.M)
SLIDEV_ARGS = re.compile(r"slidev(?: (?:build|export))?((?: [\w.-]+\.md)+)")


def check_deck_layout() -> list[str]:
    """Each deck: one thin entry in presentation/ plus one source under decks/."""
    failures = []
    sources: dict[str, str] = {}
    entries = []
    for entry in sorted(PRESENTATION.glob("*.md")):
        if entry.name == "README.md":
            continue
        entries.append(entry.name)
        match = ENTRY.fullmatch(entry.read_text(encoding="utf-8"))
        src = SRC.search(match.group("head")) if match else None
        if not ENTRY_NAME.fullmatch(entry.name) or not src:
            failures.append(f"presentation/{entry.name}: not a thin entry; put slides in "
                            "decks/ and keep only settings plus src: here")
            continue
        sources[src.group(1)] = entry.name
        if not SOURCE_PATH.fullmatch(src.group(1)):
            failures.append(f"presentation/{entry.name}: src {src.group(1)} breaks the naming rule")
        elif not (PRESENTATION / src.group(1)).is_file():
            failures.append(f"presentation/{entry.name}: src {src.group(1)} does not exist")
    for source in sorted((PRESENTATION / "decks").rglob("*.md")):
        if source.name == "README.md":  # folder guide, not a deck source
            continue
        relative = source.relative_to(PRESENTATION).as_posix()
        if relative not in sources:
            failures.append(f"presentation/{relative}: deck source without an entry")

    # Every registered deck and every entry named by an npm script must exist,
    # and every entry must be registered so the site build and CI export it.
    registry = json.loads((PRESENTATION / "presentations.json").read_text(encoding="utf-8"))
    registered = {deck["entry"] for deck in registry["decks"]}
    scripts = (PRESENTATION / "package.json").read_text(encoding="utf-8")
    named = {name for args in SLIDEV_ARGS.findall(scripts) for name in args.split()}
    for name in sorted((named | registered) - set(entries)):
        failures.append(f"presentations.json or an npm script uses a missing entry: {name}")
    for name in sorted(set(entries) - registered):
        failures.append(f"presentation/{name}: entry is not listed in presentations.json")
    return failures


def check_tracked_runtime_state() -> list[str]:
    """Reject agent runtime state, build output and release media in the Git
    index, staged files included."""
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True,
                             capture_output=True, text=True).stdout.split("\0")
    failures = []
    for path in filter(None, tracked):
        dirs = Path(path).parts[:-1]
        if any(part in RUNTIME_STATE_DIRS for part in dirs):
            failures.append(f"{path}: agent runtime state must not be committed; "
                            "run git rm --cached on it (.gitignore already ignores it)")
        elif any(part in BUILD_OUTPUT_DIRS for part in dirs):
            failures.append(f"{path}: build output must not be committed; "
                            "regenerate it, or publish it as a CI artifact or release asset")
        elif path.lower().endswith(RELEASE_MEDIA):
            failures.append(f"{path}: PDF, PPTX, video and audio files belong in a "
                            "GitHub Release, not in Git")
    return failures


def main() -> int:
    failures: list[str] = []

    for item in REQUIRED:
        if not (ROOT / item).is_file():
            failures.append(f"Missing source: {item}")
    for item in REMOVED:
        if (ROOT / item).exists():
            failures.append(f"Legacy top-level directory remains: {item}")

    failures += check_deck_layout()
    failures += check_tracked_runtime_state()

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

    # Published HTML routes must not change; existing links depend on them.
    routes = {deck["route"] for deck in json.loads(
        (PRESENTATION / "presentations.json").read_text(encoding="utf-8"))["decks"]}
    index = (PRESENTATION / "site.html").read_text(encoding="utf-8")
    for route in PUBLISHED_ROUTES:
        if route not in routes or route not in index:
            failures.append(f"Published route changed: {route}")

    for failure in failures:
        print(f"ERROR: {failure}")
    print(f"Checked {checks} local links in Markdown; {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
