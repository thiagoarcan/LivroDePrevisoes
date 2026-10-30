"""Single-process behavioral test runner with exact-source evidence."""
import argparse,csv,hashlib,json,os,sys,time,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('PREVISOES_TEST_OUTPUT', str(ROOT/'revisao_interface_2026_10_25/resultados')))
OUT.mkdir(parents=True,exist_ok=True)

class RecordedResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.records=[];self.started={}
    def startTest(self,test):self.started[test.id()]=time.perf_counter();super().startTest(test)
    def record(self,test,status,trace=''):
        self.records.append({'test':test.id(),'status':status,'seconds':round(time.perf_counter()-self.started.get(test.id(),time.perf_counter()),3),'trace':trace})
    def addSuccess(self,test):self.record(test,'passed');super().addSuccess(test)
    def addFailure(self,test,err):self.record(test,'failed',self._exc_info_to_string(err,test));super().addFailure(test,err)
    def addError(self,test,err):self.record(test,'error',self._exc_info_to_string(err,test));super().addError(test,err)
    def addSkip(self,test,reason):self.record(test,'skipped',reason);super().addSkip(test,reason)

def fingerprints():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'index.html',ROOT/'build_all.py',*sorted(ROOT.glob('parts_*.py'))]}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--distributed',action='store_true');parser.add_argument('--name',default='suite_final');args=parser.parse_args()
    if args.distributed:os.environ['PREVISOES_TEST_DISTRIBUTED']='1'
    os.environ.pop('PREVISOES_TEST_BASELINE',None)
    before=fingerprints();started=time.perf_counter()
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*_browser.py')
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout,resultclass=RecordedResult).run(suite)
    after=fingerprints()
    report={'tests':result.testsRun,'passed':len([x for x in result.records if x['status']=='passed']),
            'failed':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
            'seconds':round(time.perf_counter()-started,3),'distributed_html':args.distributed,
            'sources_stable':before==after,'source_hashes':after,'results':result.records}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/(args.name+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    with (OUT/(args.name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['test','status','seconds','trace'],delimiter=';');writer.writeheader();writer.writerows(result.records)
    print('SOURCES_STABLE',report['sources_stable'])
    sys.exit(0 if result.testsRun>0 and result.wasSuccessful() and before==after and not result.skipped else 1)
