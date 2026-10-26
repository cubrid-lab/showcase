import React from 'react';
import {Easing, Freeze, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {THEME} from '../brand';
import {MONO, SANS} from '../fonts';

/** Camera keyframe: at frame `at` (relative to the shot) zoom by `zoom` around normalized point (x, y). */
export type CameraKey = {at: number; zoom: number; x: number; y: number};

/** Highlight box in normalized footage coordinates (0..1), shown from `from` to `to`. */
export type Callout = {from: number; to: number; x: number; y: number; w: number; h: number; label?: string};

/**
 * One piece of a clip, played back to back with the others: source seconds `from`..`to` at
 * `rate`, or, with `hold`, the frame at `from` frozen for `hold` frames. Rates of 2 and above
 * get an on-screen "×N" badge (storyboard 5.4: speed-ups are labelled).
 */
export type Segment = {from: number; to?: number; rate?: number; hold?: number};

/** Normalized region of the footage that stays visible; everything else is cut away. */
export type Mask = {x: number; y: number; w: number; h: number};

export type FootageProps = {
	/** MP4 under public/, e.g. "footage/pycubrid-terminal.mp4". */
	src: string;
	/** Source frames to skip at the start of the clip (single-segment shorthand). */
	trimBefore?: number;
	playbackRate?: number;
	segments?: Segment[];
	/** Footage audio is muted by default; the video's sound comes from narration and music. */
	muted?: boolean;
	camera?: CameraKey[];
	callouts?: Callout[];
	mask?: Mask;
	/** Normalized part of the footage shown in the window (a crop); camera and callouts keep full-footage coordinates. */
	viewport?: Mask;
	/** Footage aspect ratio (width / height); 16:9 by default. */
	aspect?: number;
};

type Placed = {start: number; frames: number; seg: Segment};

const FPS = 30;

export const placeSegments = (p: FootageProps): Placed[] => {
	const segs: Segment[] = p.segments ?? [{from: (p.trimBefore ?? 0) / FPS, rate: p.playbackRate ?? 1}];
	let start = 0;
	return segs.map((seg) => {
		const frames =
			seg.hold !== undefined ? seg.hold : seg.to === undefined ? 100000 : Math.round(((seg.to - seg.from) * FPS) / (seg.rate ?? 1));
		const placed = {start, frames, seg};
		start += frames;
		return placed;
	});
};

/** Source time in seconds at a shot frame. */
export const sourceTimeAt = (p: FootageProps, frame: number) => {
	const segs = placeSegments(p);
	const hit = segs.find((s) => frame >= s.start && frame < s.start + s.frames) ?? segs[segs.length - 1];
	return hit.seg.hold !== undefined ? hit.seg.from : hit.seg.from + ((frame - hit.start) * (hit.seg.rate ?? 1)) / FPS;
};

/** Playback rate shown at a shot frame (1 when frozen). */
export const rateAt = (p: FootageProps, frame: number) => {
	const hit = placeSegments(p).find((s) => frame >= s.start && frame < s.start + s.frames);
	return hit && hit.seg.hold === undefined ? hit.seg.rate ?? 1 : 1;
};

/** The video itself, segment by segment, filling its parent. */
export const SegmentPlayer: React.FC<FootageProps> = (p) => {
	const style: React.CSSProperties = {width: '100%', height: '100%', objectFit: 'cover'};
	return (
		<>
			{placeSegments(p).map(({start, frames, seg}, i) => (
				<Sequence key={i} from={start} durationInFrames={frames} layout="none">
					{seg.hold !== undefined ? (
						<Freeze frame={0}>
							<OffthreadVideo src={staticFile(p.src)} trimBefore={Math.round(seg.from * FPS)} muted style={style} />
						</Freeze>
					) : (
						<OffthreadVideo
							src={staticFile(p.src)}
							trimBefore={Math.round(seg.from * FPS)}
							playbackRate={seg.rate ?? 1}
							muted={p.muted ?? true}
							style={style}
						/>
					)}
				</Sequence>
			))}
		</>
	);
};

const cameraAt = (keys: CameraKey[] | undefined, frame: number) => {
	if (!keys || keys.length === 0) {
		return {zoom: 1, x: 0.5, y: 0.5};
	}
	const sorted = [...keys].sort((a, b) => a.at - b.at);
	const pick = (k: 'zoom' | 'x' | 'y') =>
		sorted.length === 1
			? sorted[0][k]
			: interpolate(
					frame,
					sorted.map((s) => s.at),
					sorted.map((s) => s[k]),
					{easing: Easing.bezier(0.2, 0.8, 0.2, 1), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
				);
	return {zoom: pick('zoom'), x: pick('x'), y: pick('y')};
};

/** Real footage with zoom/pan keyframes and callout highlights that follow the camera. */
export const Footage: React.FC<FootageProps> = (props) => {
	const {camera, callouts, mask} = props;
	const vp = props.viewport ?? {x: 0, y: 0, w: 1, h: 1};
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const raw = cameraAt(camera, frame);
	const cam = {zoom: raw.zoom, x: (raw.x - vp.x) / vp.w, y: (raw.y - vp.y) / vp.h};
	// Zoom around (x, y) and keep the focus point centred, clamped so no empty edge shows.
	const clampT = (c: number) => Math.min(0.5 * (cam.zoom - 1), Math.max(-0.5 * (cam.zoom - 1), (0.5 - c) * cam.zoom));
	const tx = clampT(cam.x) * 100;
	const ty = clampT(cam.y) * 100;

	return (
		<div style={{position: 'absolute', inset: 0, overflow: 'hidden', background: THEME.bg}}>
			<div
				style={{
					position: 'absolute',
					inset: 0,
					transform: `translate(${tx}%, ${ty}%) scale(${cam.zoom})`,
					transformOrigin: '50% 50%',
				}}
			>
				<div
					style={{
						position: 'absolute',
						left: `${(-vp.x / vp.w) * 100}%`,
						top: `${(-vp.y / vp.h) * 100}%`,
						width: `${100 / vp.w}%`,
						height: `${100 / vp.h}%`,
					}}
				>
				<div
					style={{
						position: 'absolute',
						inset: 0,
						clipPath: mask
							? `inset(${mask.y * 100}% ${(1 - mask.x - mask.w) * 100}% ${(1 - mask.y - mask.h) * 100}% ${mask.x * 100}%)`
							: undefined,
					}}
				>
					<SegmentPlayer {...props} />
				</div>
				{(callouts ?? []).map((c, i) => {
					if (frame < c.from || frame > c.to) {
						return null;
					}
					const inP = spring({frame: frame - c.from, fps, config: {damping: 200}, durationInFrames: 10});
					const out = interpolate(frame, [c.to - 6, c.to], [1, 0], {extrapolateLeft: 'clamp'});
					return (
						<React.Fragment key={i}>
							{/* Dim everything outside the box (an even-odd SVG path is far cheaper to rasterize than a huge box-shadow). */}
							<svg viewBox="0 0 1 1" preserveAspectRatio="none" style={{position: 'absolute', inset: 0, width: '100%', height: '100%'}}>
								<path
									fillRule="evenodd"
									fill="#0D1117"
									opacity={0.5 * inP * out}
									d={`M0 0H1V1H0Z M${c.x} ${c.y}h${c.w}v${c.h}h${-c.w}Z`}
								/>
							</svg>
							<div
								style={{
									position: 'absolute',
									left: `${c.x * 100}%`,
									top: `${c.y * 100}%`,
									width: `${c.w * 100}%`,
									height: `${c.h * 100}%`,
									border: `${4 / cam.zoom}px solid ${THEME.python}`,
									borderRadius: 8 / cam.zoom,
									boxShadow: `0 0 0 ${8 / cam.zoom}px rgba(255,212,59,0.14)`,
									opacity: inP * out,
									transform: `scale(${1.08 - 0.08 * inP})`,
								}}
							>
								{c.label ? (
									<div
										style={{
											position: 'absolute',
											left: 0,
											top: '100%',
											marginTop: 10 / cam.zoom,
											padding: `${6 / cam.zoom}px ${14 / cam.zoom}px`,
											background: THEME.python,
											color: '#0D1117',
											fontFamily: SANS,
											fontWeight: 800,
											fontSize: 26 / cam.zoom,
											borderRadius: 8 / cam.zoom,
											whiteSpace: 'nowrap',
										}}
									>
										{c.label}
									</div>
								) : null}
							</div>
						</React.Fragment>
					);
				})}
				</div>
			</div>
		</div>
	);
};

/** "×N" badge for sped-up footage. */
export const SpeedBadge: React.FC<{rate: number}> = ({rate}) => {
	if (rate < 2) {
		return null;
	}
	const text = Number.isInteger(rate) ? String(rate) : rate.toFixed(1);
	return (
		<div
			style={{
				padding: '4px 14px',
				borderRadius: 8,
				background: THEME.python,
				color: '#0D1117',
				fontFamily: MONO,
				fontWeight: 700,
				fontSize: 24,
				lineHeight: 1.2,
			}}
		>
			×{text}
		</div>
	);
};
