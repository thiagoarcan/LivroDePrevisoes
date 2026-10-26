"""Independent targeted review; distributed HTML copied into temporary origin."""
import json, os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tests'))
os.environ['PREVISOES_TEST_DISTRIBUTED'] = '1'
from browser_support import build_temporary_html, open_app, source_fingerprints
from playwright.sync_api import sync_playwright
OUT = Path(__file__).resolve().parent
before = source_fingerprints()
temp, path = build_temporary_html()
rows = []
measure = '''()=>{
 const box=s=>{const e=document.querySelector(s),r=e.getBoundingClientRect();return {display:getComputedStyle(e).display,visible:!!e.getClientRects().length,x:r.x,y:r.y,w:r.width,h:r.height,text:e.textContent.trim().slice(0,80)}};
 return {width:innerWidth,height:innerHeight,tier:document.body.dataset.layoutMode,scroll:document.documentElement.scrollWidth,nav:box('.app-nav'),drawer:box('#appMobileDrawer'),clock:box('#liveClock'),audio:box('#chipHeaderAudioWarning'),statusParent:box('.header-status-bar'),audioReady:App.Audio.isUnlocked,main:box('.app-main')};
}'''
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context, page, errors = open_app(browser, path, width=1024, height=768)
    for width, height in [(390,844),(768,1024),(1024,768),(1199,800),(1440,900)]:
        page.set_viewport_size({'width':width,'height':height})
        page.evaluate('async()=>{await App.UI.applyResponsiveLayoutMode("auto",false);await App.UI.navigateTo("viewDashboard");App.Audio.isUnlocked=false;App.Audio.updateStatusPill();scrollTo(0,0)}')
        page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
        row = page.evaluate(measure)
        page.screenshot(path=str(OUT/f'integral-header-{width}.png'), animations='disabled')
        if width == 390:
            page.evaluate('async()=>{await App.UI.navigateTo("viewPendingEvents");scrollTo(0,0)}')
            row['card_actions'] = page.locator('#containerPendingCards .event-card-actions').first.evaluate('e=>[...e.querySelectorAll("button")].map(b=>({text:b.textContent.trim(),label:b.getAttribute("aria-label"),visible:!!b.getClientRects().length,rect:b.getBoundingClientRect().toJSON(),handler:b.getAttribute("onclick")}))')
            page.screenshot(path=str(OUT/'integral-mobile-actions.png'),full_page=True,animations='disabled')
        if width == 1024:
            page.evaluate('async()=>{await App.UI.navigateTo("viewNewEvent")}')
            page.locator('#btnToggleStylusCanvas').click()
            page.evaluate('scrollTo(0,0)')
            row['form'] = page.evaluate('''()=>Object.fromEntries(['.fieldset-localizacao','.fieldset-programacao','.fieldset-atividade','.fieldset-lousa','#stylusDrawingCanvas','#eventDraftSummary'].map(s=>[s,document.querySelector(s).getBoundingClientRect().toJSON()]))''')
            page.screenshot(path=str(OUT/'integral-tablet-form.png'),full_page=True,animations='disabled')
        rows.append(row)
    context.close();browser.close()
temp.cleanup()
result={'distributed_html':True,'rows':rows,'page_errors':errors,'sources_stable':source_fingerprints()==before,'source_hashes':before}
(OUT/'revisao-integral-probe.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
