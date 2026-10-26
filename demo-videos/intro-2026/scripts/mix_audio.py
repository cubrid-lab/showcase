#!/usr/bin/env python3
"""Mixes the narration and music stems of the main cut and masters it for YouTube.

    python3 scripts/mix_audio.py [--assets DIR] [--out out/audio]

Reads timelines/main.json for narration placement (shot start + offset frames), the
voice WAVs and music stems from the asset directory, and writes:

  mix.wav        48 kHz stereo float mix before mastering
  music-bus.wav, narration-bus.wav  the two buses of mix.wav (for the loudness graph)
  master.wav     48 kHz stereo 24-bit, -14 LUFS integrated, true peak <= -1 dBTP
  loudness.json  measurements of every stage (ffmpeg ebur128/loudnorm)
  envelope.json  the music gain envelope (dB, 10 ms steps) for the loudness graph

Ducking is a sidechain-style envelope computed from the narration placement: the
drums/bass/pads/keys stems drop DUCK_DB under narration, the fx stem (chapter hits,
impacts, risers) only FX_DUCK_DB, so the hits stay audible. Needs numpy and ffmpeg.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import numpy as np

SR = 48000
FPS = 30
DUCK_DB = -8.0
FX_DUCK_DB = -3.0
ATTACK_S = 0.15
RELEASE_S = 0.35
FADE_OUT_S = 1.5
TARGET_I = -14.0
TARGET_TP = -1.0
STEMS = ("drums", "bass", "pads", "keys")

ROOT = Path(__file__).resolve().parent.parent


def read_wav(path: Path) -> np.ndarray:
    """Decodes any WAV (PCM or extensible, mono or stereo) to float32 (frames, 2) at 48 kHz via ffmpeg."""
    raw = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
        capture_output=True,
        check=True,
    ).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


def write_wav_float(path: Path, x: np.ndarray) -> None:
    """Writes float32 WAV through ffmpeg (the wave module only writes PCM)."""
    subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", str(path)],
        input=np.ascontiguousarray(x, np.float32).tobytes(),
        check=True,
    )


def ebur128(path: Path, pre: str = "") -> dict:
    flt = (pre + "," if pre else "") + "ebur128=peak=true"
    out = subprocess.run(
        ["ffmpeg", "-nostdin", "-hide_banner", "-i", str(path), "-af", flt, "-f", "null", "-"],
        capture_output=True,
        text=True,
    ).stderr
    summary = out[out.rfind("Summary:"):]
    get = lambda key: float(re.search(key + r":\s+(-?[\d.]+|-inf)", summary).group(1))  # noqa: E731
    return {"I_LUFS": get("I"), "LRA_LU": get("LRA"), "TP_dBTP": get("Peak")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", default="/data/video-intro-assets")
    ap.add_argument("--out", default=str(ROOT / "out" / "audio"))
    args = ap.parse_args()
    assets, out = Path(args.assets), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    tl = json.loads((ROOT / "timelines" / "main.json").read_text())
    total = max(s["start"] + s["duration"] for s in tl["shots"])
    n = round(total / FPS * SR)

    # Narration, placed exactly as in the composition.
    vox = np.zeros((n, 2), np.float32)
    windows = []
    for s in tl["shots"]:
        nar = s.get("narration")
        if not nar:
            continue
        x = read_wav(assets / nar["src"])
        at = round((s["start"] + nar.get("offset", 0)) / FPS * SR)
        end = min(n, at + len(x))
        vox[at:end] += x[: end - at] * nar.get("volume", 1.0)
        windows.append((at / SR, end / SR, s["id"]))
        if at + len(x) > round((s["start"] + s["duration"]) / FPS * SR):
            print(f"note: {s['id']} narration runs past its shot ({len(x) / SR:.2f} s)")

    # Ducking envelope (0 = no duck, 1 = full duck) with linear attack/release ramps.
    t = np.arange(n) / SR
    w = np.zeros(n, np.float32)
    for a, b, _ in windows:
        up = np.clip((t - (a - ATTACK_S)) / ATTACK_S, 0, 1)
        down = np.clip(((b + RELEASE_S) - t) / RELEASE_S, 0, 1)
        w = np.maximum(w, np.minimum(up, down))
    g_main = 10 ** (DUCK_DB * w / 20)
    g_fx = 10 ** (FX_DUCK_DB * w / 20)
    fade = np.clip((total / FPS - t) / FADE_OUT_S, 0, 1)

    music = np.zeros((n, 2), np.float32)
    for stem in STEMS:
        music += read_wav(assets / "music" / "stems" / f"{stem}.wav")[:n] * (g_main * fade)[:, None]
    music += read_wav(assets / "music" / "stems" / "fx.wav")[:n] * (g_fx * fade)[:, None]

    mix = vox + music
    write_wav_float(out / "mix.wav", mix)
    write_wav_float(out / "music-bus.wav", music)
    write_wav_float(out / "narration-bus.wav", vox)
    step = SR // 100
    (out / "envelope.json").write_text(
        json.dumps(
            {
                "step_s": 0.01,
                "music_gain_db": [round(float(20 * np.log10(g_main[i])), 2) for i in range(0, n, step)],
                "narration": [{"shot": k, "from_s": round(a, 3), "to_s": round(b, 3)} for a, b, k in windows],
            }
        )
    )

    # Master: gain to -14 LUFS, then a peak limiter; iterate until I and true peak are on target.
    pre = ebur128(out / "mix.wav")
    gain, limit = TARGET_I - pre["I_LUFS"], -1.6
    for _ in range(8):
        chain = f"volume={gain:.3f}dB,alimiter=limit={10 ** (limit / 20):.4f}:attack=3:release=60:level=false"
        m = ebur128(out / "mix.wav", chain)
        if abs(m["I_LUFS"] - TARGET_I) <= 0.1 and m["TP_dBTP"] <= TARGET_TP:
            break
        gain += TARGET_I - m["I_LUFS"]
        if m["TP_dBTP"] > TARGET_TP:
            limit -= m["TP_dBTP"] - TARGET_TP + 0.1
    subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(out / "mix.wav"), "-af", chain, "-c:a", "pcm_s24le", "-ar", str(SR), str(out / "master.wav")],
        check=True,
    )
    final = ebur128(out / "master.wav")
    report = {
        "targets": {"I_LUFS": TARGET_I, "TP_dBTP": TARGET_TP},
        "ducking": {"music_db": DUCK_DB, "fx_db": FX_DUCK_DB, "attack_s": ATTACK_S, "release_s": RELEASE_S},
        "mix_before_master": pre,
        "master_chain": chain,
        "master": final,
        "narration_lines": len(windows),
    }
    (out / "loudness.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
