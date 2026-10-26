"""Auditoria em perfil temporário. Não altera fontes ou base do usuário."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'auditoria_interface'
VIEWS = ['viewDashboard', 'viewNewEvent', 'viewPendingEvents', 'viewCompletedEvents',
         'viewCadastros', 'viewConfigAlerts', 'viewConfigColors', 'viewBackup', 'viewDiagnostic']
METRICS = r"""() => {
 const shown=e=>!!e.getClientRects().length && getComputedStyle(e).visibility!=='hidden';
 const rect=e=>{if(!e)return null;let r=e.getBoundingClientRect(),s=getComputedStyle(e);return {id:e.id,cls:String(e.className),x:r.x,y:r.y,w:r.width,h:r.height,display:s.display,position:s.position,font:s.fontSize,color:s.color,bg:s.backgroundColor}};
 const controls=[...document.querySelectorAll('button,input:not([type=hidden]),select,textarea,a')].filter(shown).map(e=>({...rect(e),text:(e.innerText||e.getAttribute('aria-label')||e.title||e.name||'').trim().slice(0,90),type:e.type,disabled:e.disabled,aria:e.getAttribute('aria-label')}));
 return {width:innerWidth,height:innerHeight,scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight,layout:document.body.getAttribute('data-layout-mode'),theme:document.body.className,view:App.UI.currentView,header:rect(document.querySelector('.app-header')),nav:rect(document.querySelector('.app-nav')),bottom:rect(document.getElementById('mobileBottomNav')),banner:rect(document.getElementById('mobileActiveAlarmsBanner')),controls,overflow:[...document.querySelectorAll('body *')].filter(shown).map(rect).filter(e=>e.x+e.w>innerWidth+2||e.x< -2).slice(0,35)};
}"""

def save_json(name, data):
    (OUT / 'dados' / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def main():
    records, flows, errors, captures = [], {}, [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(timezone_id='America/Sao_Paulo', viewport={'width':1440,'height':1000})
        page = context.new_page()
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto((ROOT/'index.html').as_uri())
        page.wait_for_function('window.App && App.AlarmEngine.intervalId !== null')
        page.evaluate('async()=>{App.AlarmEngine.stop();await App.AlarmEngine.tick()}')
        flows['browser'] = browser.version
        flows['initial'] = page.evaluate('async()=>({consoles:(await App.DB.getAll("consoles")).length,settings:await App.Service.getSettings()})')
        page.evaluate('async()=>{await App.Service.loadDemoData(); await App.UI.renderDashboard()}')
        for label, width, height, mode in [
            ('celular_auto',390,844,'auto'), ('celular_manual',390,844,'mobile'),
            ('tablet_auto',820,1180,'auto'), ('tablet_manual',1024,768,'tablet'),
            ('desktop_auto',1440,1000,'auto')]:
            page.set_viewport_size({'width':width,'height':height})
            page.evaluate('(mode)=>App.UI.applyResponsiveLayoutMode(mode,false)',mode)
            for view in VIEWS:
                page.evaluate('(v)=>App.UI.navigateTo(v)', view)
                page.wait_for_timeout(35)
                page.evaluate('window.scrollTo(0,0)')
                record=page.evaluate(METRICS);record['profile']=label;records.append(record)
                name=f'{label}_{view}.png'
                page.screenshot(path=str(OUT/'capturas'/name),full_page=True,animations='disabled')
                captures.append({'file':name,'profile':label,'view':view,'width':width,'height':height})
            save_json('metricas_navegador.json',records)
            save_json('capturas_indice.json',captures)
            print('CAPTURADO',label,flush=True)

        for width,height in [(320,640),(360,800),(480,800),(600,960),(767,900),(768,1024),
                             (1024,768),(1199,800),(1200,800),(1600,900),(1919,1080),
                             (1920,1080),(2200,1080),(2559,1080),(2560,1080),(3440,1440)]:
            page.set_viewport_size({'width':width,'height':height})
            page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)')
            for view in VIEWS:
                page.evaluate('(v)=>App.UI.navigateTo(v)',view)
                record=page.evaluate(METRICS);record['profile']='limite_auto';records.append(record)
        print('LIMITES_MEDIDOS',flush=True)
        page.set_viewport_size({'width':1920,'height':1080})
        page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)')
        for theme in ['dark','light','industrial']:
            page.evaluate('(t)=>App.UI.applyTheme(t)',theme)
            page.wait_for_timeout(250)
            for view in ['viewDashboard','viewPendingEvents','viewNewEvent']:
                page.evaluate('(v)=>App.UI.navigateTo(v)',view)
                name=f'tema_{theme}_{view}.png'
                page.screenshot(path=str(OUT/'capturas'/name),full_page=True,animations='disabled')
                captures.append({'file':name,'profile':'tema_'+theme,'view':view,'width':1920,'height':1080})
                record=page.evaluate(METRICS);record['profile']='tema_'+theme;records.append(record)
        for mode,width,height in [('conventional',1440,1000),('widescreen',1920,1080),('ultrawide',3440,1440),('compact',390,844)]:
            page.set_viewport_size({'width':width,'height':height})
            page.evaluate('(m)=>App.UI.applyResponsiveLayoutMode(m,false)',mode)
            page.evaluate('App.UI.applyTheme("dark")')
            for view in ['viewDashboard','viewPendingEvents']:
                page.evaluate('(v)=>App.UI.navigateTo(v)',view)
                name=f'modo_{mode}_{view}.png'
                page.screenshot(path=str(OUT/'capturas'/name),full_page=True,animations='disabled')
                captures.append({'file':name,'profile':mode,'view':view,'width':width,'height':height})
        print('TEMAS_E_MODOS_CAPTURADOS',flush=True)

        page.set_viewport_size({'width':390,'height':844})
        page.evaluate('App.UI.applyResponsiveLayoutMode("mobile",false)')
        page.evaluate('App.UI.navigateTo("viewPendingEvents")')
        event_id=page.evaluate('App.UI.activePendingEvents[0].id')
        completed_id=page.evaluate('async()=>(await App.DB.getAll("events")).find(e=>e.status==="concluido").id')
        for key,expr in [
            ('drawer','document.getElementById("btnToggleMobileMenu").click()'),
            ('filtros','document.getElementById("btnToggleFilters").click()'),
            ('acoes',f'App.UI.openEventActionSheet({json.dumps(event_id)})'),
            ('conclusao',f'App.UI.showCompleteModal({json.dumps(event_id)})'),
            ('adiamento',f'App.UI.showSnoozeModal({json.dumps(event_id)})'),
            ('reabertura',f'App.UI.showReopenModal({json.dumps(completed_id)})'),
            ('detalhes',f'App.UI.showDetailsModal({json.dumps(event_id)})'),
            ('status','App.UI.openAppStatusModal()'),
            ('confirmacao','App.UI.showConfirmModal("Excluir previsão","Confirmação de auditoria",()=>{})'),
            ('dependencias','App.UI.showDependencyModal("Dependências",["1 evento vinculado"],()=>{})'),
            ('importacao','App.UI.showImportSummaryModal({schemaVersion:1,exportedAt:new Date().toISOString(),data:{consoles:[],pipelines:[],operationalUnits:[],events:[]}})'),
            ('alarme',f'App.UI.showAlarmModal(await App.DB.get("events",{json.dumps(event_id)}))')]:
            page.evaluate('()=>{document.querySelectorAll(".modal-overlay.active").forEach(e=>e.classList.remove("active"));document.getElementById("filterDrawer").style.display="none";document.getElementById("btnCloseMobileDrawer").click()}')
            try:
                page.evaluate('async()=>{'+expr+'}')
                page.wait_for_timeout(50)
                name=f'celular_manual_modal_{key}.png'
                page.screenshot(path=str(OUT/'capturas'/name),full_page=True,animations='disabled')
                captures.append({'file':name,'profile':'modal_mobile','view':key,'width':390,'height':844})
                flows['modal_'+key]=page.evaluate('()=>({active:[...document.querySelectorAll(".modal-overlay.active")].map(e=>({id:e.id,box:{width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height},children:[...e.querySelectorAll("button")].map(b=>({id:b.id,text:b.textContent.trim(),h:b.getBoundingClientRect().height,y:b.getBoundingClientRect().y}))})),focus:document.activeElement.id,drawer:document.getElementById("appMobileDrawer").className,filterClass:document.getElementById("filterDrawer").className})')
            except Exception as e:
                flows['modal_'+key]={'error':str(e)[:500]}
        print('MODAIS_CAPTURADOS',flush=True)
        save_json('testes_fluxos.json',flows)
        save_json('metricas_navegador.json',records)
        save_json('capturas_indice.json',captures)
        page.evaluate('()=>{document.querySelectorAll(".modal-overlay.active").forEach(e=>e.classList.remove("active"));document.getElementById("btnCloseMobileDrawer").click();document.getElementById("filterDrawer").style.display="none"}')
        flows['confirmation_cancel']=page.evaluate('()=>{let actions=[];App.UI.showConfirmModal("A","A",()=>actions.push("A"));document.getElementById("btnCancelConfirm").click();App.UI.showConfirmModal("B","B",()=>actions.push("B"));document.getElementById("btnAcceptConfirm").click();return actions}')
        page.evaluate('App.UI.navigateTo("viewNewEvent")')
        flows['description_type']=page.evaluate('()=>({tag:document.getElementById("inputEventDescription").tagName,type:document.getElementById("inputEventDescription").type})')
        page.locator('#inputEventDescription').fill('Texto preservado na rotação')
        page.evaluate('document.getElementById("btnToggleStylusCanvas").click()')
        canvas=page.locator('#stylusDrawingCanvas')
        canvas.scroll_into_view_if_needed()
        box=canvas.bounding_box()
        page.mouse.move(box['x']+20,box['y']+30);page.mouse.down()
        page.mouse.move(box['x']+100,box['y']+70,steps=6);page.mouse.up()
        flows['canvas_before']=page.evaluate('()=>({width:App.UI.stylusCanvas.width,height:App.UI.stylusCanvas.height,rect:App.UI.stylusCanvas.getBoundingClientRect().toJSON(),drawing:App.UI.getStylusData(),history:App.UI.stylusHistory.length})')
        page.set_viewport_size({'width':844,'height':390})
        page.wait_for_timeout(150)
        flows['rotation']=page.evaluate('()=>({text:document.getElementById("inputEventDescription").value,drawing:App.UI.getStylusData(),width:App.UI.stylusCanvas.width,height:App.UI.stylusCanvas.height,rect:App.UI.stylusCanvas.getBoundingClientRect().toJSON()})')
        page.locator('#btnFullscreenStylusCanvas').click()
        name='lousa_tela_cheia_paisagem.png';page.screenshot(path=str(OUT/'capturas'/name),full_page=True,animations='disabled')
        captures.append({'file':name,'profile':'lousa','view':'fullscreen','width':844,'height':390})
        flows['canvas_fullscreen']=page.evaluate('()=>({box:document.getElementById("boxStylusCanvas").getBoundingClientRect().toJSON(),canvas:App.UI.stylusCanvas.getBoundingClientRect().toJSON(),toolbar:getComputedStyle(document.getElementById("btnUndoStylusCanvas").parentElement).position})')
        page.locator('#btnFullscreenStylusCanvas').click()
        drawing=flows['rotation']['drawing']
        flows['drawing_preserved_rotation']=drawing==flows['canvas_before']['drawing']
        page.evaluate('(id)=>{return App.DB.get("events",id).then(e=>{e.stylusDrawing=App.UI.getStylusData();return App.DB.update("events",e)})}',event_id)
        page.set_viewport_size({'width':390,'height':844})
        page.evaluate('(id)=>App.UI.showDetailsModal(id)',event_id)
        flows['drawing_details']=page.evaluate('()=>({img:getComputedStyle(document.getElementById("detailsModalDrawingImg")).display,outer:getComputedStyle(document.getElementById("detailsModalDrawingBox")).display,inner:getComputedStyle(document.getElementById("detailsStylusContainer")).display,visible:document.getElementById("detailsModalDrawingImg").getClientRects().length>0})')
        page.screenshot(path=str(OUT/'capturas'/'detalhes_com_desenho_oculto.png'),full_page=True,animations='disabled')
        captures.append({'file':'detalhes_com_desenho_oculto.png','profile':'modal_mobile','view':'drawing_hidden','width':390,'height':844})
        page.evaluate('document.querySelectorAll(".modal-overlay.active").forEach(e=>e.classList.remove("active"))')
        page.evaluate('App.UI.navigateTo("viewPendingEvents")')
        page.locator('#inputSearchPending').fill('PIG')
        page.wait_for_timeout(100)
        page.evaluate('App.UI.navigateTo("viewDashboard")')
        flows['spotlight_before']=page.evaluate('()=>({desc:document.getElementById("spotlightDescription").textContent,time:document.getElementById("spotlightTimeLeft").textContent,source:App.UI.activePendingEvents[0]?.description})')
        page.evaluate('App.UI.updateLiveTimers()')
        flows['spotlight_after']=page.evaluate('()=>({desc:document.getElementById("spotlightDescription").textContent,time:document.getElementById("spotlightTimeLeft").textContent})')
        page.screenshot(path=str(OUT/'capturas'/'dashboard_contador_evento_incorreto.png'),full_page=True,animations='disabled')
        captures.append({'file':'dashboard_contador_evento_incorreto.png','profile':'mobile_filtered','view':'spotlight_mismatch','width':390,'height':844})
        page.evaluate('App.UI.navigateTo("viewPendingEvents")')
        page.locator('#inputSearchPending').fill('')
        page.wait_for_timeout(60)
        flows['filter_sheet']=page.evaluate('()=>{document.getElementById("btnToggleFilters").click();let e=document.getElementById("filterDrawer"),s=getComputedStyle(e);return {class:e.className,display:s.display,position:s.position,rect:e.getBoundingClientRect().toJSON(),footerVisible:!!document.getElementById("btnSheetApplyFilters").getClientRects().length}}')
        page.evaluate('document.getElementById("filterDrawer").style.display="none"')
        page.locator('#btnToggleFilters').focus()
        page.evaluate('(id)=>App.UI.showCompleteModal(id)',event_id)
        flows['modal_focus_open']=page.evaluate('()=>({focus:document.activeElement.id,inModal:!!document.activeElement.closest(".modal-overlay")})')
        page.keyboard.press('Tab')
        flows['modal_focus_tab']=page.evaluate('()=>({focus:document.activeElement.id,inModal:!!document.activeElement.closest(".modal-overlay")})')
        page.keyboard.press('Escape')
        flows['modal_focus_close']=page.evaluate('()=>({focus:document.activeElement.id,activeModals:document.querySelectorAll(".modal-overlay.active").length})')
        page.emulate_media(reduced_motion='reduce')
        flows['reduced_motion']=page.evaluate('()=>({cards:[...document.querySelectorAll(".pulsing-card")].slice(0,2).map(e=>getComputedStyle(e).animationDuration),badges:[...document.querySelectorAll(".pulsing-badge")].slice(0,2).map(e=>getComputedStyle(e).animationDuration)})')
        # Remove snapshots base64 from the main JSON; equality remains recorded.
        for key in ['canvas_before','rotation']:
            flows[key]['drawing_length']=len(flows[key].pop('drawing') or '')
        flows['errors']=errors
        save_json('metricas_navegador.json',records)
        save_json('capturas_indice.json',captures)
        save_json('testes_fluxos.json',flows)
        context.close();browser.close()
        print('CONCLUIDO',len(records),'medições',len(captures),'capturas',len(errors),'erros',flush=True)

if __name__=='__main__':
    main()
