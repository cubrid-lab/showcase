# Intro video 2026 — motion-graphics project

Code-based motion graphics for the ≤3-minute, ad-style introduction video of the
CUBRID Lab Python projects: **pycubrid**, **sqlalchemy-cubrid**,
**cubrid-mcp-server** (read-only by default) and **cubrid-cookbook-python**.
Main cut 1920×1080 at 30 fps, Korean TTS narration.

Built with [Remotion](https://www.remotion.dev). The storyboard, voice, music and
real screen captures are plugged in as data and media files; the components
stay unchanged.

> **Status: production.** `timelines/main.json` is the final 25-shot main cut of
> [`VIDEO_DESIGN.md`](VIDEO_DESIGN.md) (2:56) with real footage, narration and music; see
> [Production](#production) to rebuild it end to end and [`PROVENANCE.md`](PROVENANCE.md) for
> every input. `short.json` and `demo.json` are still placeholder timelines (`meta.draft: true`
> puts a red `DRAFT · PLACEHOLDER` badge on every frame).

## Commands

Run from this directory. Node 24 (as in `presentation/`), ffmpeg/ffprobe on `PATH`
for the placeholder and still scripts, and network access (fonts, pinned brand
assets, and Remotion's headless Chrome download on first render).

```bash
npm ci
npm run studio            # Remotion Studio (also generates placeholders)
npm run render:main       # Main composition  -> out/main.mp4   (timelines/main.json)
npm run render:short      # Short composition -> out/short.mp4  (timelines/short.json)
npm run render:demo       # 20 s pipeline demo -> out/demo.mp4  (timelines/demo.json)
npm run render:stills -- Main 120 900 2700   # single frames -> out/stills/main-<frame>.png
npm run stills:demo       # 4 JPEG stills from out/demo.mp4 -> stills/
npm run placeholders      # (re)generate PLACEHOLDER media in public/placeholder/
npm run typecheck
scripts/render-final.sh [assetsDir] [outDir]   # main cut: render, mix, master, MP4 + WebM, captions, contact sheet
DRAFT=1 scripts/render-final.sh                # 960x540 draft of the same pipeline
```

`render:stills` defaults to four frames of `Demo`. `scripts/extract-stills.mjs
<video> <dir> [seconds ...]` extracts stills from any rendered file.

Rendering is slow on a loaded machine (OffthreadVideo frame extraction); the
delayRender timeout is 180 s in `remotion.config.ts`. Lower the parallelism
with `--concurrency=1` if frames time out.

## Pinned versions

| Package | Version | Released |
| --- | --- | --- |
| `remotion`, `@remotion/cli`, `@remotion/google-fonts` | 4.0.534 | 2026-10-07 |
| `react`, `react-dom` | 19.1.0 | 2025 |
| `typescript` | 5.9.3 | 2025 |
| `@types/react` | 19.1.8 | 2025 |

Exact versions in `package.json`, locked by `package-lock.json`. Remotion
packages must always share one version.

Fonts: Pretendard Variable (SIL OFL 1.1; linked from `presentation/public/fonts/` by
`scripts/prepare-media.mjs`, not vendored), with Noto Sans KR and JetBrains Mono (SIL OFL 1.1)
loaded from Google Fonts at render time (`src/fonts.ts`).

## Layout

```text
src/
  Root.tsx            compositions Main / Short / Demo, one per timeline file
  TimelineVideo.tsx   shots, lower thirds, transitions, narration, ducked music, subtitles
  Shots.tsx           shot `type` -> renderer registry
  timeline.ts         timeline schema, duration, ducking curve
  brand.ts            pinned brand revision, asset URLs, token loader, cube geometry
  fonts.ts
  components/
    BrandCubeAssemble.tsx   cube faces fly in, lock, resolve into the pinned icon
    KineticTitle.tsx        word-by-word masked rise, accent underline (Korean + Latin)
    Footage.tsx             MP4 with zoom/pan keyframes and callout highlights
    Mockups.tsx             WindowMockup / TerminalMockup / BrowserMockup frames
    Overlays.tsx            FeatureCallout chips, LowerThird, DraftBadge
    Subtitles.tsx           .srt/.vtt parser and burned-in subtitle track
    EndCard.tsx             lockup, install commands, links, AI-voice + independence notices
    Transitions.tsx         CubeWipe (three org-colour 30° panels), KeyWipe (main cut), FadeThrough
    Intro.tsx               main-cut shots: hook, flash, brand tiles/lockup, chapter, proof, config, cards, finale, end card
timelines/            main.json, short.json, demo.json
public/               footage/, voice/, music/ (gitignored media), subtitles/
scripts/              make-placeholders.mjs, render-stills.mjs, extract-stills.mjs,
                      build_main_timeline.py, prepare-media.mjs, render-final.sh, mix_audio.py,
                      loudness_report.py, contact-sheet.mjs, review-stills.mjs
captions/             ko/en .srt/.vtt of the main cut
stills/               4 frames of the pipeline demo render
```

## Timeline format

The composition length is the end of the last shot. All times are frames at 30 fps;
media paths are relative to `public/`.

```jsonc
{
  "meta": {"title": "…", "fps": 30, "width": 1920, "height": 1080, "draft": true, "note": "…"},
  "music": {"src": "music/bed.wav", "volume": 0.5, "duckedVolume": 0.12,
            "rampFrames": 8, "fadeInFrames": 15, "fadeOutFrames": 45},
  "subtitles": "subtitles/main.ko.srt",
  "shots": [
    {
      "id": "s03-pycubrid", "start": 165, "duration": 135, "type": "terminal",
      "transitionIn": {"type": "cubeWipe", "duration": 20},   // centred on the cut
      "props": { /* per type, below */ },
      "narration": {"src": "voice/s03.wav", "offset": 10, "durationInFrames": 96},
      "lowerThird": {"title": "pycubrid", "subtitle": "…", "from": 12, "duration": 100}
    }
  ]
}
```

| `type` | `props` |
| --- | --- |
| `cubeAssemble` | `repo` (brand registry key, or `organization` for the emblem), `size`, `title?`, `subtitle?` |
| `iconRow` | `repos[]`, `labels?[]`, `size?`, `stagger?` |
| `title` | `kicker?`, `lines[] {text, accent?, size?, weight?}`, `align?`, `accentColor?`, `stagger?` |
| `terminal` / `window` / `browser` | `footage {src, trimBefore?, playbackRate?, muted?, camera[] {at, zoom, x, y}, callouts[] {from, to, x, y, w, h, label?}}`, `title?`, `url?` (browser), `heading?`, `chips? {chips[], delay?}`, `width?`, `tilt?` |
| `features` | `chips[]`, `heading? (title props)`, `delay?`, `stagger?` |
| `endCard` | `theme` (`dark`/`light`), `lockup` (`horizontal`/`stacked`), `headline?`, `installs[]`, `links[]`, `aiVoiceDisclosure?`, `independenceNotice?` |

Main-cut shot types (`src/components/Intro.tsx`, style of the style frames):

| `type` | Storyboard shots | `props` |
| --- | --- | --- |
| `hook` | H1, H2 | `stage` (1: grid draws, grey line slams in; 2: “Python으로.” drops in, underline wipe) |
| `flash` | H3 | `flashes[] {footage, kind?, title?, url?}`, `each` (frames per flash) |
| `brandTiles` / `brandLockup` | B1 / B2 | `beat?` |
| `chapter` | P1, S1, C1, K1 | `repo`, `kicker`, `name`, `tagline?` |
| `proof` | P2–P4, S2–S4, C2–C4, K2 | `heading {kicker?, parts[] {t, accent?, underline?, br?}, still?}`, `kind?`, `mockup` (below), `align?`, `chips? {items[], at[]}`, `cards?[] {at, kicker, text}`, `windowAt?` |
| `button` / `hit` | P5 / S5 | `repo`, `heading`, `command` (button) |
| `config` | C5 | `rows[] {name, def, desc, highlight?}`, `rowAt[]`, `tools[]`, `toolsAt`, `writeAt`, `offNote`, `writeNote`, `source` |
| `cards` | K3 | `heading`, `cards[] {label, path}`, `at`, `beat`, `mockup`, `note` |
| `finale` / `introEndCard` | F1 / F2 | `items[] {repo, line}`, `heading` / `installs[]`, `url`, `notices[]` |

`mockup` takes `footage`, `title?`, `url?`, `width?`, `enter?` (false for the second half of a
split shot), `labels?[]` (persistent title-bar labels), `source?` (provenance line under the
window) and `clock?` (shows the recording's own `rec m:ss`). `footage` adds to the fields above:
`segments[] {from, to?, rate?, hold?}` (source seconds; played back to back; `hold` freezes
`from` for N frames; every segment at 2× or more shows a “×N” badge), `viewport {x, y, w, h}`
(crop of the source shown in the window) and `mask {x, y, w, h}` (everything outside is cut
away, e.g. C4 ends above the agent's SQL block). Camera and callout coordinates stay in
full-footage coordinates. A shot's `review` frame is used by the stills and the contact sheet.

`timelines/main.json` is generated by `scripts/build_main_timeline.py`; edit the script.

Camera and callout coordinates are normalized to the footage (0..1); callouts follow
the zoom. Frames in `camera`, `callouts` and `lowerThird` are relative to the shot.
Add a shot type by writing a component and registering it in `src/Shots.tsx`.

## Plugging in media

1. **Storyboard** — replace `timelines/main.json` (and `short.json`) with the
   storyboard's shots. Set `meta.draft` to `false` only for the final cut.
2. **Footage** — put screen captures (H.264 MP4, 1920×1080, 30 fps preferred) in
   `public/footage/` and point `props.footage.src` at `footage/<file>.mp4`. Use
   `trimBefore` to skip lead-in frames; add `camera` keys and `callouts` for
   zoom/pan and highlights. Footage audio is muted unless `muted: false`.
3. **Voice** — export each narration line as WAV (48 kHz) to `public/voice/` and set
   `narration.src` on its shot. Set `durationInFrames` to the line length
   (`ceil(seconds × 30)`) so the music ducks exactly under it.
4. **Music** — put the bed in `public/music/` and set `music.src`; tune
   `volume` / `duckedVolume` / `rampFrames`. Confirm the track's license allows
   this use before committing a reference to it.
5. **Subtitles** — put the `.srt` or `.vtt` in `public/subtitles/` and set
   `subtitles`. Cue times are seconds from the start of the composition.

Media under `public/footage`, `public/voice`, `public/music` and
`public/placeholder` is gitignored, as are `out/` and every `*.mp4`/`*.wav`.
Store finals outside git (see `../README.md`: Git LFS or a video link).

Placeholder media (`npm run placeholders`) is colored ffmpeg test clips stamped
`PLACEHOLDER - <KIND> FOOTAGE`, beeping tones for narration and a sine pad for
music. It is never a deliverable.

## Production

The main cut is built from four inputs that are not committed: real footage, narration,
music and the pinned brand marks. Each comes with its own provenance record; the summary and
input checksums are in [`PROVENANCE.md`](PROVENANCE.md).

### End to end

Prerequisites besides Node 24: ffmpeg/ffprobe 4.4+ with libx264, libvpx-vp9 and libopus, and
Python 3.10+ with NumPy and Matplotlib for the audio scripts
(`python3 -m pip install numpy matplotlib`).

```bash
cd demo-videos/intro-2026
npm ci
# 1. Assets in one directory (default /data/video-intro-assets, or $INTRO_ASSETS):
#    footage/*.mp4 + provenance.json   vhs/Playwright takes (P2..K3, H3-*)
#    mcp/*.mp4 + provenance.json       C2, C3, C4 (agent replay), C4_script (demo client)
#    voice/<shot>.wav + manifest.json  MeloTTS lines, ko/en .srt/.vtt
#    music/bed.wav + stems/*.wav       generated score (music/src/generate.py, seed 51)
# 2. Optional: regenerate the timeline after changing the shot list or the voice lines
python3 scripts/build_main_timeline.py
# 3. Draft (960x540, about 3 minutes here), then the master
DRAFT=1 scripts/render-final.sh
scripts/render-final.sh /data/video-intro-assets /data/video-intro-assets/out
```

`render-final.sh` runs, in order:

1. `scripts/prepare-media.mjs` hard-links the media into `public/` (gitignored) and fails on
   any missing file.
2. `remotion render … Main --muted` (H.264, CRF 16, x264 `slow`, yuv420p, 1920×1080, 30 fps;
   `CONCURRENCY`, default 4). Brand marks and Google fonts are fetched at render time, so the
   render needs network access.
3. `scripts/mix_audio.py` places each narration line at its shot start + 0.2 s, ducks the
   music stems 8 dB under narration (attack 150 ms, release 350 ms; the fx stem with the
   chapter hits only 3 dB), and masters to −14 LUFS integrated / ≤ −1 dBTP (gain plus a peak
   limiter, iterated against ffmpeg `ebur128`).
4. Mux to `cubrid-lab-intro-2026.mp4` (H.264 High + AAC 48 kHz 320 kb/s, faststart) and
   `cubrid-lab-intro-2026.webm` (VP9 CRF 31 + Opus 192 kb/s).
5. Copies the caption tracks from `captions/` (Korean primary, English secondary; not burned
   in, per the storyboard).
6. `scripts/contact-sheet.mjs` extracts one still per shot at its `review` frame from the MP4.
7. `scripts/loudness_report.py` writes `loudness.png` (master, music bus and narration bus
   short-term loudness with the duck envelope) and `loudness-report.md`.

`node scripts/review-stills.mjs Main out/review 0.5 [shotId …]` renders single shots straight
from the source for quick checks.

### Captions

`captions/cubrid-lab-intro-2026.{ko,en}.{srt,vtt}` are the narration tracks produced with the
voice lines (cue start = line start, 0.2 s after the shot). Korean: at most 2 lines of about
18 characters; English: at most 2 lines of 42 characters.

### Licenses

- Narration: MeloTTS (code MIT, `myshell-ai/MeloTTS-Korean` model MIT), run locally; disclosed
  on the end card and to be disclosed in the YouTube description.
- Music: original procedural score generated for CUBRID Lab, no third-party material;
  intended CC0 1.0 dedication **pending maintainer confirmation**.
- Fonts: Pretendard, Noto Sans KR, JetBrains Mono — SIL OFL 1.1.
- Brand marks: see [Brand assets](#brand-assets-and-open-permissions).
- Remotion: source-available, see [Remotion license](#remotion-license); the license governs
  use of the framework, not the rendered video.

## Brand assets and open permissions

Nothing from `cubrid-lab/brand` is copied here. The emblem, role icons, wordmark
lockups and numeric tokens (`tokens/geometry.json`, `tokens/colors.json`,
`tokens/organization.json`, `registry/repositories.json`) are loaded at render
time from commit-pinned URLs at revision
`3a385be773af94077c56548a24cdb9313bdc3b5c` (`src/brand.ts`).
`BrandCubeAssemble` rebuilds the three cube faces from the geometry tokens
(the same construction as `cube_polygons()` in the MIT-licensed
`scripts/build.py`) for the fly-in, then crossfades to the unmodified pinned
SVG; from `delay + assembleFrames + resolveFrames` on, only the pinned SVG is
visible.

Use of the marks in this video follows brand policy decision 5
([cubrid-lab/brand#47](https://github.com/cubrid-lab/brand/pull/47), merged as `1d9b374`): rendering, animating
and combining them in CUBRID Lab videos is allowed as long as every held frame of a finished
mark matches the approved SVG exactly; a cube assembly may show partial faces only while it
moves. The main cut does not use the face assembly at all: role icons and the lockup move only
as whole images (position, scale, opacity) and settle at scale 1, opacity 1, unrotated. The
emblem face colours appear only inside the unmodified lockup (`KeyWipe` replaces `CubeWipe` in
the main cut).

The end card always carries the AI-voice disclosure and the independence notice
(`src/components/EndCard.tsx`). Never place a lockup or icon next to an official
CUBRID logo.

## Remotion license

Remotion is source-available, not OSI open source. Its
[license](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md) is free
(including commercial use) for individuals, for-profit organizations with up to
3 employees, and non-profit / not-for-profit organizations; larger for-profit
companies need a paid Company License. CUBRID Lab, an independent,
maintainer-run open-source organization, falls under the free tier as long as
that remains true; re-check eligibility if a company funds or produces the video.
The MIT-licensed alternative is Motion Canvas; the components here would need porting.
