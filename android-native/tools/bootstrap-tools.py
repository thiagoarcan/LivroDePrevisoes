#!/usr/bin/env python3
"""Download checksum-pinned open-source artifacts; never installs/licences an SDK."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import urllib.request
import zipfile

TOOLS = Path(__file__).resolve().parent
DEFAULT_CACHE = TOOLS.parent / 'build' / 'toolchain'
ALLOWED_PREFIXES = ('https://repo.maven.apache.org/maven2/', 'https://dl.google.com/dl/android/maven2/', 'https://raw.githubusercontent.com/JetBrains/kotlin/v1.9.24/license/')


def verify(path, artifact):
    return path.is_file() and path.stat().st_size == artifact['size'] and hashlib.sha256(path.read_bytes()).hexdigest() == artifact['sha256']


def prepare_framework(source, target):
    """Drop Robolectric's unrelated Kotlin 2.x runtime/metadata from the compiler view.

    The original source jar remains intact and pinned. Android classes/resources
    are unchanged; this derived jar is compile/link-only and never packaged.
    """
    with zipfile.ZipFile(source) as original, zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=1) as output:
        for entry in sorted(original.infolist(), key=lambda entry: entry.filename):
            name = entry.filename
            if entry.is_dir() or name.startswith(('kotlin/', 'kotlinx/')) or name.endswith('.kotlin_module'):
                continue
            fixed = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            fixed.compress_type = zipfile.ZIP_DEFLATED
            fixed.external_attr = 0o644 << 16
            output.writestr(fixed, original.read(entry), compresslevel=1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--cache', type=Path, default=Path(os.environ.get('TOOLCHAIN_CACHE', DEFAULT_CACHE)))
    args = parser.parse_args()
    cache = args.cache.resolve()
    cache.mkdir(parents=True, exist_ok=True)
    cache_lock = (cache / '.bootstrap.lock').open('w')
    fcntl.flock(cache_lock, fcntl.LOCK_EX)
    lock = json.loads((TOOLS / 'artifacts.lock.json').read_text())
    for artifact in lock['artifacts']:
        relative = Path(artifact['file'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe artifact path')
        dest = cache / relative
        if verify(dest, artifact):
            continue
        if args.verify_only:
            raise ValueError('Missing or checksum-mismatched artifact: ' + str(dest))
        if not artifact['url'].startswith(ALLOWED_PREFIXES):
            raise ValueError('Unapproved artifact source: ' + artifact['url'])
        dest.parent.mkdir(parents=True, exist_ok=True)
        partial = dest.with_suffix(dest.suffix + '.partial')
        print('Downloading', dest.name, flush=True)
        urllib.request.urlretrieve(artifact['url'], partial)
        if not verify(partial, artifact):
            partial.unlink(missing_ok=True)
            raise ValueError('Downloaded artifact checksum mismatch: ' + dest.name)
        partial.replace(dest)
    notices = cache / 'licenses'
    notices.mkdir(exist_ok=True)
    extracts = [
        ('aapt2-9.5.0-16666295-linux.jar', 'aapt2', cache / 'aapt2'),
        ('aapt2-9.5.0-16666295-linux.jar', 'NOTICE', notices / 'aapt2-NOTICE.txt'),
        ('ecj-3.39.0.jar', 'about.html', notices / 'ecj-about.html'),
        ('apksig-9.5.0.jar', 'LICENSE', notices / 'apksig-LICENSE.txt'),
        ('r8-9.5.28.jar', 'LICENSE', notices / 'r8-LICENSE.txt'),
    ]
    for archive, member, dest in extracts:
        with zipfile.ZipFile(cache / archive) as package:
            data = package.read(member)
            if not dest.exists() or dest.read_bytes() != data:
                partial = dest.with_name(dest.name + '.extract.partial')
                partial.write_bytes(data)
                partial.replace(dest)
    (cache / 'aapt2').chmod(0o755)
    framework = cache / 'android-framework-compile.jar'
    checksum = cache / 'android-framework-compile.sha256'
    if not framework.exists() or not checksum.exists() or hashlib.sha256(framework.read_bytes()).hexdigest() != checksum.read_text().strip():
        prepare_framework(cache / 'android-all-16-robolectric-13921718.jar', framework)
        checksum.write_text(hashlib.sha256(framework.read_bytes()).hexdigest() + '\n')
    print('Verified %d pinned artifacts in %s' % (len(lock['artifacts']), cache))


if __name__ == '__main__':
    main()
