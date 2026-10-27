"""Resize the distributed HTML without reloading or manually applying layout."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from browser_support import ROOT, open_app

VIEWS=['viewDashboard','viewNewEvent','viewPendingEvents','viewCompletedEvents','viewCadastros','viewConfigAlerts','viewConfigColors','viewBackup','viewDiagnostic']
SIZES=[(320,740),(390,844),(767,900),(768,1024),(820,1180),(1180,820),(1199,900),(1200,900),(1440,900),(1919,1080),(1920,1080),(2559,1080),(2560,1080),(3440,1440),(3840,2160),(5120,1440),(844,390),(390,844)]
def tier(w):return 'mobile' if w<768 else 'tablet' if w<1200 else 'conventional' if w<1920 else 'widescreen' if w<2560 else 'ultrawide'
results=[]
with sync_playwright() as p:
    b=p.chromium.launch(channel='msedge',headless=True)
    c,page,errors=open_app(b,ROOT/'index.html')
    for view in VIEWS:
        page.evaluate('(v)=>App.UI.navigateTo(v)',view)
        if view=='viewNewEvent':page.locator('#inputEventDescription').fill('Preservar rascunho durante redimensionamento')
        for w,h in SIZES:
            page.set_viewport_size({'width':w,'height':h})
            page.wait_for_function('(t)=>document.body.dataset.layoutMode===t',arg=tier(w))
            page.wait_for_timeout(100)
            d=page.evaluate('''()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,
                view:App.UI.currentView,tier:document.body.dataset.layoutMode,
                main:document.querySelector('.app-main').getBoundingClientRect().toJSON(),
                draft:document.getElementById('inputEventDescription').value})''')
            passed=not d['overflow'] and d['view']==view and d['main']['width']>0
            if view=='viewNewEvent':passed=passed and d['draft']=='Preservar rascunho durante redimensionamento'
            results.append({'view':view,'width':w,'height':h,'passed':passed,'details':d})
        print(view,'checked',flush=True)
    b.close()
out=ROOT/'output/playwright/remodel-20261026/dynamic-resize.json'
out.write_text(json.dumps({'cases':len(results),'failed':sum(not r['passed'] for r in results),'errors':errors,'results':results},ensure_ascii=False,indent=2),encoding='utf-8')
print('RESULT',len(results),'cases;',sum(not r['passed'] for r in results),'failed;',len(errors),'errors')
assert all(r['passed'] for r in results) and not errors
