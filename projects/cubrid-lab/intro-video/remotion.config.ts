import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setCodec('h264');
Config.setPixelFormat('yuv420p');
Config.setOverwriteOutput(true);
// Brand icons, emblem and lockups are loaded at render time from commit-pinned
// raw.githubusercontent.com URLs (see src/brand.ts), so rendering needs network access.
// The generous timeout also covers OffthreadVideo frame extraction on a loaded machine.
Config.setDelayRenderTimeoutInMilliseconds(180000);
