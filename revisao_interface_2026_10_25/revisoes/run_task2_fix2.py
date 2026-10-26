"""Focused actor-fallback fix verification; temporary browser profiles only."""
from pathlib import Path
import json,sys,unittest
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root));sys.path.insert(0,str(root/'tests'))
suite=unittest.defaultTestLoader.loadTestsFromNames(['test_edit_journey_browser','test_ui_browser','test_ui_controller_browser'])
result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout).run(suite)
summary={'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'details':[{'test':str(t),'trace':trace} for t,trace in result.failures+result.errors]}
(Path(__file__).parent/'task2-fix2-tests.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
sys.exit(0 if result.wasSuccessful() else 1)
