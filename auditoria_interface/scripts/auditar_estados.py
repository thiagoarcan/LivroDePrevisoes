from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'auditoria_interface'

def main():
    data={};shots=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',headless=True)
        context=browser.new_context(timezone_id='America/Sao_Paulo',viewport={'width':390,'height':844})
        page=context.new_page()
        page.goto((ROOT/'index.html').as_uri())
        page.wait_for_function('App.AlarmEngine.intervalId!==null')
        page.evaluate('async()=>{App.AlarmEngine.stop();await App.AlarmEngine.tick();await App.Service.loadDemoData()}')
        def ev(code):return page.evaluate(code)
        def shot(name):
            if name != 'estado_banner_rolagem.png':
                page.evaluate('window.scrollTo(0,0)')
            page.screenshot(path=str(OUT/'capturas'/name),full_page=name!='estado_banner_rolagem.png',animations='disabled');shots.append(name)
        ev('App.UI.applyResponsiveLayoutMode("mobile",false)')
        ev('App.UI.navigateTo("viewCompletedEvents")')
        data['completed_expansion']=ev('()=>{let c=document.querySelector(".completed-event-card"),d=c.querySelector(".completed-card-details");let before={display:getComputedStyle(d).display,height:d.getBoundingClientRect().height,expanded:c.classList.contains("expanded")};c.click();return {before,after:{display:getComputedStyle(d).display,height:d.getBoundingClientRect().height,expanded:c.classList.contains("expanded")}}}')
        shot('estado_concluidos_expansao_ineficaz.png')
        ev('App.UI.navigateTo("viewPendingEvents")')
        event_id=ev('App.UI.activePendingEvents[0].id')
        data['alarm_frozen']=ev('async()=>{let e=App.UI.activePendingEvents[0];await App.UI.showAlarmModal(e);let before=document.getElementById("alarmModalCountdown").textContent;const old=Date.now;Date.now=()=>old()+90000;App.UI.updateLiveTimers();let expected=App.Utils.formatTimeRemaining(new Date(e.scheduledAt).getTime()).text;let after=document.getElementById("alarmModalCountdown").textContent;Date.now=old;return {before,after,expected}}')
        shot('estado_alarme_contador_congelado.png')
        ev('document.getElementById("btnCloseAlarmModal").click()')
        ev('async()=>{for(let e of App.UI.activePendingEvents.slice(0,2)){e.alarmState="triggered";await App.DB.update("events",e)}await App.UI.navigateTo("viewDashboard")}')
        data['alarm_badges']=ev('()=>({header:document.getElementById("headerAlarmBadge").textContent,metric:document.getElementById("metricUnacknowledged").textContent,tablet:document.getElementById("tabletAlarmsCount").textContent,banner:document.getElementById("bannerActiveAlarmsText").textContent})')
        shot('estado_alarmes_ativos_celular.png')
        ev('window.scrollTo(0,650)');page.wait_for_timeout(60)
        data['banner_scrolled']=ev('()=>({header:document.querySelector(".app-header").getBoundingClientRect().toJSON(),banner:document.getElementById("mobileActiveAlarmsBanner").getBoundingClientRect().toJSON()})')
        shot('estado_banner_rolagem.png')
        page.set_viewport_size({'width':1024,'height':768})
        ev('App.UI.applyResponsiveLayoutMode("tablet",false)');ev('App.UI.navigateTo("viewDashboard")')
        shot('estado_alarmes_ativos_tablet.png')
        ev('App.UI.navigateTo("viewPendingEvents")')
        data['detail_default']=ev('()=>({selected:App.UI.selectedDetailEventId,tab:App.UI.selectedDetailTab,text:document.getElementById("pendingDetailPane").innerText})')
        shot('estado_detalhe_tablet_inicial.png')
        page.evaluate('(id)=>App.UI.selectPendingDetailEvent(id)',event_id)
        data['detail_clicked']=ev('()=>({tab:App.UI.selectedDetailTab,text:document.getElementById("pendingDetailPane").innerText})')
        shot('estado_detalhe_tablet_apos_clique.png')
        ev('App.UI.navigateTo("viewCadastros")');ev('App.UI.switchCadastrosCategory("tags")')
        data['category_before']=ev('()=>({active:App.UI.activeCadastrosCategory,current:App.UI.currentCadastrosCategory||null})')
        ev('App.UI.applyResponsiveLayoutMode("tablet",false)')
        data['category_after']=ev('()=>({active:App.UI.activeCadastrosCategory,current:App.UI.currentCadastrosCategory||null})')
        page.set_viewport_size({'width':390,'height':844})
        ev('App.UI.applyResponsiveLayoutMode("mobile",false)');ev('App.UI.navigateTo("viewPendingEvents")')
        ev('document.getElementById("btnToggleFilters").focus()')
        page.evaluate('(id)=>App.UI.showCompleteModal(id)',event_id)
        data['focus_open']=ev('()=>({id:document.activeElement.id,inModal:!!document.activeElement.closest(".modal-overlay")})')
        page.keyboard.press('Tab')
        data['focus_tab']=ev('()=>({id:document.activeElement.id,inModal:!!document.activeElement.closest(".modal-overlay")})')
        page.keyboard.press('Escape')
        data['focus_escape']=ev('()=>({id:document.activeElement.id,modals:document.querySelectorAll(".modal-overlay.active").length})')
        ev('document.getElementById("btnToggleMobileMenu").focus()')
        focus=[]
        for _ in range(22):
            page.keyboard.press('Tab');focus.append(ev('()=>({id:document.activeElement.id,drawer:!!document.activeElement.closest("#appMobileDrawer"),x:document.activeElement.getBoundingClientRect().x})'))
        data['tab_sequence_drawer_closed']=focus
        themes={}
        for theme in ['dark','light','industrial']:
            page.evaluate('(t)=>App.UI.applyTheme(t)',theme)
            page.wait_for_timeout(250)
            themes[theme]=ev('()=>{const x=s=>{let e=document.querySelector(s);let c=getComputedStyle(e);return {color:c.color,bg:c.backgroundColor,font:c.fontSize}};return {muted:x(".card-subtitle"),nav:x(".app-nav .nav-item"),primary:x(".btn-primary"),body:x("body"),surface:getComputedStyle(document.body).getPropertyValue("--bg-surface"),overdue:x(".event-countdown")}}')
        data['theme_colors']=themes
        ev('App.UI.applyTheme("light")');page.wait_for_timeout(250);shot('estado_tema_claro_celular.png')
        ev('App.UI.applyTheme("industrial")');page.wait_for_timeout(250);shot('estado_tema_industrial_celular.png')
        ev('App.UI.applyTheme("dark")')
        ev('async()=>{let e=App.UI.activePendingEvents[0];e.description="Atividade operacional longa para verificar quebra de texto e preservação das ações essenciais. ".repeat(10);e.notes="Observações com várias linhas.\\n".repeat(8);await App.DB.update("events",e);await App.UI.renderPendingEvents()}')
        shot('estado_texto_longo_celular.png')
        # Validate real downloads through the GUI; keep generated test files inside audit only.
        ev('App.UI.navigateTo("viewBackup")')
        downloads=[]
        for button in ['btnExportJSON','btnExportCSVAllPending','btnExportCSVAllCompleted','btnExportCSVCadastros']:
            with page.expect_download() as download_info:page.locator('#'+button).click()
            download=download_info.value
            target=OUT/'dados'/('teste_'+download.suggested_filename)
            download.save_as(str(target))
            downloads.append({'button':button,'name':download.suggested_filename,'saved':target.name,'bytes':target.stat().st_size})
        data['downloads']=downloads
        # Check all seven preference values survive actual reload in this temporary profile.
        persistence=[]
        for mode in ['auto','compact','mobile','tablet','conventional','widescreen','ultrawide']:
            page.evaluate('(m)=>App.UI.applyResponsiveLayoutMode(m,true)',mode)
            page.reload();page.wait_for_function('App.AlarmEngine.intervalId!==null')
            ev('App.AlarmEngine.stop()')
            persistence.append(ev('async()=>({requested:(await App.Service.getSettings()).responsiveLayoutMode,loaded:App.UI.responsiveLayoutMode})'))
        data['mode_persistence']=persistence
        ev('App.UI.applyResponsiveLayoutMode("mobile",false)');ev('App.UI.navigateTo("viewBackup")')
        data['demo_before']=ev('async()=>({events:(await App.DB.getAll("events")).length,uos:(await App.DB.getAll("operationalUnits")).length})')
        page.locator('#btnLoadDemoData').click();page.locator('#btnAcceptConfirm').click()
        page.wait_for_timeout(400)
        data['demo_after']=ev('async()=>({events:(await App.DB.getAll("events")).length,uos:(await App.DB.getAll("operationalUnits")).length,toasts:document.getElementById("toastContainer").textContent.trim()})')
        shot('estado_botao_demo_base_esvaziada.png')
        ev('App.UI.navigateTo("viewPendingEvents")');shot('estado_pendentes_vazio.png')
        ev('App.UI.navigateTo("viewDashboard")');shot('estado_painel_vazio.png')
        # Synthetic scale test; not a device performance benchmark.
        page.set_viewport_size({'width':1440,'height':1000})
        ev('App.UI.applyResponsiveLayoutMode("auto",false)')
        data['render_500']=ev('async()=>{await App.Service.loadDemoData();let src=(await App.DB.getAll("events")).find(e=>e.status==="pendente");await new Promise((res,rej)=>{let t=App.DB.db.transaction("events","readwrite"),s=t.objectStore("events");for(let i=0;i<500;i++)s.add({...src,id:"audit-scale-"+i,hasAlarm:false});t.oncomplete=res;t.onerror=rej});let start=performance.now();await App.UI.navigateTo("viewPendingEvents");return {ms:Math.round(performance.now()-start),cards:document.querySelectorAll("#containerPendingCards .event-card").length,rows:document.querySelectorAll("#tbodyPendingEvents tr").length}}')
        data['captures']=shots
        (OUT/'dados/testes_estados.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
        context.close();browser.close()
        print('ESTADOS_CONCLUIDOS',len(shots),'capturas',flush=True)
if __name__=='__main__':main()
