package br.com.livrodeprevisoes.data

import br.com.livrodeprevisoes.domain.SnapshotStore
import br.com.livrodeprevisoes.domain.StrictJson
import java.nio.ByteBuffer
import java.nio.charset.CodingErrorAction
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.io.FileOutputStream
import java.nio.file.Files
import java.nio.file.StandardCopyOption
import java.time.Instant
import java.util.UUID

/** App-private persistence. A failed write never replaces the last committed snapshot. */
class FileSnapshotStore(private val file: File) : SnapshotStore {
    @Synchronized override fun load(): JSONObject? {
        if (!file.exists()) return null
        require(file.isFile) { "O arquivo de dados não é um arquivo regular." }
        val text=Charsets.UTF_8.newDecoder().onMalformedInput(CodingErrorAction.REPORT)
            .onUnmappableCharacter(CodingErrorAction.REPORT).decode(ByteBuffer.wrap(file.readBytes())).toString()
        return StrictJson.parseObject(text)
    }

    @Synchronized override fun save(snapshot: JSONObject) {
        atomicWrite(file, snapshot.toString())
    }

    /** Diagnostics are separate from the portable business-data backup. */
    @Synchronized fun errors(): List<JSONObject> {
        val logs = logFile()
        if (!logs.exists()) return emptyList()
        val array = JSONArray(logs.readText(Charsets.UTF_8))
        return (0 until array.length()).map { JSONObject(array.getJSONObject(it).toString()) }
    }

    @Synchronized fun logError(context: String, message: String) {
        val existing = try { errors() } catch (_: Exception) { emptyList() }
        val recent = (existing + JSONObject().put("id", UUID.randomUUID().toString())
            .put("timestamp", Instant.now().toString()).put("context", context.take(200))
            .put("message", message.take(4000))).takeLast(200)
        atomicWrite(logFile(), JSONArray(recent).toString())
    }

    @Synchronized fun clearErrors() { atomicWrite(logFile(), "[]") }

    private fun logFile() = File(file.parentFile, file.name + ".errors.json")

    private fun atomicWrite(target: File, text: String) {
        val parent = target.absoluteFile.parentFile ?: error("Diretório de dados indisponível.")
        check(parent.isDirectory || parent.mkdirs()) { "Não foi possível preparar o diretório de dados." }
        val pending = File(parent, target.name + ".pending")
        // Never remove an unexpected directory or unrelated artifact to make a write succeed.
        check(!pending.exists() || pending.isFile) { "O arquivo temporário de gravação está bloqueado." }
        try {
            FileOutputStream(pending, false).use { output ->
                output.write(text.toByteArray(Charsets.UTF_8))
                output.flush()
                output.fd.sync()
            }
            Files.move(pending.toPath(), target.toPath(), StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING)
        } finally {
            if (pending.isFile) pending.delete()
        }
    }
}
