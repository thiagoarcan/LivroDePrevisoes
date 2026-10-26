"""Verify the single-file distribution contains the current exported blocks."""
from pathlib import Path
import hashlib,json,sys
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

def main():
    from parts_css import CSS_CONTENT
    from parts_html import HTML_CONTENT
    from parts_js_core import JS_CORE
    from parts_js_service import JS_SERVICE
    from parts_js_ui import JS_UI
    content=(ROOT/'index.html').read_text(encoding='utf-8')
    soup=BeautifulSoup(content,'html.parser')
    checks={name:bool(block) and content.count(block)==1 for name,block in
            [('css',CSS_CONTENT),('html',HTML_CONTENT),('core',JS_CORE),('service',JS_SERVICE),('ui_with_presentation',JS_UI)]}
    checks['presentation_module_included']='App.Presentation' in JS_UI
    checks['single_inline_script']=len(soup.find_all('script'))==1 and not soup.script.get('src')
    checks['single_inline_stylesheet']=len(soup.find_all('style'))==1 and not soup.find('link',rel='stylesheet')
    checks['no_external_embedded_resources']=not any(str(node.get(attr,'')).startswith(('https:','http:','//'))
            for tag,attr in [('script','src'),('img','src'),('iframe','src'),('link','href')]
            for node in soup.find_all(tag))
    report={'checks':checks,'passed':sum(checks.values()),'failed':sum(not x for x in checks.values()),
            'index_sha256':hashlib.sha256((ROOT/'index.html').read_bytes()).hexdigest()}
    (ROOT/'revisao_interface_2026_10_25/resultados/artefato_distribuido.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if not report['failed'] else 1

if __name__=='__main__':sys.exit(main())
