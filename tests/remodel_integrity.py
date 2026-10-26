"""Verify preserved bindings/core and exact generated distribution without external packages."""
import hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASELINE='7fc610408dfca1d49c245216613f4355236ec268'
def previous(name):return subprocess.check_output(['git','show',BASELINE+':'+name],cwd=ROOT)
current=(ROOT/'index.html').read_text(encoding='utf-8')
old=previous('index.html').decode('utf-8')
ids=lambda text: sorted(re.findall(r'\bid="([^"]+)"',text))
result={'ids_preserved':ids(old)==ids(current),'before_normalized_bytes':len(old.replace('\r\n','\n').encode('utf-8')),'after_normalized_bytes':len(current.encode('utf-8')),'distributed_bytes':(ROOT/'index.html').stat().st_size,
 'unchanged':{name:previous(name).replace(b'\r\n',b'\n')==(ROOT/name).read_bytes().replace(b'\r\n',b'\n') for name in ['parts_js_core.py','parts_js_service.py','parts_js_presentation.py','build_all.py']},
 'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'index.html',*ROOT.glob('parts_*.py')]}}
for p in ROOT.glob('parts_*.py'):compile(p.read_text(encoding='utf-8'),str(p),'exec')
(ROOT/'output/playwright/remodel-20261026/inline.js').write_text('\n'.join(re.findall(r'<script>(.*?)</script>',current,re.S)),encoding='utf-8')
(ROOT/'output/playwright/remodel-20261026/integrity.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
assert result['ids_preserved'] and all(result['unchanged'].values())
