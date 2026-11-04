#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only WITH GPL-3.0-linking-exception
"""Build upstream and modified C simulators, then run the integration tests."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(*command):
    subprocess.run([str(x) for x in command], cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-source', type=Path)
    parser.add_argument('--wasi-sdk', type=Path, default=os.environ.get('FM1_WASI_SDK'))
    args = parser.parse_args()
    if args.wasi_sdk is None:
        parser.error('Pass --wasi-sdk or set FM1_WASI_SDK')
    provenance = json.loads((ROOT / 'UPSTREAM.json').read_text())
    baseline = (args.baseline_source or ROOT / 'build/upstream').resolve()
    if not (baseline / '.git').exists():
        if baseline.exists() and any(baseline.iterdir()):
            raise SystemExit('Refusing to overwrite a nonempty baseline directory')
        run('git', 'init', baseline)
        run('git', '-C', baseline, 'fetch', '--depth', '1', provenance['repository'], provenance['commit'])
        run('git', '-C', baseline, 'checkout', '--detach', 'FETCH_HEAD')
    sha = subprocess.check_output(['git', '-C', str(baseline), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(baseline), 'status', '--porcelain'], text=True)
    if sha != provenance['commit'] or dirty:
        raise SystemExit('Baseline must be the clean, pinned upstream commit')
    for source, output in ((baseline, 'build/baseline'), (ROOT / 'firmware', 'build/preview')):
        run(sys.executable, 'tools/build_preview.py', '--source', source,
            '--output', output, '--wasi-sdk', args.wasi_sdk)
    # Execute the file directly: this reports each node:test case and its count.
    run('node', 'tests/simulator.test.mjs')


if __name__ == '__main__':
    main()
