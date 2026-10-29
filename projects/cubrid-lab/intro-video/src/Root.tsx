import React from 'react';
import {Composition} from 'remotion';
import './fonts';
import {TimelineVideo} from './TimelineVideo';
import {Timeline, timelineDuration} from './timeline';
import demoCut from '../timelines/demo-cut.json';
import demo from '../timelines/demo.json';
import main from '../timelines/main.json';
import short from '../timelines/short.json';

const TIMELINES: Array<[string, Timeline]> = [
	['Main', main as Timeline],
	['Short', short as Timeline],
	['Demo', demo as Timeline],
	['DemoCut', demoCut as Timeline],
];

export const RemotionRoot: React.FC = () => (
	<>
		{TIMELINES.map(([id, timeline]) => (
			<Composition
				key={id}
				id={id}
				component={TimelineVideo}
				durationInFrames={timelineDuration(timeline)}
				fps={timeline.meta.fps}
				width={timeline.meta.width}
				height={timeline.meta.height}
				defaultProps={{timeline}}
			/>
		))}
	</>
);
