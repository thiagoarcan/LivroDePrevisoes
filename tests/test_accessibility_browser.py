"""Rendered accessibility/geometry checks; no claim of formal certification."""
import json,re,sys,unittest
from playwright.sync_api import sync_playwright
from browser_support import ROOT,build_temporary_html,open_app

class Accessibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp,cls.path=build_temporary_html();cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(channel='msedge',headless=True)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.temp.cleanup()
    def setUp(self):self.context,self.page,self.errors=open_app(self.browser,self.path)
    def tearDown(self):self.context.close()
    def ev(self,code):return self.page.evaluate(code)
    def test_no_duplicate_ids_after_repeated_navigation(self):
        for _ in range(2):
            for view in ['viewDashboard','viewNewEvent','viewPendingEvents','viewCompletedEvents','viewCadastros','viewConfigAlerts','viewConfigColors','viewBackup','viewDiagnostic']:
                self.page.evaluate('(v)=>App.UI.navigateTo(v)',view)
        duplicates=self.ev('()=>{let seen=new Set(),duplicates=[];for(let e of document.querySelectorAll("[id]")){if(seen.has(e.id))duplicates.push(e.id);seen.add(e.id)}return duplicates}')
        self.assertEqual(duplicates,[]);self.assertEqual(self.errors,[])
    def test_mobile_fields_and_main_actions_have_touch_size(self):
        self.page.set_viewport_size({'width':390,'height':844});self.ev('App.UI.applyResponsiveLayoutMode("auto",false)');self.ev('App.UI.navigateTo("viewNewEvent")')
        dimensions=self.ev('()=>["selectEventPipeline","selectEventUO","inputEventDate","inputEventTime","inputEventDescription","btnSubmitEvent","btnSubmitAndNew"].map(id=>{let r=document.getElementById(id).getBoundingClientRect();return {id,w:r.width,h:r.height,font:parseFloat(getComputedStyle(document.getElementById(id)).fontSize)}})')
        for x in dimensions:
            self.assertGreaterEqual(x['h'],44,x);self.assertGreaterEqual(x['font'],14,x)
    def test_description_enter_does_not_submit(self):
        self.ev('App.UI.navigateTo("viewNewEvent")')
        ids=self.ev('async()=>({pipeline:(await App.DB.getAll("pipelines")).find(e=>e.name==="OSCAN").id,uo:(await App.DB.getAll("operationalUnits")).find(e=>e.name==="REFAP").id})')
        self.page.locator('#selectEventPipeline').select_option(ids['pipeline']);self.page.locator('#selectEventUO').select_option(ids['uo'])
        self.page.locator('#inputEventDescription').fill('Não salvar por Enter');self.page.locator('#inputEventDescription').press('Enter')
        self.page.wait_for_timeout(80)
        count=self.ev('async()=>(await App.DB.getAll("events")).filter(e=>e.description.includes("Não salvar por Enter")).length')
        self.assertEqual(count,0)
    def test_metric_cards_support_keyboard(self):
        self.ev('App.UI.navigateTo("viewDashboard")')
        role=self.ev('()=>{let e=document.querySelector(".metric-card[data-filter=overdue]");return {tag:e.tagName,role:e.getAttribute("role"),tab:e.tabIndex}}')
        self.assertTrue(role['tag']=='BUTTON' or role['role']=='button' and role['tab']>=0,role)
        self.page.locator('.metric-card[data-filter=overdue]').focus();self.page.keyboard.press('Enter')
        self.page.wait_for_timeout(60)
        self.assertEqual(self.ev('App.UI.currentView'),'viewPendingEvents')
        self.assertTrue(self.ev('App.UI.activePendingEvents.every(e=>new Date(e.scheduledAt).getTime()<Date.now())'))
    def test_rendered_text_contrast_key_components(self):
        # Project acceptance threshold:4.5 normal /3 large;skip gradients requiring visual sampling.
        failures=[];checked=0
        for theme in ['dark','light','industrial']:
            self.page.evaluate('(t)=>App.UI.applyTheme(t)',theme);self.page.wait_for_timeout(250)
            for view in ['viewDashboard','viewNewEvent','viewPendingEvents','viewConfigAlerts']:
                self.page.evaluate('(v)=>App.UI.navigateTo(v)',view)
                samples=self.ev('''()=>{const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number);const lum=a=>a.slice(0,3).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0);let out=[];for(let e of document.querySelectorAll('.card-subtitle,.form-help,.metric-label,.nav-item,.btn-primary,.event-countdown')){if(!e.getClientRects().length||e.disabled)continue;let s=getComputedStyle(e),node=e,bg=null,gradient=false;while(node){let c=getComputedStyle(node);if(c.backgroundImage!=='none')gradient=true;let a=rgb(c.backgroundColor);if(a.length===3||a[3]===1){bg=a;break}node=node.parentElement}if(!bg||gradient)continue;let a=lum(rgb(s.color)),b=lum(bg),large=parseFloat(s.fontSize)>=24||parseFloat(s.fontSize)>=18.66&&parseInt(s.fontWeight)>=700;out.push({id:e.id,cls:String(e.className),text:e.textContent.trim().slice(0,45),ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05),minimum:large?3:4.5,color:s.color,bg})}return out}''')
                checked+=len(samples)
                failures.extend({'theme':theme,'view':view,**x} for x in samples if x['ratio']+0.02<x['minimum'])
        self.assertGreater(checked,25)
        self.assertEqual(failures,[],json.dumps(failures,ensure_ascii=False,indent=2))

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout).run(unittest.defaultTestLoader.loadTestsFromTestCase(Accessibility))
    (ROOT/'revisao_interface_2026_10_25/resultados/accessibility_ultimo.json').write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'details':[{'test':str(t),'trace':s} for t,s in result.failures+result.errors]},ensure_ascii=False,indent=2),encoding='utf-8')
    sys.exit(0 if result.wasSuccessful() else 1)
