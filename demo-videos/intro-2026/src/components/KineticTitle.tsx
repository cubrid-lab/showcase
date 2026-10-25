import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {THEME} from '../brand';
import {SANS} from '../fonts';

export type TitleLine = {text: string; accent?: boolean; size?: number; weight?: 500 | 700 | 900};

export type KineticTitleProps = {
	kicker?: string;
	lines: TitleLine[];
	align?: 'left' | 'center';
	accentColor?: string;
	/** Frames between words. */
	stagger?: number;
	/** Shot length; the title clears during its last `exitFrames`. */
	shotDuration?: number;
	exitFrames?: number;
};

/** Bold ad-style title: each word rises out of a mask, accents get a sweep underline. */
export const KineticTitle: React.FC<KineticTitleProps> = ({
	kicker,
	lines,
	align = 'center',
	accentColor = THEME.python,
	stagger = 3,
	shotDuration,
	exitFrames = 8,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const exit =
		shotDuration === undefined
			? 0
			: interpolate(frame, [shotDuration - exitFrames, shotDuration], [0, 1], {
					extrapolateLeft: 'clamp',
					extrapolateRight: 'clamp',
				});
	let wordIndex = kicker ? 2 : 0;

	return (
		<div
			style={{
				fontFamily: SANS,
				color: THEME.text,
				textAlign: align,
				display: 'flex',
				flexDirection: 'column',
				alignItems: align === 'center' ? 'center' : 'flex-start',
				gap: 8,
				opacity: 1 - exit,
				transform: `translateY(${-40 * exit}px)`,
			}}
		>
			{kicker ? (
				<div
					style={{
						fontSize: 34,
						fontWeight: 700,
						letterSpacing: '0.18em',
						textTransform: 'uppercase',
						color: THEME.textMuted,
						opacity: interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'}),
						transform: `translateX(${interpolate(frame, [0, 12], [-30, 0], {extrapolateRight: 'clamp'})}px)`,
					}}
				>
					{kicker}
				</div>
			) : null}
			{lines.map((line, li) => {
				const words = line.text.split(' ');
				const lineStart = wordIndex * stagger;
				wordIndex += words.length;
				const underline = spring({frame: frame - lineStart - 8, fps, config: {damping: 200}});
				return (
					<div key={li} style={{position: 'relative', lineHeight: 1.12}}>
						{words.map((w, wi) => {
							const p = spring({
								frame: frame - lineStart - wi * stagger,
								fps,
								config: {damping: 16, stiffness: 160, mass: 0.7},
							});
							return (
								<span
									key={wi}
									style={{display: 'inline-block', overflow: 'hidden', verticalAlign: 'bottom', paddingBottom: 6}}
								>
									<span
										style={{
											display: 'inline-block',
											fontSize: line.size ?? 120,
											fontWeight: line.weight ?? 900,
											letterSpacing: '-0.02em',
											color: line.accent ? accentColor : THEME.text,
											transform: `translateY(${(1 - p) * 110}%) skewY(${(1 - p) * 6}deg)`,
										}}
									>
										{w}
										{wi < words.length - 1 ? ' ' : ''}
									</span>
								</span>
							);
						})}
						{line.accent ? (
							<div
								style={{
									position: 'absolute',
									left: align === 'center' ? '50%' : 0,
									bottom: -6,
									height: 10,
									width: `${underline * 100}%`,
									transform: align === 'center' ? 'translateX(-50%)' : undefined,
									background: accentColor,
									borderRadius: 5,
								}}
							/>
						) : null}
					</div>
				);
			})}
		</div>
	);
};
