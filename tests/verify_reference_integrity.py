"""Compare references and original snapshots with the historical audit hashes."""
from pathlib import Path
import hashlib,json,sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'revisao_interface_2026_10_25'

def main():
    read=lambda name:json.loads((ROOT/'auditoria_interface/dados'/name).read_text(encoding='utf-8'))
    checks=[]
    for item in read('inventario_referencias.json'):
        path=ROOT/item['arquivo']
        checks.append({'file':item['arquivo'],'kind':'reference',
                       'passed':path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']})
    for item in read('manifesto_fontes.json'):
        is_reference=Path(item['file']).suffix.lower() in ['.docx','.pdf']
        path=ROOT/item['file'] if is_reference else OUT/'originais'/item['file']
        checks.append({'file':str(path.relative_to(ROOT)),'kind':'reference' if is_reference else 'original_snapshot',
                       'passed':path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']})
    report={'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks)}
    (OUT/'resultados/integridade_referencias.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if not report['failed'] else 1

if __name__=='__main__':sys.exit(main())
