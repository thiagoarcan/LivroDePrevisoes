"""Scoped independent verification of the final fix against distributed HTML."""
import json, os, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tests'))
os.environ['PREVISOES_TEST_DISTRIBUTED']='1'
from browser_support import build_temporary_html, open_app, source_fingerprints
from playwright.sync_api import sync_playwright
before=source_fingerprints()
suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(n) for n in ['test_final_findings_browser','test_final_actions_browser'])
with (OUT/'final-fix-review-tests.log').open('w',encoding='utf-8') as stream:
    result=unittest.TextTestRunner(verbosity=2,stream=stream).run(suite)
rows=[]
temp,path=build_temporary_html()
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    context,page,errors=open_app(browser,path,width=320,height=640,touch=True)
    page.evaluate('App.Audio.isUnlocked=false;App.Audio.updateStatusPill()')
    rows.append(page.evaluate('''()=>Object.fromEntries(['.app-header','#liveClock','#chipHeaderAudioWarning'].map(s=>[s,document.querySelector(s).getBoundingClientRect().toJSON()]))'''))
    page.screenshot(path=str(OUT/'fix-review-header-320.png'),animations='disabled')
    for width,height in [(1024,768),(1199,800)]:
        page.set_viewport_size({'width':width,'height':height})
        page.evaluate('async()=>{await App.UI.applyResponsiveLayoutMode("auto",false);await App.UI.navigateTo("viewPendingEvents")}')
        rows.append(page.evaluate('''()=>({width:innerWidth,boxes:Object.fromEntries(['.app-nav','.pending-master','.pending-detail-pane'].map(s=>[s,document.querySelector(s).getBoundingClientRect().toJSON()]))})'''))
    page.set_viewport_size({'width':390,'height':844})
    page.evaluate('async()=>{await App.UI.applyResponsiveLayoutMode("auto",false);await App.UI.navigateTo("viewPendingEvents")}')
    more=page.locator('#containerPendingCards .btn-card-more-actions').first
    more.click();page.wait_for_selector('#modalEventActionSheet.active')
    page.keyboard.press('Escape')
    assert more.evaluate('e=>document.activeElement===e'), 'Sheet Escape must restore focus to More'
    more.click();page.wait_for_selector('#modalEventActionSheet.active')
    page.locator('#modalEventActionSheet .action-sheet-destructive button').click()
    page.wait_for_selector('#modalConfirm.active')
    page.locator('#btnCancelConfirm').click()
    assert more.evaluate('e=>document.activeElement===e'), 'Delete cancellation must restore focus to original More'
    rows.append({'sheet_escape_and_delete_cancel_restore_focus':True})
    context.close();browser.close()
temp.cleanup()
report={'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'distributed_html':True,'sources_stable':before==source_fingerprints(),'source_hashes':before,'geometry':rows,'page_errors':errors}
(OUT/'final-fix-review-probe.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if result.wasSuccessful() and not errors and report['sources_stable'] else 1)
