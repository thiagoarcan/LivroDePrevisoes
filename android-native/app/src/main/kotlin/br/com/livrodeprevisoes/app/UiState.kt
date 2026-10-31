package br.com.livrodeprevisoes.app

import org.json.JSONObject
import java.text.Normalizer
import java.time.Instant
import java.time.Duration

/** A successful document write is a one-shot capability, never a button click. */
class ExportGate(initial: String? = null) {
    var pending: String? = initial
        private set
    fun begin(action: String) { check(pending == null) { "Já existe uma exportação em andamento." }; pending = action }
    fun finished(written: Boolean): String? {
        val action = pending
        pending = null
        return if (written) action else null
    }
}

class DrawingSnapshot(private val original: String) {
    private var modified = false
    fun changed() { modified = true }
    fun encoded(capture: () -> String): String = if (modified) capture() else original
}

data class EventFilters(
    val pipeline: String = "", val unit: String = "", val equipment: String = "", val tag: String = "",
    val dateFrom: String = "", val dateTo: String = "", val alarm: String = "", val alarmState: String = "", val window: String = ""
)

private fun searchable(value: String) = Normalizer.normalize(value, Normalizer.Form.NFD)
    .replace(Regex("\\p{M}+"), "").lowercase(java.util.Locale.ROOT)
private fun instant(value: String): Instant = runCatching { Instant.parse(value) }.getOrDefault(Instant.MAX)
fun deadlineIsLate(scheduledAt: String, now: Instant = Instant.now()) = instant(scheduledAt).isBefore(now)

fun filterEvents(rows: List<JSONObject>, status: String, console: String, query: String, priority: String,
                 hierarchy: (JSONObject) -> String, filters: EventFilters = EventFilters(), now: Instant = Instant.now()): List<JSONObject> {
    val search = searchable(query.trim())
    val filtered = rows.filter { event ->
        val planned = instant(event.optString("scheduledAt"))
        val date = event.optString("scheduledDate", event.optString("scheduledAt").take(10))
        event.optBoolean("active", true) && event.optString("status") == status &&
            (console.isBlank() || event.optString("consoleId") == console) &&
            (priority.isBlank() || event.optString("priority", "Normal") == priority) &&
            (search.isBlank() || searchable(event.optString("description") + " " + event.optString("notes") + " " + hierarchy(event)).contains(search)) &&
            (filters.pipeline.isBlank() || event.optString("pipelineId") == filters.pipeline) &&
            (filters.unit.isBlank() || event.optString("uoId") == filters.unit) &&
            (filters.equipment.isBlank() || event.optString("equipmentTypeId") == filters.equipment) &&
            (filters.tag.isBlank() || event.optString("tagId") == filters.tag) &&
            (filters.dateFrom.isBlank() || date >= filters.dateFrom) && (filters.dateTo.isBlank() || date <= filters.dateTo) &&
            (filters.alarm.isBlank() || event.optBoolean("hasAlarm") == (filters.alarm == "on")) &&
            (filters.alarmState.isBlank() || event.optString("alarmState") == filters.alarmState) &&
            when (filters.window) {
                "overdue" -> planned.isBefore(now)
                "15", "30", "60" -> !planned.isBefore(now) && planned <= now.plusSeconds(filters.window.toLong() * 60)
                else -> true
            }
    }
    return if (status == "concluido") filtered.sortedByDescending { instant(it.optString("completedAt").takeUnless { value -> value.isBlank() || value == "null" } ?: it.optString("scheduledAt")) }
    else filtered.sortedBy { instant(it.optString("scheduledAt")) }
}

fun readBounded(input: java.io.InputStream, maxBytes: Int = 32 * 1024 * 1024): String {
    val output = java.io.ByteArrayOutputStream()
    val block = ByteArray(8192)
    var total = 0
    while (true) {
        val n = input.read(block)
        if (n == -1) break
        total += n
        require(total <= maxBytes) { "O arquivo excede o limite de 32 MiB. Nenhum dado foi alterado." }
        output.write(block, 0, n)
    }
    val text = Charsets.UTF_8.newDecoder().onMalformedInput(java.nio.charset.CodingErrorAction.REPORT).onUnmappableCharacter(java.nio.charset.CodingErrorAction.REPORT).decode(java.nio.ByteBuffer.wrap(output.toByteArray())).toString().removePrefix("\uFEFF")
    var quoted = false; var escaped = false; var depth = 0
    for (char in text) {
        if (quoted) {
            if (escaped) escaped = false else if (char == '\\') escaped = true else if (char == '"') quoted = false
        } else when (char) {
            '"' -> quoted = true
            '[', '{' -> { depth++; require(depth <= 128) { "O JSON excede o limite seguro de profundidade. Nenhum dado foi alterado." } }
            ']', '}' -> depth--
        }
    }
    return text
}

fun successfulBackupSettings(action: String, settings: JSONObject, now: Instant = Instant.now()): JSONObject? =
    if (action == "json") JSONObject(settings.toString()).put("lastBackupAt", now.toString()) else null
fun backupIsDue(settings: JSONObject, now: Instant = Instant.now()): Boolean {
    val last = runCatching { Instant.parse(settings.optString("lastBackupAt")) }.getOrNull() ?: return true
    return !now.isBefore(last.plusSeconds(settings.optInt("backupReminderDays", 7).coerceIn(1, 3650).toLong() * 86400))
}
fun pickableRecords(rows: List<JSONObject>, originals: Set<String>) = rows.filter { it.optBoolean("active", true) || it.optString("id") in originals }

fun sortHistory(rows: List<JSONObject>): List<JSONObject> = rows.sortedByDescending { instant(it.optString("timestamp", it.optString("createdAt"))) }

data class PageBounds(val page: Int, val start: Int, val endExclusive: Int, val total: Int)
fun pageBounds(total: Int, requestedPage: Int, size: Int = 100): PageBounds {
    require(total >= 0 && size > 0) { "Total e tamanho de página inválidos." }
    val lastPage = if (total == 0) 0 else (total - 1) / size
    val page = requestedPage.coerceIn(0, lastPage)
    val start = page * size
    return PageBounds(page, start, start + minOf(size, total - start), total)
}
