"""Focused review probes; isolated browser storage, no product writes."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tests'))
from browser_support import build_temporary_html,open_app
from playwright.sync_api import sync_playwright

temp,path=build_temporary_html()
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(channel='msedge',headless=True)
        context,page,errors=open_app(browser,path,width=390,height=844)
        page.evaluate('App.UI.navigateTo("viewCompletedEvents")')
        before=page.evaluate('({cards:document.querySelectorAll(".completed-event-card").length,rows:document.querySelectorAll("#tbodyCompletedEvents tr").length})')
        page.set_viewport_size({'width':1440,'height':1000})
        page.wait_for_timeout(300)
        after=page.evaluate('({tier:document.body.dataset.layoutMode,cards:document.querySelectorAll(".completed-event-card").length,rows:document.querySelectorAll("#tbodyCompletedEvents tr").length,cardsDisplay:getComputedStyle(document.getElementById("containerCompletedCards")).display})')
        print(json.dumps({'completed_resize':{'before':before,'after':after}},ensure_ascii=False))
        context.close()
        context,page,errors=open_app(browser,path)
        race=page.evaluate('''async()=>{
          const [a,b]=(await App.DB.getAll('events')).filter(x=>x.status==='pendente');
          const original=App.DB.getAll;let release,reached;
          const ready=new Promise(r=>reached=r);let once=true;
          App.DB.getAll=function(store){if(store==='consoles'&&once){once=false;reached();return new Promise(r=>release=()=>original.call(App.DB,store).then(r));}return original.call(App.DB,store);};
          const pending=App.UI.showCompleteModal(a.id);await ready;
          await App.UI.showAlarmModal(b);release();await pending;App.DB.getAll=original;
          const before={displayed:document.getElementById('completeModalEventDesc').textContent,expectedId:a.id,actualBoundId:App.UI.modalStack.find(x=>x.element.id==='modalCompleteEvent').event.id};
          document.getElementById('btnConfirmCompleteModal').click();
          while(App.UI.modalBusy.has('modalCompleteEvent'))await new Promise(r=>setTimeout(r,10));
          return {before,after:{a:(await App.DB.get('events',a.id)).status,b:(await App.DB.get('events',b.id)).status}};
        }''')
        print(json.dumps({'complete_alarm_race':race},ensure_ascii=False))
        context.close()
        context,page,errors=open_app(browser,path)
        cache=page.evaluate('''async()=>{
          await App.UI.navigateTo('viewCadastros');const p=(await App.DB.getAll('pipelines'))[0];
          const events=[];window.addEventListener('app-ui-update',e=>events.push(e.detail.reason));
          await App.UI.togglePipelineActive(p.id);
          return {id:p.id,db:(await App.DB.get('pipelines',p.id)).active,cache:App.UI.getPresentationState().snapshot.pipelines.find(x=>x.id===p.id).active,notifications:events};
        }''')
        print(json.dumps({'pipeline_cache':cache},ensure_ascii=False))
        context.close()
        context,page,errors=open_app(browser,path,width=390,height=844)
        session=context.new_cdp_session(page)
        session.send('Emulation.setPageScaleFactor',{'pageScaleFactor':2})
        page.wait_for_timeout(150)
        print(json.dumps({'zoom_keyboard_flag':page.evaluate('({scale:visualViewport.scale,height:visualViewport.height,innerHeight,focused:document.activeElement.tagName,keyboardOpen:document.body.classList.contains("keyboard-open")})')},ensure_ascii=False))
        context.close();browser.close()
finally:temp.cleanup()
