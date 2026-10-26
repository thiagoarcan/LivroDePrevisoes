"""Validate the delivered report links and browser search/gallery behavior."""
from pathlib import Path
import json,sys
from urllib.parse import unquote,urlsplit
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'revisao_interface_2026_10_25'

def main():
    path=OUT/'RELATORIO_FINAL.html'
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    missing=[]
    for node,attr in [('a','href'),('img','src')]:
        for e in soup.find_all(node):
            value=e.get(attr,'');url=urlsplit(value)
            if not url.scheme and url.path and not (OUT/unquote(url.path)).resolve().is_file():missing.append(value)
    errors=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',headless=True)
        context=browser.new_context(viewport={'width':1280,'height':900})
        page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto(path.as_uri(),timeout=15000)
        initial=page.locator('#findings article').count()
        page.locator('#search').fill('GUI-10')
        filtered=page.locator('#findings article:visible').count()
        page.locator('#search').fill('')
        restored=page.locator('#findings article:visible').count()
        page.locator('.gallery details summary').first.click()
        page.wait_for_function('document.querySelector(".gallery details[open] img").naturalWidth>0',timeout=15000)
        gallery=page.locator('.gallery details').count()
        context.close();browser.close()
    matrix=json.loads((OUT/'resultados/layout_completo.json').read_text(encoding='utf-8'))
    extra=json.loads((OUT/'resultados/task4-captures.json').read_text(encoding='utf-8'))
    expected_gallery=len(set(matrix['screenshots']+extra['screenshots']))
    checks={'all_local_links_exist':not missing,'forty_findings':initial==40,'search_filters':filtered==1,
            'search_restores':restored==40,'gallery_has_final_captures':gallery==expected_gallery,'no_page_errors':not errors}
    report={'checks':checks,'passed':all(checks.values()),'missing_links':missing,'page_errors':errors}
    (OUT/'resultados/verificacao_relatorio_final.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['passed'] else 1

if __name__=='__main__':sys.exit(main())
