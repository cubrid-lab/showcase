#!/usr/bin/env bash
# End-to-end production render of the main cut (see README "Production").
#
#   scripts/render-final.sh [assetsDir] [outDir]
#     assetsDir  footage/, mcp/, voice/, music/ (default: $INTRO_ASSETS or /data/video-intro-assets)
#     outDir     deliverables (default: <assetsDir>/out)
#   DRAFT=1      960x540 draft (scale 0.5, CRF 26) instead of the master; no WebM
#   CONCURRENCY  Remotion render concurrency (default 4)
#
# Steps: link media -> Remotion render (video only) -> narration/music mix + master to -14 LUFS /
# -1 dBTP -> mux MP4 (H.264 High + AAC 48 kHz 320k) -> WebM (VP9 + Opus) -> captions ->
# contact sheet -> loudness report.
set -euo pipefail
cd "$(dirname "$0")/.."

ASSETS=${1:-${INTRO_ASSETS:-/data/video-intro-assets}}
OUT=${2:-$ASSETS/out}
NAME=cubrid-lab-intro-2026
CONCURRENCY=${CONCURRENCY:-4}
mkdir -p "$OUT" out

node scripts/prepare-media.mjs "$ASSETS"
npx tsc --noEmit

if [[ "${DRAFT:-0}" == 1 ]]; then
	npx remotion render src/index.ts Main out/video-draft.mp4 --muted --scale=0.5 --crf=26 \
		--concurrency="$CONCURRENCY" --log=error
	python3 scripts/mix_audio.py --assets "$ASSETS" --out out/audio
	ffmpeg -nostdin -v error -y -i out/video-draft.mp4 -i out/audio/master.wav -map 0:v -map 1:a \
		-c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$OUT/$NAME-draft-540p.mp4"
	echo "draft: $OUT/$NAME-draft-540p.mp4"
	exit 0
fi

npx remotion render src/index.ts Main out/video-master.mp4 --muted --codec=h264 --crf=16 \
	--x264-preset=slow --pixel-format=yuv420p --concurrency="$CONCURRENCY" --log=error
python3 scripts/mix_audio.py --assets "$ASSETS" --out out/audio

ffmpeg -nostdin -v error -y -i out/video-master.mp4 -i out/audio/master.wav -map 0:v -map 1:a \
	-c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart "$OUT/$NAME.mp4"
ffmpeg -nostdin -v error -y -i out/video-master.mp4 -i out/audio/master.wav -map 0:v -map 1:a \
	-c:v libvpx-vp9 -crf 31 -b:v 0 -row-mt 1 -deadline good -cpu-used 2 -pix_fmt yuv420p \
	-c:a libopus -b:a 192k -ar 48000 -shortest "$OUT/$NAME.webm"

for lang in ko en; do
	for ext in srt vtt; do
		cp "captions/$NAME.$lang.$ext" "$OUT/"
	done
done

node scripts/contact-sheet.mjs "$OUT/$NAME.mp4" "$OUT/contact-sheet.png"
python3 scripts/loudness_report.py --audio out/audio --video "$OUT/$NAME.mp4" "$OUT/$NAME.webm"
cp out/audio/loudness.png out/audio/loudness-report.md "$OUT/"
for f in "$OUT/$NAME.mp4" "$OUT/$NAME.webm"; do
	ffprobe -v error -show_entries format=duration:stream=codec_name,profile,width,height,r_frame_rate,sample_rate,bit_rate \
		-of compact "$f"
done
