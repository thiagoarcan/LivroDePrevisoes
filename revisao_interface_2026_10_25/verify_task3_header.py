import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from browser_support import *
from playwright.sync_api import sync_playwright
temp,path=build_temporary_html();rows=[]
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True);c,page,errors=open_app(b,path)
 for width in [320,768,1200,3440]:
  page.set_viewport_size({'width':width,'height':844 if width<768 else 1000})
  page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false);App.UI.navigateTo("viewDashboard")')
  page.evaluate('()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
  row=page.evaluate('''()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,clock:document.getElementById('liveClock').textContent,clockBox:document.getElementById('liveClock').getBoundingClientRect().toJSON(),header:document.querySelector('.app-header').getBoundingClientRect().toJSON(),bell:document.getElementById('btnHeaderAlarmBell').getBoundingClientRect().toJSON(),console:document.getElementById('headerActiveConsole').getBoundingClientRect().toJSON()})''')
  assert row['clock']!='--:--:--',row
  assert row['scroll']<=width+2 and row['bell']['right']<=width+2 and row['console']['right']<=width+2,row
  assert row['clockBox']['width']>16 and row['clockBox']['height']>=16 and row['clockBox']['left']>=0 and row['clockBox']['right']<=width+2,row
  assert row['clockBox']['top']>=row['header']['top'] and row['clockBox']['bottom']<=row['header']['bottom'],row
  page.screenshot(path=str(ROOT/f'revisao_interface_2026_10_25/resultados/final_header_real_{width}.png'),animations='disabled',timeout=15000)
  rows.append(row)
 assert not errors,errors
 c.close();b.close()
temp.cleanup()
(ROOT/'revisao_interface_2026_10_25/resultados/task3-header-real.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('GREEN header real 320/768/1200/3440: clock, console and bell within viewport.')
