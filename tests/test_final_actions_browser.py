"""Useful tablet regions and operational actions affected by the final review."""
import re,unittest
from playwright.sync_api import sync_playwright
from browser_support import build_temporary_html,open_app

CONTRAST=r'''e=>{const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number),lum=c=>c.slice(0,3).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((a,x,i)=>a+x*[.2126,.7152,.0722][i],0);let n=e,bg;while(n){const c=rgb(getComputedStyle(n).backgroundColor);if(c.length===3||c[3]===1){bg=c;break}n=n.parentElement}const a=lum(rgb(getComputedStyle(e).color)),b=lum(bg);return (Math.max(a,b)+.05)/(Math.min(a,b)+.05)}'''

class FinalActions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp,cls.path=build_temporary_html();cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(channel='msedge',headless=True)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.temp.cleanup()
    def setUp(self):self.context,self.page,self.errors=open_app(self.browser,self.path,width=390,height=844,touch=True)
    def tearDown(self):self.assertEqual(self.errors,[]);self.context.close()
    def test_tablet_list_detail_have_usable_width_and_selection(self):
        for width,height in [(1024,768),(1199,800)]:
            self.page.set_viewport_size({'width':width,'height':height})
            self.page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false);App.UI.navigateTo("viewPendingEvents")')
            boxes=self.page.evaluate('''()=>Object.fromEntries(['.app-nav','.pending-master','.pending-detail-pane'].map(s=>[s,document.querySelector(s).getBoundingClientRect().toJSON()]))''')
            rail,master,detail=[boxes[k] for k in ['.app-nav','.pending-master','.pending-detail-pane']]
            self.assertGreater(rail['width'],40);self.assertGreaterEqual(master['left'],rail['right'])
            self.assertGreater(master['width'],320);self.assertGreater(detail['width'],280)
            self.assertGreaterEqual(detail['left'],master['right']);self.assertLessEqual(detail['right'],width)
            cards=self.page.locator('#containerPendingCards .event-card');self.assertGreaterEqual(cards.count(),2)
            card=cards.nth(1);identity=card.get_attribute('data-event-id');card.locator('.event-desc').tap()
            self.page.wait_for_function('(id)=>App.UI.selectedDetailEventId===id',arg=identity)
            description=card.locator('.event-desc').inner_text()
            self.page.wait_for_function('(description)=>document.querySelector(".pending-detail-pane").textContent.includes(description)',arg=description)
            self.assertIn(description,self.page.locator('.pending-detail-pane').inner_text())
    def test_firing_card_and_spotlight_keep_acknowledge_snooze_complete_direct(self):
        event_id=self.page.evaluate('''async()=>{let e=App.UI.getPresentationState().snapshot.events.find(e=>e.status==='pendente'&&e.consoleId===App.UI.activeConsoleId);e.alarmState='triggered';e.scheduledAt=new Date(Date.now()-3600000).toISOString();await App.DB.update('events',e);await App.UI.renderDashboard();return e.id}''')
        actions=self.page.locator('#spotlightActions')
        for label in ['Reconhecer','Adiar','Concluir','Mais']:self.assertTrue(actions.get_by_role('button',name=re.compile(label)).is_visible())
        self.page.evaluate('App.UI.navigateTo("viewPendingEvents")')
        card=self.page.locator(f'#containerPendingCards .event-card[data-event-id="{event_id}"]')
        for label in ['Reconhecer','Adiar','Concluir','Mais']:self.assertTrue(card.get_by_role('button',name=re.compile(label)).is_visible())
        card.get_by_role('button',name='Adiar',exact=True).tap();self.page.wait_for_selector('#modalSnooze.active')
        self.page.locator('#btnCancelSnooze').tap()
        self.assertEqual(self.page.evaluate('(id)=>App.DB.get("events",id)',event_id)['alarmState'],'triggered')
        card.get_by_role('button',name='Reconhecer',exact=True).tap()
        self.page.wait_for_function('async(id)=>(await App.DB.get("events",id)).alarmState==="acknowledged"',arg=event_id)
        event=self.page.evaluate('(id)=>App.DB.get("events",id)',event_id)
        self.assertEqual(event['status'],'pendente');self.assertTrue(event['active'])
    def test_sheet_secondary_routes_and_destructive_section_preserve_identity(self):
        self.page.evaluate('App.UI.navigateTo("viewPendingEvents")')
        card=self.page.locator('#containerPendingCards .event-card').first;event_id=card.get_attribute('data-event-id')
        before=self.page.evaluate('async()=>(await App.DB.getAll("events")).length')
        def sheet():
            self.page.evaluate('App.UI.navigateTo("viewPendingEvents")')
            self.page.locator(f'.event-card[data-event-id="{event_id}"]').get_by_role('button',name=re.compile('Mais')).tap()
            result=self.page.locator('#modalEventActionSheet.active');result.wait_for(state='visible');return result
        menu=sheet();destructive=menu.get_by_role('region',name='Ação destrutiva')
        self.assertTrue(destructive.is_visible());self.assertEqual(destructive.get_by_role('button').count(),1)
        menu.get_by_role('button',name=re.compile('Detalhes')).tap();self.page.wait_for_selector('#modalEventDetails.active')
        self.assertEqual(self.page.evaluate('App.UI.selectedEventForAction.id'),event_id)
        self.page.keyboard.press('Escape')
        sheet().get_by_role('button',name=re.compile('Editar')).tap()
        self.page.wait_for_function('(id)=>document.getElementById("eventEditId").value===id',arg=event_id)
        self.assertEqual(self.page.locator('#eventEditId').input_value(),event_id)
        self.page.locator('#btnCancelEditEvent').click()
        sheet().get_by_role('button',name=re.compile('Duplicar')).tap()
        self.page.wait_for_function('App.UI.currentView==="viewNewEvent"')
        self.assertEqual(self.page.locator('#eventEditId').input_value(),'')
        self.assertEqual(self.page.evaluate('async()=>(await App.DB.getAll("events")).length'),before)
    def test_audio_status_text_and_header_warning_contrast_in_three_themes(self):
        self.page.set_viewport_size({'width':320,'height':640})
        self.page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)')
        for theme in ['dark','light','industrial']:
            self.page.evaluate('(t)=>App.UI.applyTheme(t)',theme)
            self.page.locator('#btnHeaderAppStatus').tap();self.page.wait_for_selector('#modalAppStatus.active')
            for ready in [False,True]:
                self.page.evaluate('''ready=>{let ctx=App.Audio.ctx;App.Audio.ctx={state:ready?'running':'suspended'};App.Audio.isUnlocked=ready;App.Audio.updateStatusPill();App.Audio.ctx=ctx}''',ready)
                text=self.page.locator('#statusModalAudio>span')
                self.assertGreaterEqual(text.evaluate(CONTRAST),4.5,(theme,ready,text.inner_text()))
            self.page.keyboard.press('Escape')
            self.page.evaluate('App.Audio.isUnlocked=false;App.Audio.updateStatusPill()')
            warning=self.page.locator('#chipHeaderAudioWarning');self.assertTrue(warning.is_visible())
            self.assertGreaterEqual(warning.evaluate(CONTRAST),4.5,theme)
            clock_box=self.page.locator('#liveClock').bounding_box();warning_box=warning.bounding_box()
            self.assertLess(abs(clock_box['y']+clock_box['height']/2-warning_box['y']-warning_box['height']/2),2,(theme,clock_box,warning_box))

if __name__=='__main__':unittest.main()
