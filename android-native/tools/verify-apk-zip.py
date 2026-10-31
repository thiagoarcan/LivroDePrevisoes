#!/usr/bin/env python3
import hashlib, struct, sys, zipfile, zlib
from apk_integrity import class_descriptors, validate_class_boundaries
path=sys.argv[1]
with zipfile.ZipFile(path) as z, open(path,'rb') as f:
    names=z.namelist()
    assert len(names)==len(set(names)), 'Duplicate ZIP entries'
    assert {'AndroidManifest.xml','classes.dex'}.issubset(names), 'Required APK entry missing'
    assert {'assets/licenses/kotlin-LICENSE.txt', 'assets/licenses/kotlin-NOTICE.txt'}.issubset(names), 'Kotlin license/notice missing'
    assert not z.testzip(), 'ZIP CRC integrity failure'
    assert not any(n.startswith('lib/') for n in names), 'Unexpected native library'
    for i in z.infolist():
        if i.compress_type==zipfile.ZIP_STORED:
            f.seek(i.header_offset+26)
            filename_len,extra_len=struct.unpack('<HH',f.read(4))
            offset=i.header_offset+30+filename_len+extra_len
            assert offset % 4 == 0, (i.filename,'not 4-byte aligned',offset)
        if i.filename.startswith('classes') and i.filename.endswith('.dex'):
            dex=z.read(i)
            assert dex.startswith(b'dex\n'), 'Invalid DEX header'
            validate_class_boundaries(class_descriptors(dex))
            assert b'Landroid/webkit/WebView;' not in dex, 'Unexpected WebView wrapper reference'
            assert struct.unpack_from('<I',dex,32)[0]==len(dex), 'DEX size mismatch'
            assert hashlib.sha1(dex[32:]).digest()==dex[12:32], 'DEX SHA1 mismatch'
            assert zlib.adler32(dex[12:]) & 0xffffffff == struct.unpack_from('<I',dex,8)[0], 'DEX checksum mismatch'
    if 'resources.arsc' in names:
        assert z.getinfo('resources.arsc').compress_type==zipfile.ZIP_STORED, 'resources.arsc must be stored'
print('Verified ZIP CRCs, required entries, DEX integrity, no native code, 4-byte alignment, Kotlin notices, and exclusion of framework/JSON/test/compiler code.')
