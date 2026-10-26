"""Presentation contract: real context, scoped selection and live unsaved preview."""
import unittest
from playwright.sync_api import sync_playwright
from browser_support import build_temporary_html,open_app

class Presentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp,cls.path=build_temporary_html();cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(channel='msedge',headless=True)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.temp.cleanup()
    def setUp(self):self.context,self.page,self.errors=open_app(self.browser,self.path)
    def tearDown(self):self.context.close()
    def test_dashboard_context_uses_snapshot_not_previous_list(self):
        self.page.evaluate('App.UI.activePendingEvents=[];App.UI.navigateTo("viewDashboard")')
        self.page.wait_for_timeout(100)
        data=self.page.evaluate('''()=>({actual:document.getElementById('dashboardContextPanel')?.dataset.total,expected:App.UI.getPresentationState().snapshot.events.filter(e=>e.active!==false&&e.status==='pendente'&&(!App.UI.activeConsoleId||e.consoleId===App.UI.activeConsoleId)).length})''')
        self.assertEqual(data['actual'],str(data['expected']))
    def test_draft_preview_is_live_and_does_not_persist(self):
        self.page.evaluate('App.UI.navigateTo("viewNewEvent")')
        self.assertEqual(self.page.locator('#inputEventDescription').input_value(),'')
        self.assertTrue(self.page.locator('#inputEventNotes').count()==1)
        self.page.locator('#inputEventDescription').fill('Rascunho sem gravação')
        self.assertIn('Rascunho sem gravação',self.page.locator('#eventDraftSummary').inner_text())
        self.assertEqual(self.page.evaluate('async()=>(await App.DB.getAll("events")).filter(e=>e.description==="Rascunho sem gravação").length'),0)
    def test_pending_table_and_cards_share_master_with_detail(self):
        self.assertTrue(self.page.evaluate('''()=>{let g=document.querySelector('.pending-master-detail-grid'),a=document.getElementById('containerPendingCards'),b=document.getElementById('containerPendingTable');return a.parentElement===b.parentElement&&g.contains(b)&&g.contains(document.getElementById('pendingDetailPane'))}'''))
    def test_new_event_has_operational_fieldsets(self):
        legends=[text.strip() for text in self.page.locator('#formEvent fieldset legend').all_text_contents()]
        for name in ['Localização','Programação','Atividade','Alarme','Lousa']:self.assertIn(name,legends)
    def test_mobile_catalog_has_list_editor_and_return(self):
        self.page.set_viewport_size({'width':390,'height':844})
        self.page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false);App.UI.navigateTo("viewCadastros")')
        self.page.locator('[data-catalog-new=formConsole]').click()
        self.page.locator('#inputConsoleName').fill('Rascunho cadastral')
        self.page.locator('#formConsole [data-catalog-back]').click()
        self.assertFalse(self.page.locator('#inputConsoleName').is_visible())
        self.assertEqual(self.page.locator('#inputConsoleName').input_value(),'Rascunho cadastral')

if __name__=='__main__':unittest.main(verbosity=2)
