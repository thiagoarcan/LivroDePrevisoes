from pathlib import Path
import difflib,hashlib,json
root=Path(__file__).resolve().parents[1];out=root/'revisao_interface_2026_10_25/resultados';orig=root/'revisao_interface_2026_10_25/originais'
for name in ['parts_css.py','parts_html.py','parts_js_presentation.py']:
    before=(orig/name).read_text(encoding='utf-8') if (orig/name).exists() else ''
    after=(root/name).read_text(encoding='utf-8')
    diff=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='originais/'+name,tofile=name))
    (out/('task3-'+name+'.diff')).write_text(diff,encoding='utf-8')
name='parts_js_ui.py';after=(root/name).read_text(encoding='utf-8');before=after.split('\nfrom parts_js_presentation import JS_PRESENTATION')[0]+'\n'
(out/'task3-ui-concatenacao.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='task2-final/'+name,tofile=name)),encoding='utf-8')
names=['parts_css.py','parts_html.py','parts_js_presentation.py','parts_js_ui.py','parts_js_core.py','parts_js_service.py','index.html','build_all.py']
(out/'task3-source-hashes.json').write_text(json.dumps({n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names},indent=2),encoding='utf-8')
print('Diffs de CSS/HTML/apresentacao e import/concatenacao Python registrados.')
