package br.com.livrodeprevisoes.alerts
import org.json.JSONObject
import org.json.JSONArray
import org.junit.Assert.*
import org.junit.Test

class AlarmDeliveryPolicyTest {
    private val stamp="2026-10-31T12:00:00Z"
    private fun event()=JSONObject().put("id","event-1").put("active",true).put("status","pendente").put("hasAlarm",true).put("alarmState","triggered").put("lastAlarmTriggeredAt",stamp)
    private fun history(channels:List<String>)=JSONObject().put("eventId","event-1").put("action","disparo_alarme").put("timestamp",stamp).put("channels",JSONArray(channels))
    @Test fun deliveryRechecksTheExactClaimAndRejectsOperatorChanges() {
        assertTrue(AlarmDeliveryPolicy.current(event(),"event-1",stamp))
        for((key,value) in listOf("status" to "concluido","alarmState" to "acknowledged","alarmState" to "snoozed","active" to false,"hasAlarm" to false,"lastAlarmTriggeredAt" to "2026-10-31T12:01:00Z")) {
            assertFalse("$key=$value must invalidate old delivery",AlarmDeliveryPolicy.current(event().put(key,value),"event-1",stamp))
        }
        assertFalse(AlarmDeliveryPolicy.current(null,"event-1",stamp))
    }
    @Test fun undeliveredNoRepeatClaimCanRetryWithoutIncrementingAlarmState() {
        val event=event().put("alarmRepeat",false).put("alarmTriggerCount",1)
        val before=event.toString()
        assertEquals(listOf("event-1"),AlarmDeliveryPolicy.undelivered(listOf(event),listOf(history(emptyList()))).map{it.getString("id")})
        assertTrue(AlarmDeliveryPolicy.undelivered(listOf(event),listOf(history(listOf("audio")))).isEmpty())
        assertTrue(AlarmDeliveryPolicy.undelivered(listOf(event().put("alarmState","acknowledged")),listOf(history(emptyList()))).isEmpty())
        assertEquals(before,event.toString())
    }
    @Test fun completedSnoozedRemovedAndReplacedClaimsCancelPostedNotifications() {
        val posted=mapOf("event-1" to stamp,"missing" to stamp)
        assertEquals(setOf("missing"),AlarmDeliveryPolicy.staleNotifications(posted,listOf(event())))
        assertEquals(setOf("event-1","missing"),AlarmDeliveryPolicy.staleNotifications(posted,listOf(event().put("status","concluido"))))
        assertEquals(setOf("event-1","missing"),AlarmDeliveryPolicy.staleNotifications(posted,listOf(event().put("alarmState","snoozed"))))
    }
    @Test fun pauseResumeInvalidatesAlreadyQueuedMainThreadCallbacks() {
        val gate=ForegroundGate();gate.resume();val old=gate.token()
        assertTrue(gate.isCurrent(old));gate.pause();assertFalse(gate.isCurrent(old))
        gate.resume();assertFalse(gate.isCurrent(old));assertTrue(gate.isCurrent(gate.token()))
    }
    @Test fun visualQueuedBehindAnotherDialogRetriesWithoutRepeatingDeliveredAudio() {
        val first=event();val second=event().put("id","event-2")
        val records=listOf(history(listOf("audio","visual")),history(listOf("audio")).put("eventId","event-2"))
        assertEquals(listOf("event-2"),AlarmDeliveryPolicy.missingVisual(listOf(first,second),records,mapOf("event-1" to stamp)).map{it.getString("id")})
        assertTrue(AlarmDeliveryPolicy.missingVisual(listOf(second),records,mapOf("event-2" to stamp)).isEmpty())
        assertTrue(AlarmDeliveryPolicy.missingVisual(listOf(second.put("alarmState","acknowledged")),records,emptyMap()).isEmpty())
        assertEquals("audio",records[1].getJSONArray("channels").getString(0))
    }

}
