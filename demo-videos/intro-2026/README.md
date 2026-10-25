# Intro video 2026 — motion-graphics project

Code-based motion graphics for the ≤3-minute, ad-style introduction video of the
CUBRID Lab Python projects: **pycubrid**, **sqlalchemy-cubrid**,
**cubrid-mcp-server** (read-only by default) and **cubrid-cookbook-python**.
Main cut 1920×1080 at 30 fps, Korean TTS narration.

Built with [Remotion](https://www.remotion.dev). The storyboard, voice, music and
real screen captures are plugged in as data and media files; the components
stay unchanged.

> **Status: scaffold.** Every timeline here is a placeholder (`meta.draft: true`
> puts a red `DRAFT · PLACEHOLDER` badge on every frame). Read
> [Brand assets](#brand-assets-and-open-permissions) before publishing any render.

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

Fonts: Noto Sans KR (Hangul + Latin, weights 500/700/900) and JetBrains Mono,
both SIL OFL 1.1, loaded from Google Fonts at render time (`src/fonts.ts`).

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
    Transitions.tsx         CubeWipe (three org-colour 30° panels), FadeThrough
timelines/            main.json, short.json, demo.json
public/               footage/, voice/, music/ (gitignored media), subtitles/
scripts/              make-placeholders.mjs, render-stills.mjs, extract-stills.mjs
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

## Brand assets and open permissions

Nothing from `cubrid-lab/brand` is copied here. The emblem, role icons, wordmark
lockups and numeric tokens (`tokens/geometry.json`, `tokens/colors.json`,
`tokens/organization.json`, `registry/repositories.json`) are loaded at render
time from commit-pinned URLs at revision
`38b46469a1e18c7e9f7270f0b3d286ab45c3b376` (`src/brand.ts`).
`BrandCubeAssemble` rebuilds the three cube faces from the geometry tokens
(the same construction as `cube_polygons()` in the MIT-licensed
`scripts/build.py`) for the fly-in, then crossfades to the unmodified pinned
SVG; from `delay + assembleFrames + resolveFrames` on, only the pinned SVG is
visible.

**Before publishing a render, get a recorded maintainer decision in
[cubrid-lab/brand](https://github.com/cubrid-lab/brand/issues).** At the pinned
revision, `BRAND_USAGE.md` and `docs/ORGANIZATION_MARK_USAGE.md` permit the role
icons only in their own repository's README/docs site, the emblem only as
avatar, profile mark and website header/favicon, and the lockups only on CUBRID
Lab surfaces, all by pinned URL; they list rasterizing, modifying and using another
repository's icon as not permitted. A video necessarily rasterizes the assets,
shows four repositories' icons in a showcase video, and animates
derived (unresolved) cube frames. None of that is covered yet.

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
