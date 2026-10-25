import {loadFont as loadNotoSansKR} from '@remotion/google-fonts/NotoSansKR';
import {loadFont as loadJetBrainsMono} from '@remotion/google-fonts/JetBrainsMono';

// Noto Sans KR (SIL OFL 1.1) covers Hangul and Latin; JetBrains Mono (OFL) is for commands.
// Fonts are fetched from Google Fonts at render time; nothing is vendored.
export const {fontFamily: SANS} = loadNotoSansKR('normal', {
	weights: ['500', '700', '900'],
	subsets: ['korean', 'latin'],
	ignoreTooManyRequestsWarning: true,
});

export const {fontFamily: MONO} = loadJetBrainsMono('normal', {
	weights: ['500', '700'],
	subsets: ['latin'],
});
