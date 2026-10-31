#!/usr/bin/env python3
"""Package an AAPT2 resource APK plus D8 output, aligning stored entries to 4 bytes.
No native libraries are supported by this native Kotlin/JVM build pipeline.
"""
import pathlib, struct, sys, zipfile

base, dex, output, licenses = sys.argv[1:]
entries = {}
for name in ('kotlin-LICENSE.txt', 'kotlin-NOTICE.txt'):
    entries['assets/licenses/' + name] = (pathlib.Path(licenses) / name).read_bytes()
with zipfile.ZipFile(base) as src:
    for entry in src.infolist():
        if entry.is_dir():
            continue
        if entry.filename.startswith('lib/'):
            raise ValueError('Native libraries require SDK zipalign and 16 KiB alignment')
        entries[entry.filename] = src.read(entry)
for path in sorted(pathlib.Path(dex).glob('classes*.dex')):
    entries[path.name] = path.read_bytes()
if 'classes.dex' not in entries:
    raise ValueError('D8 did not produce classes.dex')
with zipfile.ZipFile(output, 'w') as dest:
    for name, data in sorted(entries.items()):
        entry=zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
        entry.compress_type=zipfile.ZIP_STORED
        entry.external_attr=0o644 << 16
        offset=dest.fp.tell()+30+len(name.encode('utf-8'))
        # A well-formed ZIP extra field: 0xCAFE, 0–3 bytes of padding.
        padding=(-offset) % 4
        if padding:
            entry.extra=struct.pack('<HH',0xCAFE,padding)+bytes(padding)
        dest.writestr(entry,data)
