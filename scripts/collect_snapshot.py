#!/usr/bin/env python3
"""Collect metrics snapshot for the CUBRID Python ecosystem.

Usage:
    GITHUB_TOKEN=ghp_xxx python scripts/collect_snapshot.py

Output:
    presentation/snapshots/YYYY-MM-DD.json

Requires GITHUB_TOKEN with repo scope for traffic API (unique clones).
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPOS = [
    "cubrid-lab/pycubrid",
    "cubrid-lab/sqlalchemy-cubrid",
    "cubrid-lab/cubrid-mcp-server",
    "cubrid-lab/cubrid-cookbook-python",
]

REPO_SHORT = {
    "cubrid-lab/pycubrid": "pycubrid",
    "cubrid-lab/sqlalchemy-cubrid": "sqlalchemy-cubrid",
    "cubrid-lab/cubrid-mcp-server": "cubrid-mcp-server",
    "cubrid-lab/cubrid-cookbook-python": "cubrid-cookbook-python",
}

PYPI_PACKAGES = {
    "cubrid-lab/pycubrid": "pycubrid",
    "cubrid-lab/sqlalchemy-cubrid": "sqlalchemy-cubrid",
}

SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "presentation" / "snapshots"


def gh(args: list[str]) -> str:
    """Run a gh CLI command and return stdout."""
    result = subprocess.run(
        ["gh"] + args,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout.strip()


def collect_repo_metrics(repo: str) -> dict:
    """Collect metrics for a single repo."""
    short = REPO_SHORT[repo]
    metrics: dict = {"repo": short}

    # Stars
    try:
        raw = gh(["repo", "view", repo, "--json", "stargazerCount", "--jq", ".stargazerCount"])
        metrics["stars"] = {"value": int(raw), "source": "GitHub API", "stale": False}
    except Exception as e:
        metrics["stars"] = {"value": None, "source": "GitHub API", "stale": True, "error": str(e)}

    # Merged PRs
    try:
        raw = gh(["pr", "list", "-R", repo, "--state", "merged", "--limit", "1000", "--json", "number", "--jq", "length"])
        metrics["mergedPRs"] = {"value": int(raw), "source": "GitHub API", "stale": False}
    except Exception as e:
        metrics["mergedPRs"] = {"value": None, "source": "GitHub API", "stale": True, "error": str(e)}

    # Unique clones (14d) — requires push access
    try:
        raw = gh(["api", f"repos/{repo}/traffic/clones", "--jq", ".uniques"])
        metrics["uniqueClones14d"] = {
            "value": int(raw),
            "period": "last 14 days",
            "source": "GitHub Traffic API",
            "note": "Per-repo unique; cross-repo deduplication not possible",
            "stale": False,
        }
    except Exception as e:
        metrics["uniqueClones14d"] = {
            "value": None,
            "period": "last 14 days",
            "source": "GitHub Traffic API",
            "stale": True,
            "error": str(e),
        }

    # Latest release
    try:
        raw = gh(["release", "view", "-R", repo, "--json", "tagName,publishedAt", "--jq", "[.tagName,.publishedAt] | @tsv"])
        parts = raw.split("\t")
        metrics["latestRelease"] = {"tag": parts[0], "date": parts[1] if len(parts) > 1 else None, "stale": False}
    except Exception:
        metrics["latestRelease"] = {"tag": None, "stale": True}

    # PyPI releases (where applicable)
    if repo in PYPI_PACKAGES:
        pkg = PYPI_PACKAGES[repo]
        try:
            raw = subprocess.run(
                ["curl", "-sf", f"https://pypi.org/pypi/{pkg}/json"],
                capture_output=True, text=True, timeout=15,
            )
            if raw.returncode == 0:
                data = json.loads(raw.stdout)
                metrics["pypiReleases"] = {
                    "value": len(data.get("releases", {})),
                    "source": "PyPI JSON API",
                    "stale": False,
                }
            else:
                raise RuntimeError("curl failed")
        except Exception as e:
            metrics["pypiReleases"] = {"value": None, "source": "PyPI JSON API", "stale": True, "error": str(e)}

    return metrics


def build_snapshot(repo_data: list[dict]) -> dict:
    """Assemble individual repo metrics into a full snapshot."""
    now = datetime.now(timezone.utc)

    def sum_metric(key: str) -> dict:
        per_repo = {}
        total = 0
        any_stale = False
        for r in repo_data:
            m = r.get(key, {})
            short = r["repo"]
            val = m.get("value")
            if val is not None:
                per_repo[short] = val
                total += val
            else:
                per_repo[short] = None
                any_stale = True
        result = {"perRepo": per_repo, "total": total, "stale": any_stale}
        # Copy metadata from first non-empty entry
        for r in repo_data:
            m = r.get(key, {})
            if m.get("value") is not None:
                for k in ("source", "period", "note", "unit"):
                    if k in m:
                        result[k] = m[k]
                break
        return result

    snapshot = {
        "snapshotDate": now.strftime("%Y-%m-%d"),
        "collectedAt": now.isoformat(),
        "repos": [r["repo"] for r in repo_data],
        "metrics": {
            "stars": {**sum_metric("stars"), "unit": "stars"},
            "mergedPRs": {**sum_metric("mergedPRs"), "unit": "merged PRs"},
            "uniqueClones14d": {
                **sum_metric("uniqueClones14d"),
                "unit": "per-repo unique clones (cross-repo overlap not removed)",
                "period": "last 14 days",
            },
            "pypiReleases": {**sum_metric("pypiReleases"), "unit": "releases"},
        },
        "perRepo": repo_data,
    }

    return snapshot


def main():
    # Check gh auth
    try:
        gh(["auth", "status"])
    except RuntimeError:
        print("Error: gh CLI not authenticated. Run 'gh auth login' first.", file=sys.stderr)
        sys.exit(1)

    print(f"Collecting metrics for {len(REPOS)} repos...")

    repo_data = []
    for repo in REPOS:
        short = REPO_SHORT[repo]
        print(f"  {short}...", end=" ", flush=True)
        try:
            data = collect_repo_metrics(repo)
            repo_data.append(data)
            stars = data.get("stars", {}).get("value", "?")
            prs = data.get("mergedPRs", {}).get("value", "?")
            print(f"stars={stars}, PRs={prs}")
        except Exception as e:
            print(f"ERROR: {e}")
            repo_data.append({"repo": short, "error": str(e)})

    snapshot = build_snapshot(repo_data)

    # Write snapshot
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = snapshot["snapshotDate"]
    out_path = SNAPSHOT_DIR / f"{date_str}.json"

    if out_path.exists():
        print(f"\nWarning: {out_path} already exists. Appending timestamp.", file=sys.stderr)
        ts = datetime.now(timezone.utc).strftime("%H%M%S")
        out_path = SNAPSHOT_DIR / f"{date_str}T{ts}.json"

    with open(out_path, "w") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    print(f"\nSnapshot saved: {out_path}")
    print(f"  Stars: {snapshot['metrics']['stars']['total']}")
    print(f"  Merged PRs: {snapshot['metrics']['mergedPRs']['total']}")
    clones = snapshot['metrics']['uniqueClones14d']
    # Clone traffic is dominated by CI runners — recorded, not an adoption metric
    print(f"  Unique clones (14d, per-repo sum, CI-dominated): {clones['total']}")
    if clones.get('stale'):
        print("    (some clone data unavailable -- may need push access)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
