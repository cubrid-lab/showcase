#!/usr/bin/env node
// Generates PLACEHOLDER media under public/placeholder/ with ffmpeg so every
// timeline renders before real footage, narration and music exist. The files
// are gitignored and regenerated on demand; existing files are kept.
import {execFileSync} from 'node:child_process';
import {existsSync, mkdirSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..', 'public', 'placeholder');
const FONT = process.env.PLACEHOLDER_FONT ?? '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';

const ffmpeg = (args, out) => {
	const target = join(root, out);
	if (existsSync(target)) {
		return;
	}
	mkdirSync(dirname(target), {recursive: true});
	execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...args, target], {stdio: 'inherit'});
	console.log(`placeholder: ${out}`);
};

const text = (label, y, size) =>
	`drawtext=fontfile=${FONT}:text='${label}':fontcolor=white:fontsize=${size}:x=(w-text_w)/2:y=${y}:box=1:boxcolor=black@0.55:boxborderw=24`;

// Colored, moving test clips: 20 s, 1920x1080, 30 fps, labeled PLACEHOLDER with a running timecode.
const CLIPS = {
	terminal: '0x1F2430',
	browser: '0x123A6B',
	window: '0x0B5D44',
};
for (const [name, color] of Object.entries(CLIPS)) {
	ffmpeg(
		[
			'-f', 'lavfi', '-i', `color=c=${color}:s=1920x1080:r=30:d=20`,
			'-f', 'lavfi', '-i', 'testsrc2=s=640x360:r=30:d=20',
			'-filter_complex',
			'[1:v]format=yuva420p,colorchannelmixer=aa=0.5[t];' +
				`[0:v][t]overlay=x=(W-w)/2:y=(H-h)/2+120,` +
				[
					text(`PLACEHOLDER - ${name.toUpperCase()} FOOTAGE`, 220, 84),
					text('replace with real capture in public/footage', 340, 40),
					`drawtext=fontfile=${FONT}:text='%{pts\\:hms}':fontcolor=white:fontsize=48:x=60:y=h-110`,
				].join(','),
			'-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'veryfast', '-crf', '28', '-an',
		],
		`footage/${name}.mp4`,
	);
}

// Narration stand-ins: beeping tones (not speech), one per line slot.
for (const [i, freq] of [660, 740, 830, 880, 990, 1040].entries()) {
	ffmpeg(
		[
			'-f', 'lavfi', '-i', `sine=frequency=${freq}:sample_rate=48000:duration=3`,
			'-af', "volume='if(lt(mod(t,0.5),0.3),0.6,0)':eval=frame",
			'-ac', '2',
		],
		`voice/line-${i + 1}.wav`,
	);
}

// Music bed stand-in: a soft three-note pad, long enough for a 3-minute cut.
ffmpeg(
	[
		'-f', 'lavfi', '-i', 'sine=frequency=220:sample_rate=48000:duration=190',
		'-f', 'lavfi', '-i', 'sine=frequency=277.18:sample_rate=48000:duration=190',
		'-f', 'lavfi', '-i', 'sine=frequency=329.63:sample_rate=48000:duration=190',
		'-filter_complex', "amix=inputs=3,volume=2.5,tremolo=f=0.5:d=0.4",
		'-ac', '1', '-ar', '24000',
	],
	'music/bed.wav',
);
