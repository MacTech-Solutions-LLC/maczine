#!/usr/bin/env node
// Render a MacZine article template to PDF with locally installed Chrome.
//
//   node scripts/render-pdf.mjs template/maczine-article.html [out.pdf]
//
// No dependencies — finds Chrome/Chromium/Edge on macOS, Linux or Windows
// and prints the page 1:1 (the template controls size via @page).

import { spawnSync } from 'node:child_process'
import { existsSync } from 'node:fs'
import { resolve, basename } from 'node:path'

const [input, output] = process.argv.slice(2)
if (!input) {
  console.error('usage: node scripts/render-pdf.mjs <template.html> [out.pdf]')
  process.exit(1)
}
const src = resolve(input)
if (!existsSync(src)) { console.error(`no such file: ${src}`); process.exit(1) }
const out = resolve(output || src.replace(/\.html?$/i, '') + '.pdf')

const candidates = [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium-browser',
  '/usr/bin/chromium',
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
]
const chrome = candidates.find(existsSync)
if (!chrome) {
  console.error('no Chrome/Chromium/Edge found — install one, or add its path to scripts/render-pdf.mjs')
  process.exit(1)
}

const r = spawnSync(chrome, [
  '--headless', '--disable-gpu', '--no-pdf-header-footer',
  `--print-to-pdf=${out}`, `file://${src}`
], { stdio: ['ignore', 'ignore', 'pipe'] })

if (r.status !== 0 || !existsSync(out)) {
  console.error(String(r.stderr || 'chrome failed'))
  process.exit(1)
}
console.log(`rendered ${basename(src)} → ${out}`)
