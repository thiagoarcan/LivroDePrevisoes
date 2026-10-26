from pathlib import Path
import sys, json
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tests'))
from browser_support import build_temporary_html, open_app
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    temp, path = build_temporary_html()
    browser = p.chromium.launch(channel='msedge', headless=True)
    context, page, errors = open_app(browser, path, width=390, height=844)
    page.evaluate('App.UI.applyTheme("light");App.UI.navigateTo("viewDiagnostic")')
    page.locator('#tableDiagCollections').scroll_into_view_if_needed()
    page.screenshot(path=str(Path(__file__).with_name('task3-fix1-review-diagnostic-390.png')))
    dimensions = page.locator('#tableDiagCollections').evaluate('(t)=>({width:t.offsetWidth,rows:[...t.rows].map(r=>r.getBoundingClientRect().height),wrapper:t.parentElement.clientWidth})')
    result = {'diagnostic': dimensions, 'pageerrors': errors}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))
    context.close()
    browser.close()
    temp.cleanup()
