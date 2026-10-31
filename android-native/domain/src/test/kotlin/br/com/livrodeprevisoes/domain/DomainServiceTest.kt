package br.com.livrodeprevisoes.domain

import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import java.io.IOException
import java.time.Instant
import java.time.ZoneId

internal class MemorySnapshotStore(initial: JSONObject? = null) : SnapshotStore {
    var value = initial?.let { JSONObject(it.toString()) }
    var saves = 0
    var failSave = false
    override fun load(): JSONObject? = value?.let { JSONObject(it.toString()) }
    override fun save(snapshot: JSONObject) {
        if (failSave) throw IOException("Disco indisponível")
        value = JSONObject(snapshot.toString())
        saves++
    }
}

class DomainServiceTest {
    private val instant = Instant.parse("2026-10-31T12:00:00Z")
    private fun service(store: MemorySnapshotStore = MemorySnapshotStore()) = LivroService(store, { instant }, ZoneId.of("UTC"))

    @Test fun emptyStoreIsSeededOnceWithUsableDefaults() {
        val store = MemorySnapshotStore()
        val s = service(store)
        assertEquals(1, store.saves)
        assertEquals(12, s.rows("consoles").size)
        assertEquals("C04", s.rows("consoles").first { it.getString("id") == s.settings().getString("activeConsoleId") }.getString("name"))
        assertEquals(15, s.settings().getInt("defaultLeadTimeMinutes"))
        assertEquals(10, s.snapshot().getJSONObject("data").length())
        assertEquals(5, s.rows("colorRanges").size)
        service(store)
        assertEquals(1, store.saves)
    }

    @Test fun corruptStoredDataIsNeverReplacedWithEmptyDefaults() {
        val store = MemorySnapshotStore(JSONObject("{\"schemaVersion\":1,\"data\":{}}"))
        val original = store.value.toString()
        assertThrows(IllegalArgumentException::class.java) { service(store) }
        assertEquals(0, store.saves)
        assertEquals(original, store.value.toString())
    }

    @Test fun exportSnapshotUsesCurrentExportTimeWithoutChangingPersistedData() {
        val f = DomainFixture()
        val persisted = f.store.value.toString(); val saves = f.store.saves
        f.clock = f.clock.plusSeconds(7200)
        assertEquals("2026-10-31T14:00:00Z", f.service.snapshot().getString("exportedAt"))
        assertEquals(persisted, f.store.value.toString())
        assertEquals(saves, f.store.saves)
    }

    @Test fun allReadResultsAreDefensiveCopies() {
        val s = service()
        s.rows("consoles").first().put("name", "CORROMPIDO")
        s.settings().put("soundVolume", 0)
        s.snapshot().getJSONObject("data").put("consoles", JSONArray())
        assertEquals(12, s.rows("consoles").size)
        assertFalse(s.rows("consoles").any { it.getString("name") == "CORROMPIDO" })
        assertEquals(80, s.settings().getInt("soundVolume"))
        assertThrows(IllegalArgumentException::class.java) { s.rows("inventado") }
    }
}
