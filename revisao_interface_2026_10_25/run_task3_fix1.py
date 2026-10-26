"""Run focused review regressions against the immutable review base or current sources."""
import argparse,sys,types,unittest,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root));sys.path.insert(0,str(root/'tests'))
parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');parser.add_argument('--all',action='store_true');args=parser.parse_args()
if args.baseline:
    for name in ['parts_css','parts_html','parts_js_presentation']:
        path=root/'revisao_interface_2026_10_25/revisoes/task3_r1_base'/(name+'.py')
        module=types.ModuleType(name);module.__file__=str(path);sys.modules[name]=module;exec(compile(path.read_text(encoding='utf-8'),str(path),'exec'),module.__dict__)
suite=unittest.defaultTestLoader.discover(str(root/'tests')) if args.all else unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(name) for name in ['test_layout_quality_browser','test_layout_review_browser','test_edit_journey_browser'])
label='baseline' if args.baseline else 'suite' if args.all else 'focused'
out=root/'revisao_interface_2026_10_25/resultados'
with (out/f'task3-fix1-{label}.log').open('w',encoding='utf-8') as stream:result=unittest.TextTestRunner(verbosity=2,stream=stream).run(suite)
report={'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'details':[{'test':str(t),'trace':s} for t,s in result.failures+result.errors]}
(out/f'task3-fix1-{label}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='details'}));print('\n'.join(d['test'] for d in report['details']))
sys.exit(0 if result.wasSuccessful() else 1)
