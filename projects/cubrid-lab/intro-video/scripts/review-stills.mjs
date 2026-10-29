#!/usr/bin/env node
// Renders one still per shot of a composition straight from the source (one bundle, no encode):
//   node scripts/review-stills.mjs [Composition=Main] [outDir=out/review] [scale=0.5] [shotId ...]
// The frame is the shot's `review` frame (relative to the shot) or its midpoint.
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import {mkdirSync, readFileSync} from 'node:fs';
import {dirname, join, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const [comp = 'Main', outDir = 'out/review', scale = '0.5', ...only] = process.argv.slice(2);
const timeline = JSON.parse(readFileSync(join(root, 'timelines', `${process.env.TIMELINE ?? comp.toLowerCase()}.json`), 'utf8'));
mkdirSync(join(root, outDir), {recursive: true});

const serveUrl = await bundle({entryPoint: join(root, 'src', 'index.ts'), publicDir: join(root, 'public')});
const composition = await selectComposition({serveUrl, id: comp});
for (const shot of timeline.shots) {
	if (only.length && !only.includes(shot.id)) {
		continue;
	}
	const frame = shot.start + (shot.review ?? Math.floor(shot.duration / 2));
	const output = join(root, outDir, `${shot.id}-${frame}.png`);
	await renderStill({serveUrl, composition, frame, output, scale: Number(scale), timeoutInMilliseconds: 180000});
	console.log(output);
}
