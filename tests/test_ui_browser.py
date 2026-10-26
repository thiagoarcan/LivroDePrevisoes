"""Behavioral regressions for audited UI defects; runs real IndexedDB and DOM."""
import json,sys,unittest
from pathlib import Path
from playwright.sync_api import sync_playwright
from browser_support import ROOT,build_temporary_html,open_app

class UIRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp,cls.path=build_temporary_html()
        cls.pw=sync_playwright().start()
        cls.browser=cls.pw.chromium.launch(channel='msedge',headless=True)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop();cls.temp.cleanup()
    def setUp(self):
        self.context,self.page,self.errors=open_app(self.browser,self.path)
    def tearDown(self):
        self.context.close()
    def ev(self,code):return self.page.evaluate(code)

    def test_cancelled_confirmation_never_executes(self):
        actions=self.ev('()=>{let actions=[];App.UI.showConfirmModal("A","A",()=>actions.push("A"));document.getElementById("btnCancelConfirm").click();App.UI.showConfirmModal("B","B",()=>actions.push("B"));document.getElementById("btnAcceptConfirm").click();return actions}')
        self.assertEqual(actions,['B'])
    def test_cancelled_dependency_never_executes(self):
        actions=self.ev('()=>{let actions=[];App.UI.showDependencyModal("A",["x"],()=>actions.push("A"));document.getElementById("btnCloseDependencyModal").click();App.UI.showDependencyModal("B",["y"],()=>actions.push("B"));document.getElementById("btnDependencyInactivate").click();return actions}')
        self.assertEqual(actions,['B'])
    def test_demo_button_actually_loads_demo(self):
        self.ev('App.UI.navigateTo("viewBackup")')
        self.page.locator('#btnLoadDemoData').click();self.page.locator('#btnAcceptConfirm').click()
        self.page.wait_for_timeout(200)
        result=self.ev('async()=>({events:(await App.DB.getAll("events")).filter(e=>e.active!==false).length,uos:(await App.DB.getAll("operationalUnits")).length})')
        self.assertGreaterEqual(result['events'],6);self.assertGreaterEqual(result['uos'],4)
    def test_details_shows_saved_drawing(self):
        result=self.ev('async()=>{let ev=(await App.DB.getAll("events")).find(e=>e.status==="pendente");let canvas=document.createElement("canvas");canvas.width=10;canvas.height=10;canvas.getContext("2d").fillRect(0,0,10,10);ev.stylusDrawing=canvas.toDataURL("image/png");await App.DB.update("events",ev);await App.UI.showDetailsModal(ev.id);let img=document.getElementById("detailsModalDrawingImg");return {visible:!!img.getClientRects().length,source:img.src.startsWith("data:image/png;base64,")}}')
        self.assertTrue(result['visible']);self.assertTrue(result['source'])
    def test_spotlight_keeps_own_countdown_after_filtered_list(self):
        result=self.ev('async()=>{await App.UI.navigateTo("viewPendingEvents");document.getElementById("inputSearchPending").value="PIG";await App.UI.renderPendingEvents();await App.UI.navigateTo("viewDashboard");let before=document.getElementById("spotlightTimeLeft").textContent;App.UI.updateLiveTimers();return {before,after:document.getElementById("spotlightTimeLeft").textContent}}')
        self.assertEqual(result['before'],result['after'])
    def test_alarm_modal_countdown_moves(self):
        result=self.ev('async()=>{let e=(await App.DB.getAll("events")).find(e=>e.status==="pendente");await App.UI.showAlarmModal(e);let old=Date.now,before=document.getElementById("alarmModalCountdown").textContent;Date.now=()=>old()+120000;App.UI.updateLiveTimers();let after=document.getElementById("alarmModalCountdown").textContent;Date.now=old;return {before,after}}')
        self.assertNotEqual(result['before'],result['after'])
    def test_alarm_countdown_shows_second_precision(self):
        result=self.ev('async()=>{let e=(await App.DB.getAll("events")).find(e=>e.status==="pendente");e.scheduledAt=new Date(Date.now()+8*60000+10000).toISOString();await App.DB.update("events",e);await App.UI.showAlarmModal(e);let old=Date.now,before=document.getElementById("alarmModalCountdown").textContent;Date.now=()=>old()+1100;await App.UI.updateLiveTimers();let after=document.getElementById("alarmModalCountdown").textContent;Date.now=old;return {before,after}}')
        self.assertNotEqual(result['before'],result['after'],result)
    def test_temporal_classification_updates_without_action(self):
        result=self.ev('async()=>{let ev=(await App.DB.getAll("events")).find(e=>e.status==="pendente"&&e.consoleId===App.UI.activeConsoleId);ev.scheduledAt=new Date(Date.now()+16*60000).toISOString();ev.hasAlarm=false;await App.DB.update("events",ev);await App.UI.navigateTo("viewPendingEvents");let old=Date.now;Date.now=()=>old()+120000;await App.UI.updateLiveTimers();let card=[...document.querySelectorAll("#containerPendingCards .event-card")].find(e=>e.dataset.eventId===ev.id),after=card?.innerText||"";Date.now=old;return after}')
        self.assertIn('Crítico',result)
    def test_tablet_detail_initial_content_and_alarm_value(self):
        self.page.set_viewport_size({'width':1024,'height':768})
        text=self.ev('async()=>{await App.UI.applyResponsiveLayoutMode("tablet",false);await App.UI.navigateTo("viewPendingEvents");return document.getElementById("pendingDetailPane").innerText}')
        self.assertIn('Hierarquia',text.title());self.assertNotIn('undefined',text)
    def test_alarm_counts_agree(self):
        result=self.ev('async()=>{let es=(await App.DB.getAll("events")).filter(e=>e.status==="pendente");for(let e of es.slice(0,2)){e.alarmState="triggered";await App.DB.update("events",e)}await App.UI.renderDashboard();return {metric:document.getElementById("metricUnacknowledged").textContent,side:document.getElementById("tabletAlarmsCount").textContent}}')
        self.assertEqual(result,{'metric':'2','side':'2'})
    def test_completed_cards_really_expand(self):
        self.ev('App.UI.applyResponsiveLayoutMode("mobile",false)');self.ev('App.UI.navigateTo("viewCompletedEvents")')
        result=self.ev('()=>{let card=document.querySelector(".completed-event-card"),extra=card.querySelector(".completed-card-details,.completed-card-extra");let before=!!extra.getClientRects().length;card.click();return {before,after:!!extra.getClientRects().length}}')
        self.assertEqual(result,{'before':False,'after':True})
    def test_description_is_multiline(self):
        self.assertEqual(self.ev('document.getElementById("inputEventDescription").tagName'),'TEXTAREA')
    def test_category_survives_layout_change(self):
        result=self.ev('async()=>{await App.UI.applyResponsiveLayoutMode("tablet",false);await App.UI.navigateTo("viewCadastros");App.UI.switchCadastrosCategory("tags");await App.UI.applyResponsiveLayoutMode("tablet",false);return document.querySelector("#cadastrosCategoryBar .active")?.dataset.cat}')
        self.assertEqual(result,'tags')
    def test_modal_moves_and_traps_focus_and_restores(self):
        self.ev('App.UI.navigateTo("viewPendingEvents")');self.page.locator('#btnToggleFilters').focus()
        result=self.ev('async()=>{let e=(await App.DB.getAll("events")).find(e=>e.status==="pendente");await App.UI.showCompleteModal(e.id);return !!document.activeElement.closest("#modalCompleteEvent")}')
        self.assertTrue(result)
        for _ in range(12):
            self.page.keyboard.press('Tab');self.assertTrue(self.ev('!!document.activeElement.closest("#modalCompleteEvent")'))
        self.page.keyboard.press('Escape');self.assertEqual(self.ev('document.activeElement.id'),'btnToggleFilters')
    def test_closed_drawer_not_in_tab_sequence(self):
        self.page.set_viewport_size({'width':390,'height':844});self.ev('App.UI.applyResponsiveLayoutMode("mobile",false)')
        self.page.locator('#btnToggleMobileMenu').focus()
        for _ in range(22):
            self.page.keyboard.press('Tab');self.assertFalse(self.ev('!!document.activeElement.closest("#appMobileDrawer")'))
    def test_drawer_opens_and_closes_by_keyboard(self):
        self.page.set_viewport_size({'width':390,'height':844});self.ev('App.UI.applyResponsiveLayoutMode("mobile",false)')
        self.page.locator('#btnToggleMobileMenu').click();self.assertTrue(self.ev('!!document.activeElement.closest("#appMobileDrawer")'))
        self.page.keyboard.press('Escape');self.assertFalse(self.ev('document.getElementById("appMobileDrawer").classList.contains("open")'))
        self.assertEqual(self.ev('document.activeElement.id'),'btnToggleMobileMenu')
    def test_filters_are_bottom_sheet_on_mobile(self):
        self.page.set_viewport_size({'width':390,'height':844});self.ev('App.UI.applyResponsiveLayoutMode("mobile",false)');self.ev('App.UI.navigateTo("viewPendingEvents")')
        self.page.locator('#btnToggleFilters').click()
        position=self.ev('getComputedStyle(document.getElementById("filterDrawer")).position')
        self.assertEqual(position,'fixed')
    def test_cancel_import_discards_old_file(self):
        result=self.ev('async()=>{let seen=[];let old=App.Backup.importJSON;App.Backup.importJSON=async v=>{seen.push(v.exportedAt);return {applied:true,inserted:0,updated:0,skipped:0,conflicts:[]}};let base=await App.Backup.createSnapshot();App.UI.showImportSummaryModal({...base,exportedAt:"2026-01-01T00:00:00Z"});document.getElementById("btnCancelImportSummary").click();App.UI.showImportSummaryModal({...base,exportedAt:"2026-02-01T00:00:00Z"});document.getElementById("btnConfirmImportSummary").click();await new Promise(r=>setTimeout(r,100));App.Backup.importJSON=old;return seen}')
        self.assertEqual(result,['2026-02-01T00:00:00Z'])
    def test_metrics_apply_correct_time_filter(self):
        self.ev('App.UI.navigateTo("viewDashboard")');self.page.locator('[data-filter="15min"]').click()
        visible=self.ev('App.UI.activePendingEvents.map(e=>new Date(e.scheduledAt).getTime()-Date.now())')
        self.assertTrue(visible);self.assertTrue(all(0<=x<=15*60000 for x in visible),visible)
    def test_new_master_data_appears_in_filters(self):
        result=self.ev('async()=>{await App.UI.navigateTo("viewPendingEvents");let c=await App.Service.saveConsole({name:"NOVA"});await App.UI.renderPendingEvents();return [...document.getElementById("filterConsole").options].some(o=>o.value===c.id)}')
        self.assertTrue(result)
    def test_action_sheet_has_context(self):
        result=self.ev('async()=>{let e=(await App.DB.getAll("events")).find(e=>e.status==="pendente");await App.UI.openEventActionSheet(e.id);return document.getElementById("actionSheetEventSubtitle").textContent.trim()}')
        self.assertNotIn(result,['','--'])
    def test_display_preferences_actually_disable_pulsing(self):
        result=self.ev('async()=>{let s=await App.Service.getSettings();s.pulsingEnabled=false;s.highlightCardEnabled=false;await App.Service.saveSettings(s);await App.UI.navigateTo("viewPendingEvents");return document.querySelectorAll("#containerPendingCards .pulsing-card").length}')
        self.assertEqual(result,0)
    def test_settings_keep_zero_values(self):
        self.ev('App.UI.navigateTo("viewConfigAlerts")')
        self.page.locator('#inputDefaultLeadTime').fill('0')
        self.ev('()=>{let r=document.getElementById("rangeSoundVolume");r.value="0";r.dispatchEvent(new Event("input",{bubbles:true}))}')
        self.page.locator('#formAlertSettings button[type="submit"]').click()
        self.page.wait_for_timeout(100)
        result=self.ev('async()=>{let s=await App.Service.getSettings();return {lead:s.defaultLeadTimeMinutes,volume:s.soundVolume}}')
        self.assertEqual(result,{'lead':0,'volume':0})
    def test_all_dialogs_and_controls_have_accessible_names(self):
        missing=self.ev('()=>[...document.querySelectorAll("[role=dialog]")].filter(e=>!e.getAttribute("aria-label")&&!e.getAttribute("aria-labelledby")).map(e=>e.id)')
        self.assertEqual(missing,[])
        missing=self.ev('()=>[...document.querySelectorAll("input:not([type=hidden]),select,textarea")].filter(e=>!e.disabled&&!e.hidden&&getComputedStyle(e).display!=="none"&&!e.closest("label")&&!e.labels?.length&&!e.getAttribute("aria-label")&&!e.getAttribute("aria-labelledby")).map(e=>e.id)')
        self.assertEqual(missing,[])

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(UIRegression)
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout).run(suite)
    target=ROOT/'revisao_interface_2026_10_25/resultados/ui_ultimo.json'
    target.write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'details':[{'test':str(t),'trace':s} for t,s in result.failures+result.errors]},ensure_ascii=False,indent=2),encoding='utf-8')
    sys.exit(0 if result.wasSuccessful() else 1)
