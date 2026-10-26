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
        self.ev('async()=>{const e=(await App.DB.getAll("events")).find(x=>x.status==="pendente");await App.UI.showAlarmModal(e);document.getElementById("btnAlarmSnoozePrompt").click()}')
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

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout).run(unittest.defaultTestLoader.loadTestsFromTestCase(UIController))
    sys.exit(0 if result.wasSuccessful() else 1)
