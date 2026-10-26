"""Reproduce scoped RED against the review snapshot or verify current sources."""
from pathlib import Path
import argparse,importlib.util,json,sys,unittest
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root));sys.path.insert(0,str(root/'tests'))
parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');parser.add_argument('--all',action='store_true');parser.add_argument('tests',nargs='*');args=parser.parse_args()
if args.baseline:
    source=root/'revisao_interface_2026_10_25/revisoes/task2_r1_base/parts_js_ui.py'
    spec=importlib.util.spec_from_file_location('parts_js_ui',source);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);sys.modules['parts_js_ui']=module
suite=unittest.defaultTestLoader.discover(str(root/'tests')) if args.all else unittest.defaultTestLoader.loadTestsFromNames(args.tests or ['test_ui_controller_browser.UIController'])
suffix='baseline' if args.baseline else 'suite' if args.all else 'controller'
out=root/'revisao_interface_2026_10_25/revisoes'
with (out/f'task2-fix1-{suffix}.log').open('w',encoding='utf-8') as stream:
    result=unittest.TextTestRunner(verbosity=2,stream=stream).run(suite)
summary={'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'details':[{'test':str(t),'trace':trace} for t,trace in result.failures+result.errors]}
(out/f'task2-fix1-{suffix}.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='details'}))
print('\n'.join(d['test'] for d in summary['details']))
sys.exit(0 if result.wasSuccessful() else 1)
