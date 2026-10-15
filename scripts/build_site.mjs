import { execFileSync } from 'node:child_process'
import { copyFileSync, mkdirSync, rmSync } from 'node:fs'
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
const decks = [
  ['slides.md', 'contests/2026-ossdevcon'],
  ['operator-first-validation.ko.md', 'events/2026-builder-season4/01-validation/ko'],
  ['operator-first-validation.en.md', 'events/2026-builder-season4/01-validation/en'],
]

// Only this fixed, generated directory is replaced; normal deck builds stay intact.
rmSync(output, { recursive: true, force: true })
mkdirSync(output, { recursive: true })
for (const [entry, route] of decks) {
  execFileSync(process.execPath, [cli, 'build', entry, '--base', `${base}${route}/`,
    '--out', join(output, route), '--router-mode', 'hash'], {
    cwd: presentation,
    stdio: 'inherit',
  })
}
copyFileSync(join(presentation, 'site.html'), join(output, 'index.html'))
copyFileSync(join(presentation, 'public/favicon.svg'), join(output, 'favicon.svg'))
console.log(`Showcase HTML ready in ${output} (base ${base})`)
