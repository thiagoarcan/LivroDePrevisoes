"""Fallback and browser capability paths available on this machine."""
import json,sys,unittest
from playwright.sync_api import sync_playwright
from browser_support import ROOT,build_temporary_html,open_app

class Compatibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp,cls.path=build_temporary_html();cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(channel='msedge',headless=True)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.temp.cleanup()
    def setUp(self):self.context,self.page,self.errors=open_app(self.browser,self.path)
    def tearDown(self):self.context.close()
    def ev(self,code):return self.page.evaluate(code)
    def test_two_tabs_lease_fallback_without_navigator_locks(self):
        event_id=self.ev('async()=>App.DB.atomic(["events"],d=>{for(let e of d.events)e.hasAlarm=false;let e=d.events.find(e=>e.status==="pendente");Object.assign(e,{hasAlarm:true,useDefaultAlarmSettings:false,alarmMinutesBefore:0,alarmAudio:false,alarmVisual:false,alarmNotification:false,alarmRepeat:false,alarmState:"idle",lastAlarmTriggeredAt:null,alarmTriggerCount:0,scheduledAt:new Date(Date.now()-60000).toISOString()});return e.id})')
        second=self.context.new_page();second.goto(self.path.as_uri());second.wait_for_function('App.AlarmEngine.intervalId!==null');second.evaluate('App.AlarmEngine.stop()')
        for page in [self.page,second]:page.evaluate('Object.defineProperty(navigator,"locks",{value:undefined,configurable:true})')
        self.ev('window.testTick=App.AlarmEngine.tick();true')
        second.evaluate('App.AlarmEngine.tick()');self.ev('window.testTick')
        result=self.page.evaluate('async(id)=>({event:await App.DB.get("events",id),history:(await App.DB.getAll("eventHistory")).filter(e=>e.eventId===id&&e.action==="disparo_alarme")})',event_id)
        self.assertEqual(result['event']['alarmTriggerCount'],1);self.assertEqual(len(result['history']),1)
        second.close();self.assertEqual(self.errors,[])
    def test_permission_denied_and_unavailable_notification_are_safe(self):
        result=self.ev('()=>{let old=App.Notifications.isSupported;App.Notifications.isSupported=()=>false;let value=App.Notifications.send("teste",{});let state=App.Notifications.getPermissionState();App.Notifications.isSupported=old;return {value,state}}')
        self.assertIsNone(result['value']);self.assertEqual(result['state'],'indisponivel')
        # Permission-state read is real; don't display desktop notifications or alter OS settings.
        self.assertIn(self.ev('App.Notifications.getPermissionState()'),['concedida','negada','nao_solicitada','indisponivel'])
    def test_no_audio_nodes_for_zero_or_invalid_volume(self):
        result=self.ev('()=>{let old=App.Audio.ctx,oldUnlock=App.Audio.unlock,calls=0;App.Audio.ctx={createGain(){calls++;throw new Error("Audio node created")}};App.Audio.unlock=()=>{calls++};for(let type of ["chime","beep","siren","blip"]){App.Audio.play(type,0);App.Audio.play(type,NaN)}App.Audio.ctx=old;App.Audio.unlock=oldUnlock;return calls}')
        self.assertEqual(result,0)

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout).run(unittest.defaultTestLoader.loadTestsFromTestCase(Compatibility))
    (ROOT/'revisao_interface_2026_10_25/resultados/compatibility_ultimo.json').write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'details':[{'test':str(t),'trace':s} for t,s in result.failures+result.errors]},ensure_ascii=False,indent=2),encoding='utf-8')
    sys.exit(0 if result.wasSuccessful() else 1)
