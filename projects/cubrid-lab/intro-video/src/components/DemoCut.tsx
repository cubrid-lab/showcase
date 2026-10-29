import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {SANS} from '../fonts';
import {C, IconOnTile, IsoBackdrop} from './Intro';

const REPOS = ['pycubrid', 'sqlalchemy-cubrid', 'cubrid-mcp-server', 'cubrid-cookbook-python'];

/** Demo cut title card: the four role icons (whole images on tiles) and one title line. */
export const DemoTitleShot: React.FC<{title: string}> = ({title}) => {
	const frame = useCurrentFrame();
	const t = interpolate(frame, [0, 12], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return (
		<IsoBackdrop>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 70, fontFamily: SANS}}>
				<div style={{display: 'flex', gap: 60}}>
					{REPOS.map((repo, i) => (
						<IconOnTile key={repo} repo={repo} size={200} tileAt={i * 4} iconAt={i * 4 + 3} />
					))}
				</div>
				<div style={{textAlign: 'center', opacity: t}}>
					<div style={{fontSize: 68, fontWeight: 900, letterSpacing: '-0.03em', color: C.text}}>{title}</div>
				</div>
			</AbsoluteFill>
		</IsoBackdrop>
	);
};
