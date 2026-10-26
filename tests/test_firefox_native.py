"""Native installed Firefox headless smoke/layout matrix, no driver download.

Uses an isolated profile, same-origin iframe viewports and posts test results to
an ephemeral loopback server. Never connects to the user's browser profile.
"""
from pathlib import Path
import argparse,http.server,json,os,subprocess,tempfile,threading,time,sys
from browser_support import ROOT,build_temporary_html,source_fingerprints

SCRIPT=r"""
<script>
if(window===top){
(async()=>{
 const results=[];const record=(name,passed,details)=>results.push({name,passed:!!passed,details});
 const wait=async fn=>{for(let i=0;i<1500;i++){if(await fn())return;await new Promise(r=>setTimeout(r,20))}throw new Error('Initialization timeout')};
 try{
  await wait(()=>window.App&&App.AlarmEngine.intervalId!==null);App.AlarmEngine.stop();await App.AlarmEngine.tick();
  record('firefox-live-clock',/\d{2}\/\d{2}\/\d{4}/.test(document.getElementById('liveClock').textContent),document.getElementById('liveClock').textContent);
  if(!(await App.DB.getAll('events')).length)await App.Service.loadDemoData();
  record('firefox-local-date',App.Utils.formatDate('2026-10-25')==='25/10/2026',App.Utils.formatDate('2026-10-25'));
  record('firefox-iso-time',App.Utils.formatTime('2026-10-25T15:30:00.000Z')==='12:30',App.Utils.formatTime('2026-10-25T15:30:00.000Z'));
  let backup=await App.Backup.createSnapshot();
  try{let b=structuredClone(backup);delete b.data.events[0].hasAlarm;App.Backup.validateBackupData(b);record('firefox-missing-alarm-rejected',false,null)}catch(e){record('firefox-missing-alarm-rejected',true,e.message)}
  let acts=[];App.UI.showConfirmModal('A','A',()=>acts.push('A'));document.getElementById('btnCancelConfirm').click();App.UI.showConfirmModal('B','B',()=>acts.push('B'));document.getElementById('btnAcceptConfirm').click();record('firefox-cancel-discard',acts.join(',')==='B',acts);
  let frame=document.createElement('iframe');frame.style.border='0';frame.style.width='390px';frame.style.height='844px';frame.src=location.pathname+'?frame=1';document.body.appendChild(frame);
  await wait(()=>frame.contentWindow.App&&frame.contentWindow.App.AlarmEngine.intervalId!==null);let w=frame.contentWindow;w.App.AlarmEngine.stop();w.document.getElementById('liveClock').textContent=document.getElementById('liveClock').textContent;
  const views=['viewDashboard','viewNewEvent','viewPendingEvents','viewCompletedEvents','viewCadastros','viewConfigAlerts','viewConfigColors','viewBackup','viewDiagnostic'];
  const widths=WIDTHS_TOKEN,modes=MODES_TOKEN;
  for(let width of widths){frame.style.width=width+'px';frame.style.height=(width<768?844:1000)+'px';await new Promise(r=>setTimeout(r,40));for(let mode of modes){await w.App.UI.applyResponsiveLayoutMode(mode,false);for(let view of views){await w.App.UI.navigateTo(view);let scroll=w.document.documentElement.scrollWidth;record('firefox-layout:'+width+':'+mode+':'+view,scroll<=width+2,{width,scroll,layout:w.document.body.dataset.layoutMode})}}}
  for(let theme of ['dark','light','industrial']){w.App.UI.applyTheme(theme);for(let view of views){await w.App.UI.navigateTo(view);record('firefox-theme:'+theme+':'+view,w.document.documentElement.scrollWidth<=w.innerWidth+2,null)}}
 }catch(e){record('firefox-harness',false,String(e.stack||e))}
 await fetch('/results',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({browser:navigator.userAgent,tests:results.length,passed:results.filter(x=>x.passed).length,failed:results.filter(x=>!x.passed).length,results})});
})()
}
</script>
"""

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');parser.add_argument('--timeout',type=int,default=240);args=parser.parse_args()
    binary=Path(os.environ.get('PREVISOES_FIREFOX_BINARY', 'C:/Program Files/Mozilla Firefox/firefox.exe'))
    out=Path(os.environ.get('PREVISOES_TEST_OUTPUT', str(ROOT/'revisao_interface_2026_10_25/resultados')))
    out.mkdir(parents=True,exist_ok=True)
    if not binary.exists():
        (out/'firefox_resultado.json').write_text(json.dumps({'available':False,'reason':'Installed Firefox not found'}),encoding='utf-8');return 2
    before=source_fingerprints()
    temp,path=build_temporary_html();received={};done=threading.Event()
    widths=[390,1024,1440,3440] if args.quick else [320,360,390,480,600,767,768,820,1024,1199,1200,1440,1600,1919,1920,2200,2559,2560,3440]
    modes=['auto'] if args.quick else ['auto','compact','mobile','tablet','conventional','widescreen','ultrawide']
    script=SCRIPT.replace('WIDTHS_TOKEN',json.dumps(widths)).replace('MODES_TOKEN',json.dumps(modes))
    source=path.read_text(encoding='utf-8').replace('</body>',script+'</body>')
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            body=source.encode('utf-8');self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
        def do_POST(self):
            received.update(json.loads(self.rfile.read(int(self.headers['Content-Length']))));self.send_response(200);self.end_headers();self.wfile.write(b'OK');done.set()
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    with tempfile.TemporaryDirectory(prefix='previsoes-firefox-profile-',ignore_cleanup_errors=True) as profile:
        Path(profile,'user.js').write_text('user_pref("browser.shell.checkDefaultBrowser",false);user_pref("datareporting.policy.dataSubmissionEnabled",false);user_pref("network.captive-portal-service.enabled",false);user_pref("network.connectivity-service.enabled",false);user_pref("app.update.enabled",false);',encoding='utf-8')
        with (out/'firefox_processo.log').open('w',encoding='utf-8') as log:
            process=subprocess.Popen([str(binary),'-headless','-no-remote','-profile',profile,f'http://127.0.0.1:{server.server_port}/'],stdout=log,stderr=log,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            completed=done.wait(args.timeout)
            if process.poll() is None and sys.platform=='win32':
                subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=log,stderr=log,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            elif process.poll() is None:
                process.terminate()
            try:process.wait(timeout=10)
            except subprocess.TimeoutExpired:process.kill();process.wait(timeout=10)
        if not completed:received={'available':False,'reason':'Headless isolated Firefox did not complete harness','timeout':args.timeout}
    server.shutdown();temp.cleanup()
    after=source_fingerprints()
    received.update(quick=args.quick,distributed_html=os.environ.get('PREVISOES_TEST_DISTRIBUTED')=='1',sources_stable=before==after,source_hashes=after)
    (out/('firefox_quick.json' if args.quick else 'firefox_resultado.json')).write_text(json.dumps(received,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in received.items() if k!='results'},ensure_ascii=False))
    return 0 if completed and received.get('failed')==0 and received['sources_stable'] else 1
if __name__=='__main__':sys.exit(main())
