import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {THEME} from '../brand';
import {MONO, SANS} from '../fonts';
import {Footage, FootageProps, SpeedBadge, rateAt, sourceTimeAt} from './Footage';

type FrameStyle = 'window' | 'terminal' | 'browser';

export type MockupProps = {
	footage: FootageProps;
	title?: string;
	/** Browser only: text in the address bar. */
	url?: string;
	/** Width of the content area in px; height follows the footage aspect (16:9). */
	width?: number;
	/** Entrance tilt in degrees (ad-style 3D settle). 0 disables it. */
	tilt?: number;
	/** false: no entrance animation (a continuation of the previous shot). */
	enter?: boolean;
	/** Persistent labels in the title bar, e.g. "recorded session replay". */
	labels?: string[];
	/** Small provenance line under the window. */
	source?: string;
	/** Show the recording's own clock (m:ss) next to the speed badge, so cuts in a sped-up take stay visible. */
	clock?: boolean;
};

const Dots: React.FC = () => (
	<div style={{display: 'flex', gap: 10}}>
		{[0, 1, 2].map((c) => (
			<div key={c} style={{width: 14, height: 14, borderRadius: 7, background: '#3A414A'}} />
		))}
	</div>
);

const MockupFrame: React.FC<MockupProps & {kind: FrameStyle}> = ({
	kind,
	footage,
	title,
	url,
	width = 1440,
	tilt = 8,
	enter = true,
	labels = [],
	source,
	clock = false,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const p = enter ? spring({frame, fps, config: {damping: 200}, durationInFrames: 14}) : 1;
	const vp = footage.viewport ?? {x: 0, y: 0, w: 1, h: 1};
	const height = Math.round(width / (((footage.aspect ?? 16 / 9) * vp.w) / vp.h));
	const t = sourceTimeAt(footage, frame);
	const clockText = `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
	const rate = rateAt(footage, frame);

	return (
		<div style={{perspective: 2400}}>
			<div
				style={{
					width,
					borderRadius: 18,
					overflow: 'hidden',
					background: '#161B22',
					border: '1px solid #30363D',
					boxShadow: '0 40px 120px rgba(0,0,0,0.55)',
					transform: `translateY(${(1 - p) * 80}px) rotateX(${(1 - p) * tilt}deg) scale(${0.92 + 0.08 * p})`,
					opacity: interpolate(p, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'}),
				}}
			>
				<div
					style={{
						height: 52,
						display: 'flex',
						alignItems: 'center',
						gap: 18,
						padding: '0 20px',
						background: '#0F141A',
						borderBottom: '1px solid #30363D',
					}}
				>
					<Dots />
					{kind === 'browser' ? (
						<div
							style={{
								flex: 1,
								height: 32,
								borderRadius: 16,
								background: '#0D1117',
								color: '#8B949E',
								fontFamily: MONO,
								fontSize: 19,
								display: 'flex',
								alignItems: 'center',
								padding: '0 16px',
							}}
						>
							{url ?? 'https://'}
						</div>
					) : (
						<div style={{flex: 1, color: '#8B949E', fontFamily: MONO, fontWeight: 500, fontSize: 20, whiteSpace: 'nowrap'}}>{title}</div>
					)}
					{labels.map((l) => (
						<div
							key={l}
							style={{
								padding: '4px 14px',
								borderRadius: 999,
								border: '2px solid #8C7520',
								background: 'rgba(64,53,15,0.45)',
								color: THEME.python,
								fontFamily: SANS,
								fontWeight: 700,
								fontSize: 20,
								whiteSpace: 'nowrap',
							}}
						>
							{l}
						</div>
					))}
				</div>
				<div style={{position: 'relative', width, height}}>
					<Footage {...footage} />
					<div style={{position: 'absolute', top: 16, right: 16, display: 'flex', gap: 10, alignItems: 'center'}}>
						{clock ? (
							<div style={{padding: '4px 12px', borderRadius: 8, background: 'rgba(13,17,23,.85)', border: '1px solid #30363D', color: '#C9D1D9', fontFamily: MONO, fontSize: 22}}>
								rec {clockText}
							</div>
						) : null}
						<SpeedBadge rate={rate} />
					</div>
				</div>
			</div>
			{source ? (
				<div
					style={{
						marginTop: 10,
						textAlign: 'right',
						fontFamily: MONO,
						fontSize: 17,
						color: '#6E7681',
						opacity: interpolate(p, [0.5, 1], [0, 1]),
					}}
				>
					{source}
				</div>
			) : null}
		</div>
	);
};

export const WindowMockup: React.FC<MockupProps> = (p) => <MockupFrame kind="window" {...p} />;
export const TerminalMockup: React.FC<MockupProps> = (p) => <MockupFrame kind="terminal" {...p} />;
export const BrowserMockup: React.FC<MockupProps> = (p) => <MockupFrame kind="browser" {...p} />;
