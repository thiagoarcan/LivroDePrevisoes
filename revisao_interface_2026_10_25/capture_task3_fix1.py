"""Additional visual review evidence for every scoped Task 3 fix."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from browser_support import *
from playwright.sync_api import sync_playwright
out=ROOT/'revisao_interface_2026_10_25/resultados';temp,path=build_temporary_html();captured=[];measurements=[]
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True);c,page,errors=open_app(b,path)
 def capture(name,full=False):
  page.screenshot(path=str(out/f'task3-fix1-{name}.png'),full_page=full,animations='disabled',timeout=15000);captured.append(f'task3-fix1-{name}.png')
 def size(width,height=1000):
  page.set_viewport_size({'width':width,'height':height});page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)')
 for width in [768,1024,1440,1920,3440]:
  size(width)
  for view in ['viewDashboard','viewConfigAlerts']:
   page.evaluate('(v)=>App.UI.navigateTo(v)',view);page.evaluate('window.scrollTo(0,0)');capture(f'{width}-{view}')
  measurements.append(page.evaluate('''()=>{const r=s=>document.querySelector(s).getBoundingClientRect().toJSON();return{width:innerWidth,view:App.UI.currentView,notice:r('#viewConfigAlerts>.notice-banner'),form:r('#formAlertSettings'),preview:r('#settingsPreviewPanel'),console:r('#headerActiveConsole')}}'''))
 size(390,844)
 event_id=page.evaluate('App.UI.getPresentationState().snapshot.events.find(e=>e.status==="pendente").id')
 for theme in ['dark','light','industrial']:
  page.evaluate('(t)=>App.UI.applyTheme(t)',theme)
  for modal in ['confirm','complete','dependency']:
   if modal=='confirm':page.evaluate('App.UI.showConfirmModal("Excluir previsão","Confirme a exclusão do registro.",()=>{})')
   elif modal=='complete':page.evaluate('(id)=>App.UI.showCompleteModal(id)',event_id)
   else:page.evaluate('App.UI.showDependencyModal("Vínculos preservados",["2 UOs vinculadas ao duto"],()=>{})')
   capture(f'modal-{modal}-{theme}-390');page.keyboard.press('Escape')
 page.evaluate('App.UI.applyTheme("light")')
 for width in [320,390]:
  size(width,844);page.evaluate('App.UI.navigateTo("viewBackup")')
  snapshot=page.evaluate('async()=>JSON.stringify(await App.Backup.createSnapshot())')
  page.locator('#inputImportBackupFile').set_input_files({'name':'backup-operacional-console-C04-2026-10-25-arquivo-com-nome-completo.json','mimeType':'application/json','buffer':snapshot.encode()})
  page.locator('#inputImportBackupFile').scroll_into_view_if_needed();capture(f'backup-file-{width}')
 for width in [390,1024,1440]:
  size(width,844 if width==390 else 1000)
  for view in ['viewDiagnostic','viewCadastros','viewConfigColors']:
   page.evaluate('(v)=>App.UI.navigateTo(v)',view)
   if view=='viewCadastros':page.evaluate('App.UI.switchCadastrosCategory("tags");App.Presentation.refresh("catalog")')
   page.evaluate('window.scrollTo(0,0)');capture(f'{view}-{width}')
 size(390,844);page.evaluate('App.UI.navigateTo("viewCompletedEvents")');page.evaluate('window.scrollTo(0,0)');capture('completed-filters-collapsed')
 page.locator('#completedFilters summary').click();capture('completed-filters-open')
 size(3440);page.evaluate('App.UI.navigateTo("viewCadastros")')
 for category,method,store,name in [('pipelines','editPipeline','pipelines','OSCAN'),('uos','editUO','operationalUnits','TEDEP')]:
  page.evaluate('''async({category,method,store,name})=>{App.UI.switchCadastrosCategory(category);let item=(await App.DB.getAll(store)).find(x=>x.name===name);await App.UI[method](item.id)}''',{'category':category,'method':method,'store':store,'name':name})
  capture('junction-'+category)
 assert not errors,errors
 c.close();b.close()
temp.cleanup();(out/'task3-fix1-captures.json').write_text(json.dumps({'screenshots':captured,'measurements':measurements},ensure_ascii=False,indent=2),encoding='utf-8')
print('Review screenshots:',len(captured),'page errors:',len(errors))
