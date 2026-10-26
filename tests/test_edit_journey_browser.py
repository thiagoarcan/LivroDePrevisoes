"""Regression for editing through the rendered list and saving the same record."""
import unittest
from playwright.sync_api import sync_playwright
from browser_support import build_temporary_html,open_app


class EditJourney(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp,cls.path=build_temporary_html()
        cls.pw=sync_playwright().start()
        cls.browser=cls.pw.chromium.launch(channel='msedge',headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop();cls.temp.cleanup()

    def test_edit_from_list_updates_same_event_and_keeps_history(self):
        context,page,errors=open_app(self.browser,self.path)
        try:
            count=page.evaluate('async()=>(await App.DB.getAll("events")).length')
            page.evaluate('App.UI.navigateTo("viewPendingEvents")')
            event=page.evaluate('App.UI.activePendingEvents[0]')
            self.assertIsNotNone(event)
            page.locator('#inputSearchPending').fill(event['description'])
            page.locator('#viewPendingEvents button[onclick*="editEvent"]:visible').first.click()
            page.wait_for_function('document.getElementById("eventEditId").value!==""')
            self.assertEqual(page.locator('#eventEditId').input_value(),event['id'])
            self.assertEqual(page.locator('#inputEventDescription').input_value(),event['description'])
            page.locator('#inputEventDescription').fill('Descrição editada no navegador\nSegunda linha preservada')
            notes_group=page.locator('details').filter(has=page.locator('#inputEventNotes'))
            if notes_group.count() and notes_group.get_attribute('open') is None:
                notes_group.locator('summary').click()
            page.locator('#inputEventNotes').fill('Observação editada com acentuação.')
            page.set_viewport_size({'width':1024,'height':768})
            page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)')
            self.assertEqual(page.locator('#eventEditId').input_value(),event['id'])
            page.locator('#btnSubmitEvent').click()
            page.wait_for_function('async(id)=>(await App.DB.get("events",id)).description.startsWith("Descrição editada")',arg=event['id'])
            state=page.evaluate('async(id)=>({event:await App.DB.get("events",id),count:(await App.DB.getAll("events")).length,history:(await App.DB.getAll("eventHistory")).filter(h=>h.eventId===id)})',event['id'])
            self.assertEqual(state['count'],count)
            self.assertEqual(state['event']['status'],'pendente')
            self.assertEqual(state['event']['description'],'Descrição editada no navegador\nSegunda linha preservada')
            self.assertEqual(state['event']['notes'],'Observação editada com acentuação.')
            self.assertGreater(state['event']['version'],event['version'])
            self.assertIn('edicao',[h['action'] for h in state['history']])
            self.assertEqual(errors,[])
        finally:
            context.close()

    def test_missing_completion_actor_is_not_replaced_with_creator(self):
        context,page,errors=open_app(self.browser,self.path)
        try:
            for actor in [None,'','   ','Pessoa que concluiu']:
                expected='Pessoa que concluiu' if actor=='Pessoa que concluiu' else 'Não informado'
                page.set_viewport_size({'width':1440,'height':1000})
                page.evaluate('App.UI.applyResponsiveLayoutMode("auto",false)')
                page.evaluate('''async(actor)=>{let e=(await App.DB.getAll('events')).find(e=>e.status==='concluido');
                    e.createdBy='Pessoa que apenas criou';e.completedBy=actor;await App.DB.update('events',e);
                    await App.UI.navigateTo('viewCompletedEvents')}''',actor)
                text=page.locator('#tbodyCompletedEvents').text_content()
                self.assertNotIn('Pessoa que apenas criou',text)
                self.assertIn(expected,text)
                actor_detail=page.locator('#completedDetailPane dt').filter(has_text='Controlador').locator('xpath=following-sibling::dd[1]').inner_text()
                self.assertEqual(actor_detail,expected)
                page.set_viewport_size({'width':390,'height':844})
                page.wait_for_function('document.querySelector("#containerCompletedCards .completed-event-card")')
                text=page.locator('#containerCompletedCards').text_content()
                self.assertNotIn('Pessoa que apenas criou',text)
                self.assertIn(expected,text)
            self.assertEqual(errors,[])
        finally:
            context.close()


if __name__=='__main__':unittest.main(verbosity=2)
