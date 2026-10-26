#!/usr/bin/env node
// One still per shot from a rendered main cut, at the shot's `review` frame, tiled into a labelled
// contact sheet:
//   node scripts/contact-sheet.mjs <video> <out.png> [stillsDir]
// Stills are also kept (stillsDir, default: next to out.png in <name>-stills/).
import {execFileSync} from 'node:child_process';
import {mkdirSync, readFileSync} from 'node:fs';
import {basename, dirname, extname, join, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const [video, out, stillsArg] = process.argv.slice(2);
if (!video || !out) {
	throw new Error('usage: contact-sheet.mjs <video> <out.png> [stillsDir]');
}
const stills = stillsArg ?? join(dirname(out), `${basename(out, extname(out))}-stills`);
mkdirSync(stills, {recursive: true});
const {shots, meta} = JSON.parse(readFileSync(join(root, 'timelines', 'main.json'), 'utf8'));
const ff = (args) => execFileSync('ffmpeg', ['-nostdin', '-hide_banner', '-loglevel', 'error', '-y', ...args]);
const files = [];
for (const [i, shot] of shots.entries()) {
	const frame = shot.start + (shot.review ?? Math.floor(shot.duration / 2));
	const t = frame / meta.fps;
	const tc = `${Math.floor(t / 60)}:${(t % 60).toFixed(1).padStart(4, '0')}`;
	const file = join(stills, `${String(i + 1).padStart(2, '0')}-${shot.id}.png`);
	const label = `${shot.id}  ${tc}  (${shot.type})`.replace(/:/g, '\\:');
	ff([
		'-ss', t.toFixed(3), '-i', video, '-frames:v', '1',
		'-vf', `scale=640:360,pad=640:404:0:0:#0D1117,drawtext=text='${label}':x=12:y=372:fontsize=22:fontcolor=#F0F6FC`,
		file,
	]);
	files.push(file);
}
const cols = 4;
const rows = Math.ceil(files.length / cols);
const inputs = files.flatMap((f) => ['-i', f]);
const layout = files.map((_, i) => `${(i % cols) * 644}_${Math.floor(i / cols) * 408}`).join('|');
ff([
	...inputs,
	'-filter_complex',
	`${files.map((_, i) => `[${i}]`).join('')}xstack=inputs=${files.length}:layout=${layout}:fill=#0D1117,pad=${cols * 644}:${rows * 408}:0:0:#0D1117`,
	'-frames:v', '1', out,
]);
console.log(`${out} (${files.length} shots), stills in ${stills}`);
