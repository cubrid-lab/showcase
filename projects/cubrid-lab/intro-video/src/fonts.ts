import {loadFont as loadNotoSansKR} from '@remotion/google-fonts/NotoSansKR';
import {loadFont as loadJetBrainsMono} from '@remotion/google-fonts/JetBrainsMono';
import {continueRender, delayRender, staticFile} from 'remotion';

// Noto Sans KR (SIL OFL 1.1) covers Hangul and Latin; JetBrains Mono (OFL) is for commands.
// Fetched from Google Fonts at render time; nothing is vendored.
const {fontFamily: NOTO} = loadNotoSansKR('normal', {
	weights: ['500', '700', '900'],
	subsets: ['korean', 'latin'],
	ignoreTooManyRequestsWarning: true,
});

export const {fontFamily: MONO} = loadJetBrainsMono('normal', {
	weights: ['500', '700'],
	subsets: ['latin'],
});

// Pretendard Variable (SIL OFL 1.1), the storyboard's display/body face. It is not vendored
// here: scripts/prepare-media.mjs links presentation/public/fonts/PretendardVariable.woff2
// into public/fonts/. Without it the text falls back to Noto Sans KR.
const PRETENDARD_FILE = 'fonts/PretendardVariable.woff2';

if (typeof document !== 'undefined' && typeof FontFace !== 'undefined') {
	const handle = delayRender('Loading Pretendard');
	const face = new FontFace('Pretendard', `url(${staticFile(PRETENDARD_FILE)}) format('woff2')`, {weight: '45 920'});
	face
		.load()
		.then((f) => (document.fonts as unknown as {add: (x: FontFace) => void}).add(f))
		.catch(() => undefined)
		.finally(() => continueRender(handle));
}

export const SANS = `Pretendard, ${NOTO}, sans-serif`;
