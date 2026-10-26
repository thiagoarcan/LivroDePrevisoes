"""Controller edge cases against real temporary browser storage."""
import sys,unittest
from playwright.sync_api import sync_playwright
from browser_support import ROOT,build_temporary_html,open_app

class UIController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp,cls.path=build_temporary_html();cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(channel='msedge',headless=True)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.temp.cleanup()
    def setUp(self):self.context,self.page,self.errors=open_app(self.browser,self.path)
    def tearDown(self):self.context.close()
    def ev(self,code):return self.page.evaluate(code)
    def test_async_confirmation_is_single_and_cannot_escape(self):
        self.ev('()=>{window.calls=0;App.UI.showConfirmModal("Operação","Aguarde",async()=>{calls++;await new Promise(r=>window.finish=r)});document.getElementById("btnAcceptConfirm").click();document.getElementById("btnAcceptConfirm").click()}')
        self.page.keyboard.press('Escape')
        self.assertEqual(self.ev('calls'),1);self.assertTrue(self.ev('document.getElementById("modalConfirm").classList.contains("active")'))
        self.ev('finish()');self.page.wait_for_selector('#modalConfirm.active',state='hidden')
    def test_alarm_snooze_escape_only_closes_top(self):
        opened=self.ev('async()=>{const e=(await App.DB.getAll("events")).find(x=>x.status==="pendente");await App.UI.showAlarmModal(e);document.getElementById("btnAlarmSnoozePrompt").click();return document.getElementById("modalSnooze").classList.contains("active")}')
        self.assertTrue(opened)
        self.page.keyboard.press('Escape')
        self.assertFalse(self.ev('document.getElementById("modalSnooze").classList.contains("active")'))
        self.assertTrue(self.ev('document.getElementById("modalAlarmTrigger").classList.contains("active")'))
        self.assertTrue(self.ev('!!document.activeElement.closest("#modalAlarmTrigger")'))
    def test_pagination_keeps_all_data_but_one_modality_and_fifty_nodes(self):
        result=self.ev('''async()=>{const e=(await App.DB.getAll('events')).find(x=>x.status==='pendente'&&x.consoleId===App.UI.activeConsoleId);await App.DB.atomic(['events'],draft=>{draft.events=Array.from({length:503},(_,i)=>({...e,id:'page-'+i,description:'Evento '+i}));});await App.UI.navigateTo('viewPendingEvents');return {all:App.UI.activePendingEvents.length,cards:document.querySelectorAll('#containerPendingCards .event-card').length,rows:document.querySelectorAll('#tbodyPendingEvents tr').length,label:document.getElementById('pendingPagination').textContent}}''')
        self.assertEqual(result['all'],503);self.assertEqual(result['cards'],50);self.assertEqual(result['rows'],0);self.assertIn('503',result['label'])
        self.page.locator('#pendingPagination button').last.click();self.page.wait_for_function('document.querySelector("#containerPendingCards .event-card").dataset.eventId===App.UI.activePendingEvents[50].id')
        self.page.locator('#btnViewTable').click();self.page.wait_for_function('document.querySelectorAll("#tbodyPendingEvents tr").length===50')
        self.assertEqual(self.ev('document.querySelectorAll("#containerPendingCards .event-card").length'),0)
    def test_dashboard_urgent_list_is_bounded(self):
        count=self.ev('''async()=>{const e=(await App.DB.getAll('events')).find(x=>x.status==='pendente');await App.DB.atomic(['events'],draft=>{draft.events=Array.from({length:503},(_,i)=>({...e,id:'urgent-'+i,scheduledAt:new Date(Date.now()-60000).toISOString()}));});await App.UI.renderDashboard();return document.querySelectorAll('#tbodyDashboardUrgent tr').length}''')
        self.assertLessEqual(count,50)
    def test_idle_timers_do_not_read_or_render_pages(self):
        result=self.ev('''async()=>{await App.UI.renderDashboard();const snapshot=App.DB.snapshot,render=App.UI.renderDashboard;let reads=0,renders=0;App.DB.snapshot=(...a)=>{reads++;return snapshot.apply(App.DB,a)};App.UI.renderDashboard=(...a)=>{renders++;return render.apply(App.UI,a)};try{for(let i=0;i<5;i++)await App.UI.updateLiveTimers();return {reads,renders}}finally{App.DB.snapshot=snapshot;App.UI.renderDashboard=render}}''')
        self.assertEqual(result,{'reads':0,'renders':0})
    def test_zero_settings_and_event_alarm_reopen_without_defaults(self):
        result=self.ev('''async()=>{const settings=await App.Service.getSettings();settings.defaultLeadTimeMinutes=0;settings.soundVolume=0;settings.maxRepeats=0;await App.Service.saveSettings(settings);await App.UI.navigateTo('viewConfigAlerts');const controls=['inputDefaultLeadTime','rangeSoundVolume','inputSettingMaxRepeats'].map(id=>document.getElementById(id).value);const e=(await App.DB.getAll('events')).find(x=>x.status==='pendente');e.alarmMinutesBefore=0;e.alarmMaxRepeats=0;await App.DB.update('events',e);await App.UI.editEvent(e.id);return {controls,event:[document.getElementById('inputEventAlarmLeadTime').value,document.getElementById('inputEventAlertMaxRepeats').value]}}''')
        self.assertEqual(result,{'controls':['0','0','0'],'event':['0','0']})
    def test_completed_metric_uses_local_day_and_can_be_cleared(self):
        result=self.ev('''async()=>{const now=Date.now;Date.now=()=>new Date('2026-10-26T01:00:00Z').getTime();try{const e=(await App.DB.getAll('events')).find(x=>x.status==='concluido');await App.DB.atomic(['events'],d=>{d.events=[{...e,id:'local-today',completedAt:'2026-10-26T00:30:00Z'},{...e,id:'local-yesterday',completedAt:'2026-10-25T01:30:00Z'}]});await App.UI.renderDashboard();document.querySelector('[data-filter=completed]').click();await App.UI.renderCompletedEvents();const before=App.UI.activeCompletedEvents.length;document.getElementById('btnClearCompletedScope')?.click();await App.UI.renderCompletedEvents();return {metric:document.getElementById('metricCompletedToday').textContent,before,after:App.UI.activeCompletedEvents.length}}finally{Date.now=now}}''')
        self.assertEqual(result,{'metric':'1','before':1,'after':2})
    def test_fullscreen_drawing_escape_returns_to_form(self):
        self.ev('App.UI.navigateTo("viewNewEvent")');self.page.locator('#btnToggleStylusCanvas').click();self.page.locator('#btnFullscreenStylusCanvas').click()
        self.assertTrue(self.ev('!!document.activeElement.closest("#boxStylusCanvas")'))
        self.page.keyboard.press('Escape');self.assertFalse(self.ev('document.getElementById("boxStylusCanvas").classList.contains("fullscreen-lousa")'))
    def test_declined_import_reports_conflict_without_success(self):
        result=self.ev('''async()=>{const backup=await App.Backup.createSnapshot(),original=App.Backup.importJSON;App.Backup.importJSON=async()=>({applied:false,inserted:0,updated:0,skipped:1,conflicts:[{store:'events',id:'x',reason:'Revisão conflitante'}]});try{App.UI.showImportSummaryModal(backup);document.getElementById('btnConfirmImportSummary').click();await new Promise(r=>setTimeout(r,30));return {active:document.getElementById('modalImportSummary').classList.contains('active'),message:document.getElementById('importSummaryCounts').textContent,success:[...document.querySelectorAll('.toast-success')].some(x=>x.textContent.includes('Importação'))}}finally{App.Backup.importJSON=original}}''')
        self.assertTrue(result['active']);self.assertIn('Revisão conflitante',result['message']);self.assertFalse(result['success'])

    def test_complete_identity_survives_interleaved_alarm(self):
        result=self.ev('''async()=>{
          const [a,b]=(await App.DB.getAll('events')).filter(e=>e.status==='pendente');
          const original=App.DB.getAll;let release,reached,once=true;const ready=new Promise(r=>reached=r);
          App.DB.getAll=function(store){if(store==='consoles'&&once){once=false;reached();return new Promise(resolve=>release=()=>original.call(App.DB,store).then(resolve));}return original.call(App.DB,store)};
          try{const pending=App.UI.showCompleteModal(a.id);await ready;await App.UI.showAlarmModal(b);release();await pending;
            const bound=App.UI.modalStack.find(x=>x.element.id==='modalCompleteEvent')?.event?.id;
            document.getElementById('btnConfirmCompleteModal').click();while(App.UI.modalBusy.has('modalCompleteEvent'))await new Promise(r=>setTimeout(r,5));
            return {bound,expected:a.id,a:(await App.DB.get('events',a.id)).status,b:(await App.DB.get('events',b.id)).status};
          }finally{App.DB.getAll=original;}
        }''')
        self.assertEqual(result['bound'],result['expected']);self.assertEqual(result['a'],'concluido');self.assertEqual(result['b'],'pendente')

    def test_newer_request_wins_for_every_event_dialog(self):
        result=self.ev('''async()=>{
          const [a,b]=(await App.DB.getAll('events')).filter(e=>e.status==='pendente'),results=[];
          const cases=[['showCompleteModal','modalCompleteEvent'],['showReopenModal','modalReopenEvent'],['showSnoozeModal','modalSnooze'],['showDetailsModal','modalEventDetails'],['openEventActionSheet','modalEventActionSheet'],['showAlarmModal','modalAlarmTrigger']];
          for(const [method,modal] of cases){
            const originalGet=App.DB.get,originalAll=App.DB.getAll;let release,reached,once=true;const ready=new Promise(r=>reached=r);
            const delay=run=>{once=false;reached();return new Promise(resolve=>release=()=>run().then(resolve));};
            App.DB.get=function(store,id){if(method!=='showAlarmModal'&&once&&store==='events'&&id===a.id)return delay(()=>originalGet.call(App.DB,store,id));return originalGet.call(App.DB,store,id)};
            App.DB.getAll=function(store){if(method==='showAlarmModal'&&once&&store==='consoles')return delay(()=>originalAll.call(App.DB,store));return originalAll.call(App.DB,store)};
            try{const slow=App.UI[method](method==='showAlarmModal'?a:a.id);await ready;await App.UI[method](method==='showAlarmModal'?b:b.id);await release();await slow;await new Promise(r=>setTimeout(r,20));
              const textId={showCompleteModal:'completeModalEventDesc',showDetailsModal:'detailsModalDescription',openEventActionSheet:'actionSheetEventTitle',showAlarmModal:'alarmModalDescription'}[method];
              results.push({method,bound:App.UI.modalStack.find(x=>x.element.id===modal)?.event?.id,expected:b.id,textCorrect:!textId || document.getElementById(textId).textContent===b.description});App.UI.closeModal(modal);
            }finally{App.DB.get=originalGet;App.DB.getAll=originalAll;}
          }return results;
        }''')
        self.assertTrue(all(x.get('bound')==x['expected'] and x['textCorrect'] for x in result),result)

    def test_cancelled_loading_dialog_does_not_open_later(self):
        result=self.ev('''async()=>{
          const e=(await App.DB.getAll('events')).find(x=>x.status==='pendente'),original=App.DB.get;let release,reached;const ready=new Promise(r=>reached=r);
          App.DB.get=function(store,id){if(store==='events'&&id===e.id){reached();return new Promise(resolve=>release=()=>original.call(App.DB,store,id).then(resolve))}return original.call(App.DB,store,id)};
          try{const pending=App.UI.showCompleteModal(e.id);await ready;App.UI.closeModal('modalCompleteEvent');release();await pending;return document.getElementById('modalCompleteEvent').classList.contains('active');}finally{App.DB.get=original;}
        }''')
        self.assertFalse(result)

    def test_completed_modality_changes_preserve_page_filter_selection_and_expansion(self):
        self.page.set_viewport_size({'width':390,'height':844})
        self.ev('''async()=>{const original=(await App.DB.getAll('events')).find(e=>e.status==='concluido');await App.DB.atomic(['events'],d=>{d.events=Array.from({length:110},(_,i)=>({...original,id:'completed-'+String(i).padStart(3,'0'),description:'Mudança '+i}));});await App.UI.applyResponsiveLayoutMode('auto',false);await App.UI.navigateTo('viewCompletedEvents');document.getElementById('inputSearchCompleted').value='Mudança';await App.UI.renderCompletedEvents();App.UI.pages.completed=2;await App.UI.renderCompletedEvents();App.UI.toggleCompletedCard(document.querySelector('.completed-event-card'));}''')
        selected=self.ev('App.UI.selectedCompletedEventId')
        for width,mode,expected in [(1440,None,'table'),(390,None,'cards'),(1440,'mobile','cards'),(1440,'conventional','table'),(1440,'mobile','cards')]:
            self.page.set_viewport_size({'width':width,'height':1000})
            if mode:self.page.evaluate('(mode)=>App.UI.applyResponsiveLayoutMode(mode,false)',mode)
            self.page.wait_for_function('(mode)=>mode==="cards"?document.querySelectorAll(".completed-event-card").length===50:document.querySelectorAll("#tbodyCompletedEvents tr").length===50',arg=expected)
            state=self.ev('''()=>({page:App.UI.pages.completed,filter:document.getElementById('inputSearchCompleted').value,selection:App.UI.selectedCompletedEventId,cards:document.querySelectorAll('.completed-event-card').length,rows:document.querySelectorAll('#tbodyCompletedEvents tr').length,expanded:document.querySelector('.completed-event-card')?.getAttribute('aria-expanded')})''')
            self.assertEqual(state['page'],2);self.assertEqual(state['filter'],'Mudança');self.assertEqual(state['selection'],selected)
            self.assertEqual((state['cards'],state['rows']),(50,0) if expected=='cards' else (0,50))
            if expected=='cards':self.assertEqual(state['expanded'],'true')

    def test_pending_modality_and_page_survive_resize_and_manual_tiers(self):
        self.ev('''async()=>{const original=(await App.DB.getAll('events')).find(e=>e.status==='pendente'&&e.consoleId===App.UI.activeConsoleId);await App.DB.atomic(['events'],d=>{d.events=Array.from({length:110},(_,i)=>({...original,id:'pending-'+String(i).padStart(3,'0'),description:'Manter '+i}));});await App.UI.navigateTo('viewPendingEvents');document.getElementById('inputSearchPending').value='Manter';await App.UI.renderPendingEvents();App.UI.pages.pending=2;await App.UI.renderPendingEvents();await App.UI.selectPendingDetailEvent(App.UI.activePendingEvents[50].id)}''')
        selected=self.ev('App.UI.selectedDetailEventId')
        self.ev('async()=>{App.UI.viewMode="table";App.UI.updateViewModeUI();await App.UI.renderPendingEvents()}')
        for width,mode in [(390,'auto'),(1440,'mobile'),(1440,'conventional')]:
            self.page.set_viewport_size({'width':width,'height':1000});self.page.evaluate('(mode)=>App.UI.applyResponsiveLayoutMode(mode,false)',mode)
            state=self.ev('''()=>({page:App.UI.pages.pending,selection:App.UI.selectedDetailEventId,filter:document.getElementById('inputSearchPending').value,cards:document.querySelectorAll('#containerPendingCards .event-card').length,rows:document.querySelectorAll('#tbodyPendingEvents tr').length})''')
            self.assertEqual(state,{'page':2,'selection':selected,'filter':'Manter','cards':0,'rows':50})
            self.assertTrue(self.ev('!!document.getElementById("containerPendingTable").getClientRects().length'))

    def test_five_catalog_toggles_publish_committed_snapshot(self):
        result=self.ev('''async()=>{
          await App.UI.navigateTo('viewCadastros');const results=[];
          for(const [method,store] of [['toggleConsoleActive','consoles'],['togglePipelineActive','pipelines'],['toggleUOActive','operationalUnits'],['toggleEquipmentTypeActive','equipmentTypes'],['toggleEquipmentTagActive','equipmentTags']]){
            const original=(await App.DB.getAll(store))[0];let observed=[];
            const listener=e=>observed.push({reason:e.detail.reason,value:App.UI.getPresentationState().snapshot[store].find(x=>x.id===original.id)?.active});window.addEventListener('app-ui-update',listener);
            try{await App.UI[method](original.id);results.push({method,db:(await App.DB.get(store,original.id)).active,cache:App.UI.getPresentationState().snapshot[store].find(x=>x.id===original.id)?.active,observed});await App.UI[method](original.id);}finally{window.removeEventListener('app-ui-update',listener);}
          }return results;
        }''')
        for x in result:
            self.assertFalse(x['db'],x);self.assertFalse(x['cache'],x);self.assertTrue(any(e['value'] is False for e in x['observed']),x)

    def test_catalog_forms_publish_create_update_and_confirmed_delete(self):
        self.ev('''async()=>{await App.UI.navigateTo('viewCadastros');window.catalogSignals=[];window.addEventListener('app-ui-update',e=>{if(e.detail.reason==='catalog')catalogSignals.push(structuredClone(App.UI.getPresentationState().snapshot))});}''')
        configs=[('consoles','formConsole','inputConsoleName','editConsole','deleteConsole','name'),('pipelines','formPipeline','inputPipelineName','editPipeline','deletePipeline','name'),('operationalUnits','formUO','inputUOName','editUO','deleteUO','name'),('equipmentTypes','formEquipmentType','inputEquipmentTypeName','editEquipmentType','deleteEquipmentType','name'),('equipmentTags','formEquipmentTag','inputTagCode','editEquipmentTag','deleteEquipmentTag','tag')]
        for store,form,field,edit,delete,key in configs:
            with self.subTest(store=store):
                name='CRUD-'+store
                self.page.evaluate('''async({store,form,field,name})=>{
                  const s=await App.DB.snapshot();
                  if(store==='pipelines'){document.getElementById('selectPipelineConsole').value=App.UI.activeConsoleId;[...document.querySelectorAll('#boxPipelineUOs input')].forEach((x,i)=>x.checked=i<2);}
                  if(store==='equipmentTypes')document.getElementById('selectEquipmentTypeUO').value=s.operationalUnits[0].id;
                  if(store==='equipmentTags'){const type=s.equipmentTypes[0];document.getElementById('selectTagUO').value=type.uoId;await App.UI.loadEquipmentTypeOptions(type.uoId,'selectTagType');document.getElementById('selectTagType').value=type.id;}
                  document.getElementById(field).value=name;document.getElementById(form).requestSubmit();
                }''',{'store':store,'form':form,'field':field,'name':name})
                self.page.wait_for_function('''({store,key,name})=>catalogSignals.some(s=>s[store].some(x=>x[key]===name))''',arg={'store':store,'key':key,'name':name})
                row=self.page.evaluate('''async({store,key,name})=>(await App.DB.getAll(store)).find(x=>x[key]===name)''',{'store':store,'key':key,'name':name})
                self.page.evaluate('''async({edit,id,field,form,name})=>{await App.UI[edit](id);document.getElementById(field).value=name;document.getElementById(form).requestSubmit()}''',{'edit':edit,'id':row['id'],'field':field,'form':form,'name':name+'-edit'})
                self.page.wait_for_function('''({store,key,name})=>catalogSignals.some(s=>s[store].some(x=>x[key]===name))''',arg={'store':store,'key':key,'name':name+'-edit'})
                state=self.page.evaluate('''async({store,id,key})=>({db:(await App.DB.get(store,id))[key],cache:App.UI.getPresentationState().snapshot[store].find(x=>x.id===id)[key]})''',{'store':store,'id':row['id'],'key':key})
                self.assertEqual(state,{'db':name+'-edit','cache':name+'-edit'})
                self.page.evaluate('''async({method,id})=>{catalogSignals=[];await App.UI[method](id)}''',{'method':delete,'id':row['id']})
                self.assertEqual(self.ev('catalogSignals.length'),0)
                self.page.locator('#btnAcceptConfirm').click()
                self.page.wait_for_function('''({store,id})=>catalogSignals.some(s=>!s[store].some(x=>x.id===id))''',arg={'store':store,'id':row['id']})
                self.assertIsNone(self.page.evaluate('''async({store,id})=>(await App.DB.get(store,id))||null''',{'store':store,'id':row['id']}))
                self.page.wait_for_function('!App.UI.modalBusy.has("modalConfirm")')

    def test_pinch_zoom_does_not_claim_keyboard_and_editable_shrink_does(self):
        self.page.set_viewport_size({'width':390,'height':844});self.ev('App.UI.navigateTo("viewNewEvent")')
        cdp=self.context.new_cdp_session(self.page);cdp.send('Emulation.setPageScaleFactor',{'pageScaleFactor':2})
        self.page.wait_for_function('visualViewport.scale===2');self.page.wait_for_timeout(50)
        self.assertFalse(self.ev('document.body.classList.contains("keyboard-open")'))
        cdp.send('Emulation.setPageScaleFactor',{'pageScaleFactor':1});self.page.wait_for_function('visualViewport.scale===1')
        result=self.ev('''()=>{
          const viewport=visualViewport,originalHeight=Object.getOwnPropertyDescriptor(viewport,'height'),originalScale=Object.getOwnPropertyDescriptor(viewport,'scale');
          const update=()=>viewport.dispatchEvent(new Event('resize'));
          try{document.getElementById('inputEventDescription').focus();Object.defineProperty(viewport,'height',{configurable:true,value:innerHeight*.5});Object.defineProperty(viewport,'scale',{configurable:true,value:1});update();const keyboard=document.body.classList.contains('keyboard-open');Object.defineProperty(viewport,'scale',{configurable:true,value:2});update();const zoom=document.body.classList.contains('keyboard-open');document.activeElement.blur();Object.defineProperty(viewport,'scale',{configurable:true,value:1});update();return {keyboard,zoom,blur:document.body.classList.contains('keyboard-open')};}
          finally{if(originalHeight)Object.defineProperty(viewport,'height',originalHeight);else delete viewport.height;if(originalScale)Object.defineProperty(viewport,'scale',originalScale);else delete viewport.scale;update();}
        }''')
        self.assertEqual(result,{'keyboard':True,'zoom':False,'blur':False})

    def test_delayed_catalog_confirmation_publishes_only_after_commit(self):
        result=self.ev('''async()=>{
          const s=await App.DB.snapshot();const row=await App.Service.savePipeline({name:'EXCLUIR-COMMIT',consoleId:App.UI.activeConsoleId,uoIds:s.operationalUnits.slice(0,2).map(x=>x.id)});await App.UI.navigateTo('viewCadastros');
          const original=App.Service.deletePipeline;let release;const gate=new Promise(r=>release=r),signals=[];
          const listener=e=>{if(e.detail.reason==='catalog')signals.push(App.UI.getPresentationState().snapshot.pipelines.some(x=>x.id===row.id))};window.addEventListener('app-ui-update',listener);
          App.Service.deletePipeline=async id=>{await gate;return original.call(App.Service,id)};
          try{await App.UI.deletePipeline(row.id);document.getElementById('btnAcceptConfirm').click();await Promise.resolve();
            const before={signals:signals.length,exists:!!(await App.DB.get('pipelines',row.id)),busy:App.UI.modalBusy.has('modalConfirm')};release();
            while(App.UI.modalBusy.has('modalConfirm'))await new Promise(r=>setTimeout(r,5));
            return {before,after:{signals,db:!!(await App.DB.get('pipelines',row.id)),cache:App.UI.getPresentationState().snapshot.pipelines.some(x=>x.id===row.id)}};
          }finally{App.Service.deletePipeline=original;window.removeEventListener('app-ui-update',listener);}
        }''')
        self.assertEqual(result['before'],{'signals':0,'exists':True,'busy':True});self.assertFalse(result['after']['db']);self.assertFalse(result['after']['cache']);self.assertIn(False,result['after']['signals'])

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:],module=sys.modules[__name__]) if len(sys.argv)>1 else unittest.defaultTestLoader.loadTestsFromTestCase(UIController)
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
