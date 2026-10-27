// Render every style frame in frames.html to PNG, then the contact sheet.
//
//   cd demo-videos/intro-2026/style-frames/src
//   npm install --no-save --package-lock=false playwright-chromium@1.64.1
//   npx playwright install chromium
//   node render.mjs                # marks=slot  -> ../png/ (committed)
//   node render.mjs --marks=pinned --out=/tmp/frames-pinned
//                                   # loads the commit-pinned brand SVGs; for local review only
//
// Committed PNGs use the default `slot` mode: the brand policy forbids committing
// rasterized copies of the icons and lockups (see VIDEO_DESIGN.md, "Brand marks").
import { chromium } from "playwright-chromium";
import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const arg = (name, fallback) =>
  (process.argv.find((a) => a.startsWith(`--${name}=`)) || `=${fallback}`).split("=").slice(1).join("=");
const marks = arg("marks", "slot");
const out = resolve(arg("out", resolve(here, "../png")));
mkdirSync(out, { recursive: true });

const SIZES = { w: { width: 1920, height: 1080 }, v: { width: 1080, height: 1920 } };
const page_url = (q) => `${pathToFileURL(resolve(here, "frames.html")).href}?${q}`;

const browser = await chromium.launch();
const probe = await browser.newPage();
await probe.goto(page_url("frame=H2"));
const { ids, sizes } = await probe.evaluate(() => ({ ids: window.FRAME_IDS, sizes: window.FRAME_SIZES }));
await probe.close();

const rendered = [];
for (const id of ids) {
  const page = await browser.newPage({ viewport: SIZES[sizes[id]], deviceScaleFactor: 1 });
  await page.goto(page_url(`frame=${id}&marks=${marks}`), { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  const file = resolve(out, `${sizes[id] === "w" ? "main" : "short"}-${id}.png`);
  await page.locator("#stage").screenshot({ path: file });
  rendered.push(file);
  await page.close();
}

const sheet = await browser.newPage({ viewport: { width: 2400, height: 1600 } });
await sheet.goto(`${pathToFileURL(resolve(here, "contact-sheet.html")).href}?dir=${encodeURIComponent(pathToFileURL(out).href)}`, {
  waitUntil: "networkidle",
});
await sheet.evaluate(() => document.fonts.ready);
await sheet.locator("#sheet").screenshot({ path: resolve(out, "contact-sheet.png") });
await browser.close();
console.log([...rendered, resolve(out, "contact-sheet.png")].join("\n"));
