#!/usr/bin/env python3
"""Fetch the pinned official Robolectric JVM runner (no Android SDK required)."""
from __future__ import annotations
import argparse
import concurrent.futures
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.parse
import urllib.request
import zipfile

TOOLS = Path(__file__).resolve().parent
DEFAULT_CACHE = TOOLS.parent / 'build' / 'robolectric'
LOCK = TOOLS / 'robolectric-artifacts.lock.json'
ALLOWED_HOSTS = {'repo.maven.apache.org', 'dl.google.com'}


def is_verified(path: Path, artifact: dict) -> bool:
    if not path.is_file() or path.stat().st_size != artifact['size']:
        return False
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest() == artifact['sha256']


def fetch_artifact(cache: Path, artifact: dict, verify_only: bool) -> None:
    path = cache / artifact['file']
    if is_verified(path, artifact):
        return
    if verify_only:
        raise RuntimeError(f'Missing or unverified artifact: {path.name}; run robolectric-bootstrap.py')
    parsed = urllib.parse.urlparse(artifact['url'])
    if parsed.scheme != 'https' or parsed.hostname not in ALLOWED_HOSTS:
        raise RuntimeError(f'Non-official artifact origin: {path.name}')
    temporary = path.with_name(path.name + '.download')
    print(f'Downloading {path.name}', file=sys.stderr)
    try:
        with urllib.request.urlopen(artifact['url'], timeout=180) as response, temporary.open('wb') as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
        if not is_verified(temporary, artifact):
            raise RuntimeError(f'SHA-256 or length mismatch: {path.name}')
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def extract_classes(cache: Path, artifact: dict, verify_only: bool) -> Path:
    output = cache / (Path(artifact['file']).stem + '-classes.jar')
    expected = artifact['classes_sha256']
    if output.is_file() and hashlib.sha256(output.read_bytes()).hexdigest() == expected:
        return output
    if verify_only:
        raise RuntimeError(f'Missing or unverified AAR classes: {output.name}')
    with zipfile.ZipFile(cache / artifact['file']) as archive:
        classes = archive.read('classes.jar')
    if hashlib.sha256(classes).hexdigest() != expected:
        raise RuntimeError(f'AAR classes SHA-256 mismatch: {output.name}')
    temporary = output.with_name(output.name + '.extract')
    temporary.write_bytes(classes)
    temporary.replace(output)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, default=Path(os.environ.get('ROBOLECTRIC_CACHE', DEFAULT_CACHE)))
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--classpath', action='store_true', help='print only the runner runtime classpath to stdout')
    args = parser.parse_args()
    lock = json.loads(LOCK.read_text())
    artifacts = lock['artifacts']
    if lock.get('schema') != 1:
        raise RuntimeError('Unsupported Robolectric lock schema')
    names = set()
    for artifact in artifacts:
        name = artifact['file']
        if Path(name).name != name or name in names:
            raise RuntimeError('Invalid or duplicate artifact filename')
        names.add(name)
    if any(name not in names for name in lock['runtime']):
        raise RuntimeError('Runtime artifact missing from lock')
    args.cache.mkdir(parents=True, exist_ok=True)
    cache = args.cache.resolve()
    with (cache / '.bootstrap.lock').open('w') as mutex:
        fcntl.flock(mutex, fcntl.LOCK_EX)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(lambda a: fetch_artifact(cache, a, args.verify_only), artifacts))
        paths = {a['file']: (extract_classes(cache, a, args.verify_only) if a['file'].endswith('.aar') else cache / a['file']) for a in artifacts}
    if args.classpath:
        print(':'.join(str(paths[name]) for name in lock['runtime']))
    else:
        print(f'Verified {len(artifacts)} pinned Robolectric artifacts in {cache}')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, zipfile.BadZipFile, KeyError) as error:
        print(f'Robolectric bootstrap: {error}', file=sys.stderr)
        raise SystemExit(1)
