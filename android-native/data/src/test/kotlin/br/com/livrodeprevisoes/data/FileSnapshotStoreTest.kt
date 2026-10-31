package br.com.livrodeprevisoes.data

import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import java.nio.file.Files
import java.io.File

class FileSnapshotStoreTest {
    private fun fixture(run: (File) -> Unit) {
        val directory = Files.createTempDirectory("livro-store-test").toFile()
        try { run(File(directory, "livro.json")) } finally { directory.deleteRecursively() }
    }
    @Test fun missingStoreIsEmptyAndRoundTripPreservesUnicodeAndDetachedValues() = fixture { file ->
        val store = FileSnapshotStore(file)
        assertNull(store.load())
        val snapshot = JSONObject().put("operator", "João — Operação").put("nested", JSONObject().put("id", "safe"))
        store.save(snapshot)
        snapshot.getJSONObject("nested").put("id", "modified")
        val read = FileSnapshotStore(file).load()!!
        assertEquals("João — Operação", read.getString("operator"))
        assertEquals("safe", read.getJSONObject("nested").getString("id"))
        read.put("operator", "not persisted")
        assertEquals("João — Operação", store.load()!!.getString("operator"))
    }
    @Test fun corruptExistingStoreRaisesWithoutDeletingOrReplacingBytes() = fixture { file ->
        file.writeText("{broken-original", Charsets.UTF_8)
        try { FileSnapshotStore(file).load(); fail("Corrupt persisted data must not be treated as empty") } catch (_: Exception) { }
        assertEquals("{broken-original", file.readText())
    }
    @Test fun blockedTemporaryWritePreservesCommittedSnapshot() = fixture { file ->
        val store = FileSnapshotStore(file)
        store.save(JSONObject().put("version", 1))
        val original = file.readBytes()
        val blocked = File(file.parentFile, file.name + ".pending")
        blocked.mkdir(); File(blocked, "do-not-remove").writeText("sentinel")
        try { store.save(JSONObject().put("version", 2)); fail("Blocked write must fail") } catch (_: Exception) { }
        assertArrayEquals(original, file.readBytes())
        assertEquals("sentinel", File(blocked, "do-not-remove").readText())
    }
    @Test fun persistedErrorLogIsBoundedAndNeverIncludedInMainSnapshot() = fixture { file ->
        val store = FileSnapshotStore(file)
        store.save(JSONObject().put("version", 1))
        repeat(205) { store.logError("test", "failure $it") }
        val reloaded = FileSnapshotStore(file)
        assertEquals(200, reloaded.errors().size)
        assertEquals("failure 204", reloaded.errors().last().getString("message"))
        assertEquals(1, reloaded.load()!!.getInt("version"))
        assertFalse(reloaded.load()!!.has("errorLogs"))
        reloaded.clearErrors()
        assertEquals(0, store.errors().size)
    }
    @Test fun trailingGarbageAndMalformedUtf8AreNotSilentlyRepaired() = fixture { file ->
        val store=FileSnapshotStore(file)
        for(text in listOf("{\"version\":1} CORRUPTED", "{\"version\":1}{}", "{version:1}", "{\"version\":1,}")) {
            file.writeText(text)
            try { store.load(); fail("Corrupt persisted document must be rejected: $text") } catch (_: Exception) { }
            assertEquals(text,file.readText())
        }
        val bytes=byteArrayOf(123,34,120,34,58,34,0xc3.toByte(),0x28,34,125)
        file.writeBytes(bytes)
        try { store.load(); fail("Invalid UTF-8 must be rejected") } catch (_: Exception) { }
        assertArrayEquals(bytes,file.readBytes())
    }

}
