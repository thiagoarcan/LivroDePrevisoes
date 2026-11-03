package br.com.livrodeprevisoes.domain

import org.junit.Assert.*
import org.junit.Test
import java.time.Instant

class AlarmScheduleTest {
    private fun next(f: DomainFixture): Instant? = f.service.javaClass.getMethod("nextAlarmAt").invoke(f.service) as Instant?
    @Test fun deadlineSurvivesServiceRecreationAndFollowsSnoozeAndAcknowledge() {
        val f=DomainFixture()
        val e=f.service.saveEvent(f.input().put("scheduledTime","12:10").put("hasAlarm",true))
        assertEquals(f.clock.plusSeconds(600),next(f))
        f.clock=f.clock.plusSeconds(600)
        f.service.fireAlarm(e.getString("id"),emptyList())
        assertNull(next(f))
        f.service.snoozeAlarm(e.getString("id"),10)
        assertEquals(f.clock.plusSeconds(600),next(f))
        f.service.acknowledgeAlarm(e.getString("id"))
        assertNull(next(f))
    }
    @Test fun repeatDeadlineStopsAtLimitAndDisabledEventsAreExcluded() {
        val f=DomainFixture()
        val e=f.service.saveEvent(f.input().put("hasAlarm",true).put("alarmRepeat",true).put("alarmMaxRepeats",1).put("alarmRepeatInterval",2))
        assertEquals(f.clock,next(f))
        f.service.fireAlarm(e.getString("id"),emptyList())
        assertEquals(f.clock.plusSeconds(120),next(f))
        f.clock=f.clock.plusSeconds(120)
        f.service.fireAlarm(e.getString("id"),emptyList())
        assertNull(next(f))
    }
}
