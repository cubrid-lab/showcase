import React from 'react';
import {Easing, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {THEME} from '../brand';
import {SANS} from '../fonts';

/** Camera keyframe: at frame `at` (relative to the shot) zoom by `zoom` around normalized point (x, y). */
export type CameraKey = {at: number; zoom: number; x: number; y: number};

/** Highlight box in normalized footage coordinates (0..1), shown from `from` to `to`. */
export type Callout = {from: number; to: number; x: number; y: number; w: number; h: number; label?: string};

export type FootageProps = {
	/** MP4 under public/, e.g. "footage/pycubrid-terminal.mp4". */
	src: string;
	/** Source frames to skip at the start of the clip. */
	trimBefore?: number;
	playbackRate?: number;
	/** Footage audio is muted by default; the video's sound comes from narration and music. */
	muted?: boolean;
	camera?: CameraKey[];
	callouts?: Callout[];
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
					{easing: Easing.inOut(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
				);
	return {zoom: pick('zoom'), x: pick('x'), y: pick('y')};
};

/** Real footage with zoom/pan keyframes and callout highlights that follow the camera. */
export const Footage: React.FC<FootageProps> = ({src, trimBefore, playbackRate, muted = true, camera, callouts}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const cam = cameraAt(camera, frame);
	// Keep the focus point on screen: translate so (x, y) moves toward the centre as zoom grows.
	const tx = (0.5 - cam.x) * (cam.zoom - 1) * 100;
	const ty = (0.5 - cam.y) * (cam.zoom - 1) * 100;

	return (
		<div style={{position: 'absolute', inset: 0, overflow: 'hidden', background: '#000'}}>
			<div
				style={{
					position: 'absolute',
					inset: 0,
					transform: `translate(${tx}%, ${ty}%) scale(${cam.zoom})`,
					transformOrigin: '50% 50%',
				}}
			>
				<OffthreadVideo
					src={staticFile(src)}
					trimBefore={trimBefore}
					playbackRate={playbackRate}
					muted={muted}
					style={{width: '100%', height: '100%', objectFit: 'cover'}}
				/>
				{(callouts ?? []).map((c, i) => {
					if (frame < c.from || frame > c.to) {
						return null;
					}
					const inP = spring({frame: frame - c.from, fps, config: {damping: 200}, durationInFrames: 10});
					const out = interpolate(frame, [c.to - 6, c.to], [1, 0], {extrapolateLeft: 'clamp'});
					return (
						<React.Fragment key={i}>
						{/* Dim everything outside the box (an even-odd SVG path is far cheaper to rasterize than a huge box-shadow). */}
						<svg
							viewBox="0 0 1 1"
							preserveAspectRatio="none"
							style={{position: 'absolute', inset: 0, width: '100%', height: '100%'}}
						>
							<path
								fillRule="evenodd"
								fill="#0D1117"
								opacity={0.45 * inP * out}
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
								borderRadius: 10 / cam.zoom,
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
										fontWeight: 900,
										fontSize: 28 / cam.zoom,
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
	);
};
