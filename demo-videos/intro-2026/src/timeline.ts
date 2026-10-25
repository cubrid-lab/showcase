/**
 * Timeline schema. A storyboard is dropped in as timelines/<name>.json; the
 * composition length is the end of the last shot. All times are frames at
 * `meta.fps` (30). Media paths are relative to public/.
 */
export type Narration = {
	/** WAV under public/, e.g. "voice/s03.wav". */
	src: string;
	/** Frames after the shot start before the line begins. */
	offset?: number;
	volume?: number;
	/** Length of the line in frames, used for music ducking. Defaults to the rest of the shot. */
	durationInFrames?: number;
};

export type Transition = {type: 'cubeWipe' | 'fade'; duration: number};

export type Shot = {
	id: string;
	start: number;
	duration: number;
	type: string;
	props?: Record<string, unknown>;
	narration?: Narration;
	/** Played centred on this shot's start, covering the cut. */
	transitionIn?: Transition;
	lowerThird?: {title: string; subtitle?: string; from?: number; duration?: number; accent?: string};
};

export type Music = {
	src: string;
	volume?: number;
	/** Volume under narration. */
	duckedVolume?: number;
	/** Ramp length of each duck in frames. */
	rampFrames?: number;
	fadeInFrames?: number;
	fadeOutFrames?: number;
};

export type Timeline = {
	meta: {title: string; fps: number; width: number; height: number; draft?: boolean; note?: string};
	music?: Music;
	/** .srt or .vtt under public/. */
	subtitles?: string;
	shots: Shot[];
};

export const timelineDuration = (t: Timeline) =>
	Math.max(1, ...t.shots.map((s) => s.start + s.duration));

export const narrationWindows = (t: Timeline): Array<[number, number]> =>
	t.shots
		.filter((s) => s.narration)
		.map((s) => {
			const n = s.narration as Narration;
			const from = s.start + (n.offset ?? 0);
			return [from, from + (n.durationInFrames ?? s.duration - (n.offset ?? 0))];
		});

/** Music volume at a frame: ducked inside narration windows with linear ramps, faded at the ends. */
export const musicVolumeAt = (t: Timeline, frame: number): number => {
	const m = t.music;
	if (!m) {
		return 0;
	}
	const full = m.volume ?? 0.6;
	const ducked = m.duckedVolume ?? 0.15;
	const ramp = Math.max(1, m.rampFrames ?? 8);
	let duck = 0;
	for (const [from, to] of narrationWindows(t)) {
		const d = Math.min(1, Math.max(0, Math.min((frame - (from - ramp)) / ramp, (to + ramp - frame) / ramp)));
		duck = Math.max(duck, d);
	}
	const total = timelineDuration(t);
	const fadeIn = Math.min(1, frame / Math.max(1, m.fadeInFrames ?? 15));
	const fadeOut = Math.min(1, (total - frame) / Math.max(1, m.fadeOutFrames ?? 30));
	return (full + (ducked - full) * duck) * Math.max(0, Math.min(fadeIn, fadeOut));
};
