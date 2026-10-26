import functools, http.server, pathlib, sys, tempfile, threading, unittest
from playwright.sync_api import sync_playwright
import os, runpy
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

class CoreBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from parts_css import CSS_CONTENT
        from parts_html import HTML_CONTENT
        from parts_js_core import JS_CORE
        from parts_js_service import JS_SERVICE
        from parts_js_ui import JS_UI
        if os.environ.get('PREVISOES_CORE_BASELINE') == '1':
            originals = ROOT / 'revisao_interface_2026_10_25' / 'originais'
            JS_CORE = runpy.run_path(str(originals / 'parts_js_core.py'))['JS_CORE']
            JS_SERVICE = runpy.run_path(str(originals / 'parts_js_service.py'))['JS_SERVICE']
        cls.tmp = tempfile.TemporaryDirectory()
        # All five current blocks, isolated origin and browser profile; never build shared index.
        html = '<!doctype html><html><head><meta charset="UTF-8"><style>'+CSS_CONTENT+'</style></head><body>'+HTML_CONTENT+'<script>'+JS_CORE+JS_SERVICE+JS_UI+'</script></body></html>'
        pathlib.Path(cls.tmp.name, 'index.html').write_text(html, encoding='utf-8')
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *args): pass
        cls.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=cls.tmp.name))
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(channel='msedge', headless=True)
        cls.url = f'http://127.0.0.1:{cls.server.server_port}/'
    @classmethod
    def tearDownClass(cls):
        cls.browser.close(); cls.pw.stop(); cls.server.shutdown(); cls.tmp.cleanup()
    def setUp(self):
        self.ctx = self.browser.new_context(timezone_id='America/Sao_Paulo')
        self.page = self.ctx.new_page()
        with self.page.expect_console_message(predicate=lambda message: 'inicializado com sucesso' in message.text):
            self.page.goto(self.url)
        self.page.wait_for_function('window.App && App.DB.db && App.UI.currentView')
        self.page.wait_for_function("async () => !!(await App.DB.get('settings','app_settings'))")
        self.page.evaluate('App.AlarmEngine.stop()')
        self.page.evaluate('''async () => {
          await App.Service.saveSettings({...await App.Service.getSettings(),localUserName:'Operador Teste'});
          const c=(await App.DB.getAll('consoles'))[0];
          const a=await App.Service.saveUO({name:'Alpha'}),b=await App.Service.saveUO({name:'Beta'});
          const p=await App.Service.savePipeline({name:'Duto A',consoleId:c.id,uoIds:[a.id,b.id]});
          window.fixture={consoleId:c.id,pipelineId:p.id,uoId:a.id,scheduledDate:'2026-10-25',scheduledTime:'12:00',description:'Teste',hasAlarm:true,alarmMinutesBefore:0,alarmAudio:false,alarmVisual:false,alarmRepeat:false,alarmMaxRepeats:0};
        }''')
    def tearDown(self): self.ctx.close()
    def runjs(self, code):
        return self.page.evaluate('async () => Promise.race([(async () => {'+code+'})(),new Promise((_,reject)=>setTimeout(()=>reject(new Error("Test exceeded 15s")),15000))])')
    def test_local_date_and_csv_formula(self):
        self.assertEqual(self.runjs("return [App.Utils.formatDate('2026-10-25T02:30:00Z'),App.Utils.formatTime('2026-10-25T02:30:00Z'),App.Utils.formatDate(new Date('2026-10-25T02:30:00Z')),App.Utils.escapeCSV('=SUM(A1)'),App.Utils.formatDateTime('2026-10-25')];"), ['24/10/2026','23:30','24/10/2026',"'=SUM(A1)",'25/10/2026 00:00'])
    def test_impossible_calendar_day_rejected(self):
        self.assertTrue(self.runjs("try{await App.Service.saveEvent({...fixture,scheduledDate:'2026-02-31'});return false;}catch(e){return true;}"))
    def test_incompatible_reference_rejected(self):
        self.assertTrue(self.runjs("const u=await App.Service.saveUO({name:'Gamma'});try{await App.Service.saveEvent({...fixture,uoId:u.id});return false;}catch(e){return true;}"))
    def test_distinct_pipeline_units_required(self):
        self.assertTrue(self.runjs("try{await App.Service.savePipeline({name:'Bad',consoleId:fixture.consoleId,uoIds:[fixture.uoId,fixture.uoId]});return false;}catch(e){return true;}"))
    def test_zero_repeat_and_real_actor(self):
        self.assertEqual(self.runjs("const e=await App.Service.saveEvent(fixture);const c=await App.Service.completeEvent(e.id);return [e.alarmMaxRepeats,e.createdBy,c.completedBy];"),[0,'Operador Teste','Operador Teste'])
    def test_history_preserved_on_delete(self):
        self.assertEqual(self.runjs("const e=await App.Service.saveEvent(fixture);await App.Service.deleteEvent(e.id);return [(await App.DB.get('events',e.id))?.active,(await App.DB.getAll('eventHistory')).filter(h=>h.eventId===e.id).length];"),[False,2])
    def test_snooze_out_of_bounds(self):
        self.assertTrue(self.runjs("const e=await App.Service.saveEvent(fixture);try{await App.Service.snoozeAlarm(e.id,0);return false;}catch(e){return true;}"))
    def test_atomic_abort_after_write(self):
        self.assertEqual(self.runjs("if(!App.DB.atomic)return ['missing'];let rejected=false;try{await App.DB.atomic(['consoles'],(d,tx)=>{d.consoles.push({id:'abort',name:'ABORT'});tx.objectStore('consoles').put({id:'written',name:'WRITTEN'}).onsuccess=()=>tx.abort();});}catch(e){rejected=true;}return [rejected,await App.DB.get('consoles','written'),await App.DB.get('consoles','abort')];"),[True,None,None])
    def test_crud_rejects_abort_after_request_success(self):
        self.assertEqual(self.runjs("const nativePut=IDBObjectStore.prototype.put;IDBObjectStore.prototype.put=function(...args){const q=nativePut.apply(this,args);q.addEventListener('success',()=>this.transaction.abort());return q;};let failed=false;try{await App.DB.update('consoles',{id:'abort-crud',name:'Abort'});}catch(e){failed=true;}IDBObjectStore.prototype.put=nativePut;return [failed,await App.DB.get('consoles','abort-crud')];"),[True,None])
    def test_backup_rejects_unsafe_metadata_and_missing_collections(self):
        self.assertEqual(self.runjs("const data={};for(const s of ['consoles','pipelines','operationalUnits','pipelineOperationalUnits','equipmentTypes','equipmentTags','events','eventHistory','colorRanges','settings'])data[s]=await App.DB.getAll(s);const b={schemaVersion:1,exportedAt:'<img src=x onerror=alert(1)>',data};let rejected=0;try{App.Backup.validateBackupData(JSON.stringify(b));}catch(e){rejected++;}b.exportedAt=new Date().toISOString();delete data.eventHistory;try{App.Backup.validateBackupData(JSON.stringify(b));}catch(e){rejected++;}return rejected;"),2)
    def test_invalid_import_preserves_base(self):
        self.assertTrue(self.runjs("const before=JSON.stringify(await App.DB.getAll('consoles'));let failed=false;try{await App.Backup.importJSON({schemaVersion:1,data:{consoles:[],pipelines:[],operationalUnits:[],events:[]}},'replace');}catch(e){failed=true;}return failed&&before===JSON.stringify(await App.DB.getAll('consoles'));"))
    def test_duplicate_and_orphan_backup_rows_rejected(self):
        self.assertEqual(self.runjs("const data={};for(const s of ['consoles','pipelines','operationalUnits','pipelineOperationalUnits','equipmentTypes','equipmentTags','events','eventHistory','colorRanges','settings'])data[s]=await App.DB.getAll(s);const b={schemaVersion:1,exportedAt:new Date().toISOString(),data};let n=0;data.consoles.push(data.consoles[0]);try{App.Backup.validateBackupData(JSON.stringify(b));}catch(e){n++;}data.consoles.pop();data.pipelines[0].consoleId='missing';try{App.Backup.validateBackupData(JSON.stringify(b));}catch(e){n++;}return n;"),2)
    def test_merge_does_not_regress_equal_version_older_timestamp(self):
        self.assertTrue(self.runjs("const data={};for(const s of ['consoles','pipelines','operationalUnits','pipelineOperationalUnits','equipmentTypes','equipmentTags','events','eventHistory','colorRanges','settings'])data[s]=await App.DB.getAll(s);const c=data.consoles[0];const id=c.id,original=c.name;c.name='OLD';c.updatedAt='2020-01-01T00:00:00Z';await App.Backup.importJSON({schemaVersion:1,exportedAt:new Date().toISOString(),data},'merge');return (await App.DB.get('consoles',id)).name===original;"))
    def test_parallel_ticks_one_alarm_and_title_persists(self):
        self.assertEqual(self.runjs("const e=await App.Service.saveEvent({...fixture,scheduledDate:'2020-01-01'});await Promise.all([App.AlarmEngine.tick(),App.AlarmEngine.tick()]);const current=await App.DB.get('events',e.id);await App.AlarmEngine.tick();return [current.alarmTriggerCount,(await App.DB.getAll('eventHistory')).filter(h=>h.action==='disparo_alarme').length,document.title.includes('ALARME')];"),[1,1,True])
    def test_stale_fire_cannot_overwrite_completed_event(self):
        self.assertEqual(self.runjs("const e=await App.Service.saveEvent(fixture);await App.Service.completeEvent(e.id);await App.AlarmEngine.fireAlarm(e,await App.Service.getSettings(),await App.Service.getColorRanges());return (await App.DB.get('events',e.id)).status;"),'concluido')
    def test_supported_industrial_theme_and_all_layouts(self):
        self.assertEqual(self.runjs("const settings=await App.Service.getSettings();for(const mode of ['auto','compact','mobile','tablet','conventional','widescreen','ultrawide'])await App.Service.saveSettings({...settings,theme:'industrial',responsiveLayoutMode:mode});return (await App.Service.getSettings()).theme;"),'industrial')
    def test_backup_replace_rolls_back_aborted_write(self):
        self.assertEqual(self.runjs("const b=await App.Backup.createSnapshot();const id=b.data.consoles[0].id,original=b.data.consoles[0].name;b.data.consoles[0].name='Changed';const native=IDBObjectStore.prototype.add;IDBObjectStore.prototype.add=function(...args){const q=native.apply(this,args);if(this.name==='consoles'&&args[0].id===id)q.onsuccess=()=>this.transaction.abort();return q;};let rejected=false;try{await App.Backup.importJSON(b,'replace');}catch(e){rejected=true;}finally{IDBObjectStore.prototype.add=native;}return [rejected,(await App.DB.get('consoles',id)).name===original];"),[True,True])
    def test_backup_duplicate_business_conflict_preserves_every_store(self):
        self.assertEqual(self.runjs("const b=await App.Backup.createSnapshot();b.data.consoles[0].id='different-id';for(const p of b.data.pipelines)if(p.consoleId===fixture.consoleId)p.consoleId='different-id';b.data.settings[0].value.activeConsoleId=null;const before=JSON.stringify(await App.DB.snapshot());const r=await App.Backup.importJSON(b,'merge');return [r.applied,r.conflicts.length>0,before===JSON.stringify(await App.DB.snapshot())];"),[False,True,True])
    def test_import_legacy_snapshot_and_roundtrip(self):
        self.assertEqual(self.runjs("await App.Service.saveEvent(fixture);const b=await App.Backup.createSnapshot();for(const s of ['settings','colorRanges'])for(const row of b.data[s]){delete row.version;delete row.updatedAt;}for(const e of b.data.events){delete e.createdBy;delete e.completedBy;}const r=await App.Backup.importJSON(b,'replace');return [r.applied,(await App.Backup.createSnapshot()).data.events.length];"),[True,1])
    def test_backup_rejects_invalid_types_png_and_impossible_iso(self):
        self.assertEqual(self.runjs("await App.Service.saveEvent(fixture);const base=await App.Backup.createSnapshot();let count=0;for(const update of [b=>b.exportedAt='2026-02-31T00:00:00Z',b=>b.data.events[0].stylusDrawing='data:image/svg+xml,<svg onload=alert(1)>',b=>b.data.events[0].id=\"x');alert(1);//\",b=>b.data.events[0].status='other',b=>b.data.settings[0].value.soundVolume=101,b=>b.data.colorRanges[0].color='red;display:none',b=>b.data.events[0].alarmMaxRepeats='bad',b=>b.data.events[0].version='1',b=>b.data.events[0].alarmMaxRepeats='0',b=>b.data.settings[0].value.soundVolume='50']){const b=structuredClone(base);update(b);try{App.Backup.validateBackupData(b);}catch(e){count++;}}return count;"),10)
    def test_existing_inactive_references_only_on_original_link(self):
        self.assertEqual(self.runjs("const e=await App.Service.saveEvent(fixture);await App.Service.toggleUOActive(fixture.uoId);let freshRejected=false;try{await App.Service.saveEvent(fixture);}catch(e){freshRejected=true;}const edited=await App.Service.saveEvent({...e,description:'Edited'});return [freshRejected,edited.description];"),[True,'Edited'])
    def test_master_change_cannot_break_existing_event(self):
        self.assertTrue(self.runjs("await App.Service.saveEvent(fixture);const other=await App.Service.saveConsole({name:'Other'});const links=await App.DB.getAll('pipelineOperationalUnits');try{await App.Service.savePipeline({id:fixture.pipelineId,name:'Duto A',consoleId:other.id,uoIds:links.filter(l=>l.pipelineId===fixture.pipelineId).map(l=>l.uoId)});return false;}catch(e){return (await App.DB.get('pipelines',fixture.pipelineId)).consoleId===fixture.consoleId;}"))
    def test_reopen_and_reschedule_reset_alarm_cycle(self):
        self.assertEqual(self.runjs("const e=await App.Service.saveEvent({...fixture,scheduledDate:'2020-01-01'});await App.AlarmEngine.tick();await App.Service.completeEvent(e.id);let bad=false;try{await App.Service.reopenEvent(e.id,'2026-02-31','12:00');}catch(e){bad=true;}const reopened=await App.Service.reopenEvent(e.id,'2027-01-01','14:00');return [bad,reopened.alarmTriggerCount,reopened.lastAlarmTriggeredAt,reopened.completedBy];"),[True,0,None,None])
    def test_zero_default_lead_does_not_fire_fifteen_minutes_early(self):
        self.assertEqual(self.runjs("await App.Service.saveSettings({...await App.Service.getSettings(),defaultLeadTimeMinutes:0});const dt=new Date(Date.now()+5*60000),date=dt.getFullYear()+'-'+String(dt.getMonth()+1).padStart(2,'0')+'-'+String(dt.getDate()).padStart(2,'0'),time=String(dt.getHours()).padStart(2,'0')+':'+String(dt.getMinutes()).padStart(2,'0');const e=await App.Service.saveEvent({...fixture,scheduledDate:date,scheduledTime:time,useDefaultAlarmSettings:true});await App.AlarmEngine.tick();return (await App.DB.get('events',e.id)).alarmTriggerCount;"),0)
    def test_async_visual_error_is_logged_without_loop(self):
        self.assertEqual(self.runjs("const e=await App.Service.saveEvent({...fixture,scheduledDate:'2020-01-01',alarmVisual:true});App.UI.showAlarmModal=async()=>{throw new Error('visual failure');};await App.AlarmEngine.tick();await App.AlarmEngine.tick();return [(await App.DB.getAll('errorLogs')).filter(x=>x.message==='visual failure').length,(await App.DB.getAll('eventHistory')).find(x=>x.action==='disparo_alarme').channels];"),[1,[]])
    def test_two_tabs_claim_single_firing(self):
        self.assertEqual(self.runjs("const e=await App.Service.saveEvent({...fixture,scheduledDate:'2020-01-01'});const peer=window.open(location.href,'peer');await new Promise(resolve=>peer.addEventListener('load',resolve));peer.App.AlarmEngine.stop();await Promise.all([App.AlarmEngine.tick(),peer.App.AlarmEngine.tick()]);peer.close();return [(await App.DB.get('events',e.id)).alarmTriggerCount,(await App.DB.getAll('eventHistory')).filter(x=>x.action==='disparo_alarme').length];"),[1,1])
    def test_demo_clear_and_backup_roundtrip(self):
        self.assertEqual(self.runjs("await App.Service.clearAllData();await App.Service.loadDemoData();const b=await App.Backup.createSnapshot();App.Backup.validateBackupData(b);return [b.data.events.length,b.data.pipelineOperationalUnits.length,b.data.settings[0].value.activeConsoleId!==null,b.data.events.filter(e=>e.status==='concluido').length,b.data.operationalUnits.length,b.data.equipmentTags.length];"),[6,6,True,1,4,4])
    def test_csv_download_bom_formula_and_inactive_filter(self):
        self.assertEqual(self.runjs("const e=await App.Service.saveEvent({...fixture,description:'=SUM(A1)'});let blob;App.Backup.downloadBlob=b=>blob=b;await App.Backup.exportCSV('pending');const bytes=new Uint8Array(await blob.arrayBuffer()),text=await blob.text();await App.Service.deleteEvent(e.id);await App.Backup.exportCSV('pending');return [Array.from(bytes.slice(0,3)),text.includes(\"'=SUM(A1)\"),!(await blob.text()).includes('SUM(A1)')];"),[[239,187,191],True,True])
    def test_backup_rejects_unknown_collection_and_wrong_free_text_type(self):
        self.assertEqual(self.runjs("await App.Service.saveEvent(fixture);const b=await App.Backup.createSnapshot();let rejected=0;b.data.events[0].notes={text:'wrong'};try{App.Backup.validateBackupData(b);}catch(e){rejected++;}b.data.events[0].notes='';b.data.unknown=[];try{App.Backup.validateBackupData(b);}catch(e){rejected++;}return rejected;"),2)
    def test_zero_and_nan_volume_never_create_real_oscillators(self):
        self.assertEqual(self.runjs("App.Audio.init();const ctx=App.Audio.ctx,original=ctx.createOscillator.bind(ctx);let count=0;ctx.createOscillator=(...args)=>{count++;return original(...args);};for(const type of ['chime','beep','siren','blip'])for(const volume of [0,NaN]){try{App.Audio.play(type,volume);}catch(e){}}const settings={...await App.Service.getSettings(),soundVolume:0,soundEnabled:true};App.Audio.isUnlocked=true;const available=App.AlarmEngine.channels({useDefaultAlarmSettings:true},settings).audio;await ctx.close();return [count,available];"),[0,False])
    def test_replace_requires_preventive_backup_without_metadata_side_effects(self):
        self.assertEqual(self.runjs("""
          const event=await App.Service.saveEvent(fixture), backup=await App.Backup.createSnapshot();
          backup.data.events=[];backup.data.eventHistory=[];
          const names=[...App.DB.DATA_STORES,'errorLogs'],before=JSON.stringify(await App.DB.snapshot(names));
          const originalExport=App.Backup.exportJSON;let called=0,exportRejected=false;
          App.Backup.exportJSON=async()=>{called++;throw new Error('backup failed');};
          try{await App.Backup.importJSON(backup,'replace');}catch(e){exportRejected=true;}
          const preservedAfterExport=before===JSON.stringify(await App.DB.snapshot(names));
          App.Backup.exportJSON=originalExport;
          const originalDownload=App.Backup.downloadBlob;let downloadRejected=false;
          App.Backup.downloadBlob=async()=>{throw new Error('download failed');};
          try{await App.Backup.importJSON(backup,'replace');}catch(e){downloadRejected=true;}
          const preservedAfterDownload=before===JSON.stringify(await App.DB.snapshot(names));
          let savedEvents=-1,originalStillPresent=false;
          App.Backup.downloadBlob=async blob=>{savedEvents=JSON.parse(await blob.text()).data.events.length;originalStillPresent=!!(await App.DB.get('events',event.id));};
          const result=await App.Backup.importJSON(backup,'replace');App.Backup.downloadBlob=originalDownload;
          return [called,exportRejected,preservedAfterExport,downloadRejected,preservedAfterDownload,savedEvents,originalStillPresent,result.applied,await App.DB.get('events',event.id)];
        """),[1,True,True,True,True,1,True,True,None])
    def test_backup_requires_functional_fields_and_preserves_legacy_optional_metadata(self):
        self.assertEqual(self.runjs("""
          await App.Service.clearAllData();await App.Service.loadDemoData();const backup=await App.Backup.createSnapshot();
          const required={consoles:['id','name','active','createdAt','updatedAt','version','synchronizationStatus'],pipelines:['id','name','consoleId','active','createdAt','updatedAt','version','synchronizationStatus'],operationalUnits:['id','name','active','createdAt','updatedAt','version','synchronizationStatus'],pipelineOperationalUnits:['id','pipelineId','uoId','createdAt','version','synchronizationStatus'],equipmentTypes:['id','name','uoId','active','createdAt','updatedAt','version','synchronizationStatus'],equipmentTags:['id','tag','uoId','equipmentTypeId','active','createdAt','updatedAt','version','synchronizationStatus'],events:['id','consoleId','pipelineId','uoId','equipmentTypeId','tagId','scheduledDate','scheduledTime','scheduledAt','description','notes','priority','status','hasAlarm','useDefaultAlarmSettings','alarmMinutesBefore','alarmAudio','alarmVisual','alarmNotification','alarmRepeat','alarmRepeatInterval','alarmMaxRepeats','alarmState','alarmSnoozedUntil','alarmTriggerCount','lastAlarmTriggeredAt','completedAt','completedTimeDiffMinutes','completionNote','active','createdAt','updatedAt','version','synchronizationStatus'],eventHistory:['id','eventId','action','timestamp','description','previousValue','newValue','localUser'],colorRanges:['id','name','color','minMinutes','maxMinutes','priority','blink','sound','active'],settings:['key','value']};
          const accepted=[];for(const [store,fields] of Object.entries(required))for(const field of fields){const candidate=structuredClone(backup);delete candidate.data[store][0][field];try{App.Backup.validateBackupData(candidate);accepted.push(store+'.'+field);}catch(e){}}
          const before=JSON.stringify(await App.DB.snapshot());const invalid=structuredClone(backup);delete invalid.data.events[0].hasAlarm;delete invalid.data.events[0].alarmTriggerCount;
          let rejected=false;try{await App.Backup.importJSON(invalid,'replace');}catch(e){rejected=true;}
          const preserved=before===JSON.stringify(await App.DB.snapshot());
          const legacy=structuredClone(backup);for(const row of legacy.data.events){delete row.createdBy;delete row.completedBy;delete row.stylusDrawing;}for(const store of ['colorRanges','settings'])for(const row of legacy.data[store]){delete row.createdAt;delete row.updatedAt;delete row.version;delete row.synchronizationStatus;}
          let legacyValid=true;try{App.Backup.validateBackupData(legacy);}catch(e){legacyValid=false;}
          return [accepted,rejected,preserved,legacyValid];
        """),[[],True,True,True])
    def test_idle_tick_and_unchanged_atomic_issue_zero_native_writes(self):
        self.assertEqual(self.runjs("""
          await App.Service.clearAllData();await App.Service.loadDemoData();await App.DB.atomic(['events'],d=>{for(const event of d.events)event.hasAlarm=false;});
          const originals={},writes=[];for(const method of ['add','put','clear','delete']){originals[method]=IDBObjectStore.prototype[method];IDBObjectStore.prototype[method]=function(...args){writes.push(this.name+'.'+method);return originals[method].apply(this,args);};}
          try{await App.AlarmEngine.tick();await App.DB.atomic(['events','settings'],()=>null);const completed=(await App.DB.getAll('events')).find(e=>e.status==='concluido');await App.AlarmEngine.fireAlarm(completed);}finally{for(const [method,original] of Object.entries(originals))IDBObjectStore.prototype[method]=original;}
          return writes;
        """),[])

if __name__=='__main__': unittest.main(verbosity=2)
