"""Responsive acceptance matrix. --quick reproduces baseline defects quickly."""
import argparse,json,os,sys,time
from pathlib import Path
from playwright.sync_api import sync_playwright
from browser_support import ROOT,build_temporary_html,open_app,source_fingerprints

VIEWS=['viewDashboard','viewNewEvent','viewPendingEvents','viewCompletedEvents','viewCadastros','viewConfigAlerts','viewConfigColors','viewBackup','viewDiagnostic']
WIDTHS=[320,360,390,480,600,767,768,820,1024,1199,1200,1440,1600,1919,1920,2200,2559,2560,3440]
MODES=['auto','compact','mobile','tablet','conventional','widescreen','ultrawide']
OUT=ROOT/'revisao_interface_2026_10_25/resultados'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');parser.add_argument('--screenshots',action='store_true');args=parser.parse_args()
    cases=[];captured=[];errors=[];before=source_fingerprints()
    def record(name,passed,details):cases.append({'case':name,'passed':bool(passed),'details':details})
    temp,path=build_temporary_html()
    with sync_playwright() as p:
        b=p.chromium.launch(channel='msedge',headless=True)
        context,page,page_errors=open_app(b,path)
        for width in ([390,1024,1440,3440] if args.quick else WIDTHS):
            page.set_viewport_size({'width':width,'height':844 if width<768 else 1000})
            for mode in (['auto'] if args.quick else MODES):
                page.evaluate('(m)=>App.UI.applyResponsiveLayoutMode(m,false)',mode)
                for view in VIEWS:
                    page.evaluate('(v)=>App.UI.navigateTo(v)',view)
                    page.evaluate('window.scrollTo(0,0)')
                    d=page.evaluate('''()=>{let root=document.documentElement;return {width:innerWidth,scroll:root.scrollWidth,mode:document.body.getAttribute('data-layout-mode'),view:App.UI.currentView,nav:(()=>{let e=document.querySelector('.app-nav'),r=e.getBoundingClientRect(),s=getComputedStyle(e);return{display:s.display,x:r.x,y:r.y,w:r.width,h:r.height}})(),bottom:getComputedStyle(document.getElementById('mobileBottomNav')).display,spotlightWidth:document.querySelector('.spotlight-card')?.getBoundingClientRect().width,main:document.querySelector('.app-main')?.getBoundingClientRect().toJSON()}}''')
                    record(f'overflow:{width}:{mode}:{view}',d['scroll']<=width+2,d)
                    if mode=='auto':
                        expected='mobile' if width<768 else ('tablet' if width<1200 else ('conventional' if width<1920 else ('widescreen' if width<2560 else 'ultrawide')))
                        record(f'auto-tier:{width}:{view}',d['mode']==expected,d['mode'])
                        if width<768:
                            record(f'mobile-navigation:{width}:{view}',d['nav']['display']=='none' and d['bottom']!='none',d)
                        elif width>=1200:
                            record(f'desktop-sidebar:{width}:{view}',d['nav']['w']<=300 and d['nav']['h']>=500 and d['nav']['x']>=-1,d['nav'])
                    if width>=2560 and mode in ['auto','ultrawide'] and view=='viewDashboard':
                        record(f'no-stretched-spotlight:{width}:{mode}',0<d['spotlightWidth']<=1100,d['spotlightWidth'])
                        record(f'whole-viewport-used:{width}:{mode}',d['main'] and d['main']['right']>=width-40,d['main'])
                    if args.screenshots and width in [390,1024,1440,1920,3440] and mode=='auto':
                        name=f'final_{width}_{view}.png'
                        page.screenshot(path=str(OUT/name),full_page=True,animations='disabled',timeout=15000);captured.append(name)
            print('LAYOUT',width,'cases',len(cases),'failures',sum(not x['passed'] for x in cases),flush=True)
        if not args.quick:
            # Themes, names and rendered text must remain usable in each profile.
            for width,height in [(390,844),(1024,768),(1920,1080)]:
                page.set_viewport_size({'width':width,'height':height});page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)')
                for theme in ['dark','light','industrial']:
                    page.evaluate('(t)=>App.UI.applyTheme(t)',theme)
                    for view in VIEWS:
                        page.evaluate('(v)=>App.UI.navigateTo(v)',view)
                        record(f'theme-overflow:{width}:{theme}:{view}',page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),None)
                        if args.screenshots and view=='viewDashboard':
                            name=f'final_tema_{width}_{theme}.png';page.screenshot(path=str(OUT/name),full_page=True,animations='disabled',timeout=15000);captured.append(name)
            # All dialogs on phone, tablet and desktop; internal scrolling is allowed.
            event_id=page.evaluate('async()=>(await App.DB.getAll("events")).find(e=>e.status==="pendente").id')
            completed_id=page.evaluate('async()=>(await App.DB.getAll("events")).find(e=>e.status==="concluido").id')
            expressions={
                'alarm':f'await App.UI.showAlarmModal(await App.DB.get("events",{json.dumps(event_id)}))',
                'complete':f'await App.UI.showCompleteModal({json.dumps(event_id)})',
                'snooze':f'await App.UI.showSnoozeModal({json.dumps(event_id)})',
                'reopen':f'await App.UI.showReopenModal({json.dumps(completed_id)})',
                'details':f'await App.UI.showDetailsModal({json.dumps(event_id)})',
                'actions':f'await App.UI.openEventActionSheet({json.dumps(event_id)})',
                'status':'await App.UI.openAppStatusModal()',
                'confirm':'App.UI.showConfirmModal("Confirmação","Teste de geometria",()=>{})',
                'dependency':'App.UI.showDependencyModal("Dependências",["1 evento"],()=>{})',
                'import':'App.UI.showImportSummaryModal(await App.Backup.createSnapshot())'}
            for width,height in [(320,640),(390,844),(844,390),(1024,768),(1920,1080)]:
                page.set_viewport_size({'width':width,'height':height});page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)')
                for name,expr in expressions.items():
                    page.keyboard.press('Escape')
                    page.evaluate('async()=>{'+expr+'}')
                    dims=page.evaluate('()=>[...document.querySelectorAll(".modal-overlay.active")].map(e=>{let r=(e.querySelector(".modal-box")||e).getBoundingClientRect();return {id:e.id,x:r.x,y:r.y,w:r.width,h:r.height,right:r.right,bottom:r.bottom,viewport:[innerWidth,innerHeight]}})')
                    record(f'modal-bounds:{width}x{height}:{name}',bool(dims) and all(x['x']>=-1 and x['right']<=width+2 and x['y']>=-1 and x['bottom']<=height+2 for x in dims),dims)
                    if args.screenshots and width==390:
                        file=f'final_modal_{name}.png';page.screenshot(path=str(OUT/file),animations='disabled',timeout=15000);captured.append(file)
            page.keyboard.press('Escape')
            page.emulate_media(reduced_motion='reduce');page.evaluate('App.UI.navigateTo("viewPendingEvents")')
            record('reduced-motion',page.evaluate('[...document.querySelectorAll(".pulsing-card,.pulsing-badge")].every(e=>parseFloat(getComputedStyle(e).animationDuration)===0)'),None)
            # Unacknowledged alarms must stay visible below the real header.
            for _ in range(12):page.keyboard.press('Escape')
            page.evaluate('async()=>{await App.DB.atomic(["events"],d=>{let pending=d.events.filter(e=>e.status==="pendente"&&e.active!==false);for(let e of pending.slice(0,2)){e.hasAlarm=true;e.alarmState="triggered";e.alarmTriggerCount=1;e.lastAlarmTriggeredAt=new Date().toISOString()}});await App.UI.renderDashboard()}')
            for width,height in [(320,640),(390,844),(768,1024),(1024,768),(1920,1080),(3440,1440)]:
                page.set_viewport_size({'width':width,'height':height});page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)');page.evaluate('App.UI.navigateTo("viewDashboard")')
                page.evaluate('window.scrollTo(0,500)');page.wait_for_timeout(60)
                dims=page.evaluate('()=>({header:document.querySelector(".app-header").getBoundingClientRect().toJSON(),banner:document.getElementById("mobileActiveAlarmsBanner").getBoundingClientRect().toJSON(),display:getComputedStyle(document.getElementById("mobileActiveAlarmsBanner")).display})')
                record(f'alarm-banner-visible:{width}x{height}',dims['display']!='none' and dims['banner']['top']>=max(0,dims['header']['bottom'])-2 and dims['banner']['bottom']<=height+2,dims)
                if args.screenshots:
                    name=f'final_alarme_ativo_{width}.png';page.screenshot(path=str(OUT/name),animations='disabled',timeout=15000);captured.append(name)
            try:
                pending_before=page.evaluate('async()=>(await App.DB.getAll("events")).filter(e=>e.active!==false&&e.status==="pendente").length')
                page.locator('#btnBannerAckAll').click()
                page.wait_for_timeout(100)
                state=page.evaluate('async()=>{let es=(await App.DB.getAll("events")).filter(e=>e.active!==false&&e.status==="pendente");return {pending:es.length,active:es.filter(e=>e.alarmState==="triggered").length}}')
                record('banner-ack-all-does-not-complete-events',state['active']==0 and state['pending']==pending_before and page.evaluate('getComputedStyle(document.getElementById("mobileActiveAlarmsBanner")).display==="none"'),state)
            except Exception as exc:
                record('banner-ack-all-does-not-complete-events',False,str(exc))
        errors.extend(page_errors);context.close();b.close()
    temp.cleanup()
    record('no-unhandled-page-errors',not errors,errors)
    after=source_fingerprints()
    report={'cases':len(cases),'passed':sum(x['passed'] for x in cases),'failed':sum(not x['passed'] for x in cases),'results':cases,'screenshots':captured,'quick':args.quick,
            'distributed_html':os.environ.get('PREVISOES_TEST_DISTRIBUTED')=='1','sources_stable':before==after,'source_hashes':after}
    (OUT/('layout_quick.json' if args.quick else 'layout_completo.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('RESULT',report['passed'],'/',report['cases'],flush=True)
    return 0 if not report['failed'] and report['sources_stable'] else 1
if __name__=='__main__':sys.exit(main())
