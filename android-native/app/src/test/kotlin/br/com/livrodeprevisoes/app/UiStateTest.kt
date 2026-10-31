package br.com.livrodeprevisoes.app

import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test

class UiStateTest {
    @Test fun canceledPreventiveExportNeverAuthorizesReplacement() {
        val gate = ExportGate()
        gate.begin("replace")
        assertNull(gate.finished(false))
        assertNull(gate.finished(true))
    }
    @Test fun successfulExportAuthorizesExactlyOnePendingAction() {
        val gate = ExportGate()
        gate.begin("clear")
        assertEquals("clear", gate.finished(true))
        assertNull(gate.finished(true))
    }
    @Test fun savedExportRestoresActionButNotAuthorization() {
        val original = ExportGate(); original.begin("demo")
        val restored = ExportGate(original.pending)
        assertEquals("demo", restored.pending)
        assertNull(restored.finished(false))
    }
    @Test fun listFiltersIgnoreDeletedAndMatchPortugueseAccentsAndHierarchy() {
        val rows = listOf(
            JSONObject("""{"id":"1","description":"Inspeção de bomba","status":"pendente","consoleId":"c1","scheduledAt":"2026-11-01T10:00:00Z"}"""),
            JSONObject("""{"id":"2","description":"Inspeção","status":"pendente","active":false}"""),
            JSONObject("""{"id":"3","description":"Inspeção","status":"concluido"}"""))
        assertEquals(listOf("1"), filterEvents(rows, "pendente", "c1", "inspecao", "", { "Duto Sul" }).map { it.getString("id") })
        assertEquals(1, filterEvents(rows, "pendente", "", "sul", "", { "Duto Sul" }).size)
        assertTrue(filterEvents(rows, "pendente", "c2", "", "", { "" }).isEmpty())
    }
    @Test fun pendingSortIsChronologicalAndPriorityFilterIsExact() {
        val rows = listOf(
            JSONObject("""{"id":"late","status":"pendente","priority":"Alta","scheduledAt":"2026-11-02T10:00:00Z"}"""),
            JSONObject("""{"id":"early","status":"pendente","priority":"Normal","scheduledAt":"2026-11-01T10:00:00Z"}"""))
        assertEquals(listOf("early", "late"), filterEvents(rows, "pendente", "", "", "", { "" }).map { it.getString("id") })
        assertEquals("late", filterEvents(rows, "pendente", "", "", "Alta", { "" }).single().getString("id"))
    }
    @Test fun pendingSortUsesInstantsAcrossImportedTimeZones() {
        val rows = listOf(
            JSONObject("""{"id":"later","status":"pendente","scheduledAt":"2026-11-01T09:00:00-03:00"}"""),
            JSONObject("""{"id":"first","status":"pendente","scheduledAt":"2026-11-01T10:00:00Z"}"""))
        assertEquals(listOf("first", "later"), filterEvents(rows, "pendente", "", "", "", { "" }).map { it.getString("id") })
    }
    @Test fun boundedImportRejectsOversizeInsteadOfParsingTruncatedData() {
        try {
            readBounded(java.io.ByteArrayInputStream("12345".toByteArray()), 4)
            fail("Oversized import must fail before validation")
        } catch (_: IllegalArgumentException) { }
        assertEquals("á", readBounded(java.io.ByteArrayInputStream("\uFEFFá".toByteArray()), 5))
    }
    @Test fun completedListOrdersMostRecentCompletionFirst() {
        val rows = listOf(
            JSONObject("""{"id":"first","status":"concluido","scheduledAt":"2026-11-01T09:00:00Z","completedAt":"2026-11-01T12:00:00Z"}"""),
            JSONObject("""{"id":"recent","status":"concluido","scheduledAt":"2026-11-01T10:00:00Z","completedAt":"2026-11-01T13:00:00Z"}"""))
        assertEquals(listOf("recent", "first"), filterEvents(rows, "concluido", "", "", "", { "" }).map { it.getString("id") })
    }
    @Test fun fractionalTimestampSortsBeforeFollowingSecond() {
        val rows = listOf(
            JSONObject("""{"id":"later","status":"pendente","scheduledAt":"2026-11-01T10:00:00.500Z"}"""),
            JSONObject("""{"id":"first","status":"pendente","scheduledAt":"2026-11-01T10:00:00Z"}"""))
        assertEquals(listOf("first", "later"), filterEvents(rows, "pendente", "", "", "", { "" }).map { it.getString("id") })
    }
    @Test fun statusCountsEvenOneMillisecondPastDeadlineAsLate() {
        assertTrue(deadlineIsLate("2026-11-01T10:00:00Z", java.time.Instant.parse("2026-11-01T10:00:00.001Z")))
        assertFalse(deadlineIsLate("2026-11-01T10:00:00Z", java.time.Instant.parse("2026-11-01T10:00:00Z")))
    }
    @Test fun advancedFiltersCombineHierarchyDatesAlarmAndDeadline() {
        val event = JSONObject("""{"id":"match","status":"pendente","pipelineId":"p1","uoId":"u1","equipmentTypeId":"t1","tagId":"tag1","scheduledDate":"2026-11-01","scheduledAt":"2026-11-01T10:10:00Z","hasAlarm":true,"alarmState":"triggered"}""")
        val filters = EventFilters(pipeline = "p1", unit = "u1", equipment = "t1", tag = "tag1", dateFrom = "2026-11-01", dateTo = "2026-11-01", alarm = "on", alarmState = "triggered", window = "15")
        val now = java.time.Instant.parse("2026-11-01T10:00:00Z")
        assertEquals(1, filterEvents(listOf(event), "pendente", "", "", "", { "" }, filters, now).size)
        assertTrue(filterEvents(listOf(event), "pendente", "", "", "", { "" }, filters.copy(window = "overdue"), now).isEmpty())
        assertTrue(filterEvents(listOf(event), "pendente", "", "", "", { "" }, filters.copy(tag = "other"), now).isEmpty())
        assertTrue(filterEvents(listOf(event), "pendente", "", "", "", { "" }, filters.copy(dateTo = "2026-10-31"), now).isEmpty())
        assertTrue(filterEvents(listOf(event), "pendente", "", "", "", { "" }, filters.copy(alarm = "off"), now).isEmpty())
    }
    @Test fun unchangedDrawingReturnsOriginalBytesWithoutResizing() {
        val state = DrawingSnapshot("original-1200x440-png")
        assertEquals("original-1200x440-png", state.encoded { error("Unedited drawing must not re-encode") })
        state.changed()
        assertEquals("new-ink-png", state.encoded { "new-ink-png" })
    }
    @Test fun deeplyNestedImportIsRejectedBeforeJsonParser() {
        val text = "[".repeat(129) + "0" + "]".repeat(129)
        try { readBounded(java.io.ByteArrayInputStream(text.toByteArray())); fail("Depth must be bounded before JSONObject parser") } catch (_: IllegalArgumentException) { }
        val quoted = "{\"note\":\"" + "[".repeat(200) + "\"}"
        assertEquals(quoted, readBounded(java.io.ByteArrayInputStream(quoted.toByteArray())))
    }
    @Test fun onlyRegularCompletedJsonExportUpdatesBackupMetadata() {
        val original = JSONObject("""{"lastBackupAt":null,"backupReminderDays":7}""")
        val now = java.time.Instant.parse("2026-11-01T10:00:00Z")
        assertNull(successfulBackupSettings("csv", original, now))
        assertNull(successfulBackupSettings("replace", original, now))
        assertNull(successfulBackupSettings("clear", original, now))
        assertNull(successfulBackupSettings("demo", original, now))
        assertNull(successfulBackupSettings("raw", original, now))
        assertEquals("2026-11-01T10:00:00Z", successfulBackupSettings("json", original, now)!!.getString("lastBackupAt"))
        assertTrue(original.isNull("lastBackupAt"))
    }
    @Test fun backupReminderUsesConfiguredDaysAndNeverClaimsMissingBackupExists() {
        val now = java.time.Instant.parse("2026-11-08T10:00:00Z")
        assertTrue(backupIsDue(JSONObject(), now))
        assertTrue(backupIsDue(JSONObject("""{"lastBackupAt":"2026-11-01T10:00:00Z","backupReminderDays":7}"""), now))
        assertFalse(backupIsDue(JSONObject("""{"lastBackupAt":"2026-11-01T10:00:01Z","backupReminderDays":7}"""), now))
    }
    @Test fun selectorRetainsOnlyItsOriginalInactiveReference() {
        val rows = listOf(JSONObject("""{"id":"active","active":true}"""), JSONObject("""{"id":"original","active":false}"""), JSONObject("""{"id":"other","active":false}"""))
        assertEquals(listOf("active", "original"), pickableRecords(rows, setOf("original")).map { it.getString("id") })
        assertEquals(listOf("active"), pickableRecords(rows, emptySet()).map { it.getString("id") })
    }
    @Test fun invalidUtf8ImportIsNotSilentlyRepaired() {
        try {
            readBounded(java.io.ByteArrayInputStream(byteArrayOf(0xc3.toByte(), 0x28)))
            fail("Invalid UTF-8 must not be silently replaced")
        } catch (_: java.nio.charset.CharacterCodingException) { }
    }
    @Test fun historyOrdersActualInstantsNotOffsetText() {
        val rows = listOf(JSONObject("""{"id":"old","timestamp":"2026-11-01T10:00:00Z"}"""), JSONObject("""{"id":"recent","timestamp":"2026-11-01T09:00:00-03:00"}"""))
        assertEquals(listOf("recent", "old"), sortHistory(rows).map { it.getString("id") })
    }
    @Test fun pageBoundsHandleEmptyExactAndPartialPages() {
        assertEquals(PageBounds(0, 0, 0, 0), pageBounds(0, 0))
        assertEquals(PageBounds(0, 0, 1, 1), pageBounds(1, 0))
        assertEquals(PageBounds(0, 0, 100, 100), pageBounds(100, 0))
        assertEquals(PageBounds(1, 100, 101, 101), pageBounds(101, 1))
        assertEquals(PageBounds(4, 400, 500, 500), pageBounds(500, 4))
    }
    @Test fun pageBoundsClampInvalidAndShrunkenPageIndices() {
        assertEquals(PageBounds(0, 0, 100, 500), pageBounds(500, -3))
        assertEquals(PageBounds(4, 400, 500, 500), pageBounds(500, Int.MAX_VALUE))
        assertEquals(PageBounds(3, 300, 301, 301), pageBounds(301, 4))
        assertEquals(PageBounds(0, 0, 0, 0), pageBounds(0, 4))
    }
    @Test fun fivePagesExposeEveryRowExactlyOnceWithoutInflatingAllCards() {
        val records = (0 until 500).toList()
        val shown = (0 until 5).flatMap { page ->
            val bounds = pageBounds(records.size, page)
            val visible = records.subList(bounds.start, bounds.endExclusive)
            assertEquals(100, visible.size)
            visible
        }
        assertEquals(records, shown)
        assertEquals(500, shown.toSet().size)
    }
}
