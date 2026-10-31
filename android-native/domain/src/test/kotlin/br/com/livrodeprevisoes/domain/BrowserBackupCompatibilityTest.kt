package br.com.livrodeprevisoes.domain

import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import java.io.File

/** Unmodified public browser-exported demo fixtures from auditoria_interface/dados. */
class BrowserBackupCompatibilityTest {
    @Test fun actualBrowserBackupsRoundTripWithoutLosingAnyPortableRowOrField() {
        for (filename in listOf("backup-10-38-03.json", "backup-10-39-46.json")) {
            val exported = JSONObject(fixtureText(filename))
            val validated = BackupCodec.parse(fixtureText(filename))
            val roundTripped = BackupCodec.validate(JSONObject(validated.toString()))
            assertTrue("Lossy browser roundtrip: $filename", exported.similar(roundTripped))
            val data=roundTripped.getJSONObject("data")
            assertEquals(10,data.length())
            assertEquals(12,data.getJSONArray("consoles").length())
            assertEquals(6,data.getJSONArray("events").length())
            assertEquals(7,data.getJSONArray("eventHistory").length())
            assertFalse(data.has("errorLogs"))
            assertFalse(roundTripped.has("errorLogs"))
            assertEquals("Usuário local",data.getJSONArray("settings").getJSONObject(0).getJSONObject("value").getString("localUserName"))
            assertTrue(BackupCodec.csv(roundTripped,"all").startsWith("\uFEFFID;"))
            val merge = BackupCodec.merge(roundTripped, exported)
            assertTrue(merge.applied)
            assertEquals(0,merge.inserted)
            assertEquals(0,merge.updated)
            assertEquals(52,merge.skipped)
            assertTrue(exported.similar(merge.snapshot))
        }
    }
    private fun fixtureText(filename: String): String {
        javaClass.getResourceAsStream("/browser-v1/$filename")?.use { return it.reader(Charsets.UTF_8).readText() }
        // The bare compiler runner does not process Gradle resources. Locate the
        // same checked-in fixture from repo, project, or domain working directory.
        val root = generateSequence(File(System.getProperty("user.dir")).absoluteFile) { it.parentFile }
            .flatMap { base -> sequenceOf(File(base,"android-native/domain/src/test/resources/browser-v1"),File(base,"domain/src/test/resources/browser-v1"),File(base,"src/test/resources/browser-v1")) }
            .firstOrNull { File(it,filename).isFile }
        requireNotNull(root) { "Browser fixture missing: $filename" }
        return File(root,filename).readText(Charsets.UTF_8)
    }
}
