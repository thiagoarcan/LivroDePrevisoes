"""Build and sequentially validate the frozen single-file delivery."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'revisao_interface_2026_10_25/resultados'

def fingerprints():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [ROOT/'index.html',ROOT/'build_all.py',*sorted(ROOT.glob('parts_*.py'))]}

def main():
    OUT.mkdir(exist_ok=True)
    env=dict(os.environ,PYTHONIOENCODING='utf-8',PREVISOES_TEST_DISTRIBUTED='1')
    env.pop('PREVISOES_TEST_BASELINE',None)
    commands=[
        ('build',['build_all.py']),
        ('artifact',['tests/verify_distributed_artifact.py']),
        ('references',['tests/verify_reference_integrity.py']),
        ('structural_app',['verify_app.py']),
        ('structural_adjustments',['verify_adjustments.py']),
        ('structural_mobile',['verify_mobile_tablet_adaptation.py']),
        ('suite',['tests/run_suite.py','--distributed']),
        ('layout',['tests/test_layout_browser.py','--screenshots']),
        ('firefox',['tests/test_firefox_native.py'])
    ]
    stages=[];frozen=None
    for name,args in commands:
        print('RUN',name,flush=True);started=time.perf_counter()
        result=subprocess.run([sys.executable,*args],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf-8',errors='replace')
        log=OUT/('integracao_'+name+'.log');log.write_text(result.stdout,encoding='utf-8')
        passed=result.returncode==0 and '[FALHA]' not in result.stdout and '[FAIL]' not in result.stdout
        current=fingerprints()
        if name=='build':frozen=current
        stable=current==frozen
        stages.append({'stage':name,'command':[sys.executable,*args],'exit_code':result.returncode,
                       'passed':passed and stable,'sources_stable':stable,'seconds':round(time.perf_counter()-started,3),'log':log.name})
        report={'passed':all(x['passed'] for x in stages),'complete':len(stages)==len(commands),
                'source_hashes':current,'stages':stages}
        (OUT/'validacao_integracao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print('RESULT',name,'PASS' if passed and stable else 'FAIL',round(time.perf_counter()-started,1),'seconds',flush=True)
        print('\n'.join(result.stdout.splitlines()[-4:]),flush=True)
        if not passed or not stable:return 1
    return 0

if __name__=='__main__':sys.exit(main())
