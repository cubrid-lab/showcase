#!/usr/bin/env python3
"""Collect the HTML, PDF and PPTX of each release group into one directory.

Usage (from the repository root, after `HTML_BUNDLE_DIR=... npm run build:site`,
the export:* npm scripts and presentation/scripts/verify_exports.py):

    python3 scripts/package_presentations.py --html presentation/exports/html \
        --out presentation/exports/releases

For every `release` value in presentation/presentations.json this writes
`<out>/<release>/` holding, for each deck in that group, `<exportName>.pdf`,
`<exportName>.pptx` and `<exportName>-html.zip`, plus `presentation-manifest.json`
and `SHA256SUMS`. All three formats come from the same checkout, so one source
commit identifies them. Upload one such directory, unchanged, as a new
GitHub prerelease.

The HTML ZIP is built with a relative base: unzip it and serve the folder with
any static server, for example `python3 -m http.server`. Browsers block the
deck's scripts when index.html is opened straight from disk.

Requires pypdf (same pin as the export verification).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRESENTATION = ROOT / "presentation"
sys.dont_write_bytecode = True  # keep the checkout clean when importing the verifier
sys.path.insert(0, str(PRESENTATION / "scripts"))
from verify_exports import check_pdf, check_pptx, expected_slide_count  # noqa: E402
from pypdf import PdfReader  # noqa: E402

PAGES_URL = "https://cubrid-lab.github.io/showcase"
SRC = re.compile(r"^src:\s*\./(\S+)\s*$", re.M)
# Fixed timestamp so the same build always gives the same ZIP bytes.
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def zip_dir(folder: Path, target: Path, prefix: str) -> None:
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in folder.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(f"{prefix}/{path.relative_to(folder).as_posix()}", ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())


def package_version(name: str) -> str | None:
    package = PRESENTATION / "node_modules" / name / "package.json"
    return json.loads(package.read_text())["version"] if package.is_file() else None


def source_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def build_record() -> dict:
    record = {"builtAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    if os.environ.get("GITHUB_RUN_ID"):
        server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
        record |= {
            "workflowRunUrl": f"{server}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
            "event": os.environ.get("GITHUB_EVENT_NAME"),
            "ref": os.environ.get("GITHUB_REF"),
        }
    if os.environ.get("PR_HEAD_SHA"):
        # A pull-request checkout is GitHub's temporary merge commit, which is on no branch.
        record |= {
            "pullRequestHead": os.environ["PR_HEAD_SHA"],
            "note": "built from a pull-request test merge; publish releases from a main run instead",
        }
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--exports", default="presentation/exports", type=Path,
                        help="directory with the exported PDF and PPTX files")
    parser.add_argument("--html", required=True, type=Path,
                        help="HTML_BUNDLE_DIR used for build:site")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    decks = json.loads((PRESENTATION / "presentations.json").read_text())["decks"]
    commit, build = source_commit(), build_record()
    tools = {"Slidev": package_version("@slidev/cli"),
             "playwright-chromium": package_version("playwright-chromium")}
    deck_config = json.loads((PRESENTATION / "deck.json").read_text())
    shutil.rmtree(args.out, ignore_errors=True)

    failed = False
    for release in dict.fromkeys(deck["release"] for deck in decks):
        target = args.out / release
        target.mkdir(parents=True)
        manifest = {
            "schemaVersion": 2,
            "release": release,
            "sourceRepository": "https://github.com/cubrid-lab/showcase",
            "sourceCommit": commit,
            "build": build | {"workflow": ".github/workflows/presentation-export.yml"},
            "tools": tools,
            "pptxFormat": "one static image per slide with text speaker notes; slide text and shapes are not editable",
            "htmlBundle": "unzip, then serve the folder with a static server such as `python3 -m http.server`",
            "softwareRelease": False,
            "decks": [],
        }
        for deck in (d for d in decks if d["release"] == release):
            name = deck["exportName"]
            entry = PRESENTATION / deck["entry"]
            expected = expected_slide_count(deck["entry"])
            pdf, pptx = args.exports / f"{name}.pdf", args.exports / f"{name}.pptx"
            errors = check_pdf(pdf, expected) + check_pptx(pptx, expected)
            html = args.html / name
            if not (html / "index.html").is_file():
                errors.append(f"{html}: missing HTML bundle")
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            if errors:
                failed = True
                continue
            shutil.copy2(pdf, target / pdf.name)
            shutil.copy2(pptx, target / pptx.name)
            zip_dir(html, target / f"{name}-html.zip", f"{name}-html")
            source = SRC.search(entry.read_text()).group(1)
            record = {
                "event": deck["event"],
                "round": deck.get("round"),
                "language": deck["language"],
                "entry": f"presentation/{deck['entry']}",
                "source": f"presentation/{source}",
                "sourceSHA256": sha256(PRESENTATION / source),
                "slides": expected,
                "pdfPages": len(PdfReader(pdf).pages),
                "files": {"html": f"{name}-html.zip", "pdf": pdf.name, "pptx": pptx.name},
                "latestHtml": f"{PAGES_URL}/{deck['route']}/",
                "latestHtmlNote": "follows main; it can be newer than the files in this release",
            }
            if deck.get("metricsSnapshot"):
                record["metricsSnapshot"] = f"presentation/snapshots/{deck_config['snapshot']}.json"
            manifest["decks"].append(record)

        files = sorted(p for p in target.iterdir() if p.is_file())
        manifest["files"] = {p.name: {"bytes": p.stat().st_size, "sha256": sha256(p)} for p in files}
        (target / "presentation-manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        files = sorted(p for p in target.iterdir() if p.is_file())
        (target / "SHA256SUMS").write_text("".join(f"{sha256(p)}  {p.name}\n" for p in files))
        print(f"OK: {target} ({len(manifest['decks'])} decks, {len(files) + 1} files)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
