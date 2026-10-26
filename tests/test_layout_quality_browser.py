"""Visual review regressions: useful composition, readable tables and true context."""
import re,sys,unittest
from playwright.sync_api import sync_playwright
from browser_support import build_temporary_html,open_app


class LayoutQuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp,cls.path=build_temporary_html();cls.pw=sync_playwright().start()
        cls.browser=cls.pw.chromium.launch(channel='msedge',headless=True)

    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.temp.cleanup()
    def setUp(self):self.context,self.page,self.errors=open_app(self.browser,self.path)
    def tearDown(self):self.context.close()
    def size(self,width,height=1000):
        self.page.set_viewport_size({'width':width,'height':height})
        self.page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)')
    def view(self,view):self.page.evaluate('(v)=>App.UI.navigateTo(v)',view)

    def test_wide_dashboard_regions_share_first_operational_row(self):
        for width in [1920,2200,2559,2560,3440]:
            self.size(width);self.view('viewDashboard')
            d=self.page.evaluate('''()=>{const r=s=>document.querySelector(s).getBoundingClientRect().toJSON();
                return {focus:r('.dashboard-highlight-grid'),urgent:r('#cardDashboardUrgent'),panorama:r('#dashboardContextPanel'),metrics:r('.dashboard-metrics')}}''')
            self.assertLessEqual(d['urgent']['top'],d['focus']['top']+80,(width,d))
            self.assertLessEqual(d['panorama']['top'],d['focus']['top']+160,(width,d))
            self.assertLess(d['metrics']['top'],900,(width,d))

    def test_wide_alert_settings_prioritize_form_and_compact_notice(self):
        for width in [1920,3440]:
            self.size(width);self.view('viewConfigAlerts')
            d=self.page.evaluate('''()=>{const r=s=>document.querySelector(s).getBoundingClientRect().toJSON();
                return {main:r('.app-main'),notice:r('#viewConfigAlerts>.notice-banner'),form:r('#formAlertSettings'),preview:r('#settingsPreviewPanel')}}''')
            self.assertLess(d['notice']['height'],350,d)
            self.assertLess(d['form']['left']-d['main']['left'],60,d)
            self.assertLessEqual(d['preview']['top'],d['form']['top']+250,d)

    def test_mobile_backup_operations_stack_at_readable_width(self):
        for width in [320,390,600]:
            self.size(width,844);self.view('viewBackup')
            d=self.page.evaluate('''()=>{let p=document.querySelector('.backup-operations');
                return {parent:p.getBoundingClientRect().toJSON(),children:[...p.children].filter(e=>e.getClientRects().length).map(e=>e.getBoundingClientRect().toJSON())}}''')
            self.assertGreaterEqual(len(d['children']),2)
            a,b=d['children'][:2]
            self.assertGreaterEqual(a['width'],d['parent']['width']-2,d)
            self.assertGreaterEqual(b['top'],a['bottom']-2,d)

    def test_mobile_diagnostic_table_does_not_break_narrative_by_character(self):
        self.size(390,844);self.view('viewDiagnostic')
        d=self.page.evaluate('''()=>{let rows=[...document.querySelectorAll('#tbodyDiagCollections tr')];
            return rows.map(row=>{let e=row.cells[1],s=getComputedStyle(e),r=e.getBoundingClientRect();
            return {width:r.width-parseFloat(s.paddingLeft)-parseFloat(s.paddingRight),height:row.getBoundingClientRect().height,text:e.textContent.trim()}})}''')
        self.assertGreaterEqual(len(d),10)
        for row in d:
            self.assertGreaterEqual(row['width'],120,row)
            self.assertLess(row['height'],240,row)

    def test_catalog_context_uses_actual_relation_store_and_current_tag_draft(self):
        self.size(3440)
        self.page.evaluate('''async()=>{let s=await App.DB.snapshot(),u=s.operationalUnits.find(u=>u.name==='REFAP'),p=s.pipelines.find(p=>p.name!=='OSCAN');
            let ids=s.pipelineOperationalUnits.filter(l=>l.pipelineId===p.id).map(l=>l.uoId);
            await App.Service.savePipeline({...p,uoIds:[...new Set([...ids,u.id])]})}''')
        self.view('viewCadastros')
        expected=self.page.evaluate('''async()=>{let s=await App.DB.snapshot();let p=s.pipelines.find(p=>p.name==='OSCAN');
            App.UI.switchCadastrosCategory('pipelines');await App.UI.editPipeline(p.id);
            return s.pipelineOperationalUnits.filter(l=>l.pipelineId===p.id).map(l=>s.operationalUnits.find(u=>u.id===l.uoId).name)}''')
        self.assertGreaterEqual(len(expected),2)
        for name in expected:self.assertIn(name,self.page.locator('#cadastrosRelationsPanel').inner_text())
        pipes=self.page.evaluate('''async()=>{App.UI.switchCadastrosCategory('uos');let s=await App.DB.snapshot(),u=s.operationalUnits.find(u=>u.name==='REFAP');await App.UI.editUO(u.id);
            return s.pipelineOperationalUnits.filter(l=>l.uoId===u.id).map(l=>s.pipelines.find(p=>p.id===l.pipelineId).name)}''')
        self.assertGreaterEqual(len(pipes),2)
        for name in pipes:self.assertIn(name,self.page.locator('#cadastrosRelationsPanel').inner_text())
        self.page.evaluate('App.UI.switchCadastrosCategory("tags")')
        self.page.locator('#inputTagCode').fill('TAG-PRÉVIA-99')
        self.assertIn('TAG-PRÉVIA-99',self.page.locator('#cadastrosRelationsPanel').inner_text())

    def test_mobile_catalog_tag_codes_keep_readable_column(self):
        self.size(390,844);self.view('viewCadastros')
        self.page.evaluate('App.UI.switchCadastrosCategory("tags")')
        cells=self.page.evaluate('''()=>[...document.querySelectorAll('#tbodyEquipmentTags tr')].map(row=>{
            let e=row.cells[0],s=getComputedStyle(e),r=e.getBoundingClientRect();
            return {width:r.width-parseFloat(s.paddingLeft)-parseFloat(s.paddingRight),height:row.getBoundingClientRect().height,text:e.textContent.trim()}})''')
        self.assertTrue(cells)
        for cell in cells:
            self.assertGreaterEqual(cell['width'],120,cell)
            self.assertLess(cell['height'],240,cell)

    def test_modal_text_uses_readable_background_in_each_theme(self):
        def luminance(color):
            rgb=[float(x)/255 for x in re.findall(r'[\d.]+',color)[:3]]
            vals=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]
            return sum(a*b for a,b in zip(vals,[.2126,.7152,.0722]))
        for theme in ['dark','light','industrial']:
            self.page.evaluate('(t)=>App.UI.applyTheme(t)',theme)
            self.page.evaluate('App.UI.showConfirmModal("Confirmação legível","Mensagem operacional de confirmação",()=>{})')
            colors=self.page.evaluate('''()=>{let e=document.getElementById('modalConfirmMessage'),node=e,bg;
                while(node){bg=getComputedStyle(node).backgroundColor;if(!bg.endsWith(', 0)')&&bg!=='transparent')break;node=node.parentElement}
                return {text:getComputedStyle(e).color,bg}}''')
            a,b=luminance(colors['text']),luminance(colors['bg'])
            self.assertGreaterEqual((max(a,b)+.05)/(min(a,b)+.05),4.5,(theme,colors))
            self.page.keyboard.press('Escape')

    def test_active_console_value_fits_closed_selector(self):
        for width in [1024,1440,1920,3440]:
            self.size(width)
            d=self.page.evaluate('''()=>{let e=document.getElementById('headerActiveConsole'),s=getComputedStyle(e),c=document.createElement('canvas').getContext('2d');
                c.font=s.font;return {width:e.clientWidth,needed:c.measureText(e.selectedOptions[0].textContent.trim()).width+parseFloat(s.paddingLeft)+parseFloat(s.paddingRight)+22}}''')
            self.assertGreaterEqual(d['width'],d['needed'],(width,d))

    def test_dependency_recommendation_reads_as_one_sentence(self):
        self.size(390,844)
        self.page.evaluate('App.UI.showDependencyModal("Dependências",["1 vínculo real"],()=>{})')
        d=self.page.locator('#modalDependency .notice-banner strong').bounding_box()
        self.assertIsNotNone(d)
        self.assertGreaterEqual(d['width'],70,d)
        self.assertLessEqual(d['height'],48,d)

    def test_completed_mobile_advanced_filters_are_retractable_and_preserve_value(self):
        self.size(390,844);self.view('viewCompletedEvents')
        self.assertFalse(self.page.locator('#filterCompletedConsole').is_visible())
        first=self.page.locator('#containerCompletedCards .completed-event-card').first.bounding_box()
        self.assertIsNotNone(first)
        self.assertLess(first['y'],804,first)
        disclosure=self.page.locator('#viewCompletedEvents summary').filter(has_text=re.compile('Filtros',re.I)).first
        disclosure.click()
        self.assertTrue(self.page.locator('#filterCompletedConsole').is_visible())
        option=self.page.locator('#filterCompletedConsole option').nth(1).get_attribute('value')
        self.page.locator('#filterCompletedConsole').select_option(option)
        disclosure.click()
        self.assertFalse(self.page.locator('#filterCompletedConsole').is_visible())
        disclosure.click()
        self.assertEqual(self.page.locator('#filterCompletedConsole').input_value(),option)


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout).run(unittest.defaultTestLoader.loadTestsFromTestCase(LayoutQuality))
    sys.exit(0 if result.wasSuccessful() else 1)
