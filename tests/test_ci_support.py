"""Regression tests for CI reporting and fail-closed discovery (no browser needed)."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class CIRunnerTests(unittest.TestCase):
    def run_fixture(self, source):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'tests').mkdir()
            shutil.copyfile(ROOT / 'tests/run_suite.py', root / 'tests/run_suite.py')
            (root / 'index.html').write_text('fixture', encoding='utf-8')
            (root / 'build_all.py').write_text('# fixture', encoding='utf-8')
            if source:
                (root / 'tests/test_fixture_browser.py').write_text(source, encoding='utf-8')
            output = root / 'fresh-results'
            result = subprocess.run(
                [sys.executable, str(root / 'tests/run_suite.py'), '--name', 'fixture'],
                env={**os.environ, 'PREVISOES_TEST_OUTPUT': str(output)},
                capture_output=True, text=True)
            self.assertFalse((root / 'revisao_interface_2026_10_25').exists())
            report = json.loads((output / 'fixture.json').read_text(encoding='utf-8'))
            return result, report

    def test_empty_discovery_fails(self):
        result, report = self.run_fixture('')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report['tests'], 0)

    def test_setup_error_is_reported_instead_of_crashing_reporter(self):
        result, report = self.run_fixture('import unittest\nclass Broken(unittest.TestCase):\n @classmethod\n def setUpClass(cls): raise RuntimeError("missing browser")\n def test_case(self): pass\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report['errors'], 1)
        self.assertIn('missing browser', report['results'][0]['trace'])

    def test_skips_remain_failures(self):
        result, report = self.run_fixture('import unittest\nclass Skipped(unittest.TestCase):\n @unittest.skip("unavailable")\n def test_case(self): pass\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report['skipped'], 1)

    def test_success_creates_fresh_reports(self):
        result, report = self.run_fixture('import unittest\nclass Passing(unittest.TestCase):\n def test_case(self): self.assertEqual(1+1,2)\n')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(report['passed'], 1)
        self.assertTrue(report['sources_stable'])

if __name__ == '__main__':
    unittest.main()
