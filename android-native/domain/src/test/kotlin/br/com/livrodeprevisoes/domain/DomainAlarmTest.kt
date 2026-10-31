package br.com.livrodeprevisoes.domain

import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors

class DomainAlarmTest {
    @Test fun defaultZeroLeadAndZeroRepeatAreNotReplacedWithFallbacks() {
        val f = DomainFixture()
        f.service.saveSettings(f.service.settings().put("defaultLeadTimeMinutes", 0).put("maxRepeats", 0).put("soundVolume", 0))
        val e = f.service.saveEvent(f.input().put("scheduledTime", "12:10").put("hasAlarm", true).put("useDefaultAlarmSettings", true))
        assertTrue(f.service.dueAlarms().isEmpty())
        f.clock = f.clock.plusSeconds(600)
        assertEquals(1, f.service.dueAlarms().size)
        val fired = f.service.fireAlarm(e.getString("id"), emptyList())!!
        assertEquals(1, fired.getInt("alarmTriggerCount"))
        assertEquals("triggered", fired.getString("alarmState"))
        f.clock = f.clock.plusSeconds(3600)
        assertTrue(f.service.dueAlarms().isEmpty())
        assertEquals(0, f.service.settings().getInt("soundVolume"))
    }

    @Test fun maximumRepeatsCountsAdditionalFiringsAndHonorsInterval() {
        val f = DomainFixture(); val e = f.service.saveEvent(f.input().put("hasAlarm", true).put("alarmRepeat", true).put("alarmMaxRepeats", 2).put("alarmRepeatInterval", 1))
        val id = e.getString("id")
        assertNotNull(f.service.fireAlarm(id, emptyList()))
        assertNull(f.service.fireAlarm(id, emptyList()))
        f.clock = f.clock.plusSeconds(59)
        assertTrue(f.service.dueAlarms().isEmpty())
        f.clock = f.clock.plusSeconds(1)
        assertEquals(2, f.service.fireAlarm(id, emptyList())!!.getInt("alarmTriggerCount"))
        f.clock = f.clock.plusSeconds(60)
        assertEquals(3, f.service.fireAlarm(id, emptyList())!!.getInt("alarmTriggerCount"))
        f.clock = f.clock.plusSeconds(3600)
        assertNull(f.service.fireAlarm(id, emptyList()))
    }

    @Test fun snoozeExplicitlyAllowsNextFiringAfterRepeatLimitAndAcknowledgmentStopsIt() {
        val f = DomainFixture(); val e = f.service.saveEvent(f.input().put("hasAlarm", true).put("alarmMaxRepeats", 0))
        val id = e.getString("id")
        f.service.fireAlarm(id, emptyList())
        assertThrows(IllegalArgumentException::class.java) { f.service.snoozeAlarm(id, 0) }
        f.service.snoozeAlarm(id, 5)
        f.clock = f.clock.plusSeconds(299)
        assertTrue(f.service.dueAlarms().isEmpty())
        f.clock = f.clock.plusSeconds(1)
        assertEquals(2, f.service.fireAlarm(id, emptyList())!!.getInt("alarmTriggerCount"))
        f.service.acknowledgeAlarm(id)
        f.clock = f.clock.plusSeconds(3600)
        assertTrue(f.service.dueAlarms().isEmpty())
        assertEquals("acknowledged", f.service.rows("events").single().getString("alarmState"))
    }

    @Test fun reschedulingAndReopeningResetFullAlarmCycle() {
        val f = DomainFixture(); var e = f.service.saveEvent(f.input().put("hasAlarm", true))
        val id = e.getString("id")
        f.service.fireAlarm(id, emptyList())
        e = f.service.saveEvent(JSONObject(e.toString()).put("scheduledTime", "12:30"))
        assertEquals(0, e.getInt("alarmTriggerCount"))
        assertTrue(e.isNull("lastAlarmTriggeredAt"))
        f.clock = f.clock.plusSeconds(1800)
        assertEquals(1, f.service.fireAlarm(id, emptyList())!!.getInt("alarmTriggerCount"))
        f.service.completeEvent(id)
        f.service.reopenEvent(id)
        assertEquals(1, f.service.fireAlarm(id, emptyList())!!.getInt("alarmTriggerCount"))
    }

    @Test fun oneAtomicClaimWinsEvenAcrossServiceInstances() {
        val f = DomainFixture(); val e = f.service.saveEvent(f.input().put("hasAlarm", true))
        val other = LivroService(f.store, { f.clock }, f.zone)
        val pool = Executors.newFixedThreadPool(2)
        val start = CountDownLatch(1)
        try {
            val jobs = listOf(f.service, other).map { s -> pool.submit<JSONObject?> { start.await(); s.fireAlarm(e.getString("id"), emptyList()) } }
            start.countDown()
            assertEquals(1, jobs.map { it.get() }.count { it != null })
            assertEquals(1, f.service.rows("eventHistory").count { it.getString("action") == "disparo_alarme" })
        } finally { pool.shutdownNow() }
    }

    @Test fun deliveryAuditOnlyRecordsActualChannelsForMatchingClaim() {
        val f = DomainFixture(); val e = f.service.saveEvent(f.input().put("hasAlarm", true))
        val id = e.getString("id")
        val claimed = f.service.fireAlarm(id, emptyList())!!
        var audit = f.service.rows("eventHistory").last()
        assertEquals(0, audit.getJSONArray("channels").length())
        f.service.recordAlarmDelivery(id, claimed.getString("lastAlarmTriggeredAt"), listOf("visual"))
        audit = f.service.rows("eventHistory").last()
        assertEquals("visual", audit.getJSONArray("channels").getString(0))
        assertEquals(1, f.service.rows("events").single().getInt("alarmTriggerCount"))
        val before = f.service.snapshot().toString()
        assertThrows(IllegalArgumentException::class.java) { f.service.recordAlarmDelivery(id, claimed.getString("lastAlarmTriggeredAt"), listOf("fake")) }
        assertEquals(before, f.service.snapshot().toString())
        f.service.recordAlarmDelivery(id, "2020-01-01T00:00:00Z", listOf("audio"))
        assertEquals(before, f.service.snapshot().toString())
    }

    @Test fun inactiveCompletedAndNonAlarmEventsNeverFire() {
        val f = DomainFixture(); val h = f.hierarchy()
        val a = f.service.saveEvent(f.input(h))
        val b = f.service.saveEvent(f.input(h).put("hasAlarm", true))
        val c = f.service.saveEvent(f.input(h).put("hasAlarm", true))
        f.service.completeEvent(b.getString("id"))
        f.service.deleteEvent(c.getString("id"))
        assertTrue(f.service.dueAlarms().isEmpty())
        for (e in listOf(a,b,c)) assertNull(f.service.fireAlarm(e.getString("id"), emptyList()))
    }
}
