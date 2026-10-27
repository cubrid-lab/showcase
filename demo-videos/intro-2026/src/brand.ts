import {useEffect, useState} from 'react';
import {useDelayRender} from 'remotion';

/**
 * cubrid-lab/brand revision every brand asset and token is read from.
 *
 * Nothing from the brand repository is copied into this repository: icons,
 * the emblem, lockups and the numeric tokens are fetched from commit-pinned
 * raw.githubusercontent.com URLs at studio/render time (BRAND_USAGE.md,
 * "Repository icon use"). Change the pin only to a reviewed brand revision.
 */
export const BRAND_REVISION = '3a385be773af94077c56548a24cdb9313bdc3b5c';
export const BRAND_RAW = `https://raw.githubusercontent.com/cubrid-lab/brand/${BRAND_REVISION}`;

export const iconUrl = (repo: string) => `${BRAND_RAW}/dist/icons/${repo}.svg`;
export const emblemUrl = `${BRAND_RAW}/dist/organization/mark.svg`;
export const lockupUrl = (layout: 'horizontal' | 'stacked', theme: 'dark' | 'light') =>
	`${BRAND_RAW}/dist/organization/lockup-${layout}${theme === 'dark' ? '-dark' : ''}.svg`;

/** Video palette. Dark/light text values follow tokens/organization.json `wordmarks.variants`. */
export const THEME = {
	bg: '#0D1117',
	bgRaised: '#161B22',
	text: '#F0F6FC',
	textMuted: '#A8C1E8',
	lightBg: '#FFFFFF',
	lightText: '#071B43',
	lightMuted: '#284679',
	orgTop: '#006BDA',
	orgLeft: '#00A36F',
	orgRight: '#E60039',
	python: '#FFD43B',
};

export type Point = [number, number];
export type Geometry = {
	center: [number, number];
	half_width: number;
	top_y: number;
	roof_rise: number;
	face_outer_top_y: number;
	face_center_top_y: number;
	face_outer_bottom_y: number;
	face_center_bottom_y: number;
	seam_half_width: number;
};

export type BrandTokens = {
	geometry: Geometry;
	languages: Record<string, string>;
	registry: Record<string, {role: string; language: string; status: string}>;
	organizationFaces: {top: string; left: string; right: string};
};

let cache: Promise<BrandTokens> | null = null;

const fetchJson = async (path: string) => {
	const res = await fetch(`${BRAND_RAW}/${path}`);
	if (!res.ok) {
		throw new Error(`brand token fetch failed: ${path} (${res.status})`);
	}
	return res.json();
};

export const loadBrandTokens = (): Promise<BrandTokens> => {
	if (!cache) {
		cache = Promise.all([
			fetchJson('tokens/geometry.json'),
			fetchJson('tokens/colors.json'),
			fetchJson('registry/repositories.json'),
			fetchJson('tokens/organization.json'),
		]).then(([geometry, colors, registry, organization]) => ({
			geometry,
			languages: colors.languages,
			registry: {...registry.repositories, ...registry.surfaces},
			organizationFaces: organization.face_colors,
		}));
	}
	return cache;
};

/** Loads the pinned brand tokens, holding the render until they arrive. */
export const useBrandTokens = (): BrandTokens | null => {
	const {delayRender, continueRender, cancelRender} = useDelayRender();
	const [tokens, setTokens] = useState<BrandTokens | null>(null);
	const [handle] = useState(() => delayRender('Loading pinned brand tokens'));
	useEffect(() => {
		loadBrandTokens()
			.then((t) => {
				setTokens(t);
				continueRender(handle);
			})
			.catch((err) => cancelRender(err));
	}, [handle, continueRender, cancelRender]);
	return tokens;
};

/** Same construction as cube_polygons() in cubrid-lab/brand scripts/build.py (MIT). */
export const cubePolygons = (g: Geometry): Record<'top' | 'left' | 'right', Point[]> => {
	const cx = g.center[0];
	const half = g.half_width;
	const rise = g.roof_rise;
	const seam = g.seam_half_width;
	return {
		top: [
			[cx, g.top_y],
			[cx + half, g.top_y + rise],
			[cx, g.top_y + 2 * rise],
			[cx - half, g.top_y + rise],
		],
		left: [
			[cx - half, g.face_outer_top_y],
			[cx - seam, g.face_center_top_y],
			[cx - seam, g.face_center_bottom_y],
			[cx - half, g.face_outer_bottom_y],
		],
		right: [
			[cx + seam, g.face_center_top_y],
			[cx + half, g.face_outer_top_y],
			[cx + half, g.face_outer_bottom_y],
			[cx + seam, g.face_center_bottom_y],
		],
	};
};

export const pathData = (points: Point[]) =>
	'M ' + points.map(([x, y]) => `${x.toFixed(3)} ${y.toFixed(3)}`).join(' L ') + ' Z';
