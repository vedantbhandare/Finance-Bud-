#!/usr/bin/env node
/**
 * Portable shim for invoking the backend virtualenv's Python.
 *
 * npm runs scripts through cmd.exe on Windows, which rejects forward slashes in
 * an executable path, and through sh elsewhere, which rejects backslashes. So a
 * single hardcoded venv path cannot work on both. This resolves it per platform.
 *
 *   node scripts/py.mjs --cwd backend -m pytest -q
 *   node scripts/py.mjs scripts/e2e_smoke.py
 */
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const isWindows = process.platform === 'win32';

const venvPython = isWindows
  ? join(repoRoot, 'backend', '.venv', 'Scripts', 'python.exe')
  : join(repoRoot, 'backend', '.venv', 'bin', 'python');

const args = [...process.argv.slice(2)];
let cwd = repoRoot;

const cwdIndex = args.indexOf('--cwd');
if (cwdIndex !== -1) {
  const target = args[cwdIndex + 1];
  if (!target) {
    console.error('py.mjs: --cwd requires a directory argument');
    process.exit(2);
  }
  cwd = resolve(repoRoot, target);
  args.splice(cwdIndex, 2);
}

let python = venvPython;
if (!existsSync(python)) {
  console.error(
    `py.mjs: no virtualenv at ${venvPython}\n` +
      `        falling back to "python" on PATH — install deps with:\n` +
      `        cd backend && python -m venv .venv && .venv/Scripts/pip install -r requirements.txt`,
  );
  python = isWindows ? 'python' : 'python3';
}

const result = spawnSync(python, args, { cwd, stdio: 'inherit' });
if (result.error) {
  console.error(`py.mjs: failed to launch ${python}: ${result.error.message}`);
  process.exit(1);
}
process.exit(result.status ?? 1);
