"""Reproduções complementares dos dados e estados apresentados pela GUI."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'auditoria_interface/dados'
with sync_playwright() as p:
    b=p.chromium.launch(channel='msedge',headless=True)
    c=b.new_context(timezone_id='America/Sao_Paulo')
    page=c.new_page();page.goto((ROOT/'index.html').as_uri())
    page.wait_for_function('App.AlarmEngine.intervalId!==null')
    page.evaluate('App.AlarmEngine.stop()')
    results={}
    results['zero_lead']=page.evaluate('async()=>{let originals=[App.DB.getAll,App.Service.getSettings,App.Service.getColorRanges,App.AlarmEngine.fireAlarm];let fired=[];App.DB.getAll=async()=>[{id:"zero",status:"pendente",hasAlarm:true,useDefaultAlarmSettings:true,scheduledAt:new Date(Date.now()+600000).toISOString(),alarmState:"idle"}];App.Service.getSettings=async()=>({...App.Config.DEFAULT_SETTINGS,defaultLeadTimeMinutes:0});App.Service.getColorRanges=async()=>App.Config.DEFAULT_COLOR_RANGES;App.AlarmEngine.fireAlarm=async e=>fired.push(e.id);await App.AlarmEngine.tick();[App.DB.getAll,App.Service.getSettings,App.Service.getColorRanges,App.AlarmEngine.fireAlarm]=originals;return {scheduledInMinutes:10,configuredLead:0,fired}}')
    results['zero_volume']=page.evaluate('async()=>{let original=App.Audio.play;let args=[];App.Audio.play=(t,v)=>args.push(v);await App.AlarmEngine.fireAlarm({id:"volume",useDefaultAlarmSettings:true}, {...App.Config.DEFAULT_SETTINGS,soundVolume:0,visualAlertEnabled:false},[]);App.Audio.play=original;await App.Service.deleteEvent("volume");return args}')
    page.evaluate('App.Service.loadDemoData()')
    results['band_stale']=page.evaluate('async()=>{let ev=(await App.DB.getAll("events")).find(e=>e.status==="pendente");ev.scheduledAt=new Date(Date.now()+16*60000).toISOString();ev.hasAlarm=false;await App.DB.update("events",ev);await App.UI.navigateTo("viewPendingEvents");let card=[...document.querySelectorAll("#containerPendingCards .event-card")].find(e=>e.dataset.eventId===ev.id),before=card.querySelector(".status-badge").textContent;let old=Date.now;Date.now=()=>old()+120000;App.UI.updateLiveTimers();let after=card.querySelector(".status-badge").textContent,expected=App.Service.classifyEvent(ev,App.Config.DEFAULT_COLOR_RANGES).name;Date.now=old;return {before,after,expected}}')
    results['backup_summary_script_execution']=page.evaluate('async()=>{window.auditMarker=false;let parsed=App.Backup.validateBackupData(JSON.stringify({schemaVersion:1,exportedAt:"<img src=x onerror=window.auditMarker=true>",data:{consoles:[],pipelines:[],operationalUnits:[],events:[]}}));App.UI.showImportSummaryModal(parsed);await new Promise(r=>setTimeout(r,250));document.getElementById("modalImportSummary").classList.remove("active");return window.auditMarker}')
    results['formats']=page.evaluate('()=>({date:App.Utils.formatDate("2026-10-25T15:30:00.000Z"),time:App.Utils.formatTime("2026-10-25T15:30:00.000Z"),csvFormula:App.Utils.escapeCSV("=1+1")})')
    results['merge_old']=page.evaluate('async()=>{await App.DB.insert("consoles",{id:"merge",name:"novo",version:2,updatedAt:"2026-10-25T12:00:00Z"});await App.Backup.importJSON({data:{consoles:[{id:"merge",name:"antigo",version:2,updatedAt:"2020-01-01T12:00:00Z"}]}},"merge");return await App.DB.get("consoles","merge")}')
    results['replace_invalid']=page.evaluate('async()=>{let before=(await App.DB.getAll("consoles")).length;let old=App.Backup.exportJSON;App.Backup.exportJSON=async()=>{};let error;try{let parsed=App.Backup.validateBackupData(JSON.stringify({schemaVersion:1,data:{consoles:[{}],pipelines:[],operationalUnits:[],events:[]}}));await App.Backup.importJSON(parsed,"replace")}catch(e){error=e.message}App.Backup.exportJSON=old;return {before,after:(await App.DB.getAll("consoles")).length,error,preventiveDownloadStubbed:true}}')
    (OUT/'testes_integridade_visual.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    c.close();b.close()
    print(json.dumps(results,ensure_ascii=False,indent=2))
