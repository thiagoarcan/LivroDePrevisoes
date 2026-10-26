from pathlib import Path
import hashlib,json,re
from urllib.parse import unquote,urlparse
from docx import Document
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'auditoria_interface'
def read(n):return json.loads((OUT/'dados'/n).read_text(encoding='utf-8'))
checks={};problems=[]
summary=read('resumo_auditoria.json')
req=read('matriz_requisitos_docx.json');visual=read('matriz_visual.json');findings=read('achados_consolidados.json')
checks['321_requisitos']=len(req)==321 and len({x['id'] for x in req})==321
checks['22_itens_visuais']=len(visual)==22
checks['40_achados']=len(findings)==40 and len({x['id'] for x in findings})==40
checks['90_capturas']=len(list((OUT/'capturas').glob('*.png')))==90
checks['198_medicoes']=len(read('metricas_navegador.json'))==198
checks['natureza_total']=sum(summary['requirements_nature'].values())==321
doc=Document(OUT/'RELATORIO_INTERFACE.docx')
text='\n'.join(p.text for p in doc.paragraphs)
checks['word_todos_requisitos']=all(x['id'] in text for x in req)
checks['word_todos_achados']=all(x['id'] in text for x in findings)
checks['word_todos_visuais']=all(x['id']+' | ' in text for x in visual)
checks['word_figuras']=len(doc.inline_shapes)==10
soup=BeautifulSoup((OUT/'RELATORIO_INTERFACE.html').read_text(encoding='utf-8'),'html.parser')
checks['html_matriz_integral']=len(soup.select('.matrix tbody tr'))==321
for e in soup.select('[href],[src]'):
    target=e.get('href') or e.get('src')
    if target.startswith('#'):
        if not soup.find(id=target[1:]):problems.append('Ancora ausente:'+target)
    elif not urlparse(target).scheme:
        if not (OUT/unquote(target.split('#')[0])).exists():problems.append('Arquivo ausente:'+target)
checks['links_locais_validos']=not problems
checks['fontes_inalterados_desde_manifesto']=all(hashlib.sha256((ROOT/x['file']).read_bytes()).hexdigest()==x['sha256'] for x in read('manifesto_fontes.json'))
with sync_playwright() as p:
    b=p.chromium.launch(channel='msedge',headless=True)
    page=b.new_page(viewport={'width':1280,'height':900})
    page.goto((OUT/'RELATORIO_INTERFACE.html').as_uri())
    checks['html_busca_inicial']=page.locator('#count').inner_text()=='321 de 321 itens exibidos'
    page.locator('#search').fill('DOCX-P0479')
    checks['html_busca_funciona']=page.locator('.matrix tbody tr:visible').count()==1
    checks['html_busca_resultado']='desenho' in page.locator('.matrix tbody tr:visible').inner_text().lower()
    page.locator('#search').fill('')
    page.set_viewport_size({'width':390,'height':844})
    checks['relatorio_sem_overflow_global']=page.evaluate('document.documentElement.scrollWidth<=innerWidth+2')
    b.close()
result={'checks':checks,'problems':problems,'all_passed':all(checks.values()),'files':{x.name:x.stat().st_size for x in OUT.iterdir() if x.is_file()}}
(OUT/'dados/verificacao_entrega.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result['all_passed'] else 1)
