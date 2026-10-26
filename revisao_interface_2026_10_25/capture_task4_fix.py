"""Viewport evidence for the final scoped correction wave; isolated demo data."""
import sys,json,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from browser_support import *
from test_final_actions_browser import CONTRAST
from playwright.sync_api import sync_playwright
out=ROOT/'revisao_interface_2026_10_25/resultados';temp,path=build_temporary_html();captures=[];rows=[]
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True);c,page,errors=open_app(b,path,touch=True)
 def capture(name):
  filename='task4-'+name+'.png';page.screenshot(path=str(out/filename),animations='disabled',timeout=15000);captures.append(filename)
 def size(w,h):
  page.set_viewport_size({'width':w,'height':h});page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)')
 def audio(ready):
  page.evaluate('''ready=>{let ctx=App.Audio.ctx;App.Audio.ctx={state:ready?'running':'suspended'};App.Audio.isUnlocked=ready;App.Audio.updateStatusPill();App.Audio.ctx=ctx}''',ready)
 for w,h in [(320,640),(390,844),(600,900),(768,1024),(820,1180),(1024,768),(1199,800)]:
  size(w,h);page.evaluate('App.UI.navigateTo("viewDashboard");scrollTo(0,0)')
  for ready in [False,True]:
   audio(ready);capture(f'header-{w}-audio-'+('ready' if ready else 'waiting'))
   rows.append(page.evaluate('''()=>{const box=id=>document.getElementById(id).getBoundingClientRect().toJSON();return{width:innerWidth,clock:box('liveClock'),audio:box('chipHeaderAudioWarning'),header:document.querySelector('.app-header').getBoundingClientRect().toJSON()}}'''))
 for w,h in [(1024,768),(1199,800),(768,1024)]:
  size(w,h);page.evaluate('App.UI.navigateTo("viewPendingEvents");scrollTo(0,0)');capture(f'pending-{w}')
  rows.append(page.evaluate('''()=>{const box=s=>document.querySelector(s).getBoundingClientRect().toJSON();return{width:innerWidth,rail:box('.app-nav'),list:box('.pending-master'),detail:box('.pending-detail-pane')}}'''))
  page.evaluate('App.UI.navigateTo("viewNewEvent")');page.locator('#inputEventDescription').fill('Verificar alinhamento e término de partida da bomba BB-101A')
  if not page.locator('#stylusDrawingCanvas').is_visible():page.locator('#btnToggleStylusCanvas').click()
  page.evaluate('scrollTo(0,0)');capture(f'editor-start-{w}')
  page.evaluate('''()=>{const target=document.querySelector('.fieldset-atividade'),header=document.querySelector('.app-header');scrollTo(0,scrollY+target.getBoundingClientRect().top-header.getBoundingClientRect().height-16)}''')
  capture(f'editor-drawing-{w}')
  rows.append(page.evaluate('''()=>{const box=s=>document.querySelector(s).getBoundingClientRect().toJSON();return{width:innerWidth,rail:box('.app-nav'),activity:box('.fieldset-atividade'),drawing:box('.fieldset-lousa'),canvas:box('#stylusDrawingCanvas')}}'''))
 size(390,844)
 for theme in ['dark','light','industrial']:
  page.evaluate('(t)=>App.UI.applyTheme(t)',theme);page.evaluate('App.UI.navigateTo("viewDashboard");scrollTo(0,0)');audio(False);capture(f'audio-header-{theme}')
  warning_ratio=page.locator('#chipHeaderAudioWarning').evaluate(CONTRAST)
  page.locator('#btnHeaderAppStatus').tap();page.wait_for_selector('#modalAppStatus.active');audio(False);capture(f'audio-status-{theme}')
  rows.append({'theme':theme,'audio_warning_contrast':warning_ratio,'status_audio_contrast':page.locator('#statusModalAudio>span').evaluate(CONTRAST)})
  page.keyboard.press('Escape')
 page.evaluate('App.UI.applyTheme("light");App.UI.navigateTo("viewPendingEvents")')
 card=page.locator('#containerPendingCards .event-card').first;card.scroll_into_view_if_needed();capture('mobile-priority-actions')
 card.get_by_role('button',name=re.compile('Mais')).tap();page.wait_for_selector('#modalEventActionSheet.active');capture('mobile-secondary-sheet');page.keyboard.press('Escape')
 page.locator('#btnToggleMobileMenu').tap();capture('drawer-metadata')
 assert not errors,errors
 c.close();b.close()
temp.cleanup();(out/'task4-captures.json').write_text(json.dumps({'screenshots':captures,'measurements':rows,'page_errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print('Review captures:',len(captures),'page errors:',len(errors))
