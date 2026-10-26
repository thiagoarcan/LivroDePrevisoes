import sys,json,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'tests'))
from test_core_browser import CoreBrowserTests
CoreBrowserTests.setUpClass()
t=CoreBrowserTests()
try:
 t.setUp()
 checks={}
 checks['replace_with_failing_backup']=t.runjs("const e=await App.Service.saveEvent(fixture);const b=await App.Backup.createSnapshot();b.data.events=[];b.data.eventHistory=[];let called=0;App.Backup.exportJSON=async()=>{called++;throw new Error('backup failed')};const r=await App.Backup.importJSON(b,'replace');return {called,applied:r.applied,event:await App.DB.get('events',e.id)};")
 checks['missing_required_alarm_state']=t.runjs("const e=await App.Service.saveEvent(fixture);const b=await App.Backup.createSnapshot();delete b.data.events[0].hasAlarm;delete b.data.events[0].alarmTriggerCount;const r=await App.Backup.importJSON(b,'replace');return {applied:r.applied,event:await App.DB.get('events',e.id)};")
 checks['idle_tick_writes']=t.runjs("await App.Service.clearAllData();await App.Service.loadDemoData();await App.DB.atomic(['events'],d=>{for(const e of d.events)e.hasAlarm=false});let adds=0,clears=0;const oa=IDBObjectStore.prototype.add,oc=IDBObjectStore.prototype.clear;IDBObjectStore.prototype.add=function(...a){adds++;return oa.apply(this,a)};IDBObjectStore.prototype.clear=function(...a){clears++;return oc.apply(this,a)};try{await App.AlarmEngine.tick()}finally{IDBObjectStore.prototype.add=oa;IDBObjectStore.prototype.clear=oc}return {events:(await App.DB.getAll('events')).length,history:(await App.DB.getAll('eventHistory')).length,adds,clears};")
 print(json.dumps(checks,ensure_ascii=False,indent=2))
finally:
 t.tearDown()
 CoreBrowserTests.tearDownClass()
