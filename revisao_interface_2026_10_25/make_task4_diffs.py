from pathlib import Path
import difflib,hashlib,json
root=Path(__file__).resolve().parents[1];out=root/'revisao_interface_2026_10_25/resultados';base=root/'revisao_interface_2026_10_25/revisoes/final_fix_base'
names=['parts_css.py','parts_html.py','parts_js_presentation.py','parts_js_ui.py']
for name in names:
    before=(base/name).read_text(encoding='utf-8');after=(root/name).read_text(encoding='utf-8')
    (out/('task4-'+name+'.diff')).write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='final_fix_base/'+name,tofile=name)),encoding='utf-8')
tracked=names+['parts_js_core.py','parts_js_service.py','build_all.py','index.html']
(out/'task4-source-hashes.json').write_text(json.dumps({name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in tracked},indent=2),encoding='utf-8')
print('Final wave diffs and source hashes saved.')
