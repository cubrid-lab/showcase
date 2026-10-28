import { execFileSync } from 'node:child_process'
import { copyFileSync, mkdirSync, readFileSync, rmSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = dirname(dirname(fileURLToPath(import.meta.url)))
const presentation = join(root, 'presentation')
const output = join(root, 'site-dist')
const prefix = process.env.PAGES_BASE_PATH ?? '/showcase'
const segments = prefix.split('/').filter(Boolean)
if (segments.some(segment => !/^[a-zA-Z0-9_-]+$/.test(segment))) {
  throw new Error(`Invalid Pages base path: ${prefix}`)
}
const base = segments.length ? `/${segments.join('/')}/` : '/'
const cli = join(presentation, 'node_modules/@slidev/cli/bin/slidev.mjs')
const { decks } = JSON.parse(readFileSync(join(presentation, 'presentations.json'), 'utf8'))
// HTML_BUNDLE_DIR: also build each deck with a relative base, for a release ZIP
// that opens from any local static server.
const bundles = process.env.HTML_BUNDLE_DIR

// Only this fixed, generated directory is replaced; normal deck builds stay intact.
rmSync(output, { recursive: true, force: true })
mkdirSync(output, { recursive: true })
const build = (entry, deckBase, out) =>
  execFileSync(process.execPath, [cli, 'build', entry, '--base', deckBase,
    '--out', out, '--router-mode', 'hash'], {
    cwd: presentation,
    stdio: 'inherit',
  })
for (const { entry, route, exportName } of decks) {
  build(entry, `${base}${route}/`, join(output, route))
  if (bundles) build(entry, './', join(bundles, exportName))
}
copyFileSync(join(presentation, 'site.html'), join(output, 'index.html'))
copyFileSync(join(presentation, 'public/favicon.svg'), join(output, 'favicon.svg'))
console.log(`Showcase HTML ready in ${output} (base ${base})`)
