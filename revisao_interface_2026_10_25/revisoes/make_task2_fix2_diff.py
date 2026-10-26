from pathlib import Path
import difflib
root=Path(__file__).resolve().parents[2]
base=(root/'revisao_interface_2026_10_25/revisoes/task2_r2_base/parts_js_ui.py').read_text(encoding='utf-8')
current=(root/'parts_js_ui.py').read_text(encoding='utf-8')
old="ev.completedBy || ev.createdBy || 'Usuário local'"
new="typeof ev.completedBy === 'string' && ev.completedBy.trim() ? ev.completedBy : 'Não informado'"
assert base.count(old)==2
assert current==base.replace(old,new), 'Unexpected source changes outside the two completion-actor expressions'
(Path(__file__).parent/'task2-fix2.diff').write_text(''.join(difflib.unified_diff(base.splitlines(True),current.splitlines(True),fromfile='task2_r2_base/parts_js_ui.py',tofile='parts_js_ui.py')),encoding='utf-8')
print('Only two completion-actor expressions changed; Task3 concatenation preserved.')
