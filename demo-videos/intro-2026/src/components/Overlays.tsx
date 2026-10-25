import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {THEME} from '../brand';
import {SANS} from '../fonts';

export type FeatureCalloutProps = {
	chips: string[];
	/** Frame of the first chip, relative to the shot. */
	delay?: number;
	stagger?: number;
	direction?: 'row' | 'column';
	accent?: string;
};

/** Pill chips that pop in one after another. */
export const FeatureCallout: React.FC<FeatureCalloutProps> = ({
	chips,
	delay = 0,
	stagger = 6,
	direction = 'row',
	accent = THEME.python,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return (
		<div style={{display: 'flex', flexDirection: direction, flexWrap: 'wrap', gap: 18, justifyContent: 'center'}}>
			{chips.map((chip, i) => {
				const p = spring({frame: frame - delay - i * stagger, fps, config: {damping: 12, stiffness: 180}});
				return (
					<div
						key={chip}
						style={{
							display: 'flex',
							alignItems: 'center',
							gap: 14,
							padding: '16px 30px',
							borderRadius: 999,
							background: 'rgba(22,27,34,0.92)',
							border: `2px solid ${accent}`,
							color: THEME.text,
							fontFamily: SANS,
							fontWeight: 700,
							fontSize: 36,
							transform: `scale(${p}) translateY(${(1 - p) * 30}px)`,
							opacity: Math.min(1, p * 1.5),
						}}
					>
						<div style={{width: 14, height: 14, borderRadius: 7, background: accent}} />
						{chip}
					</div>
				);
			})}
		</div>
	);
};

export type LowerThirdProps = {title: string; subtitle?: string; duration: number; accent?: string};

/** Name bar in the lower left: accent bar wipes in, text slides out of it. */
export const LowerThird: React.FC<LowerThirdProps> = ({title, subtitle, duration, accent = THEME.python}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const bar = spring({frame, fps, config: {damping: 200}, durationInFrames: 12});
	const text = spring({frame: frame - 6, fps, config: {damping: 200}, durationInFrames: 14});
	const out = interpolate(frame, [duration - 10, duration], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return (
		<div style={{position: 'absolute', left: 96, bottom: 250, display: 'flex', gap: 20, opacity: out, fontFamily: SANS}}>
			<div style={{width: 10, background: accent, borderRadius: 5, transform: `scaleY(${bar})`}} />
			<div style={{overflow: 'hidden'}}>
				<div style={{transform: `translateX(${(text - 1) * 105}%)`}}>
					<div style={{color: THEME.text, fontSize: 56, fontWeight: 900, lineHeight: 1.1}}>{title}</div>
					{subtitle ? (
						<div style={{color: THEME.textMuted, fontSize: 30, fontWeight: 500, marginTop: 6}}>{subtitle}</div>
					) : null}
				</div>
			</div>
		</div>
	);
};

/** Corner label shown while timeline.meta.draft is true, so placeholder renders are never mistaken for final cuts. */
export const DraftBadge: React.FC<{note?: string}> = ({note}) => (
	<div
		style={{
			position: 'absolute',
			top: 28,
			right: 32,
			padding: '8px 16px',
			background: '#E60039',
			color: '#fff',
			fontFamily: SANS,
			fontWeight: 900,
			fontSize: 22,
			letterSpacing: '0.08em',
			borderRadius: 6,
		}}
	>
		DRAFT · PLACEHOLDER{note ? ` · ${note}` : ''}
	</div>
);
