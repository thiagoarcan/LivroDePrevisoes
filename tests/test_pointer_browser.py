"""Synthetic pen/palm branches; does not certify physical stylus hardware."""
import sys,unittest
from playwright.sync_api import sync_playwright
from browser_support import build_temporary_html,open_app


class SyntheticPointer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp,cls.path=build_temporary_html();cls.pw=sync_playwright().start()
        cls.browser=cls.pw.chromium.launch(channel='msedge',headless=True)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.temp.cleanup()
    def setUp(self):
        self.context,self.page,self.errors=open_app(self.browser,self.path,width=1024,height=768)
        self.page.evaluate('App.UI.navigateTo("viewNewEvent")')
        self.page.locator('#btnToggleStylusCanvas').click()
        self.page.locator('#stylusDrawingCanvas').scroll_into_view_if_needed()
        self.page.evaluate('''()=>{window.pointerTest={
            send(type,kind,id,x,y,pressure=.5){let c=App.UI.stylusCanvas,r=c.getBoundingClientRect();
                c.dispatchEvent(new PointerEvent(type,{bubbles:true,cancelable:true,pointerType:kind,pointerId:id,
                    clientX:r.x+r.width*x,clientY:r.y+r.height*y,pressure,buttons:type==='pointerup'?0:1}))},
            pixels(){let c=App.UI.stylusCanvas,d=c.getContext('2d').getImageData(0,0,c.width,c.height).data,n=0;
                for(let i=3;i<d.length;i+=4)if(d[i])n++;return n}
        }}''')
    def tearDown(self):self.context.close()

    def test_pen_pressure_changes_real_stroke_area(self):
        areas=[]
        for pressure in [.1,.9]:
            areas.append(self.page.evaluate('''(pressure)=>{App.UI.clearStylusPad(true);
                pointerTest.send('pointerdown','pen',11,.2,.4,pressure);
                pointerTest.send('pointermove','pen',11,.6,.4,pressure);
                pointerTest.send('pointerup','pen',11,.6,.4,0);return pointerTest.pixels()}''',pressure))
        self.assertGreater(areas[0],0)
        self.assertGreater(areas[1],areas[0]*1.4,areas)
        self.assertEqual(self.errors,[])

    def test_palm_does_not_interrupt_pen_and_cancel_releases_pointer(self):
        state=self.page.evaluate('''()=>{pointerTest.send('pointerdown','pen',21,.2,.3,.7);
            pointerTest.send('pointermove','pen',21,.5,.3,.7);let before=App.UI.stylusCanvas.toDataURL();
            pointerTest.send('pointerdown','touch',22,.2,.8,1);pointerTest.send('pointermove','touch',22,.8,.8,1);
            pointerTest.send('pointerup','touch',22,.8,.8,0);
            let during={unchanged:before===App.UI.stylusCanvas.toDataURL(),drawing:App.UI.stylusIsDrawing,id:App.UI.stylusActivePointerId};
            pointerTest.send('pointercancel','pen',21,.5,.3,0);let stopped=!App.UI.stylusIsDrawing&&App.UI.stylusActivePointerId===null;
            let pixels=pointerTest.pixels();pointerTest.send('pointerdown','touch',23,.2,.7,1);
            pointerTest.send('pointermove','touch',23,.6,.7,1);pointerTest.send('pointerup','touch',23,.6,.7,0);
            return {during,stopped,newStroke:pointerTest.pixels()>pixels,saved:!!App.UI.getStylusData()}}''')
        self.assertEqual(state['during'],{'unchanged':True,'drawing':True,'id':21})
        self.assertTrue(state['stopped']);self.assertTrue(state['newStroke']);self.assertTrue(state['saved'])
        self.assertEqual(self.errors,[])


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout).run(unittest.defaultTestLoader.loadTestsFromTestCase(SyntheticPointer))
    sys.exit(0 if result.wasSuccessful() else 1)
