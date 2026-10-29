import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {THEME} from './brand';
import {SANS} from './fonts';
import {BrandCubeAssemble} from './components/BrandCubeAssemble';
import {DemoTitleShot} from './components/DemoCut';
import {EndCard, EndCardProps} from './components/EndCard';
import {KineticTitle, KineticTitleProps} from './components/KineticTitle';
import {BrowserMockup, MockupProps, TerminalMockup, WindowMockup} from './components/Mockups';
import {FeatureCallout, FeatureCalloutProps} from './components/Overlays';
import {
	BrandLockupShot,
	BrandTilesShot,
	ButtonShot,
	CardsShot,
	ChapterShot,
	ConfigShot,
	EndCardShot as IntroEndCardShot,
	FinaleShot,
	FlashShot,
	HitShot,
	HookShot,
	ProofShot,
} from './components/Intro';

type ShotComponent = React.FC<{props: Record<string, unknown>; duration: number}>;

const Backdrop: React.FC<{children: React.ReactNode; accent?: string}> = ({children, accent = THEME.orgTop}) => {
	const frame = useCurrentFrame();
	return (
		<AbsoluteFill style={{background: THEME.bg, overflow: 'hidden'}}>
			<AbsoluteFill
				style={{
					background: `radial-gradient(ellipse at ${30 + Math.sin(frame / 60) * 10}% 20%, ${accent}33 0%, transparent 55%), radial-gradient(ellipse at 80% 90%, ${THEME.orgRight}22 0%, transparent 50%)`,
				}}
			/>
			<AbsoluteFill
				style={{
					backgroundImage: 'linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)',
					backgroundSize: '80px 80px',
					transform: `translateY(${(frame * 0.6) % 80}px)`,
				}}
			/>
			{children}
		</AbsoluteFill>
	);
};

type CubeShot = {repo: string; size?: number; title?: string; subtitle?: string};

const CubeAssembleShot: ShotComponent = ({props}) => {
	const p = props as CubeShot;
	const frame = useCurrentFrame();
	const titleIn = interpolate(frame, [34, 46], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return (
		<Backdrop>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', gap: 36, fontFamily: SANS}}>
				<BrandCubeAssemble repo={p.repo} size={p.size ?? 320} />
				{p.title ? (
					<div style={{color: THEME.text, fontSize: 96, fontWeight: 900, opacity: titleIn, transform: `translateY(${(1 - titleIn) * 30}px)`}}>
						{p.title}
					</div>
				) : null}
				{p.subtitle ? (
					<div style={{color: THEME.textMuted, fontSize: 40, fontWeight: 500, opacity: titleIn}}>{p.subtitle}</div>
				) : null}
			</AbsoluteFill>
		</Backdrop>
	);
};

type IconRowShot = {repos: string[]; labels?: string[]; size?: number; stagger?: number};

const IconRowShot: ShotComponent = ({props}) => {
	const p = props as IconRowShot;
	const frame = useCurrentFrame();
	const stagger = p.stagger ?? 8;
	return (
		<Backdrop>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'row', gap: 90, fontFamily: SANS}}>
				{p.repos.map((repo, i) => {
					const labelIn = interpolate(frame, [i * stagger + 32, i * stagger + 42], [0, 1], {
						extrapolateLeft: 'clamp',
						extrapolateRight: 'clamp',
					});
					return (
						<div key={repo} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 28}}>
							<BrandCubeAssemble repo={repo} size={p.size ?? 220} delay={i * stagger} />
							<div style={{color: THEME.text, fontSize: 36, fontWeight: 700, opacity: labelIn}}>{p.labels?.[i] ?? repo}</div>
						</div>
					);
				})}
			</AbsoluteFill>
		</Backdrop>
	);
};

const TitleShot: ShotComponent = ({props, duration}) => (
	<Backdrop>
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', padding: 120}}>
			<KineticTitle {...(props as KineticTitleProps)} shotDuration={duration} />
		</AbsoluteFill>
	</Backdrop>
);

type MockupShot = MockupProps & {heading?: string; chips?: FeatureCalloutProps};

const mockupShot =
	(Frame: React.FC<MockupProps>): ShotComponent =>
	({props}) => {
		const p = props as MockupShot;
		return (
			<Backdrop>
				<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', gap: 30, paddingBottom: 190, paddingTop: 40, fontFamily: SANS}}>
					{p.heading ? <div style={{color: THEME.text, fontSize: 54, fontWeight: 900}}>{p.heading}</div> : null}
					<Frame {...p} width={p.width ?? (p.heading && p.chips ? 880 : p.heading || p.chips ? 1140 : 1440)} />
					{p.chips ? <FeatureCallout {...p.chips} /> : null}
				</AbsoluteFill>
			</Backdrop>
		);
	};

type FeaturesShot = FeatureCalloutProps & {heading?: KineticTitleProps};

const FeaturesShot: ShotComponent = ({props, duration}) => {
	const p = props as FeaturesShot;
	return (
		<Backdrop>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', gap: 70, padding: 120}}>
				{p.heading ? <KineticTitle {...p.heading} shotDuration={duration} /> : null}
				<FeatureCallout {...p} delay={p.delay ?? 12} />
			</AbsoluteFill>
		</Backdrop>
	);
};

const EndCardShot: ShotComponent = ({props}) => <EndCard {...(props as EndCardProps)} />;

/** Shot `type` → renderer. Add a type here and use it from any timeline. */
export const SHOT_TYPES: Record<string, ShotComponent> = {
	cubeAssemble: CubeAssembleShot,
	iconRow: IconRowShot,
	title: TitleShot,
	terminal: mockupShot(TerminalMockup),
	browser: mockupShot(BrowserMockup),
	window: mockupShot(WindowMockup),
	features: FeaturesShot,
	endCard: EndCardShot,
	// Main cut (components/Intro.tsx); props are passed through unchanged.
	hook: ({props}) => <HookShot {...(props as React.ComponentProps<typeof HookShot>)} />,
	flash: ({props}) => <FlashShot {...(props as React.ComponentProps<typeof FlashShot>)} />,
	brandTiles: ({props}) => <BrandTilesShot {...(props as React.ComponentProps<typeof BrandTilesShot>)} />,
	brandLockup: () => <BrandLockupShot />,
	chapter: ({props}) => <ChapterShot {...(props as React.ComponentProps<typeof ChapterShot>)} />,
	proof: ({props}) => <ProofShot {...(props as React.ComponentProps<typeof ProofShot>)} />,
	button: ({props}) => <ButtonShot {...(props as React.ComponentProps<typeof ButtonShot>)} />,
	hit: ({props}) => <HitShot {...(props as React.ComponentProps<typeof HitShot>)} />,
	config: ({props}) => <ConfigShot {...(props as React.ComponentProps<typeof ConfigShot>)} />,
	cards: ({props}) => <CardsShot {...(props as React.ComponentProps<typeof CardsShot>)} />,
	finale: ({props}) => <FinaleShot {...(props as React.ComponentProps<typeof FinaleShot>)} />,
	demoTitle: ({props}) => <DemoTitleShot {...(props as React.ComponentProps<typeof DemoTitleShot>)} />,
	introEndCard: ({props}) => <IntroEndCardShot {...(props as React.ComponentProps<typeof IntroEndCardShot>)} />,
};
