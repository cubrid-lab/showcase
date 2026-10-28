/**
 * Shot renderers for the main cut of the CUBRID Lab introduction video
 * (VIDEO_DESIGN.md section 3, style frames in style-frames/). Colors and type
 * follow section 5.1; brand marks are the unmodified pinned SVGs, moved only
 * as whole images (position, scale, opacity) and always held at scale 1,
 * opacity 1, no rotation once they settle (brand policy decision 5,
 * cubrid-lab/brand#47).
 */
import React from 'react';
import {AbsoluteFill, Easing, Img, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {THEME, iconUrl} from '../brand';
import {MONO, SANS} from '../fonts';
import {FootageProps} from './Footage';
import {BrowserMockup, MockupProps, TerminalMockup, WindowMockup} from './Mockups';

export const C = {
	bg: THEME.bg,
	text: THEME.text,
	text2: THEME.textMuted,
	py: THEME.python,
	keyline: '#8C7520',
	ink: '#40350F',
	neutral: '#6B7280',
	panel: '#161B22',
	panelLine: '#30363D',
	dim: '#8B949E',
};

const EASE = Easing.bezier(0.2, 0.8, 0.2, 1);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const ease = (frame: number, from: number, len: number) => interpolate(frame, [from, from + len], [0, 1], {...clamp, easing: EASE});

// ---------------------------------------------------------------------------
// Backdrop: the isometric 60°/120° grid of the style frames, with a vignette.

export const IsoBackdrop: React.FC<{children?: React.ReactNode; reveal?: number; scale?: number; opacity?: number}> = ({
	children,
	reveal = 1,
	scale = 1,
	opacity = 0.16,
}) => {
	const r = reveal * 1400;
	return (
		<AbsoluteFill style={{background: C.bg, overflow: 'hidden'}}>
			<div
				style={{
					position: 'absolute',
					inset: -200,
					opacity,
					transform: `scale(${scale})`,
					backgroundImage: [
						`repeating-linear-gradient(30deg, transparent 0 63px, ${C.neutral} 63px 64px)`,
						`repeating-linear-gradient(150deg, transparent 0 63px, ${C.neutral} 63px 64px)`,
						'repeating-linear-gradient(90deg, transparent 0 109px, rgba(107,114,128,.5) 109px 110px)',
					].join(','),
					WebkitMaskImage: reveal >= 1 ? undefined : `radial-gradient(circle at 50% 50%, #000 ${r}px, transparent ${r + 120}px)`,
					maskImage: reveal >= 1 ? undefined : `radial-gradient(circle at 50% 50%, #000 ${r}px, transparent ${r + 120}px)`,
				}}
			/>
			<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(13,17,23,0) 30%, rgba(13,17,23,.92) 80%)'}} />
			{children}
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------------------
// Kinetic heading: words rise out of a mask, accents in Python Yellow, ochre underline wipe.

export type Part = {t: string; accent?: boolean; underline?: boolean; br?: boolean; color?: string};
export type HeadingProps = {kicker?: string; parts: Part[]; size?: number; still?: boolean; delay?: number; align?: 'left' | 'center'};

export const Heading: React.FC<HeadingProps> = ({kicker, parts, size = 92, still = false, delay = 0, align = 'left'}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const f = still ? 1000 : frame - delay;
	const lines: Part[][] = [[]];
	for (const p of parts) {
		if (p.br) {
			lines.push([]);
		} else {
			lines[lines.length - 1].push(p);
		}
	}
	let idx = 0;
	return (
		<div style={{fontFamily: SANS, textAlign: align, wordBreak: 'keep-all'}}>
			{kicker ? (
				<div
					style={{
						fontFamily: MONO,
						fontWeight: 700,
						fontSize: 26,
						letterSpacing: '0.14em',
						textTransform: 'uppercase',
						color: C.text2,
						opacity: ease(f, 0, 8),
						marginBottom: 18,
					}}
				>
					{kicker}
				</div>
			) : null}
			{lines.map((line, li) => (
				<div key={li} style={{fontSize: size, fontWeight: 800, lineHeight: 1.08, letterSpacing: '-0.03em', color: C.text}}>
					{line.map((p, pi) => {
						const i = idx++;
						const rise = spring({frame: f - 2 - i * 3, fps, config: {damping: 200}, durationInFrames: 12});
						const wipe = ease(f, 10 + i * 3, 12);
						return (
							<span key={pi} style={{display: 'inline-block', overflow: 'hidden', verticalAlign: 'bottom', paddingBottom: '0.08em'}}>
								<span
									style={{
										display: 'inline-block',
										whiteSpace: 'pre',
										transform: `translateY(${(1 - rise) * 105}%)`,
										color: p.color ?? (p.accent ? C.py : C.text),
										backgroundImage: p.underline ? `linear-gradient(${C.keyline}, ${C.keyline})` : undefined,
										backgroundRepeat: 'no-repeat',
										backgroundPosition: '0 92%',
										backgroundSize: p.underline ? `${wipe * 100}% 0.16em` : undefined,
									}}
								>
									{p.t}
								</span>
							</span>
						);
					})}
				</div>
			))}
		</div>
	);
};

// ---------------------------------------------------------------------------
// Brand marks: neutral isometric tile (generic primitive) and an unmodified pinned icon.

export const Tile: React.FC<{width: number; settle?: number}> = ({width, settle = 1}) => {
	const h = width * 0.5774;
	return (
		<svg
			width={width}
			height={h}
			viewBox={`0 0 ${width} ${h}`}
			style={{display: 'block', opacity: settle, transform: `translateY(${(1 - settle) * -40}px)`}}
		>
			<polygon
				points={`${width / 2},1 ${width - 1},${h / 2} ${width / 2},${h - 1} 1,${h / 2}`}
				fill={C.panel}
				stroke={C.neutral}
				strokeWidth={2}
			/>
		</svg>
	);
};

/** Pinned role icon. `p` (0..1) drives a whole-icon drop/scale-in; at p >= 1 it is the exact SVG. */
export const RoleIcon: React.FC<{repo: string; size: number; p?: number; from?: 'drop' | 'scale'}> = ({repo, size, p = 1, from = 'scale'}) => {
	const settled = p >= 0.999;
	const transform = settled
		? undefined
		: from === 'drop'
			? `translateY(${(1 - p) * -size * 0.6}px)`
			: `scale(${0.6 + 0.4 * p})`;
	return (
		<Img
			src={iconUrl(repo)}
			width={size}
			height={size}
			alt={`${repo} icon`}
			style={{display: 'block', transform, opacity: settled ? 1 : Math.min(1, p * 1.6)}}
		/>
	);
};

const settle = (frame: number, at: number, len = 12) => {
	const v = interpolate(frame, [at, at + len], [0, 1], {...clamp, easing: EASE});
	return v > 0.995 ? 1 : v;
};

/** Icon standing on its tile. */
const IconOnTile: React.FC<{repo: string; size: number; tileAt: number; iconAt: number; from?: 'drop' | 'scale'}> = ({
	repo,
	size,
	tileAt,
	iconAt,
	from = 'scale',
}) => {
	const frame = useCurrentFrame();
	const tile = settle(frame, tileAt, 10);
	const icon = settle(frame, iconAt, 12);
	return (
		<div style={{position: 'relative', width: size * 1.25, height: size * 1.1, display: 'flex', justifyContent: 'center'}}>
			<div style={{position: 'absolute', bottom: 0}}>
				<Tile width={size * 1.25} settle={tile} />
			</div>
			<div style={{position: 'absolute', bottom: size * 0.2, opacity: icon > 0 ? 1 : 0}}>
				<RoleIcon repo={repo} size={size} p={icon} from={from} />
			</div>
		</div>
	);
};

// ---------------------------------------------------------------------------
// H1/H2 hook

export const HookShot: React.FC<{stage: 1 | 2}> = ({stage}) => {
	const frame = useCurrentFrame();
	const reveal = stage === 1 ? ease(frame, 0, 24) : 1;
	// Hook type only: 4-frame overshoot.
	const slam = (at: number) =>
		interpolate(frame, [at, at + 4, at + 8], [1.18, 0.97, 1], {...clamp, easing: Easing.out(Easing.cubic)});
	const line1Scale = stage === 1 ? slam(2) : 1;
	const line1Op = stage === 1 ? ease(frame, 2, 3) : 1;
	const drop = interpolate(frame, [2, 6, 10], [-120, 10, 0], {...clamp, easing: Easing.out(Easing.cubic)});
	const line2Op = ease(frame, 2, 3);
	const wipe = ease(frame, 10, 14);
	return (
		<IsoBackdrop reveal={reveal}>
			<div style={{position: 'absolute', inset: '54px 96px', display: 'flex', flexDirection: 'column', justifyContent: 'center', fontFamily: SANS}}>
				<div
					style={{
						fontWeight: 900,
						fontSize: 200,
						lineHeight: 0.98,
						letterSpacing: '-0.035em',
						color: C.dim,
						transform: `scale(${line1Scale})`,
						transformOrigin: 'left center',
						opacity: line1Op,
					}}
				>
					CUBRID를,
				</div>
				{stage === 2 ? (
					<div
						style={{
							fontWeight: 900,
							fontSize: 200,
							lineHeight: 0.98,
							letterSpacing: '-0.035em',
							color: C.text,
							transform: `translateY(${drop}px)`,
							opacity: line2Op,
						}}
					>
						<span
							style={{
								color: C.py,
								backgroundImage: `linear-gradient(${C.keyline}, ${C.keyline})`,
								backgroundRepeat: 'no-repeat',
								backgroundPosition: '0 92%',
								backgroundSize: `${wipe * 100}% 0.16em`,
							}}
						>
							Python
						</span>
						으로.
					</div>
				) : null}
			</div>
		</IsoBackdrop>
	);
};

// ---------------------------------------------------------------------------
// H3: four 0.5 s flash cuts of real footage

export type Flash = {footage: FootageProps; kind?: 'terminal' | 'browser'; url?: string; title?: string};

export const FlashShot: React.FC<{flashes: Flash[]; each?: number}> = ({flashes, each = 15}) => {
	const frame = useCurrentFrame();
	const i = Math.min(flashes.length - 1, Math.floor(frame / each));
	const fl = flashes[i];
	const Frame = fl.kind === 'browser' ? BrowserMockup : TerminalMockup;
	return (
		<IsoBackdrop>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingBottom: 60}}>
				{/* Offset the footage clock so every flash starts at its own segment. */}
				<ShiftedFrame by={i * each}>
					<Frame footage={fl.footage} title={fl.title} url={fl.url} width={1400} enter={false} />
				</ShiftedFrame>
			</AbsoluteFill>
		</IsoBackdrop>
	);
};

const ShiftedFrame: React.FC<{by: number; children: React.ReactNode}> = ({by, children}) => (
	<Sequence from={by} layout="none">
		{children}
	</Sequence>
);

// ---------------------------------------------------------------------------
// B1: four tiles settle on beats, icons scale in, labels type on

const ROLES: Array<[string, string]> = [
	['pycubrid', '드라이버'],
	['sqlalchemy-cubrid', 'ORM'],
	['cubrid-mcp-server', 'AI · MCP'],
	['cubrid-cookbook-python', '예제'],
];

const typeOn = (text: string, frame: number, at: number, perChar = 1.2) =>
	text.slice(0, Math.max(0, Math.floor((frame - at) / perChar)));

export const BrandTilesShot: React.FC<{beat?: number}> = ({beat = 15}) => {
	const frame = useCurrentFrame();
	return (
		<IsoBackdrop>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 56, fontFamily: SANS}}>
				<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: '0.14em', color: C.text2, opacity: ease(frame, 0, 10)}}>
					파이큐브리드팀 · PYTHON STACK
				</div>
				<div style={{display: 'flex', gap: 72, alignItems: 'flex-start'}}>
					{ROLES.map(([repo, label], i) => (
						<div key={repo} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 26, width: 300}}>
							<IconOnTile repo={repo} size={220} tileAt={i * beat} iconAt={i * beat + 4} />
							<div style={{fontSize: 52, fontWeight: 800, letterSpacing: '-0.02em', color: C.text, minHeight: 60}}>
								{typeOn(label, frame, i * beat + 10, 2)}
							</div>
							<div style={{fontFamily: MONO, fontSize: 24, color: C.text2, minHeight: 30}}>{typeOn(repo, frame, i * beat + 12, 0.6)}</div>
						</div>
					))}
				</div>
			</AbsoluteFill>
		</IsoBackdrop>
	);
};

// ---------------------------------------------------------------------------
// B2: icons slide up into a row, lockup fades in, MIT chip pops

export const BrandLockupShot: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const move = ease(frame, 0, 18);
	const moved = move >= 0.999;
	const size = interpolate(move, [0, 1], [220, 120]);
	const lockIn = ease(frame, 14, 16);
	const chip = spring({frame: frame - 34, fps, config: {damping: 12, stiffness: 180}});
	const copyIn = ease(frame, 24, 12);
	return (
		<IsoBackdrop>
			<AbsoluteFill style={{alignItems: 'center', fontFamily: SANS}}>
				<div
					style={{
						position: 'absolute',
						top: interpolate(move, [0, 1], [345, 110]),
						display: 'flex',
						gap: interpolate(move, [0, 1], [152, 64]),
					}}
				>
					{ROLES.map(([repo]) => (
						<div key={repo} style={{width: moved ? 120 : size, height: moved ? 120 : size}}>
							{/* Whole-icon scale while moving; exactly 120 px once settled. */}
							<Img src={iconUrl(repo)} width={moved ? 120 : size} height={moved ? 120 : size} alt={`${repo} icon`} />
						</div>
					))}
				</div>
				<div style={{position: 'absolute', top: 400, opacity: lockIn >= 0.999 ? 1 : lockIn, fontSize: 120, fontWeight: 900, letterSpacing: '-0.04em', color: C.text}}>
					파이큐브리드팀
				</div>
				<div style={{position: 'absolute', top: 650, display: 'flex', alignItems: 'center', gap: 28}}>
					<div style={{fontSize: 52, fontWeight: 800, letterSpacing: '-0.02em', color: C.text, opacity: copyIn, transform: `translateY(${(1 - copyIn) * 20}px)`}}>
						Python 개발자를 위한 CUBRID 오픈소스
					</div>
					<div
						style={{
							border: `3px solid ${C.keyline}`,
							color: C.py,
							background: 'rgba(64,53,15,.45)',
							borderRadius: 999,
							padding: '10px 30px',
							fontWeight: 800,
							fontSize: 44,
							transform: `scale(${chip})`,
							opacity: Math.min(1, chip * 1.5),
						}}
					>
						MIT
					</div>
				</div>
			</AbsoluteFill>
		</IsoBackdrop>
	);
};

// ---------------------------------------------------------------------------
// Chapter cards P1/S1/C1/K1

export const ChapterShot: React.FC<{repo: string; kicker: string; name: string; tagline?: string}> = ({repo, kicker, name, tagline}) => {
	const frame = useCurrentFrame();
	const nameSize = Math.min(180, Math.floor(1180 / (0.56 * name.length)));
	const textIn = ease(frame, 6, 12);
	return (
		<IsoBackdrop>
			<div style={{position: 'absolute', inset: '54px 96px', display: 'flex', alignItems: 'center', gap: 70, fontFamily: SANS}}>
				<IconOnTile repo={repo} size={380} tileAt={0} iconAt={3} from="drop" />
				<div style={{opacity: textIn, transform: `translateX(${(1 - textIn) * 40}px)`}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: '0.14em', textTransform: 'uppercase', color: C.text2}}>
						{kicker}
					</div>
					<div style={{fontWeight: 900, fontSize: nameSize, lineHeight: 1, letterSpacing: '-0.035em', color: C.text, marginTop: 22, whiteSpace: 'nowrap'}}>
						{name}
					</div>
					{tagline ? <div style={{fontWeight: 500, fontSize: 34, color: C.text2, marginTop: 22}}>{tagline}</div> : null}
				</div>
			</div>
		</IsoBackdrop>
	);
};

// ---------------------------------------------------------------------------
// Proof shots: kinetic heading, real footage in a mockup, chips and cards on beats

type Chips = {items: string[]; at: number[]};
type SideCard = {at: number; kicker: string; text: string};

export type ProofProps = {
	heading: HeadingProps;
	kind?: 'terminal' | 'browser' | 'window';
	mockup: MockupProps;
	/** Window position: left-aligned (default) or centred. */
	align?: 'left' | 'center';
	chips?: Chips;
	cards?: SideCard[];
	/** Frame the window enters (0.3–0.5 s after the benefit line). */
	windowAt?: number;
};

export const ProofShot: React.FC<ProofProps> = ({heading, kind = 'terminal', mockup, align = 'left', chips, cards, windowAt = 12}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const Frame = kind === 'browser' ? BrowserMockup : kind === 'window' ? WindowMockup : TerminalMockup;
	const width = mockup.width ?? 1152;
	const left = align === 'center' ? (1920 - width) / 2 : 96;
	return (
		<IsoBackdrop>
			<div style={{position: 'absolute', left: 96, top: 54, right: 96}}>
				<Heading size={84} {...heading} />
			</div>
			<div style={{position: 'absolute', left, top: 220}}>
				<Sequence from={mockup.enter === false ? 0 : windowAt} layout="none">
					<Frame {...mockup} />
				</Sequence>
			</div>
			{chips ? (
				<div style={{position: 'absolute', right: 96, top: 300, display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 22}}>
					{chips.items.map((c, i) => {
						const p = spring({frame: frame - chips.at[i], fps, config: {damping: 12, stiffness: 180}});
						return (
							<div
								key={c}
								style={{
									border: `2px solid ${C.keyline}`,
									color: C.py,
									background: 'rgba(30,26,10,.92)',
									borderRadius: 999,
									padding: '14px 32px',
									fontFamily: SANS,
									fontWeight: 700,
									fontSize: 40,
									transform: `scale(${p})`,
									opacity: Math.min(1, p * 1.5),
									boxShadow: '0 20px 50px rgba(0,0,0,.5)',
								}}
							>
								{c}
							</div>
						);
					})}
				</div>
			) : null}
			{(cards ?? []).map((card, i) => {
				const p = spring({frame: frame - card.at, fps, config: {damping: 200}, durationInFrames: 12});
				return (
					<div
						key={i}
						style={{
							position: 'absolute',
							left: 96,
							top: 790,
							border: `4px solid ${C.py}`,
							borderRadius: 16,
							background: '#0B0F14',
							boxShadow: '0 0 0 10px rgba(255,212,59,.12), 0 30px 80px rgba(0,0,0,.6)',
							padding: '14px 28px',
							opacity: p,
							transform: `translateY(${(1 - p) * 20}px)`,
						}}
					>
						<div style={{fontFamily: SANS, fontWeight: 700, fontSize: 20, letterSpacing: '0.1em', color: C.py, marginBottom: 4}}>{card.kicker}</div>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 40, color: C.text}}>{card.text}</div>
					</div>
				);
			})}
		</IsoBackdrop>
	);
};

// ---------------------------------------------------------------------------
// P5 button-out

export const ButtonShot: React.FC<{repo: string; heading: HeadingProps; command: string}> = ({repo, heading, command}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const recede = ease(frame, 18, 20);
	const done = recede >= 0.999;
	const size = done ? 150 : interpolate(recede, [0, 1], [360, 150]);
	const card = spring({frame: frame - 24, fps, config: {damping: 14, stiffness: 160}});
	return (
		<IsoBackdrop>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 70}}>
				<Heading {...heading} size={112} align="center" />
				<div style={{display: 'flex', alignItems: 'center', gap: 44, height: 360}}>
					<Img src={iconUrl(repo)} width={size} height={size} alt={`${repo} icon`} />
					<div
						style={{
							border: `4px solid ${C.py}`,
							borderRadius: 20,
							background: '#0B0F14',
							boxShadow: '0 0 0 12px rgba(255,212,59,.12), 0 30px 80px rgba(0,0,0,.6)',
							padding: '26px 48px',
							fontFamily: MONO,
							fontWeight: 700,
							fontSize: 64,
							color: C.text,
							transform: `scale(${card})`,
							opacity: Math.min(1, card * 1.5),
						}}
					>
						<span style={{color: C.py}}>$ </span>
						{command}
					</div>
				</div>
			</AbsoluteFill>
		</IsoBackdrop>
	);
};

// ---------------------------------------------------------------------------
// S5 hit: the ORM icon moves (whole icon) to the next tile

export const HitShot: React.FC<{repo: string; heading: HeadingProps}> = ({repo, heading}) => {
	const frame = useCurrentFrame();
	const t = ease(frame, 30, 18);
	const done = t >= 0.999;
	const dx = 520;
	const x = -dx / 2 + dx * t;
	const y = -Math.sin(Math.PI * t) * 160;
	return (
		<IsoBackdrop>
			<div style={{position: 'absolute', left: 96, right: 96, top: 120}}>
				<Heading {...heading} size={120} align="center" />
			</div>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingTop: 260}}>
				<div style={{position: 'relative', width: 900, height: 360}}>
					{[-dx / 2, dx / 2].map((tx) => (
						<div key={tx} style={{position: 'absolute', left: 450 + tx - 150, bottom: 0}}>
							<Tile width={300} />
						</div>
					))}
					<div
						style={{
							position: 'absolute',
							left: 450 - 120 + (done ? dx / 2 : x),
							bottom: 40,
							transform: done ? undefined : `translateY(${y}px)`,
						}}
					>
						<Img src={iconUrl(repo)} width={240} height={240} alt={`${repo} icon`} />
					</div>
				</div>
			</AbsoluteFill>
		</IsoBackdrop>
	);
};

// ---------------------------------------------------------------------------
// C5 config card: README configuration table and write-mode text (cubrid-mcp-server v0.6.0)

export type ConfigRow = {name: string; def: string; desc: string; highlight?: boolean};
export const ConfigShot: React.FC<{
	heading: HeadingProps;
	rows: ConfigRow[];
	rowAt: number[];
	tools: string[];
	toolsAt: number;
	writeAt: number;
	writeNote: string;
	offNote: string;
	source: string;
}> = ({heading, rows, rowAt, tools, toolsAt, writeAt, writeNote, offNote, source}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const toolsIn = ease(frame, toolsAt, 12);
	const write = spring({frame: frame - writeAt, fps, config: {damping: 14, stiffness: 160}});
	const on = frame >= writeAt;
	return (
		<IsoBackdrop>
			<div style={{position: 'absolute', left: 96, top: 54, right: 96}}>
				<Heading size={84} {...heading} />
			</div>
			<div
				style={{
					position: 'absolute',
					left: 96,
					top: 250,
					width: 1060,
					background: C.panel,
					border: `1px solid ${C.panelLine}`,
					borderRadius: 18,
					overflow: 'hidden',
					fontFamily: SANS,
				}}
			>
				<div style={{display: 'flex', padding: '16px 28px', background: '#0F141A', borderBottom: `1px solid ${C.panelLine}`, color: C.dim, fontWeight: 700, fontSize: 24}}>
					<div style={{width: 470}}>Variable</div>
					<div style={{width: 120}}>Default</div>
					<div>Description</div>
				</div>
				{rows.map((r, i) => {
					const p = ease(frame, rowAt[i], 10);
					const value = r.highlight && on ? '1' : r.def;
					return (
						<div
							key={r.name}
							style={{
								display: 'flex',
								alignItems: 'baseline',
								padding: '20px 28px',
								borderBottom: `1px solid ${C.panelLine}`,
								opacity: p,
								transform: `translateX(${(1 - p) * -30}px)`,
								background: r.highlight ? 'rgba(255,212,59,.08)' : undefined,
								boxShadow: r.highlight ? `inset 6px 0 0 ${C.py}` : undefined,
							}}
						>
							<div style={{width: 470, fontFamily: MONO, fontWeight: 700, fontSize: 30, color: r.highlight ? C.py : C.text}}>{r.name}</div>
							<div style={{width: 120, fontFamily: MONO, fontWeight: 700, fontSize: 30, color: C.text}}>
								{r.highlight ? (
									<span style={{display: 'inline-block', padding: '0 12px', borderRadius: 8, background: on ? C.py : 'transparent', color: on ? '#0D1117' : C.text}}>
										{value}
									</span>
								) : (
									value
								)}
							</div>
							<div style={{flex: 1, fontSize: 26, lineHeight: 1.35, color: C.text2}}>{r.desc}</div>
						</div>
					);
				})}
				<div style={{padding: '14px 28px', fontFamily: MONO, fontSize: 17, color: '#6E7681'}}>{source}</div>
			</div>
			<div
				style={{
					position: 'absolute',
					left: 1200,
					top: 250,
					width: 624,
					background: C.panel,
					border: `1px solid ${C.panelLine}`,
					borderRadius: 18,
					padding: '22px 28px',
					opacity: toolsIn,
					transform: `translateY(${(1 - toolsIn) * 30}px)`,
				}}
			>
				<div style={{fontFamily: SANS, fontWeight: 700, fontSize: 22, letterSpacing: '0.1em', color: C.dim, marginBottom: 14}}>MCP TOOLS</div>
				{tools.map((t) => (
					<div key={t} style={{fontFamily: MONO, fontSize: 28, lineHeight: 1.6, color: C.text}}>
						{t}
					</div>
				))}
				<div
					style={{
						marginTop: 10,
						fontFamily: MONO,
						fontSize: 28,
						lineHeight: 1.6,
						fontWeight: 700,
						color: on ? '#0D1117' : C.dim,
						background: on ? C.py : 'transparent',
						border: on ? 'none' : `2px dashed ${C.neutral}`,
						borderRadius: 8,
						padding: '4px 12px',
						transform: on ? `scale(${0.9 + 0.1 * write})` : undefined,
					}}
				>
					execute_write
				</div>
				<div style={{marginTop: 12, fontFamily: SANS, fontSize: 24, lineHeight: 1.4, color: on ? C.py : C.text2, fontWeight: 600}}>{on ? writeNote : offNote}</div>
			</div>
		</IsoBackdrop>
	);
};

// ---------------------------------------------------------------------------
// K3: real directory names as cards on beats, over the recorded tree page

export const CardsShot: React.FC<{
	heading: HeadingProps;
	cards: Array<{label: string; path: string}>;
	at: number;
	beat: number;
	mockup: MockupProps;
	note: string;
}> = ({heading, cards, at, beat, mockup, note}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const dim = ease(frame, at - 6, 10);
	return (
		<IsoBackdrop>
			<div style={{position: 'absolute', left: 96, top: 54, right: 96}}>
				<Heading size={84} {...heading} />
			</div>
			<div style={{position: 'absolute', left: (1920 - (mockup.width ?? 1152)) / 2, top: 220, opacity: 1 - 0.75 * dim}}>
				<BrowserMockup {...mockup} />
			</div>
			<div style={{position: 'absolute', left: 96, right: 96, top: 300, display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 26}}>
				{cards.map((c, i) => {
					const p = spring({frame: frame - at - i * beat, fps, config: {damping: 13, stiffness: 170}});
					return (
						<div
							key={c.path}
							style={{
								border: `1px solid ${C.panelLine}`,
								background: C.panel,
								borderRadius: 16,
								padding: '30px 28px',
								transform: `scale(${p})`,
								opacity: Math.min(1, p * 1.5),
								boxShadow: '0 30px 70px rgba(0,0,0,.55)',
							}}
						>
							<div style={{fontFamily: SANS, fontWeight: 800, fontSize: 40, lineHeight: 1.2, color: C.text}}>{c.label}</div>
							<div style={{fontFamily: MONO, fontWeight: 500, fontSize: 23, color: C.text2, marginTop: 14}}>{c.path}/</div>
						</div>
					);
				})}
			</div>
			<div style={{position: 'absolute', left: 96, top: 640, fontFamily: MONO, fontSize: 18, color: '#6E7681', opacity: ease(frame, at + cards.length * beat, 10)}}>
				{note}
			</div>
		</IsoBackdrop>
	);
};

// ---------------------------------------------------------------------------
// F1 finale: icons return with their benefit lines; grid pulls back

export const FinaleShot: React.FC<{items: Array<{repo: string; line: string}>; beat?: number; heading: HeadingProps}> = ({items, beat = 15, heading}) => {
	const frame = useCurrentFrame();
	const pull = interpolate(frame, [0, 180], [1.35, 1], {...clamp, easing: EASE});
	return (
		<IsoBackdrop scale={pull}>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 70, fontFamily: SANS}}>
				<div style={{display: 'flex', gap: 60, alignItems: 'flex-start'}}>
					{items.map((it, i) => {
						const lineIn = ease(frame, i * beat + 8, 10);
						return (
							<div key={it.repo} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 24, width: 340}}>
								<IconOnTile repo={it.repo} size={200} tileAt={i * beat} iconAt={i * beat + 3} />
								<div style={{fontSize: 46, fontWeight: 800, letterSpacing: '-0.02em', color: C.text, opacity: lineIn, transform: `translateY(${(1 - lineIn) * 16}px)`}}>
									{it.line}
								</div>
							</div>
						);
					})}
				</div>
				<Heading {...heading} size={72} align="center" delay={4 * beat + 6} />
			</AbsoluteFill>
		</IsoBackdrop>
	);
};

// ---------------------------------------------------------------------------
// F2 end card (section 5.3)

export const EndCardShot: React.FC<{installs: string[]; url: string; notices: string[]}> = ({installs, url, notices}) => {
	const frame = useCurrentFrame();
	const lock = ease(frame, 0, 12);
	const cmd = ease(frame, 8, 12);
	const link = ease(frame, 14, 12);
	const legal = ease(frame, 18, 12);
	return (
		<IsoBackdrop opacity={0.08}>
			<div style={{position: 'absolute', inset: '54px 96px 150px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', fontFamily: SANS}}>
				<div style={{opacity: lock >= 0.999 ? 1 : lock, fontSize: 120, fontWeight: 900, letterSpacing: '-0.04em', color: C.text}}>
					파이큐브리드팀
				</div>
				<div style={{display: 'flex', gap: 28, marginTop: 56, flexWrap: 'wrap', justifyContent: 'center', maxWidth: 1700, opacity: cmd, transform: `translateY(${(1 - cmd) * 20}px)`}}>
					{installs.map((c) => (
						<div
							key={c}
							style={{
								border: `4px solid ${C.py}`,
								borderRadius: 16,
								background: '#0B0F14',
								boxShadow: '0 0 0 10px rgba(255,212,59,.12)',
								padding: '14px 30px',
								fontFamily: MONO,
								fontWeight: 700,
								fontSize: 36,
								color: C.text,
							}}
						>
							{c}
						</div>
					))}
				</div>
				<div style={{marginTop: 50, fontWeight: 800, fontSize: 58, letterSpacing: '-0.02em', color: C.text, opacity: link}}>
					github.com/<span style={{color: C.py}}>{url}</span> · MIT License
				</div>
				<div style={{marginTop: 40, maxWidth: 1600, fontWeight: 500, fontSize: 24, lineHeight: 1.55, color: C.text2, wordBreak: 'keep-all', opacity: legal}}>
					{notices.map((n) => (
						<div key={n}>{n}</div>
					))}
				</div>
			</div>
		</IsoBackdrop>
	);
};
