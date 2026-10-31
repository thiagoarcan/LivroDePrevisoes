package br.com.livrodeprevisoes.domain

import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import java.io.IOException
import java.time.Instant
import java.time.ZoneId

internal class DomainFixture(val zone: ZoneId = ZoneId.of("UTC")) {
    var clock = Instant.parse("2026-10-31T12:00:00Z")
    val store = MemorySnapshotStore()
    val service = LivroService(store, { clock }, zone)
    val console get() = service.rows("consoles").first { it.getString("name") == "C04" }
    fun unit(name: String) = service.saveRecord("operationalUnits", JSONObject().put("name", name))
    fun hierarchy(): Triple<JSONObject, JSONObject, JSONObject> {
        val a = unit("ORIGEM")
        val b = unit("DESTINO")
        val p = service.saveRecord("pipelines", JSONObject().put("name", "DUTO TESTE").put("consoleId", console.getString("id")).put("uoIds", JSONArray(listOf(a.getString("id"), b.getString("id")))))
        return Triple(p, a, b)
    }
    fun input(h: Triple<JSONObject, JSONObject, JSONObject> = hierarchy()): JSONObject = JSONObject()
        .put("consoleId", console.getString("id")).put("pipelineId", h.first.getString("id")).put("uoId", h.second.getString("id"))
        .put("scheduledDate", "2026-10-31").put("scheduledTime", "12:00").put("description", "Verificar pressão")
}

class DomainCatalogTest {
    @Test fun pipelineCreationAtomicallyCreatesDistinctUnitLinks() {
        val f = DomainFixture()
        val a = f.unit("A"); val b = f.unit("B")
        val before = f.store.saves
        val p = f.service.saveRecord("pipelines", JSONObject().put("name", "  DUTO  ").put("consoleId", f.console.getString("id")).put("uoIds", JSONArray(listOf(a.getString("id"), b.getString("id")))))
        assertEquals("DUTO", p.getString("name"))
        assertEquals(1, p.getInt("version"))
        assertEquals(before + 1, f.store.saves)
        assertEquals(2, f.service.rows("pipelineOperationalUnits").count { it.getString("pipelineId") == p.getString("id") })
        assertFalse(p.has("uoIds"))
        val original = f.service.snapshot().toString()
        assertThrows(IllegalArgumentException::class.java) { f.service.saveRecord("pipelines", JSONObject(p.toString()).put("uoIds", JSONArray(listOf(a.getString("id"), a.getString("id"))))) }
        assertEquals(original, f.service.snapshot().toString())
    }

    @Test fun masterNamesAndTagsHaveTheirIntendedUniquenessScopes() {
        val f = DomainFixture(); val h = f.hierarchy()
        assertThrows(IllegalArgumentException::class.java) { f.unit(" origem ") }
        val t = f.service.saveRecord("equipmentTypes", JSONObject().put("name", "Bomba").put("uoId", h.second.getString("id")))
        val t2 = f.service.saveRecord("equipmentTypes", JSONObject().put("name", "Bomba").put("uoId", h.third.getString("id")))
        f.service.saveRecord("equipmentTags", JSONObject().put("tag", "BB-101").put("uoId", h.second.getString("id")).put("equipmentTypeId", t.getString("id")))
        assertThrows(IllegalArgumentException::class.java) { f.service.saveRecord("equipmentTags", JSONObject().put("tag", "bb-101").put("uoId", h.third.getString("id")).put("equipmentTypeId", t2.getString("id"))) }
        assertThrows(IllegalArgumentException::class.java) { f.service.saveRecord("equipmentTags", JSONObject().put("tag", "BB-102").put("uoId", h.third.getString("id")).put("equipmentTypeId", t.getString("id"))) }
    }

    @Test fun inactiveOriginalLinksRemainEditableButNewLinksAreRejected() {
        val f = DomainFixture(); val h = f.hierarchy()
        f.service.setRecordActive("operationalUnits", h.second.getString("id"), false)
        val edited = f.service.saveRecord("pipelines", JSONObject(h.first.toString()).put("name", "EDITADO").put("uoIds", JSONArray(listOf(h.second.getString("id"), h.third.getString("id")))))
        assertEquals(2, edited.getInt("version"))
        assertThrows(IllegalArgumentException::class.java) { f.service.saveRecord("equipmentTypes", JSONObject().put("name", "Novo tipo").put("uoId", h.second.getString("id"))) }
    }

    @Test fun deletionPreservesReferencedRecordsAndAllowsUnreferencedOnes() {
        val f = DomainFixture(); val h = f.hierarchy()
        val before = f.service.snapshot().toString()
        assertThrows(IllegalArgumentException::class.java) { f.service.deleteRecord("operationalUnits", h.second.getString("id")) }
        assertEquals(before, f.service.snapshot().toString())
        f.service.deleteRecord("pipelines", h.first.getString("id"))
        assertTrue(f.service.rows("pipelineOperationalUnits").isEmpty())
        f.service.deleteRecord("operationalUnits", h.second.getString("id"))
        assertEquals(1, f.service.rows("operationalUnits").size)
    }

    @Test fun failedPersistenceDoesNotCommitTheCandidate() {
        val f = DomainFixture()
        val before = f.service.snapshot().toString()
        f.store.failSave = true
        assertThrows(IOException::class.java) { f.unit("NÃO SALVA") }
        assertEquals(before, f.service.snapshot().toString())
    }

    @Test fun bulkUnitsDeduplicateAndReactivateInOneCommit() {
        val f = DomainFixture(); val a = f.unit("A")
        f.service.setRecordActive("operationalUnits", a.getString("id"), false)
        val before = f.store.saves
        val result = f.service.saveUOBatch("a;B\nB, C")
        assertEquals(before + 1, f.store.saves)
        assertEquals(3, f.service.rows("operationalUnits").size)
        assertEquals(2, result.getJSONArray("created").length())
        assertTrue(f.service.rows("operationalUnits").all { it.getBoolean("active") })
    }
}
