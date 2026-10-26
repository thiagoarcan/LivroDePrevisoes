from pathlib import Path
import json,sys,unittest
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
sys.path.insert(0,str(root/'tests'))
suite=unittest.defaultTestLoader.discover(str(root/'tests'))
out=root/'revisao_interface_2026_10_25/resultados'
with (out/'task2-suite-final.log').open('w',encoding='utf-8') as stream:
    result=unittest.TextTestRunner(verbosity=2,stream=stream).run(suite)
summary={'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'details':[{'test':str(t),'trace':trace} for t,trace in result.failures+result.errors]}
(out/'task2-suite-final.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='details'}))
print('\n'.join(d['test'] for d in summary['details']))
sys.exit(0 if result.wasSuccessful() else 1)
