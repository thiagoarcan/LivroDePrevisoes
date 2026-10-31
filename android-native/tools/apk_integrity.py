"""Inspect DEX class definitions, not merely ZIP entry names, for build-only code."""
import struct

FORBIDDEN_CLASS_PREFIXES = (
    'Landroid/', 'Landroidx/test/', 'Lcom/android/internal/', 'Ldalvik/',
    'Ljava/', 'Ljavax/', 'Lsun/', 'Lorg/json/', 'Lorg/junit/',
    'Lorg/robolectric/', 'Lorg/hamcrest/', 'Lorg/jetbrains/annotations/',
    'Lorg/jetbrains/kotlin/', 'Lcom/android/tools/',
    'Lcom/android/apksig/',
)


def class_descriptors(dex):
    """Read descriptor names for defined classes using the public DEX table layout."""
    strings_size, strings_offset = struct.unpack_from('<II', dex, 56)
    types_size, types_offset = struct.unpack_from('<II', dex, 64)
    classes_size, classes_offset = struct.unpack_from('<II', dex, 96)
    strings = []
    for index in range(strings_size):
        offset = struct.unpack_from('<I', dex, strings_offset + index * 4)[0]
        # Skip the UTF-16 character count (ULEB128); class descriptors are ASCII.
        while dex[offset] & 0x80:
            offset += 1
        offset += 1
        end = dex.index(0, offset)
        strings.append(dex[offset:end].decode('utf-8', errors='replace'))
    types = [strings[struct.unpack_from('<I', dex, types_offset + index * 4)[0]] for index in range(types_size)]
    return [types[struct.unpack_from('<I', dex, classes_offset + index * 32)[0]] for index in range(classes_size)]


def validate_class_boundaries(descriptors):
    for descriptor in descriptors:
        if descriptor.startswith(FORBIDDEN_CLASS_PREFIXES):
            raise ValueError('Build-only/platform class packaged into APK: ' + descriptor)
