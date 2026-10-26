"""Inventário independente, somente leitura dos fontes da aplicação."""
from pathlib import Path
from collections import Counter
import json, re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
html = (ROOT / 'parts_html.py').read_text(encoding='utf-8')
ui = (ROOT / 'parts_js_ui.py').read_text(encoding='utf-8')
soup = BeautifulSoup(html, 'html.parser')
ids = Counter(e['id'] for e in soup.select('[id]'))
labels = {e.get('for') for e in soup.select('label[for]')}
controls = []
for e in soup.select('input, select, textarea'):
    if e.get('type') == 'hidden':
        continue
    if e.get('id') in labels or e.find_parent('label') or e.get('aria-label') or e.get('aria-labelledby'):
        continue
    controls.append({'id': e.get('id'), 'line': e.sourceline, 'type': e.get('type', e.name), 'placeholder': e.get('placeholder'), 'title': e.get('title'), 'style': e.get('style')})
buttons = []
for e in soup.select('button'):
    if e.get('aria-label') or e.get('aria-labelledby'):
        continue
    t = e.get_text(' ', strip=True)
    if not t or t in ['×', '⋯', '☰']:
        buttons.append({'id': e.get('id'), 'line': e.sourceline, 'text': t, 'title': e.get('title')})
refs = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", ui))
dialogs = [{'id':e.get('id'),'line':e.sourceline,'label':e.get('aria-labelledby') or e.get('aria-label')} for e in soup.select('[role=dialog]')]
result = {'duplicate_ids_parts_html': {k:v for k,v in ids.items() if v>1}, 'controls_without_associated_label': controls, 'symbol_or_empty_buttons_without_aria_label':buttons, 'dialogs':dialogs, 'ui_literal_id_refs_absent_static_html': sorted(refs-set(ids)), 'metric_cards':len(soup.select('.metric-card')), 'tabindex_elements':len(soup.select('[tabindex]')), 'inputmode_elements':len(soup.select('[inputmode]')), 'enterkeyhint_elements':len(soup.select('[enterkeyhint]'))}
index = BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
index_ids = Counter(e['id'] for e in index.select('[id]'))
result['duplicate_ids_index']={k:v for k,v in index_ids.items() if v>1}
result['id_set_parts_index_equal']=set(ids)==set(index_ids)
out=ROOT/'auditoria_interface/dados/inspecao_estatica.json'
out.write_text(json.dumps(result, ensure_ascii=False, indent=2),encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
