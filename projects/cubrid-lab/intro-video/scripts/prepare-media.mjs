#!/usr/bin/env node
// Links the production media into public/ (gitignored) so timelines/main.json can use them:
//   node scripts/prepare-media.mjs [assetsDir]      (default: $INTRO_ASSETS or /data/video-intro-assets)
//
// assetsDir layout (see README "Production"): footage/*.mp4, mcp/*.mp4, voice/<shot>.wav,
// music/bed.wav + music/stems/*.wav. Pretendard comes from presentation/public/fonts in this
// repository. Files are hard-linked when possible (same filesystem), otherwise copied.
// Every file the main timeline needs is checked; a missing one is an error.
import {copyFileSync, existsSync, linkSync, mkdirSync, readFileSync, rmSync} from 'node:fs';
import {dirname, join, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const assets = resolve(process.argv[2] ?? process.env.INTRO_ASSETS ?? '/data/video-intro-assets');

const place = (from, to) => {
	const dest = join(root, 'public', to);
	if (!existsSync(from)) {
		throw new Error(`missing media: ${from}`);
	}
	mkdirSync(dirname(dest), {recursive: true});
	rmSync(dest, {force: true});
	try {
		linkSync(from, dest);
	} catch {
		copyFileSync(from, dest);
	}
};

const footage = ['P2', 'P3', 'P4', 'S2', 'S3', 'S4', 'K2', 'K2-terminal', 'K3', 'H3-P2', 'H3-S3', 'H3-K2'];
for (const f of footage) {
	place(join(assets, 'footage', `${f}.mp4`), `footage/${f}.mp4`);
}
for (const f of ['C2', 'C3', 'C4', 'C4_script']) {
	place(join(assets, 'mcp', `${f}.mp4`), `footage/${f}.mp4`);
}
place(join(assets, 'music', 'bed.wav'), 'music/bed.wav');

const timeline = JSON.parse(readFileSync(join(root, 'timelines', 'main.json'), 'utf8'));
for (const shot of timeline.shots) {
	if (shot.narration) {
		place(join(assets, shot.narration.src), shot.narration.src);
	}
}
place(join(root, '..', '..', '..', 'presentation', 'public', 'fonts', 'PretendardVariable.woff2'), 'fonts/PretendardVariable.woff2');
console.log(`media linked from ${assets} into ${join(root, 'public')}`);
