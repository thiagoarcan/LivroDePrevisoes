"""Browser-only test support: all storage belongs to temporary contexts."""
from pathlib import Path
import hashlib,os,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
MODULE_ROOT=ROOT/'revisao_interface_2026_10_25/originais' if os.environ.get('PREVISOES_TEST_BASELINE')=='1' else ROOT
sys.path.insert(0,str(MODULE_ROOT))

def source_fingerprints():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [ROOT/'index.html',ROOT/'build_all.py',*sorted(ROOT.glob('parts_*.py'))]}

def build_temporary_html():
    from parts_css import CSS_CONTENT
    from parts_html import HTML_CONTENT
    from parts_js_core import JS_CORE
    from parts_js_service import JS_SERVICE
    from parts_js_ui import JS_UI
    directory=tempfile.TemporaryDirectory(prefix='previsoes-tests-')
    path=Path(directory.name)/'index.html'
    if os.environ.get('PREVISOES_TEST_DISTRIBUTED')=='1':
        content=(ROOT/'index.html').read_text(encoding='utf-8')
    else:
        content='<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Teste isolado</title><style>'+CSS_CONTENT+'</style></head><body>'+HTML_CONTENT+'<script>'+JS_CORE+'\n'+JS_SERVICE+'\n'+JS_UI+'</script></body></html>'
    path.write_text(content,encoding='utf-8')
    return directory,path

def open_app(browser,path,width=1440,height=1000,demo=True,touch=False):
    options={'has_touch':True,'is_mobile':True,'device_scale_factor':2} if touch else {}
    context=browser.new_context(timezone_id='America/Sao_Paulo',viewport={'width':width,'height':height},**options)
    page=context.new_page()
    page.set_default_timeout(5000)
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(path.as_uri(),timeout=15000)
    try:
        page.wait_for_function('window.App && App.DB.db && App.AlarmEngine.intervalId!==null',timeout=15000)
    except Exception as exc:
        raise RuntimeError('Application startup failed; page errors: '+repr(errors)) from exc
    page.evaluate('App.AlarmEngine.stop()')
    # Render the real clock before pausing test fixtures. Otherwise geometry
    # would only exercise the much shorter initial "--:--:--" placeholder.
    page.evaluate('async()=>{await App.AlarmEngine.tick()}')
    if demo:
        page.evaluate('async()=>{await App.Service.loadDemoData();await App.UI.renderDashboard()}')
    return context,page,errors
