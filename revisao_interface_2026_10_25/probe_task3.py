import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from browser_support import *
from playwright.sync_api import sync_playwright
temp,path=build_temporary_html()
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True);c,page,errors=open_app(b,path,width=int(sys.argv[1]) if len(sys.argv)>1 else 320,height=844)
 for view in ['viewDashboard','viewNewEvent','viewPendingEvents','viewCompletedEvents','viewCadastros','viewConfigAlerts','viewConfigColors','viewBackup','viewDiagnostic']:
  page.evaluate('(v)=>App.UI.navigateTo(v)',view)
  data=page.evaluate('''()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,elements:[...document.querySelectorAll('body *')].filter(e=>e.getClientRects().length&&e.getBoundingClientRect().right>innerWidth+2&&!e.closest('.table-responsive,.hub-list-container,.modal-overlay,.mobile-drawer')).map(e=>({tag:e.tagName,id:e.id,cls:e.className,right:e.getBoundingClientRect().right,style:e.getAttribute('style')})).slice(0,30)})''')
  print(view,json.dumps(data,ensure_ascii=True))
 print('ERRORS',errors)
 c.close();b.close()
temp.cleanup()
