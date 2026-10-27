import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {THEME, lockupUrl} from '../brand';
import {MONO, SANS} from '../fonts';

export const INDEPENDENCE_NOTICE =
	'CUBRID Lab은 독립적으로 운영되며 CUBRID Corporation 또는 공식 CUBRID 프로젝트와 제휴·후원·보증 관계가 없습니다. CUBRID는 해당 소유자의 상표입니다.';
export const AI_VOICE_DISCLOSURE = '이 영상의 한국어 내레이션은 AI 음성 합성(TTS)으로 제작되었습니다.';

export type EndCardProps = {
	theme?: 'dark' | 'light';
	lockup?: 'horizontal' | 'stacked';
	headline?: string;
	installs?: string[];
	links?: string[];
	aiVoiceDisclosure?: string;
	independenceNotice?: string;
};

/**
 * Closing card: the unmodified CUBRID Lab lockup (dark or light variant, by
 * pinned URL), install commands, links, and the AI-voice and independence notices.
 */
export const EndCard: React.FC<EndCardProps> = ({
	theme = 'dark',
	lockup = 'horizontal',
	headline,
	installs = [],
	links = [],
	aiVoiceDisclosure = AI_VOICE_DISCLOSURE,
	independenceNotice = INDEPENDENCE_NOTICE,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const dark = theme === 'dark';
	const fg = dark ? THEME.text : THEME.lightText;
	const muted = dark ? THEME.textMuted : THEME.lightMuted;
	const enter = (delay: number) => spring({frame: frame - delay, fps, config: {damping: 200}, durationInFrames: 16});
	const rise = (delay: number) => ({
		opacity: enter(delay),
		transform: `translateY(${(1 - enter(delay)) * 24}px)`,
	});

	return (
		<AbsoluteFill
			style={{
				background: dark ? THEME.bg : THEME.lightBg,
				alignItems: 'center',
				justifyContent: 'center',
				fontFamily: SANS,
				color: fg,
				gap: 40,
			}}
		>
			{/* Lockup shown unmodified: no recolor, crop or outline (ORGANIZATION_MARK_USAGE.md). */}
			<Img
				src={lockupUrl(lockup, theme)}
				style={{width: lockup === 'horizontal' ? 840 : 460, ...rise(0)}}
				alt="CUBRID Lab: Open Source for a More Connected World"
			/>
			{headline ? <div style={{fontSize: 56, fontWeight: 900, ...rise(6)}}>{headline}</div> : null}
			{installs.length ? (
				<div style={{display: 'flex', flexWrap: 'wrap', gap: 18, justifyContent: 'center', maxWidth: 1600, ...rise(10)}}>
					{installs.map((cmd) => (
						<div
							key={cmd}
							style={{
								fontFamily: MONO,
								fontSize: 30,
								fontWeight: 700,
								padding: '12px 24px',
								borderRadius: 10,
								background: dark ? THEME.bgRaised : '#F0F3F8',
								border: `1px solid ${dark ? '#30363D' : '#D0D7DE'}`,
							}}
						>
							<span style={{color: muted}}>$ </span>
							{cmd}
						</div>
					))}
				</div>
			) : null}
			{links.length ? (
				<div style={{display: 'flex', gap: 40, fontSize: 30, fontWeight: 700, color: muted, ...rise(14)}}>
					{links.map((l) => (
						<span key={l}>{l}</span>
					))}
				</div>
			) : null}
			<div
				style={{
					position: 'absolute',
					bottom: 40,
					left: 120,
					right: 120,
					textAlign: 'center',
					fontSize: 22,
					fontWeight: 500,
					lineHeight: 1.5,
					color: muted,
					opacity: interpolate(frame, [12, 24], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
				}}
			>
				<div>{aiVoiceDisclosure}</div>
				<div>{independenceNotice}</div>
			</div>
		</AbsoluteFill>
	);
};
