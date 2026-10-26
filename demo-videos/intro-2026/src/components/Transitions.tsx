import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {THEME} from '../brand';

/**
 * Cube wipe: three panels in the organization face colors, slanted along the
 * 30° isometric edge, sweep across and fully cover the frame at the midpoint,
 * so the cut underneath is hidden. Place it centred on the cut.
 */
export const CubeWipe: React.FC<{duration: number}> = ({duration}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const colors = [THEME.orgTop, THEME.orgLeft, THEME.orgRight];
	const slant = Math.tan(Math.PI / 6) * height; // 30° edge across the frame height
	const span = width + slant;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
				{colors.map((color, i) => {
					const lag = i * duration * 0.08;
					const t = interpolate(frame - lag, [0, duration * 0.5, duration * 0.84], [0, 1, 2], {
						extrapolateLeft: 'clamp',
						extrapolateRight: 'clamp',
						easing: Easing.inOut(Easing.cubic),
					});
					// Bands are described by their bottom-edge x range; the top edge is shifted by `slant`.
					// t 0→1: the leading edge sweeps across; t 1→2: the trailing edge follows it out.
					const x1 = t <= 1 ? -slant + t * span : width;
					const x0 = t <= 1 ? -slant : -slant + (t - 1) * span;
					const points = [
						[x0 + slant, 0],
						[x1 + slant, 0],
						[x1, height],
						[x0, height],
					]
						.map(([x, y]) => `${x},${y}`)
						.join(' ');
					return <polygon key={color} points={points} fill={color} />;
				})}
			</svg>
		</AbsoluteFill>
	);
};

export const FadeThrough: React.FC<{duration: number}> = ({duration}) => {
	const frame = useCurrentFrame();
	const o = interpolate(frame, [0, duration / 2, duration], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return <AbsoluteFill style={{background: THEME.bg, opacity: o}} />;
};

/**
 * Key wipe for the main cut: a dark panel with a Python Yellow leading edge,
 * slanted along the 30° isometric edge, covers the cut at its midpoint. Uses only
 * UI tokens (the emblem face colors stay inside the emblem, VIDEO_DESIGN.md 5.1).
 */
export const KeyWipe: React.FC<{duration: number}> = ({duration}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const slant = Math.tan(Math.PI / 6) * height;
	const span = width + slant;
	const bands: Array<[string, number]> = [
		[THEME.python, 0],
		['#161B22', 1.5],
	];
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
				{bands.map(([color, lag], i) => {
					const t = interpolate(frame - lag, [0, duration * 0.5, duration], [0, 1, 2], {
						extrapolateLeft: 'clamp',
						extrapolateRight: 'clamp',
						easing: Easing.bezier(0.2, 0.8, 0.2, 1),
					});
					const x1 = t <= 1 ? -slant + t * span : width;
					const x0 = t <= 1 ? -slant : -slant + (t - 1) * span - (i === 0 ? 0 : 0);
					const points = [
						[x0 + slant, 0],
						[x1 + slant, 0],
						[x1, height],
						[x0, height],
					]
						.map(([x, y]) => `${x},${y}`)
						.join(' ');
					return <polygon key={color} points={points} fill={color} />;
				})}
			</svg>
		</AbsoluteFill>
	);
};
