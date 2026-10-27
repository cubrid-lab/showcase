#!/usr/bin/env node
// Renders single frames straight from a composition (no video encode):
//   npm run render:stills -- [Composition] [frame ...]
// Defaults to four frames of the Demo composition. Output: out/stills/<comp>-<frame>.png
import {execFileSync} from 'node:child_process';

const [comp = 'Demo', ...rest] = process.argv.slice(2);
const frames = rest.length ? rest : ['60', '230', '380', '560'];
for (const frame of frames) {
	execFileSync(
		'npx',
		['remotion', 'still', 'src/index.ts', comp, `out/stills/${comp.toLowerCase()}-${frame}.png`, `--frame=${frame}`],
		{stdio: 'inherit'},
	);
}
