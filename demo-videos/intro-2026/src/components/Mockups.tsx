import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {THEME} from '../brand';
import {MONO, SANS} from '../fonts';
import {Footage, FootageProps} from './Footage';

type FrameStyle = 'window' | 'terminal' | 'browser';

export type MockupProps = {
	footage: FootageProps;
	title?: string;
	/** Browser only: text in the address bar. */
	url?: string;
	/** Width of the content area in px; height follows 16:9. */
	width?: number;
	/** Entrance tilt in degrees (ad-style 3D settle). 0 disables it. */
	tilt?: number;
};

const Dots: React.FC = () => (
	<div style={{display: 'flex', gap: 10}}>
		{['#FF5F57', '#FEBC2E', '#28C840'].map((c) => (
			<div key={c} style={{width: 16, height: 16, borderRadius: 8, background: c}} />
		))}
	</div>
);

const MockupFrame: React.FC<MockupProps & {kind: FrameStyle}> = ({kind, footage, title, url, width = 1440, tilt = 12}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const p = spring({frame, fps, config: {damping: 18, stiffness: 90}});
	const height = (width * 9) / 16;
	const dark = kind !== 'window';
	const barBg = kind === 'terminal' ? '#1F2430' : dark ? '#20262E' : '#E9EEF5';
	const barText = dark ? '#C9D1D9' : THEME.lightText;
	const float = Math.sin(frame / 40) * 4;

	return (
		<div style={{perspective: 2400}}>
			<div
				style={{
					width,
					borderRadius: 18,
					overflow: 'hidden',
					background: barBg,
					boxShadow: '0 50px 120px rgba(0,0,0,0.55), 0 0 0 1px rgba(255,255,255,0.08)',
					transform: `translateY(${(1 - p) * 140 + float}px) rotateX(${(1 - p) * tilt}deg) rotateY(${(1 - p) * -tilt}deg) scale(${0.86 + 0.14 * p})`,
					opacity: interpolate(p, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'}),
				}}
			>
				<div style={{height: 56, display: 'flex', alignItems: 'center', gap: 24, padding: '0 22px'}}>
					<Dots />
					{kind === 'browser' ? (
						<div
							style={{
								flex: 1,
								height: 34,
								borderRadius: 17,
								background: '#0D1117',
								color: '#8B949E',
								fontFamily: MONO,
								fontSize: 20,
								display: 'flex',
								alignItems: 'center',
								padding: '0 18px',
							}}
						>
							{url ?? 'https://'}
						</div>
					) : (
						<div
							style={{
								flex: 1,
								textAlign: 'center',
								marginRight: 80,
								color: barText,
								fontFamily: kind === 'terminal' ? MONO : SANS,
								fontWeight: 700,
								fontSize: 22,
							}}
						>
							{title}
						</div>
					)}
				</div>
				<div style={{position: 'relative', width, height}}>
					<Footage {...footage} />
				</div>
			</div>
		</div>
	);
};

export const WindowMockup: React.FC<MockupProps> = (p) => <MockupFrame kind="window" {...p} />;
export const TerminalMockup: React.FC<MockupProps> = (p) => <MockupFrame kind="terminal" {...p} />;
export const BrowserMockup: React.FC<MockupProps> = (p) => <MockupFrame kind="browser" {...p} />;
