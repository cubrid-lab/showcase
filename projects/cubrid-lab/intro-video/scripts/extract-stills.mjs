#!/usr/bin/env node
// Extracts JPEG stills (1280 px wide) from a rendered video with ffmpeg:
//   node scripts/extract-stills.mjs <video> <outDir> [seconds ...]
// Without times, takes four evenly spaced stills.
import {execFileSync} from 'node:child_process';
import {mkdirSync} from 'node:fs';
import {basename, extname, join} from 'node:path';

const [input = 'out/demo.mp4', outDir = 'stills', ...times] = process.argv.slice(2);
const duration = Number(
	execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', input]).toString().trim(),
);
mkdirSync(outDir, {recursive: true});
const stem = basename(input, extname(input));
const at = times.length ? times.map(Number) : [0, 1, 2, 3].map((i) => ((i + 0.5) * duration) / 4);
for (const [i, t] of at.entries()) {
	const out = join(outDir, `${stem}-${String(i + 1).padStart(2, '0')}-${t.toFixed(1)}s.jpg`);
	execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-ss', t.toFixed(3), '-i', input, '-frames:v', '1', '-vf', 'scale=1280:-2', '-q:v', '4', out]);
	console.log(out);
}
