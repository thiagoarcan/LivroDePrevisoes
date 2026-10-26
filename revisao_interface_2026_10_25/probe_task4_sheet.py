import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from browser_support import *
from playwright.sync_api import sync_playwright
temp,path=build_temporary_html()
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True);c,page,errors=open_app(b,path,width=390,height=844,touch=True)
 page.evaluate('App.UI.navigateTo("viewPendingEvents")')
 page.locator('#containerPendingCards .event-card').first.get_by_role('button',name='Mais ações da previsão').tap()
 print(page.evaluate('''()=>({active:!!document.querySelector('#modalEventActionSheet.active'),content:document.getElementById('actionSheetButtonsContainer').innerHTML})'''))
 page.wait_for_selector('#modalEventActionSheet.active')
 print(page.evaluate('''()=>[...document.querySelectorAll('#actionSheetButtonsContainer button')].map(n=>({label:n.textContent,display:getComputedStyle(n).display,rect:n.getBoundingClientRect().toJSON()}))'''))
 page.screenshot(path=str(ROOT/'revisao_interface_2026_10_25/resultados/task4-sheet-probe.png'),timeout=15000)
 print(errors);c.close();b.close()
temp.cleanup()
