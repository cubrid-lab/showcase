#!/usr/bin/env python3
"""Loudness graph and report for the mastered main cut.

    python3 scripts/loudness_report.py [--audio out/audio] [--video FILE ...]

Measures with ffmpeg ebur128 (BS.1770-4): momentary/short-term loudness of the master,
and short-term loudness of the music and narration buses, so the ducking under every
narration line is visible. Writes <audio>/loudness.png and <audio>/loudness-report.md.
With --video, also measures the audio track of each delivered file. Needs matplotlib.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def series(path: Path):
    """(t, M, S) lists from ebur128 frame logging, plus the summary dict."""
    err = subprocess.run(
        ["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True,
        text=True,
    ).stderr
    t, m, s = [], [], []
    for line in err.splitlines():
        hit = re.search(r"t:\s*([\d.]+)\s+TARGET:.*?M:\s*(-?[\d.]+|-inf)\s+S:\s*(-?[\d.]+|-inf)", line)
        if hit:
            t.append(float(hit.group(1)))
            m.append(max(-60.0, float(hit.group(2))) if hit.group(2) != "-inf" else -60.0)
            s.append(max(-60.0, float(hit.group(3))) if hit.group(3) != "-inf" else -60.0)
    summ = err[err.rfind("Summary:"):]
    val = lambda k: float(re.search(k + r":\s+(-?[\d.]+)", summ).group(1))  # noqa: E731
    return t, m, s, {"I_LUFS": val("I"), "LRA_LU": val("LRA"), "TP_dBTP": val("Peak")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", default=str(Path(__file__).resolve().parent.parent / "out" / "audio"))
    ap.add_argument("--video", nargs="*", default=[])
    args = ap.parse_args()
    d = Path(args.audio)
    env = json.loads((d / "envelope.json").read_text())
    tm, mm, sm, master = series(d / "master.wav")
    tb, _, sb, music = series(d / "music-bus.wav")
    tv, _, sv, vox = series(d / "narration-bus.wav")

    # Music bus loudness inside vs outside narration. ffmpeg's short-term value at t covers
    # [t - 3 s, t], so only windows that lie entirely inside (or entirely outside) count.
    def inside(t):
        return any(w["from_s"] + 0.15 <= t - 3.0 and t <= w["to_s"] for w in env["narration"])

    def outside(t):
        return all(t <= w["from_s"] - 0.15 or t - 3.0 >= w["to_s"] + 0.35 for w in env["narration"])

    def mean(xs):
        return sum(xs) / len(xs) if xs else float("nan")

    ins = mean([v for t, v in zip(tb, sb) if inside(t) and v > -59])
    outs = mean([v for t, v in zip(tb, sb) if outside(t) and v > -59])

    fig, ax = plt.subplots(figsize=(16, 6), dpi=120)
    for w in env["narration"]:
        ax.axvspan(w["from_s"], w["to_s"], color="#FFD43B", alpha=0.12, lw=0)
    ax.plot(tm, mm, color="#A8C1E8", lw=0.6, alpha=0.6, label="master momentary (400 ms)")
    ax.plot(tm, sm, color="#0D1117", lw=1.6, label="master short-term (3 s)")
    ax.plot(tb, sb, color="#8C7520", lw=1.4, label="music bus short-term (ducked)")
    ax.plot(tv, sv, color="#2E7D32", lw=1.0, alpha=0.8, label="narration bus short-term")
    ax.axhline(-14, color="#E60039", lw=0.8, ls="--", label="target -14 LUFS")
    step = env["step_s"]
    ax2 = ax.twinx()
    g = env["music_gain_db"]
    ax2.plot([i * step for i in range(len(g))], g, color="#6B7280", lw=0.8, ls=":", label="music duck gain (dB)")
    ax2.set_ylim(-30, 2)
    ax2.set_ylabel("music duck gain (dB)")
    ax.set_ylim(-50, -5)
    ax.set_xlim(0, max(tm))
    ax.set_xlabel("time (s) · shaded = narration")
    ax.set_ylabel("LUFS")
    ax.set_title(
        f"CUBRID Lab intro — master I {master['I_LUFS']} LUFS, TP {master['TP_dBTP']} dBTP, LRA {master['LRA_LU']} LU · "
        f"music bus {outs:.1f} LUFS(S) between lines vs {ins:.1f} under narration"
    )
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="lower right", fontsize=8, ncol=3)
    fig.tight_layout()
    fig.savefig(d / "loudness.png")

    lines = [
        "# Loudness report — CUBRID Lab introduction video (main cut)",
        "",
        "Measured with ffmpeg `ebur128` (EBU R128 / ITU-R BS.1770-4, true peak).",
        "",
        "| Signal | Integrated | LRA | True peak |",
        "|---|---|---|---|",
        f"| master.wav | {master['I_LUFS']} LUFS | {master['LRA_LU']} LU | {master['TP_dBTP']} dBTP |",
        f"| music bus (ducked) | {music['I_LUFS']} LUFS | {music['LRA_LU']} LU | {music['TP_dBTP']} dBTP |",
        f"| narration bus | {vox['I_LUFS']} LUFS | {vox['LRA_LU']} LU | {vox['TP_dBTP']} dBTP |",
    ]
    for v in args.video:
        _, _, _, r = series(Path(v))
        lines.append(f"| {Path(v).name} (audio track) | {r['I_LUFS']} LUFS | {r['LRA_LU']} LU | {r['TP_dBTP']} dBTP |")
    lines += [
        "",
        f"Ducking: music bus short-term loudness averages {outs:.1f} LUFS between narration lines and {ins:.1f} LUFS under narration "
        f"({ins - outs:+.1f} LU); see `loudness.png` (shaded = narration).",
        "",
        "Targets: -14 LUFS integrated, true peak at or below -1 dBTP (YouTube).",
    ]
    (d / "loudness-report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
