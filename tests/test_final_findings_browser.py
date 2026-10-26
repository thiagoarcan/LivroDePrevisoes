"""Regressions from the independent whole-delivery review."""
import json,re,sys,unittest
from playwright.sync_api import sync_playwright
from browser_support import build_temporary_html,open_app


class FinalFindings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp,cls.path=build_temporary_html();cls.pw=sync_playwright().start()
        cls.browser=cls.pw.chromium.launch(channel='msedge',headless=True)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.temp.cleanup()
    def setUp(self):self.context,self.page,self.errors=open_app(self.browser,self.path,width=1024,height=768,touch=True)
    def tearDown(self):self.context.close()
    def size(self,width,height):
        self.page.set_viewport_size({'width':width,'height':height})
        self.page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)')
    def view(self,view):self.page.evaluate('(v)=>App.UI.navigateTo(v)',view)

    def test_tablet_landscape_has_operable_rail_and_preserves_selection(self):
        self.view('viewPendingEvents')
        selected=self.page.evaluate('App.UI.selectedDetailEventId')
        self.assertTrue(selected)
        for width,height in [(1024,768),(1199,800)]:
            self.size(width,height)
            nav=self.page.locator('.app-nav');self.assertTrue(nav.is_visible())
            r=nav.bounding_box();self.assertGreaterEqual(r['height'],400,r);self.assertGreater(r['width'],40,r);self.assertLessEqual(r['width'],120,r)
            self.assertGreaterEqual(r['x'],0,r);self.assertLessEqual(r['x']+r['width'],width,r)
            nav.get_by_role('button',name=re.compile('Painel')).focus();self.page.keyboard.press('Enter')
            self.page.wait_for_function('App.UI.currentView==="viewDashboard"')
            nav.get_by_role('button',name=re.compile('Pendentes')).tap()
            self.page.wait_for_function('App.UI.currentView==="viewPendingEvents"')
            self.assertEqual(self.page.evaluate('App.UI.selectedDetailEventId'),selected)
            self.size(768,1024)
            self.assertEqual(self.page.evaluate('App.UI.selectedDetailEventId'),selected)
        self.assertEqual(self.errors,[])

    def test_tablet_landscape_drawing_is_parallel_and_survives_rotation(self):
        self.view('viewNewEvent');self.page.locator('#inputEventDescription').fill('Rascunho tablet preservado')
        self.page.locator('#btnToggleStylusCanvas').click()
        for width,height in [(1024,768),(1199,800)]:
            self.size(width,height)
            d=self.page.evaluate('''()=>{let r=s=>document.querySelector(s).getBoundingClientRect().toJSON();
                return {editor:r('.fieldset-atividade'),drawing:r('.fieldset-lousa'),canvas:r('#stylusDrawingCanvas')}}''')
            self.assertGreaterEqual(d['drawing']['left'],d['editor']['right']-2,d)
            self.assertLessEqual(d['drawing']['top'],d['editor']['top']+100,d)
            self.assertGreater(d['editor']['width'],250,d)
            self.assertAlmostEqual(d['canvas']['width']/d['canvas']['height'],1200/440,delta=.03)
        canvas=self.page.locator('#stylusDrawingCanvas');canvas.scroll_into_view_if_needed();r=canvas.bounding_box()
        self.page.mouse.move(r['x']+20,r['y']+20);self.page.mouse.down();self.page.mouse.move(r['x']+90,r['y']+50,steps=5);self.page.mouse.up()
        before=self.page.evaluate('App.UI.getStylusData()');self.assertTrue(before)
        self.page.locator('#inputEventDescription').focus()
        self.size(768,1024);self.size(1024,768)
        self.assertEqual(self.page.locator('#inputEventDescription').input_value(),'Rascunho tablet preservado')
        self.assertEqual(self.page.evaluate('App.UI.getStylusData()'),before)
        self.assertEqual(self.page.evaluate('document.activeElement.id'),'inputEventDescription')
        self.assertEqual(self.errors,[])

    def test_mobile_and_tablet_show_real_clock_and_conditional_audio_warning(self):
        for width,height in [(320,640),(390,844),(600,900),(768,1024),(820,1180),(1024,768),(1199,800)]:
            self.size(width,height)
            self.page.evaluate('App.Audio.isUnlocked=false;App.Audio.updateStatusPill()')
            for selector in ['#liveClock','#chipHeaderAudioWarning']:
                node=self.page.locator(selector);self.assertTrue(node.is_visible(),(width,selector))
                r=node.bounding_box();self.assertGreater(r['width'],16,(width,selector,r));self.assertGreaterEqual(r['height'],16,(width,selector,r))
                self.assertGreaterEqual(r['x'],-1,(width,selector,r));self.assertLessEqual(r['x']+r['width'],width+2,(width,selector,r))
            self.assertRegex(self.page.locator('#liveClock').inner_text(),r'\d{2}:\d{2}:\d{2}')
            self.page.evaluate('''()=>{let actual=App.Audio.ctx;App.Audio.ctx={state:'running'};App.Audio.isUnlocked=true;
                App.Audio.updateStatusPill();App.Audio.ctx=actual}''')
            self.assertFalse(self.page.locator('#chipHeaderAudioWarning').is_visible())
            self.assertTrue(self.page.locator('#liveClock').is_visible())
        self.assertEqual(self.errors,[])

    def test_mobile_card_secondary_actions_use_named_sheet_and_delete_cancel_is_safe(self):
        self.size(390,844);self.view('viewPendingEvents')
        card=self.page.locator('#containerPendingCards .event-card').first
        event_id=card.get_attribute('data-event-id')
        for method in ['editEvent','duplicateEvent','showDetailsModal','deleteEvent']:
            self.assertEqual(card.locator('button[onclick*="'+method+'"]:visible').count(),0,method)
        self.assertTrue(card.get_by_role('button',name=re.compile('Concluir')).is_visible())
        card.get_by_role('button',name=re.compile('Mais')).tap()
        sheet=self.page.locator('#modalEventActionSheet.active')
        sheet.wait_for(state='visible')
        for label in ['Editar','Duplicar','Detalhes','Excluir']:
            self.assertTrue(sheet.get_by_role('button',name=re.compile(label)).is_visible(),label)
        sheet.get_by_role('button',name=re.compile('Excluir')).tap()
        self.page.wait_for_selector('#modalConfirm.active')
        self.page.locator('#btnCancelConfirm').tap()
        self.assertTrue(self.page.evaluate('async(id)=>(await App.DB.get("events",id)).active!==false',event_id))
        self.assertEqual(self.errors,[])

    def test_spotlight_mobile_secondary_actions_use_more(self):
        self.size(390,844);self.view('viewDashboard')
        actions=self.page.locator('#spotlightActions')
        for method in ['editEvent','duplicateEvent','showDetailsModal']:
            self.assertEqual(actions.locator('button[onclick*="'+method+'"]:visible').count(),0,method)
        self.assertTrue(actions.get_by_role('button',name=re.compile('Concluir')).is_visible())
        self.assertTrue(actions.get_by_role('button',name=re.compile('Mais')).is_visible())

    def test_drawer_diagnostic_and_copied_report_use_central_version(self):
        self.size(390,844);version=self.page.evaluate('App.Config.APP_VERSION')
        self.page.locator('#btnToggleMobileMenu').tap()
        self.assertIn(version,self.page.locator('#appMobileDrawer').inner_text())
        self.assertNotIn('v1.1.0',self.page.locator('#appMobileDrawer').inner_text())
        self.page.keyboard.press('Escape');self.view('viewDiagnostic')
        self.assertIn(version,self.page.locator('#diagAppVersion').inner_text())
        self.page.evaluate('Object.defineProperty(navigator,"clipboard",{configurable:true,value:{writeText:async(t)=>{window.copiedDiagnostic=t}}})')
        self.page.locator('#btnCopyDiagnostic').click()
        self.page.wait_for_function('!!window.copiedDiagnostic')
        self.assertEqual(json.loads(self.page.evaluate('window.copiedDiagnostic'))['version'],version)
        self.assertEqual(self.errors,[])

    def test_drawer_displays_configured_user_after_reload(self):
        self.size(390,844)
        self.page.evaluate('''async()=>{let s=await App.Service.getSettings();s.localUserName='Controladora Maria';await App.Service.saveSettings(s)}''')
        self.page.reload();self.page.wait_for_function('App.AlarmEngine.intervalId!==null');self.page.evaluate('App.AlarmEngine.stop()')
        self.page.locator('#btnToggleMobileMenu').tap()
        self.assertIn('Controladora Maria',self.page.locator('#labelDrawerUser').inner_text())
        self.assertEqual(self.errors,[])


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout).run(unittest.defaultTestLoader.loadTestsFromTestCase(FinalFindings))
    sys.exit(0 if result.wasSuccessful() else 1)
