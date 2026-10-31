#!/usr/bin/env python3
"""Isolated tests for checksum enforcement and extracted AAR classpath."""
import hashlib, importlib.util, pathlib, tempfile, unittest, zipfile, sys
sys.dont_write_bytecode = True
MODULE = pathlib.Path(__file__).with_name('robolectric-bootstrap.py')

class BootstrapTest(unittest.TestCase):
    def load_module(self):
        spec = importlib.util.spec_from_file_location('robolectric_bootstrap', MODULE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_cached_artifact_hash_is_required(self):
        module = self.load_module()
        with tempfile.TemporaryDirectory() as folder:
            path = pathlib.Path(folder) / 'fixture.jar'
            path.write_bytes(b'wrong')
            artifact = {'file': path.name, 'sha256': hashlib.sha256(b'correct').hexdigest(), 'size': 7}
            self.assertFalse(module.is_verified(path, artifact))
            path.write_bytes(b'correct')
            self.assertTrue(module.is_verified(path, artifact))

    def test_aar_class_extraction_is_verified_and_repairs_corruption(self):
        module = self.load_module()
        with tempfile.TemporaryDirectory() as folder:
            cache = pathlib.Path(folder)
            aar = cache / 'fixture.aar'
            classes = b'jar-bytes'
            with zipfile.ZipFile(aar, 'w') as archive:
                archive.writestr('classes.jar', classes)
            artifact = {'file': aar.name, 'classes_sha256': hashlib.sha256(classes).hexdigest()}
            output = module.extract_classes(cache, artifact, verify_only=False)
            self.assertEqual(output.read_bytes(), classes)
            output.write_bytes(b'corrupt')
            with self.assertRaises(RuntimeError):
                module.extract_classes(cache, artifact, verify_only=True)
            module.extract_classes(cache, artifact, verify_only=False)
            self.assertEqual(output.read_bytes(), classes)

    def test_invalid_aar_class_hash_fails_closed(self):
        module = self.load_module()
        with tempfile.TemporaryDirectory() as folder:
            cache = pathlib.Path(folder)
            with zipfile.ZipFile(cache / 'fixture.aar', 'w') as archive:
                archive.writestr('classes.jar', b'wrong')
            with self.assertRaises(RuntimeError):
                module.extract_classes(cache, {'file':'fixture.aar', 'classes_sha256':'0'*64}, verify_only=False)

if __name__ == '__main__':
    unittest.main()
