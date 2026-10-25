import React from 'react';
import {Img, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {cubePolygons, emblemUrl, iconUrl, pathData, useBrandTokens} from '../brand';

export type BrandCubeAssembleProps = {
	/** A repository key from the brand registry (e.g. "pycubrid"), or "organization" for the emblem. */
	repo: string;
	/** Rendered size in px of the 24x24 icon box. */
	size?: number;
	/** Frame (relative to this component) at which faces start flying in. */
	delay?: number;
	/** Frames from the first face moving to the cube being closed. */
	assembleFrames?: number;
	/** Crossfade length from the code-built faces to the pinned icon. */
	resolveFrames?: number;
};

const FACE_ORDER = ['top', 'left', 'right'] as const;
// Fly-in start offsets in 24-unit icon space, and start rotations in degrees.
const FROM: Record<(typeof FACE_ORDER)[number], {x: number; y: number; r: number}> = {
	top: {x: 0, y: -22, r: -35},
	left: {x: -24, y: 14, r: 25},
	right: {x: 24, y: 14, r: -25},
};

/**
 * Three cube faces, built in code from the pinned tokens/geometry.json, fly in
 * and lock together, then crossfade into the pinned role icon (or emblem),
 * which is loaded by URL. From `delay + assembleFrames + resolveFrames` on,
 * only the unmodified pinned SVG is visible.
 */
export const BrandCubeAssemble: React.FC<BrandCubeAssembleProps> = ({
	repo,
	size = 360,
	delay = 0,
	assembleFrames = 30,
	resolveFrames = 8,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const tokens = useBrandTokens();
	const isOrg = repo === 'organization';
	const src = isOrg ? emblemUrl : iconUrl(repo);

	const lockAt = delay + assembleFrames;
	const resolve = interpolate(frame, [lockAt, lockAt + resolveFrames], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const pulse = interpolate(frame, [lockAt - 2, lockAt + 4, lockAt + 18], [0, 1, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	let faces: React.ReactNode = null;
	if (tokens) {
		const polys = cubePolygons(tokens.geometry);
		const entry = tokens.registry[repo];
		const single = entry ? tokens.languages[entry.language] : tokens.languages.neutral;
		const colors = isOrg ? tokens.organizationFaces : {top: single, left: single, right: single};
		faces = FACE_ORDER.map((face, i) => {
			const p = spring({
				frame: frame - delay - i * 4,
				fps,
				durationInFrames: assembleFrames - 8,
				config: {damping: 14, stiffness: 120, mass: 0.8},
			});
			const f = FROM[face];
			const x = f.x * (1 - p);
			const y = f.y * (1 - p);
			const r = f.r * (1 - p);
			const d = pathData(polys[face]);
			return (
				<g key={face} transform={`translate(${x} ${y}) rotate(${r} 12 12)`} opacity={Math.min(1, p * 2)}>
					<path d={d} fill={colors[face]} />
					{/* Face shading as in build.py: top lightened 8%, left darkened 10%. */}
					{face === 'top' && !isOrg ? <path d={d} fill="#fff" opacity={0.08} /> : null}
					{face === 'left' && !isOrg ? <path d={d} fill="#000" opacity={0.1} /> : null}
				</g>
			);
		});
	}

	return (
		<div style={{position: 'relative', width: size, height: size}}>
			<div
				style={{
					position: 'absolute',
					inset: -size * 0.25,
					borderRadius: '50%',
					background: 'radial-gradient(circle, rgba(168,193,232,0.55) 0%, rgba(168,193,232,0) 60%)',
					opacity: pulse,
				}}
			/>
			<svg
				viewBox="0 0 24 24"
				width={size}
				height={size}
				style={{position: 'absolute', inset: 0, overflow: 'visible', opacity: 1 - resolve}}
			>
				{faces}
			</svg>
			<Img
				src={src}
				width={size}
				height={size}
				style={{position: 'absolute', inset: 0, opacity: resolve}}
				alt=""
			/>
		</div>
	);
};
