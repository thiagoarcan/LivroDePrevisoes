package br.com.livrodeprevisoes.domain

import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import java.io.IOException

class DomainConfigurationTest {
    @Test fun settingsRejectInvalidTypesAndKeepZeroValues() {
        val f = DomainFixture()
        f.service.saveSettings(f.service.settings().put("maxRepeats", 0).put("defaultLeadTimeMinutes", 0).put("soundVolume", 0).put("theme", "industrial"))
        assertEquals(0, f.service.settings().getInt("maxRepeats"))
        assertEquals("industrial", f.service.settings().getString("theme"))
        val before = f.service.snapshot().toString()
        for ((key,value) in listOf("soundVolume" to 101,"repeatIntervalMinutes" to 0,"soundEnabled" to "yes","theme" to "neon")) {
            assertThrows(IllegalArgumentException::class.java) { f.service.saveSettings(f.service.settings().put(key,value)) }
        }
        assertEquals(before, f.service.snapshot().toString())
    }

    @Test fun rangesMustStartAtZeroAndHaveNeitherGapsNorOverlap() {
        val f = DomainFixture(); val original = f.service.snapshot().toString()
        for (start in listOf(14, 16)) {
            val ranges = f.service.rows("colorRanges")
            ranges[1].put("minMinutes",start)
            assertThrows(IllegalArgumentException::class.java) { f.service.saveColorRanges(ranges) }
        }
        assertThrows(IllegalArgumentException::class.java) { f.service.saveColorRanges(emptyList()) }
        assertEquals(original, f.service.snapshot().toString())
        val ranges = f.service.rows("colorRanges")
        ranges[0].put("color", "#112233")
        val before = f.store.saves
        f.service.saveColorRanges(ranges)
        assertEquals(before+1, f.store.saves)
        assertEquals("#112233", f.service.rows("colorRanges")[0].getString("color"))
    }

    @Test fun destructiveOperationsRequireConfirmedPreventiveBackup() {
        val f = DomainFixture(); f.service.saveEvent(f.input())
        val original = f.service.snapshot().toString()
        assertThrows(IllegalArgumentException::class.java) { f.service.clearAllData() }
        assertThrows(IllegalArgumentException::class.java) { f.service.loadDemoData() }
        assertThrows(IllegalArgumentException::class.java) { f.service.restore(f.service.snapshot(), "replace") }
        assertEquals(original, f.service.snapshot().toString())
        val before = f.store.saves
        f.service.clearAllData(true)
        assertEquals(before+1, f.store.saves)
        assertTrue(f.service.rows("events").isEmpty())
        assertTrue(f.service.rows("eventHistory").isEmpty())
        assertEquals(12, f.service.rows("consoles").size)
        assertEquals(80, f.service.settings().getInt("soundVolume"))
    }

    @Test fun demoIsACompleteAtomicSixScenarioFixture() {
        val f = DomainFixture(); val before = f.store.saves
        f.service.loadDemoData(true)
        assertEquals(before+1, f.store.saves)
        assertEquals(6, f.service.rows("events").size)
        assertEquals(1, f.service.rows("events").count { it.getString("status") == "concluido" })
        assertEquals(4, f.service.rows("operationalUnits").size)
        assertEquals(3, f.service.rows("pipelines").size)
        assertEquals(7, f.service.rows("eventHistory").size)
    }

    @Test fun confirmedDemoReplacesExistingDataAtomicallyInsteadOfMixingIt() {
        val f = DomainFixture(); val old = f.service.saveEvent(f.input())
        f.service.saveSettings(f.service.settings().put("localUserName", "Operador anterior"))
        val before = f.store.saves
        f.service.loadDemoData(true)
        assertEquals(before + 1, f.store.saves)
        assertEquals(6, f.service.rows("events").size)
        assertFalse(f.service.rows("events").any { it.getString("id") == old.getString("id") })
        assertFalse(f.service.rows("operationalUnits").any { it.getString("name") == "ORIGEM" })
        assertEquals("Usuário local", f.service.settings().getString("localUserName"))
    }

    @Test fun failedDemoPersistenceKeepsAllExistingDataAndMetadata() {
        val f = DomainFixture(); f.service.saveEvent(f.input())
        val original = f.service.snapshot().toString(); val saves = f.store.saves
        f.store.failSave = true
        assertThrows(IOException::class.java) { f.service.loadDemoData(true) }
        assertEquals(original, f.service.snapshot().toString())
        assertEquals(saves, f.store.saves)
    }

    @Test fun restoreDoesNotRestampImportedRowsAndWritesOnlyOnce() {
        val f = DomainFixture(); val imported = f.service.snapshot()
        val console = imported.getJSONObject("data").getJSONArray("consoles").getJSONObject(0)
        console.put("name", "IMPORTADO").put("version", 7).put("updatedAt", "2026-10-30T12:00:00Z")
        val before = f.store.saves
        val result = f.service.restore(imported, "replace", true)
        assertTrue(result.applied)
        assertEquals(before+1, f.store.saves)
        assertEquals(7, f.service.rows("consoles").first().getInt("version"))
        assertEquals("2026-10-30T12:00:00Z", f.service.rows("consoles").first().getString("updatedAt"))
        f.store.failSave = true
        val original = f.service.snapshot().toString()
        assertThrows(IOException::class.java) { f.service.restore(imported, "replace", true) }
        assertEquals(original, f.service.snapshot().toString())
    }

    @Test fun mergeConflictLeavesEveryCollectionAndMetadataUnchanged() {
        val f = DomainFixture(); val imported = f.service.snapshot()
        imported.getJSONObject("data").getJSONArray("consoles").getJSONObject(0).put("name", "CONFLITANTE")
        val original = f.service.snapshot().toString(); val saves = f.store.saves
        val result = f.service.restore(imported,"merge")
        assertFalse(result.applied)
        assertFalse(result.conflicts.isEmpty())
        assertEquals(original,f.service.snapshot().toString())
        assertEquals(saves,f.store.saves)
    }
}
