import React, {useEffect, useState} from 'react';
import {AbsoluteFill, staticFile, useCurrentFrame, useDelayRender, useVideoConfig} from 'remotion';
import {SANS} from '../fonts';

export type Cue = {start: number; end: number; text: string};

const toSeconds = (stamp: string) => {
	const [hms, ms = '0'] = stamp.trim().replace(',', '.').split('.');
	const parts = hms.split(':').map(Number);
	while (parts.length < 3) {
		parts.unshift(0);
	}
	return parts[0] * 3600 + parts[1] * 60 + parts[2] + Number(`0.${ms}`);
};

/** Parses SubRip (.srt) and WebVTT (.vtt) into cues in seconds. Styling tags are stripped. */
export const parseSubtitles = (source: string): Cue[] => {
	const cues: Cue[] = [];
	const blocks = source.replace(/\r/g, '').replace(/^﻿/, '').split(/\n{2,}/);
	for (const block of blocks) {
		const lines = block.split('\n').filter((l) => l.trim() !== '');
		const timing = lines.findIndex((l) => l.includes('-->'));
		if (timing < 0) {
			continue;
		}
		const [a, b] = lines[timing].split('-->');
		cues.push({
			start: toSeconds(a),
			end: toSeconds(b.trim().split(/\s+/)[0]),
			text: lines
				.slice(timing + 1)
				.join('\n')
				.replace(/<[^>]+>/g, ''),
		});
	}
	return cues;
};

/** Burned-in subtitle track from a .srt/.vtt file under public/. */
export const SubtitleTrack: React.FC<{src: string}> = ({src}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const {delayRender, continueRender, cancelRender} = useDelayRender();
	const [cues, setCues] = useState<Cue[]>([]);
	const [handle] = useState(() => delayRender(`Loading subtitles ${src}`));

	useEffect(() => {
		fetch(staticFile(src))
			.then((r) => {
				if (!r.ok) {
					throw new Error(`subtitle file not found: ${src}`);
				}
				return r.text();
			})
			.then((text) => {
				setCues(parseSubtitles(text));
				continueRender(handle);
			})
			.catch((err) => cancelRender(err));
	}, [src, handle, continueRender, cancelRender]);

	const t = frame / fps;
	const cue = cues.find((c) => t >= c.start && t < c.end);
	if (!cue) {
		return null;
	}
	return (
		<AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 130}}>
			<div
				style={{
					maxWidth: 1500,
					padding: '10px 26px',
					borderRadius: 10,
					background: 'rgba(0,0,0,0.62)',
					color: '#fff',
					fontFamily: SANS,
					fontWeight: 700,
					fontSize: 44,
					lineHeight: 1.35,
					textAlign: 'center',
					whiteSpace: 'pre-line',
				}}
			>
				{cue.text}
			</div>
		</AbsoluteFill>
	);
};
