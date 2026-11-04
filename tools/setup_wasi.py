#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only WITH GPL-3.0-linking-exception
"""Download and verify the pinned Linux x86_64 WASI SDK 27 release."""
import hashlib
from pathlib import Path
import platform
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'wasi-sdk-27.0-x86_64-linux'
# Published asset digest from GitHub's wasi-sdk-27 expanded release asset list.
SHA256 = 'b7d4d944c88503e4f21d84af07ac293e3440b1b6210bfd7fe78e0afd92c23bc2'
URL = f'https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-27/{NAME}.tar.gz'


def main():
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise SystemExit('This setup helper targets Linux x86_64 only.')
    cache = ROOT / 'build/tools'
    cache.mkdir(parents=True, exist_ok=True)
    archive = cache / f'{NAME}.tar.gz'
    if not archive.exists():
        partial = archive.with_suffix('.partial')
        subprocess.run(['curl', '--fail', '--location', '--retry', '2',
                        '--output', str(partial), URL], check=True)
        if hashlib.sha256(partial.read_bytes()).hexdigest() != SHA256:
            raise SystemExit('WASI archive checksum mismatch; refusing extraction')
        partial.replace(archive)
    if hashlib.sha256(archive.read_bytes()).hexdigest() != SHA256:
        raise SystemExit('Cached WASI archive checksum mismatch; refusing extraction')
    # Re-extract the verified archive, so repeat setup restores known tool bytes.
    with tarfile.open(archive) as bundle:
        bundle.extractall(cache, filter='data')
    print(cache / NAME)


if __name__ == '__main__':
    main()
