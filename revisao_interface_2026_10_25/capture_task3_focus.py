"""Viewport evidence for operational controls, independent of full-page stitching."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from browser_support import *
from playwright.sync_api import sync_playwright
out=ROOT/'revisao_interface_2026_10_25/resultados'
temp,path=build_temporary_html();evidence=[]
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True)
 c,page,errors=open_app(b,path,width=3440,height=1000)
 for width,height in [(3440,1000),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false);App.UI.navigateTo("viewNewEvent")')
  page.locator('#checkEventAlarmActive').scroll_into_view_if_needed()
  rows=page.evaluate('''()=>['checkEventAlarmActive','checkEventUseDefaultAlarm'].map(id=>{let e=document.getElementById(id),r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return{id,rect:r.toJSON(),reachable:e===hit||e.contains(hit)}})''')
  assert all(r['reachable'] for r in rows),rows
  evidence.append({'viewport':[width,height],'controls':rows})
  page.screenshot(path=str(out/f'final_form_alarm_viewport_{width}.png'),animations='disabled',timeout=15000)
  page.locator('#checkKeepDutoUO').scroll_into_view_if_needed()
  value=page.evaluate('''()=>{let e=document.getElementById('checkKeepDutoUO'),r=e.getBoundingClientRect();return{id:e.id,rect:r.toJSON(),reachable:document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===e}}''')
  assert value['reachable'],value;evidence.append(value)
  page.locator('#btnSubmitEvent').scroll_into_view_if_needed()
  page.screenshot(path=str(out/f'final_form_actions_viewport_{width}.png'),animations='disabled',timeout=15000)
 assert not errors,errors
 c.close();b.close()
temp.cleanup()
(out/'task3-controls-viewport.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
print('GREEN: alarm checkboxes, keep location and saving controls at 390 and 3440 px')
