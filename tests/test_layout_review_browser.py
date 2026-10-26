"""Cross-checks for Task 3 review fixes using actual browser data and controls."""
import json,sys,unittest
from playwright.sync_api import sync_playwright
from browser_support import build_temporary_html,open_app


class LayoutReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp,cls.path=build_temporary_html();cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(channel='msedge',headless=True)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.temp.cleanup()
    def setUp(self):self.context,self.page,self.errors=open_app(self.browser,self.path)
    def tearDown(self):self.assertEqual(self.errors,[]);self.context.close()
    def size(self,width):
        self.page.set_viewport_size({'width':width,'height':844 if width<768 else 1000})
        self.page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)')
    def view(self,name):self.page.evaluate('(name)=>App.UI.navigateTo(name)',name)
    def test_modal_title_message_close_and_actions_contrast_in_three_themes(self):
        self.size(390)
        event_id=self.page.evaluate('App.UI.getPresentationState().snapshot.events.find(e=>e.status==="pendente").id')
        for theme in ['dark','light','industrial']:
            self.page.evaluate('(theme)=>App.UI.applyTheme(theme)',theme)
            for dialog in ['confirm','complete']:
                if dialog=='confirm':self.page.evaluate('App.UI.showConfirmModal("Excluir previsão","Confirme a exclusão do registro.",()=>{})')
                else:self.page.evaluate('(id)=>App.UI.showCompleteModal(id)',event_id)
                samples=self.page.evaluate(r'''()=>{
                    const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number);
                    const lum=c=>c.slice(0,3).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((a,x,i)=>a+x*[.2126,.7152,.0722][i],0);
                    return [...document.querySelectorAll('.modal-overlay.active .modal-header h3,.modal-overlay.active .modal-close,.modal-overlay.active .modal-body p,.modal-overlay.active .modal-footer .btn')].filter(e=>e.getClientRects().length&&!e.disabled).map(e=>{
                        let node=e,bg;while(node){let color=rgb(getComputedStyle(node).backgroundColor);if(color.length===3||color[3]===1){bg=color;break}node=node.parentElement}
                        const a=lum(rgb(getComputedStyle(e).color)),b=lum(bg);return {text:e.textContent.trim(),ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)};
                    });}''')
                self.assertGreaterEqual(len(samples),4,(theme,dialog,samples))
                for sample in samples:self.assertGreaterEqual(sample['ratio'],4.5,(theme,dialog,sample))
                self.page.keyboard.press('Escape')
    def test_catalog_many_to_many_and_inactive_links_use_junction_readonly(self):
        self.size(3440);self.view('viewCadastros')
        data=self.page.evaluate('''async()=>{const s=await App.DB.snapshot(),p=s.pipelines.find(p=>p.name==='OSCAN'),u=s.operationalUnits.find(u=>u.name==='TEDEP');
            return {pipeline:p.id,uo:u.id,units:s.pipelineOperationalUnits.filter(l=>l.pipelineId===p.id).map(l=>s.operationalUnits.find(u=>u.id===l.uoId).name).sort(),pipelines:s.pipelineOperationalUnits.filter(l=>l.uoId===u.id).map(l=>s.pipelines.find(p=>p.id===l.pipelineId).name).sort()}}''')
        self.assertGreaterEqual(len(data['units']),2);self.assertGreaterEqual(len(data['pipelines']),2)
        self.page.evaluate('async(id)=>{App.UI.switchCadastrosCategory("pipelines");await App.UI.editPipeline(id)}',data['pipeline'])
        linked=self.page.locator('#cadastrosRelationsPanel dt').filter(has_text='UOs vinculadas').locator('xpath=following-sibling::dd[1]').inner_text()
        self.assertEqual(sorted(linked.split(', ')),data['units'])
        self.page.evaluate('async(id)=>{App.UI.switchCadastrosCategory("uos");await App.UI.editUO(id)}',data['uo'])
        linked=self.page.locator('#cadastrosRelationsPanel dt').filter(has_text='Dutos vinculados').locator('xpath=following-sibling::dd[1]').inner_text()
        self.assertEqual(sorted(linked.split(', ')),data['pipelines'])
        self.page.evaluate('''async(data)=>{let u=await App.DB.get('operationalUnits',data.uo);u.active=false;await App.DB.update('operationalUnits',u);await App.UI.refreshPresentationCache();App.UI.switchCadastrosCategory('pipelines');await App.UI.editPipeline(data.pipeline)}''',data)
        linked=self.page.locator('#cadastrosRelationsPanel dt').filter(has_text='UOs vinculadas').locator('xpath=following-sibling::dd[1]').inner_text()
        self.assertIn('TEDEP (inativo)',linked)
        unchanged=self.page.evaluate('''()=>{let s=App.UI.getPresentationState().snapshot,before=JSON.stringify(s);App.Presentation.catalog();return before===JSON.stringify(s)}''')
        self.assertTrue(unchanged)
    def test_tables_have_named_keyboard_scroll_and_readable_cells(self):
        for width in [320,390,768,1024,1440]:
            self.size(width);self.view('viewDiagnostic')
            self.assertEqual(self.page.locator('#tableDiagCollections').count(),1,'Diagnostic table must have a stable accessible scroll region')
            wrapper=self.page.locator('#tableDiagCollections').locator('xpath=..')
            self.assertEqual(wrapper.get_attribute('role'),'region')
            self.assertIn('Coleções',wrapper.get_attribute('aria-label'))
            self.assertEqual(wrapper.get_attribute('tabindex'),'0')
            geometry=wrapper.evaluate('(e)=>({width:e.clientWidth,scroll:e.scrollWidth})')
            if geometry['scroll']>geometry['width']+2:
                wrapper.focus();self.page.keyboard.press('ArrowRight')
                self.page.wait_for_function('document.getElementById("tableDiagCollections").parentElement.scrollLeft>0')
            values=self.page.evaluate('''()=>[...document.querySelectorAll('#tbodyDiagCollections tr')].map(row=>({h:row.getBoundingClientRect().height,w:row.cells[1].getBoundingClientRect().width,text:row.cells[1].textContent}))''')
            for value in values:self.assertLess(value['h'],180,(width,value));self.assertGreater(value['w'],144,(width,value))
    def test_mobile_backup_keeps_complete_selected_filename_and_command(self):
        for width in [320,390]:
            self.size(width);self.view('viewBackup')
            self.assertEqual(self.page.locator('#backupSelectedFileName').count(),1,'Complete file name must be available outside the native input')
            filename='backup-operacional-com-nome-longo-acentuação-console-C04-2026-10-25.json'
            data=self.page.evaluate('async()=>JSON.stringify(await App.Backup.createSnapshot())')
            self.page.locator('#inputImportBackupFile').set_input_files({'name':filename,'mimeType':'application/json','buffer':data.encode()})
            self.assertEqual(self.page.locator('#backupSelectedFileName').inner_text(),filename)
            self.assertTrue(self.page.locator('#btnTriggerImportValidate').is_enabled())
            self.assertTrue(self.page.locator('#backupSelectedFileName').evaluate('(e)=>e.scrollWidth<=e.clientWidth+2'))
            self.assertGreaterEqual(self.page.locator('#inputImportBackupFile').bounding_box()['width'],200)
    def test_tablet_and_conventional_metrics_precede_focus(self):
        for width in [768,1024,1440,1919]:
            self.size(width);self.view('viewDashboard')
            metrics=self.page.locator('.dashboard-metrics').bounding_box();focus=self.page.locator('.dashboard-highlight-grid').bounding_box()
            self.assertLessEqual(metrics['y']+metrics['height'],focus['y']+2,(width,metrics,focus))
    def test_completed_filter_scope_and_resize_preserve_selected_value(self):
        self.size(390);self.view('viewCompletedEvents')
        self.assertEqual(self.page.locator('#completedFilters summary').count(),1,'Completed filters must expose a native disclosure')
        self.page.locator('#completedFilters summary').click()
        option=self.page.locator('#filterCompletedConsole option').nth(1)
        value=option.get_attribute('value');label=option.text_content().strip()
        self.page.locator('#filterCompletedConsole').select_option(value)
        self.page.wait_for_function('(label)=>document.getElementById("completedFiltersSummary").textContent.includes(label)',arg=label)
        self.page.locator('#completedFilters summary').click()
        self.size(1440)
        self.assertEqual(self.page.locator('#filterCompletedConsole').input_value(),value)
        self.assertIn(label,self.page.locator('#completedFiltersSummary').inner_text())

if __name__=='__main__':unittest.main(verbosity=2)
