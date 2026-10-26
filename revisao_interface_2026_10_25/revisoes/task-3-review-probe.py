import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tests'))
from browser_support import build_temporary_html,open_app
from playwright.sync_api import sync_playwright

OUT=Path(__file__).parent
temp,path=build_temporary_html()
result={}
rects="""selectors=>Object.fromEntries(selectors.map(s=>{let e=document.querySelector(s),r=e.getBoundingClientRect(),c=getComputedStyle(e);return [s,{x:r.x,y:r.y,width:r.width,height:r.height,display:c.display,columns:c.gridTemplateColumns,rows:c.gridTemplateRows}]}))"""
with sync_playwright() as p:
    b=p.chromium.launch(channel='msedge',headless=True)
    c,page,errors=open_app(b,path,width=1920,height=1000)
    for width in [1920,2560,3440]:
        page.set_viewport_size({'width':width,'height':1000})
        page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false);App.UI.navigateTo("viewDashboard")')
        page.wait_for_function('document.querySelector("#dashboardContextPanel meter")')
        result[f'dashboard_{width}']=page.evaluate(rects,['#spotlightCard','#cardDashboardUrgent','#dashboardContextPanel','#dashboardSelectedDetail','.dashboard-metrics'])
        page.evaluate('App.UI.navigateTo("viewConfigAlerts")')
        page.wait_for_function('document.getElementById("viewConfigAlerts").classList.contains("active")')
        result[f'alerts_{width}']=page.evaluate(rects,['#viewConfigAlerts>.notice-banner','#viewConfigAlerts>.card','#settingsPreviewPanel','#formAlertSettings .form-grid','#inputDefaultLeadTime'])
        if width in [1920,3440]:page.screenshot(path=str(OUT/f'review-alerts-{width}.png'),full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false);App.UI.navigateTo("viewBackup")')
    result['backup_390']=page.evaluate(rects,['.backup-operations','.backup-operations>div:first-child','.backup-operations>div:last-child','#inputImportBackupFile'])
    page.evaluate('App.UI.navigateTo("viewDiagnostic")')
    page.wait_for_function('document.querySelectorAll("#tbodyDiagCollections tr").length>1')
    result['diagnostic_390']=page.evaluate(rects,['.diagnostic-collections','#tbodyDiagCollections tr:first-child td:nth-child(2)','#tbodyDiagCollections tr:nth-child(7)'])
    result['diagnostic_390']['sample']=page.locator('#tbodyDiagCollections tr:first-child').inner_text()
    page.screenshot(path=str(OUT/'review-diagnostic-390.png'),full_page=True)
    page.set_viewport_size({'width':1920,'height':1000})
    page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false);App.UI.navigateTo("viewCadastros")')
    page.wait_for_function('document.querySelector("#tableConsoles tbody tr")')
    result['relations']=page.evaluate('''async()=>{
      let s=App.UI.getPresentationState().snapshot,pipe=s.pipelines.find(x=>x.name==='OSCAN'),uo=s.operationalUnits.find(x=>x.name==='REFAP');
      App.UI.switchCadastrosCategory('pipelines');await App.UI.editPipeline(pipe.id);App.Presentation.refresh('probe');
      let pipelinePanel=document.getElementById('cadastrosRelationsPanel').innerText;
      App.UI.switchCadastrosCategory('uos');await App.UI.editUO(uo.id);App.Presentation.refresh('probe');
      return {pipeline:pipe,links:s.pipelineOperationalUnits.filter(x=>x.pipelineId===pipe.id),pipelinePanel,uoPanel:document.getElementById('cadastrosRelationsPanel').innerText};
    }''')
    page.locator('[data-cat="tags"]').click()
    page.locator('[data-catalog-new="formEquipmentTag"]').click()
    page.locator('#inputTagCode').fill('TAG-PROBE-123')
    result['tag_draft']=page.locator('#cadastrosRelationsPanel').inner_text()
    result['header_console']=page.evaluate('''()=>{let e=document.getElementById('headerActiveConsole'),s=getComputedStyle(e),x=document.createElement('canvas').getContext('2d');x.font=s.font;return {text:e.selectedOptions[0].text,controlWidth:e.getBoundingClientRect().width,textWidth:x.measureText(e.selectedOptions[0].text).width,paddingLeft:s.paddingLeft,paddingRight:s.paddingRight}}''')
    page.screenshot(path=str(OUT/'review-header-1920.png'))
    page.set_viewport_size({'width':390,'height':844})
    page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false);App.UI.navigateTo("viewCompletedEvents")')
    page.wait_for_function('document.querySelector("#containerCompletedCards .completed-event-card")')
    result['completed_mobile']=page.evaluate(rects,['#viewCompletedEvents>.events-toolbar','#containerCompletedCards'])
    page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false);App.UI.applyTheme("light");App.UI.showConfirmModal("Excluir previsão", "Confirma a exclusão desta previsão?",()=>{})')
    result['light_modal']=page.evaluate('''()=>{let e=document.querySelector('#modalConfirm .modal-box'),s=getComputedStyle(e);return {background:s.backgroundColor,color:s.color,elevated:s.getPropertyValue('--bg-elevated'),surface:s.getPropertyValue('--bg-surface')}}''')
    page.screenshot(path=str(OUT/'review-modal-light-390.png'))
    page.evaluate('App.UI.closeModal("modalConfirm");App.UI.showDependencyModal("Dependências",["1 evento"],()=>{})')
    result['dependency_390']=page.evaluate(rects,['#modalDependency .notice-banner','#modalDependency .notice-banner strong'])
    page.screenshot(path=str(OUT/'review-dependency-light-390.png'))
    result['errors']=errors
    c.close();b.close()
temp.cleanup()
(OUT/'task-3-review-probe.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=True,indent=2))
