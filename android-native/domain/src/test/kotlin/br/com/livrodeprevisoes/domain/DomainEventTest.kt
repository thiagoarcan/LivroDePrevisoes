package br.com.livrodeprevisoes.domain

import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import java.time.ZoneId

class DomainEventTest {
    @Test fun newEventAndItsActorAuditCommitTogether() {
        val f = DomainFixture(); val input = f.input()
        val before = f.store.saves
        val e = f.service.saveEvent(input.put("description", "  Verificar pressão  "))
        assertEquals(before + 1, f.store.saves)
        assertEquals("pendente", e.getString("status"))
        assertEquals("Verificar pressão", e.getString("description"))
        assertEquals("2026-10-31T12:00:00Z", e.getString("scheduledAt"))
        assertEquals(1, e.getInt("version"))
        assertTrue(e.isNull("completedAt"))
        val h = f.service.rows("eventHistory").single()
        assertEquals("criacao", h.getString("action"))
        assertEquals(e.getString("id"), h.getString("eventId"))
        assertEquals("Usuário local", h.getString("localUser"))
        assertEquals(e.toString(), h.getString("newValue"))
    }

    @Test fun impossibleDatesAndDstGapsAreRejectedRatherThanRolledForward() {
        val f = DomainFixture(ZoneId.of("America/New_York")); val input = f.input()
        val before = f.service.snapshot().toString()
        for ((date,time) in listOf("2026-02-30" to "12:00", "2026-10-31" to "24:01", "2026-3-08" to "02:30", "2026-03-08" to "02:30")) {
            assertThrows(IllegalArgumentException::class.java) { f.service.saveEvent(JSONObject(input.toString()).put("scheduledDate", date).put("scheduledTime", time)) }
        }
        assertEquals(before, f.service.snapshot().toString())
        val e = f.service.saveEvent(input.put("scheduledDate", "2026-10-31").put("scheduledTime", "08:00"))
        assertEquals("2026-10-31T12:00:00Z", e.getString("scheduledAt"))
    }

    @Test fun mismatchedHierarchyAndDrawingPayloadNeverCommit() {
        val f = DomainFixture(); val h = f.hierarchy(); val input = f.input(h)
        val other = f.unit("OUTRA")
        val before = f.service.snapshot().toString()
        assertThrows(IllegalArgumentException::class.java) { f.service.saveEvent(JSONObject(input.toString()).put("uoId", other.getString("id"))) }
        assertThrows(IllegalArgumentException::class.java) { f.service.saveEvent(JSONObject(input.toString()).put("stylusDrawing", "data:text/html,<script>alert(1)</script>")) }
        assertThrows(IllegalArgumentException::class.java) { f.service.saveEvent(JSONObject(input.toString()).put("hasAlarm", "true")) }
        assertEquals(before, f.service.snapshot().toString())
    }

    @Test fun editingInactiveOriginalReferencesWorksButNewSelectionsFail() {
        val f = DomainFixture(); val h = f.hierarchy(); val input = f.input(h)
        val e = f.service.saveEvent(input)
        f.service.setRecordActive("pipelines", h.first.getString("id"), false)
        val edited = f.service.saveEvent(JSONObject(e.toString()).put("description", "Corrigida"))
        assertEquals(2, edited.getInt("version"))
        assertThrows(IllegalArgumentException::class.java) { f.service.saveEvent(input) }
    }

    @Test fun completionReopenAndSoftDeletePreserveHistoryAndResetAlarmCycle() {
        val f = DomainFixture(); val e = f.service.saveEvent(f.input().put("hasAlarm", true))
        val id = e.getString("id")
        f.clock = f.clock.plusSeconds(300)
        val complete = f.service.completeEvent(id, "  Feito  ")
        assertEquals("concluido", complete.getString("status"))
        assertEquals(5.0, complete.getDouble("completedTimeDiffMinutes"), 0.0)
        assertEquals("Feito", complete.getString("completionNote"))
        assertEquals("Usuário local", complete.getString("completedBy"))
        assertThrows(IllegalArgumentException::class.java) { f.service.completeEvent(id) }
        val reopened = f.service.reopenEvent(id, "2026-11-01", "12:30")
        assertEquals("pendente", reopened.getString("status"))
        assertEquals(0, reopened.getInt("alarmTriggerCount"))
        assertTrue(reopened.isNull("completedAt"))
        assertEquals("", reopened.getString("completionNote"))
        f.service.deleteEvent(id)
        assertFalse(f.service.rows("events").single().getBoolean("active"))
        assertEquals(listOf("criacao", "conclusao", "reabertura", "exclusao"), f.service.rows("eventHistory").map { it.getString("action") })
        assertThrows(IllegalArgumentException::class.java) { f.service.reopenEvent(id) }
        assertThrows(IllegalArgumentException::class.java) { f.service.saveEvent(reopened) }
    }

    @Test fun duplicateIsUnsavedDraftWithNoIdentityAndNewLocalSchedule() {
        val f = DomainFixture(); val e = f.service.saveEvent(f.input().put("notes", "Texto preservado").put("alarmMinutesBefore", 0))
        val before = f.store.saves
        val draft = f.service.duplicateDraft(e.getString("id"))
        assertEquals(before, f.store.saves)
        assertFalse(draft.has("id"))
        assertFalse(draft.has("status"))
        assertFalse(draft.has("version"))
        assertEquals("12:30", draft.getString("scheduledTime"))
        assertEquals("Texto preservado", draft.getString("notes"))
        val clone = f.service.saveEvent(draft)
        assertNotEquals(e.getString("id"), clone.getString("id"))
        assertEquals(2, f.service.rows("events").size)
    }

    @Test fun editingImportedEventDoesNotSilentlyMoveItsInstantAcrossTimezones() {
        val f = DomainFixture(ZoneId.of("America/Sao_Paulo"))
        val e = f.service.saveEvent(f.input())
        assertEquals("2026-10-31T15:00:00Z", e.getString("scheduledAt"))
        val inUtc = LivroService(f.store, { f.clock }, ZoneId.of("UTC"))
        val edited = inUtc.saveEvent(JSONObject(e.toString()).put("notes", "Apenas uma nota"))
        assertEquals("2026-10-31T15:00:00Z", edited.getString("scheduledAt"))
        val moved = inUtc.saveEvent(JSONObject(edited.toString()).put("scheduledTime", "12:01"))
        assertEquals("2026-10-31T12:01:00Z", moved.getString("scheduledAt"))
    }

    @Test fun removingUnitLinkOrMovingReferencedTypeWouldOrphanEventAndIsRejected() {
        val f = DomainFixture(); val h = f.hierarchy()
        val t = f.service.saveRecord("equipmentTypes", JSONObject().put("name", "Bomba").put("uoId", h.second.getString("id")))
        f.service.saveEvent(f.input(h).put("equipmentTypeId", t.getString("id")))
        val c = f.unit("TERCEIRA")
        val original = f.service.snapshot().toString()
        assertThrows(IllegalArgumentException::class.java) { f.service.saveRecord("pipelines", JSONObject(h.first.toString()).put("uoIds", JSONArray(listOf(h.third.getString("id"), c.getString("id"))))) }
        assertThrows(IllegalArgumentException::class.java) { f.service.saveRecord("equipmentTypes", JSONObject(t.toString()).put("uoId", h.third.getString("id"))) }
        assertEquals(original, f.service.snapshot().toString())
    }
}
