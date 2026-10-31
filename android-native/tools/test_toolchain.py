"""Focused integrity tests for the manual Kotlin build toolchain."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

TOOLS = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('bootstrap', TOOLS / 'bootstrap-tools.py')
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


class FrameworkClasspathTest(unittest.TestCase):
    def test_removes_foreign_kotlin_runtime_and_metadata_but_keeps_framework(self):
        with tempfile.TemporaryDirectory() as temp:
            source, target = Path(temp) / 'source.jar', Path(temp) / 'target.jar'
            entries = {
                'android/app/Activity.class': b'framework',
                'resources.arsc': b'resources',
                'META-INF/new.kotlin_module': b'kotlin-2.1',
                'kotlin/Unit.class': b'foreign-stdlib',
                'kotlinx/coroutines/Job.class': b'foreign-coroutines',
            }
            with zipfile.ZipFile(source, 'w') as package:
                for name, data in entries.items():
                    package.writestr(name, data)
            bootstrap.prepare_framework(source, target)
            with zipfile.ZipFile(target) as package:
                self.assertEqual({'android/app/Activity.class', 'resources.arsc'}, set(package.namelist()))
                self.assertEqual(b'framework', package.read('android/app/Activity.class'))


class ApkPackagingTest(unittest.TestCase):
    def test_packager_is_reproducible_aligned_and_includes_kotlin_notice(self):
        import subprocess
        import sys
        import struct
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'dex').mkdir()
            (root / 'licenses').mkdir()
            (root / 'dex/classes.dex').write_bytes(b'dex-placeholder')
            (root / 'licenses/kotlin-LICENSE.txt').write_text('Apache 2.0')
            (root / 'licenses/kotlin-NOTICE.txt').write_text('JetBrains notice')
            with zipfile.ZipFile(root / 'base.apk', 'w') as package:
                package.writestr('AndroidManifest.xml', b'manifest')
                package.writestr('resources.arsc', b'resources')
            for name in ('one.apk', 'two.apk'):
                subprocess.run([sys.executable, str(TOOLS / 'pack-apk.py'), str(root / 'base.apk'), str(root / 'dex'), str(root / name), str(root / 'licenses')], check=True)
            self.assertEqual((root / 'one.apk').read_bytes(), (root / 'two.apk').read_bytes())
            with zipfile.ZipFile(root / 'one.apk') as package, (root / 'one.apk').open('rb') as stream:
                self.assertEqual(b'Apache 2.0', package.read('assets/licenses/kotlin-LICENSE.txt'))
                for entry in package.infolist():
                    stream.seek(entry.header_offset + 26)
                    name_size, extra_size = struct.unpack('<HH', stream.read(4))
                    self.assertEqual(0, (entry.header_offset + 30 + name_size + extra_size) % 4)

    def test_packager_rejects_missing_dex(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'dex').mkdir()
            (root / 'licenses').mkdir()
            for name in ('kotlin-LICENSE.txt', 'kotlin-NOTICE.txt'):
                (root / 'licenses' / name).write_text(name)
            with zipfile.ZipFile(root / 'base.apk', 'w') as package:
                package.writestr('AndroidManifest.xml', b'manifest')
            result = subprocess.run([sys.executable, str(TOOLS / 'pack-apk.py'), str(root / 'base.apk'), str(root / 'dex'), str(root / 'out.apk'), str(root / 'licenses')], capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            self.assertIn('D8 did not produce classes.dex', result.stderr)


class DexDependencyBoundaryTest(unittest.TestCase):
    def test_rejects_packaged_android_json_and_test_libraries(self):
        spec = importlib.util.spec_from_file_location('integrity', TOOLS / 'apk_integrity.py')
        integrity = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(integrity)
        for descriptor in ('Landroid/app/Activity;', 'Lorg/json/JSONObject;', 'Lorg/junit/Test;', 'Lorg/robolectric/Robolectric;', 'Lorg/jetbrains/kotlin/cli/Main;', 'Lorg/hamcrest/Matcher;', 'Lorg/jetbrains/annotations/Nullable;'):
            with self.subTest(descriptor=descriptor), self.assertRaisesRegex(ValueError, 'Build-only/platform class'):
                integrity.validate_class_boundaries([descriptor])

    def test_accepts_app_classes_and_bundled_kotlin_runtime(self):
        spec = importlib.util.spec_from_file_location('integrity', TOOLS / 'apk_integrity.py')
        integrity = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(integrity)
        integrity.validate_class_boundaries(['Lbr/com/livrodeprevisoes/app/MainActivity;', 'Lkotlin/Unit;'])


if __name__ == '__main__':
    unittest.main()
