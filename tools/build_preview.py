#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only WITH GPL-3.0-linking-exception
"""Build the upstream C simulator on Linux with WASI SDK 27; no device writes."""
import argparse
import base64
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'firmware')
    parser.add_argument('--output', type=Path, default=ROOT / 'build/preview')
    parser.add_argument('--wasi-sdk', type=Path, default=os.environ.get('FM1_WASI_SDK'))
    args = parser.parse_args()
    if args.wasi_sdk is None:
        parser.error('Pass --wasi-sdk or set FM1_WASI_SDK to WASI SDK 27')
    source, out, sdk = args.source.resolve(), args.output.resolve(), args.wasi_sdk.resolve()
    compiler = sdk / 'bin/clang'
    version = subprocess.check_output([compiler, '--version'], text=True)
    if 'clang version 20.' not in version:
        parser.error('WASI SDK 27 uses clang 20; use the documented pinned SDK')
    manifest = json.loads((source / 'sdk/manifest.json').read_text())
    for name, expected in manifest['files'].items():
        if digest(source / name) != expected:
            raise SystemExit(f'Upstream SDK integrity mismatch: {name}')
    print(f"Verified {len(manifest['files'])} upstream SDK files", flush=True)
    out.mkdir(parents=True, exist_ok=True)
    # Never leave an older successful build at the requested output after failure.
    for name in ('index.html', 'simulator.wasm', 'build.json'):
        (out / name).unlink(missing_ok=True)
    inputs = sorted(p for folder in ('app', 'web', 'third_party/synth')
                    for p in (source / folder).rglob('*')
                    if p.is_file() and p.suffix in ('.c', '.h', '.inc')
                    and not p.is_relative_to(source / 'app/board'))
    options = [f'--sysroot={sdk / "share/wasi-sysroot"}', '-std=c11', '-O2',
               '-fwrapv', '-fno-fast-math', '-ffp-contract=off', '-DFM1_HOST_TEST',
               '-DFM1_OPEN_WEB', '-Wall', '-Wextra', '-Werror',
               '-Wno-unused-function', '-Wno-array-parameter', '-mexec-model=reactor']
    options += [f'-I{source / folder}' for folder in
                ('web/engine', 'web/synth', 'third_party/synth', 'sdk/include', 'app/synth', 'app')]
    options += [str(p) for p in inputs if p.suffix == '.c']
    wasm = out / 'simulator.wasm'
    options += ['-Wl,--strip-all', '-Wl,-z,stack-size=131072',
                '-Wl,--initial-memory=4194304', '-Wl,--max-memory=33554432', '-o', str(wasm)]
    subprocess.run([str(compiler), *options], check=True)
    release = re.search(r'^#define FM1_RELEASE_VERSION "(V\d+)"',
                        (source / 'app/version.h').read_text(), re.M).group(1)
    source_hash = hashlib.sha256('\n'.join(
        f'{p.relative_to(source).as_posix()}:{digest(p)}' for p in inputs).encode()).hexdigest()
    simulation = dict(schema=1, release_version=release, sha256=digest(wasm),
                      source_sha256=source_hash, sample_bank='synthesized-demo',
                      data=base64.b64encode(wasm.read_bytes()).decode())
    page = (source / 'sdk/Update.html.in').read_text()
    page = re.sub(r'<a\b[^>]*href="/\*FM1_SOURCE_URL\*/"[^>]*>(.*?)</a>',
                  r'<span>\1 (local preview)</span>', page)
    replacements = {'/*FM1_SOURCE_URL*/': '', '/*FM1_PAYLOAD*/': 'const FM1_PACKAGE = null;',
                    '/*FM1_SIMULATOR*/': 'const FM1_SIMULATOR = ' + json.dumps(simulation) + ';'}
    for marker, name in (('I18N', 'I18n.js'), ('SCRIPT', 'WebUpdate.js'),
                         ('SIM_SCRIPT', 'Simulator.js'), ('SAMPLE_SCRIPT', 'Samples.js')):
        replacements[f'/*FM1_{marker}*/'] = (source / 'sdk' / name).read_text()
    replacements['/*FM1_NOTICES*/'] = html.escape(
        'Local development preview; no firmware payload.\n' + '\n'.join(
            (source / name).read_text() for name in ('LICENSE.md', 'THIRD_PARTY.md')))
    for marker, value in replacements.items():
        page = page.replace(marker, value)
    if re.search(r'/\*FM1_[A-Z_]+\*/', page):
        raise SystemExit('Unexpanded preview placeholder')
    (out / 'index.html').write_text(page)
    record = dict(source_sha256=source_hash, wasm_sha256=digest(wasm),
                  compiler=version.splitlines()[0], source=str(source), device_firmware=False)
    (out / 'build.json').write_text(json.dumps(record, indent=2) + '\n')
    print(f'Built C simulator and local workbench: {out}', flush=True)


if __name__ == '__main__':
    main()
