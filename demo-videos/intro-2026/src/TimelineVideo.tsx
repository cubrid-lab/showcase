import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {THEME} from './brand';
import {DraftBadge, LowerThird} from './components/Overlays';
import {SubtitleTrack} from './components/Subtitles';
import {CubeWipe, FadeThrough} from './components/Transitions';
import {SHOT_TYPES} from './Shots';
import {Timeline, musicVolumeAt} from './timeline';

/** Renders a whole timeline: shots, lower thirds, transitions, narration, ducked music and subtitles. */
export const TimelineVideo: React.FC<{timeline: Timeline}> = ({timeline}) => {
	return (
		<AbsoluteFill style={{background: THEME.bg}}>
			{timeline.shots.map((shot) => {
				const Shot = SHOT_TYPES[shot.type];
				if (!Shot) {
					throw new Error(`Unknown shot type "${shot.type}" in shot ${shot.id}`);
				}
				return (
					<Sequence key={shot.id} name={`${shot.id} (${shot.type})`} from={shot.start} durationInFrames={shot.duration}>
						<Shot props={shot.props ?? {}} duration={shot.duration} />
						{shot.lowerThird ? (
							<Sequence
								from={shot.lowerThird.from ?? 10}
								durationInFrames={shot.lowerThird.duration ?? shot.duration - (shot.lowerThird.from ?? 10)}
								name="lower third"
							>
								<LowerThird
									title={shot.lowerThird.title}
									subtitle={shot.lowerThird.subtitle}
									accent={shot.lowerThird.accent}
									duration={shot.lowerThird.duration ?? shot.duration - (shot.lowerThird.from ?? 10)}
								/>
							</Sequence>
						) : null}
					</Sequence>
				);
			})}

			{timeline.shots
				.filter((s) => s.transitionIn)
				.map((shot) => {
					const t = shot.transitionIn!;
					const Wipe = t.type === 'cubeWipe' ? CubeWipe : FadeThrough;
					return (
						<Sequence
							key={`${shot.id}-transition`}
							name={`${t.type} → ${shot.id}`}
							from={Math.max(0, shot.start - Math.floor(t.duration / 2))}
							durationInFrames={t.duration}
						>
							<Wipe duration={t.duration} />
						</Sequence>
					);
				})}

			{timeline.shots
				.filter((s) => s.narration)
				.map((shot) => (
					<Sequence
						key={`${shot.id}-narration`}
						name={`narration ${shot.id}`}
						from={shot.start + (shot.narration!.offset ?? 0)}
						layout="none"
					>
						<Audio src={staticFile(shot.narration!.src)} volume={shot.narration!.volume ?? 1} />
					</Sequence>
				))}

			{timeline.music ? (
				<Audio src={staticFile(timeline.music.src)} volume={(f) => musicVolumeAt(timeline, f)} />
			) : null}

			{timeline.subtitles ? <SubtitleTrack src={timeline.subtitles} /> : null}
			{timeline.meta.draft ? <DraftBadge note={timeline.meta.note} /> : null}
		</AbsoluteFill>
	);
};
