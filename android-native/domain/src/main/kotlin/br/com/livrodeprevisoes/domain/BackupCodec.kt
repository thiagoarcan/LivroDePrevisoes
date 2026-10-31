package br.com.livrodeprevisoes.domain

import org.json.JSONArray
import org.json.JSONObject
import java.math.BigDecimal
import java.nio.ByteBuffer
import java.time.Duration
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.LocalTime
import java.time.OffsetDateTime
import java.time.ZoneId
import java.time.ZoneOffset
import java.time.format.DateTimeFormatter
import java.util.Base64
import java.util.Locale
import java.util.zip.CRC32
import kotlin.math.abs
import kotlin.math.floor

data class MergeResult(
    val snapshot: JSONObject,
    val inserted: Int,
    val updated: Int,
    val skipped: Int,
    val conflicts: List<String>,
    val applied: Boolean
)

/** Lossless schema-v1 interchange. No persistence, input mutation or silent repair. */
object BackupCodec {
    /** Strict text boundary: unlike JSONObject(String), never accepts trailing input. */
    fun parse(text: String): JSONObject = validate(StrictJson.parseObject(text))

    private val stores = listOf("consoles", "pipelines", "operationalUnits", "pipelineOperationalUnits", "equipmentTypes", "equipmentTags", "events", "eventHistory", "colorRanges", "settings")
    private const val MAX_SAFE_INTEGER = 9007199254740991L
    private val catalogue = "id name active createdAt updatedAt version synchronizationStatus"
    private val required = mapOf(
        "consoles" to catalogue,
        "operationalUnits" to catalogue,
        "pipelines" to "$catalogue consoleId",
        "pipelineOperationalUnits" to "id pipelineId uoId createdAt version synchronizationStatus",
        "equipmentTypes" to "$catalogue uoId",
        "equipmentTags" to "id tag uoId equipmentTypeId active createdAt updatedAt version synchronizationStatus",
        "events" to "id consoleId pipelineId uoId equipmentTypeId tagId scheduledDate scheduledTime scheduledAt description notes priority status hasAlarm useDefaultAlarmSettings alarmMinutesBefore alarmAudio alarmVisual alarmNotification alarmRepeat alarmRepeatInterval alarmMaxRepeats alarmState alarmSnoozedUntil alarmTriggerCount lastAlarmTriggeredAt completedAt completedTimeDiffMinutes completionNote active createdAt updatedAt version synchronizationStatus",
        "eventHistory" to "id eventId action timestamp description previousValue newValue localUser",
        "colorRanges" to "id name color minMinutes maxMinutes priority blink sound active",
        "settings" to "key value"
    ).mapValues { it.value.split(' ') }
    private val nullable = mapOf(
        "events" to setOf("equipmentTypeId", "tagId", "alarmSnoozedUntil", "lastAlarmTriggeredAt", "completedAt", "completedTimeDiffMinutes"),
        "eventHistory" to setOf("previousValue", "newValue")
    )
    private val booleans = setOf("active", "hasAlarm", "useDefaultAlarmSettings", "alarmAudio", "alarmVisual", "alarmNotification", "alarmRepeat", "blink", "sound")
    private val texts = setOf("notes", "completionNote", "createdBy", "completedBy", "localUser", "description", "previousValue", "newValue", "synchronizationStatus")
    private val numeric = setOf("alarmMinutesBefore", "alarmRepeatInterval", "alarmMaxRepeats", "alarmTriggerCount", "minMinutes", "maxMinutes")
    private val idPattern = Regex("[A-Za-z0-9_-]{1,128}")
    private val isoPattern = Regex("\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,9})?(?:Z|[+-]\\d{2}:\\d{2})")
    private val pngPattern = Regex("data:image/png;base64,iVBORw0KGgo[A-Za-z0-9+/]*={0,2}")

    fun validate(snapshot: JSONObject): JSONObject {
        val copy = copyJson(snapshot) as JSONObject
        val version = copy.opt("schemaVersion")
        require(version == "1" || (version is Number && decimal(version) == BigDecimal.ONE)) { "Versão de backup não suportada." }
        iso(copy.opt("exportedAt"), "Data de exportação")
        val data = copy.opt("data") as? JSONObject ?: invalid("Seção de dados inválida.")
        require(keys(data).all { it in stores }) { "Coleção desconhecida no backup." }
        val maps = linkedMapOf<String, Map<String, JSONObject>>()
        for (store in stores) {
            val array = data.opt(store) as? JSONArray ?: invalid("Coleção obrigatória ausente: $store.")
            val indexed = linkedMapOf<String, JSONObject>()
            val businessKeys = hashSetOf<String>()
            for (index in 0 until array.length()) {
                val row = array.opt(index) as? JSONObject ?: invalid("Linha inválida em $store.")
                for (field in required.getValue(store)) {
                    require(row.has(field) && (!row.isNull(field) || field in nullable[store].orEmpty())) { "Campo obrigatório ausente: $store.$field." }
                }
                val id = row.opt(if (store == "settings") "key" else "id")
                require(id is String && idPattern.matches(id) && id !in setOf("__proto__", "constructor", "prototype")) { "ID inválido em $store." }
                require(indexed.put(id, row) == null) { "ID duplicado em $store: $id." }
                businessKey(store, row)?.let { require(it.isNotEmpty() && businessKeys.add(it)) { "Duplicidade cadastral em $store." } }
                if (row.has("version")) integer(row.opt("version"), 1, MAX_SAFE_INTEGER, "Versão")
                for (field in listOf("createdAt", "updatedAt", "timestamp", "completedAt", "lastAlarmTriggeredAt")) {
                    if (!row.isNull(field)) iso(row.opt(field), "$store.$field")
                }
                for (field in keys(row)) {
                    val value = row.opt(field)
                    if (field in numeric || store == "colorRanges" && field == "priority") require(value is Number) { "Número $field inválido." }
                    if (field in texts && !row.isNull(field)) require(value is String) { "Texto $field inválido." }
                    if (field in booleans) require(value is Boolean) { "Booleano $field inválido." }
                    if (field.lowercase(Locale.ROOT) in setOf("url", "link", "href", "externalurl") && !row.isNull(field) && value != "") {
                        require(value is String && Regex("https?://.*", RegexOption.IGNORE_CASE).matches(value)) { "Link inválido." }
                    }
                }
                drawing(row.opt("stylusDrawing"))
            }
            maps[store] = indexed
        }
        fun rows(store: String) = maps.getValue(store).values
        fun ref(store: String, id: Any?): JSONObject = (if (id is String) maps.getValue(store)[id] else null) ?: invalid("Referência ausente em $store: $id.")
        for (row in rows("consoles")) text(row.opt("name"), "Console")
        for (row in rows("operationalUnits")) text(row.opt("name"), "UO")
        for (row in rows("pipelineOperationalUnits")) { ref("pipelines", row.opt("pipelineId")); ref("operationalUnits", row.opt("uoId")) }
        for (row in rows("pipelines")) {
            text(row.opt("name"), "Duto"); ref("consoles", row.opt("consoleId"))
            require(rows("pipelineOperationalUnits").filter { it.opt("pipelineId") == row.opt("id") }.map { it.opt("uoId") }.toSet().size >= 2) { "Duto exige duas UOs distintas." }
        }
        for (row in rows("equipmentTypes")) { text(row.opt("name"), "Tipo"); ref("operationalUnits", row.opt("uoId")) }
        for (row in rows("equipmentTags")) {
            text(row.opt("tag"), "TAG"); ref("operationalUnits", row.opt("uoId"))
            require(ref("equipmentTypes", row.opt("equipmentTypeId")).opt("uoId") == row.opt("uoId")) { "Tipo e TAG possuem UOs incompatíveis." }
        }
        for (row in rows("events")) {
            text(row.opt("description"), "Descrição"); ref("consoles", row.opt("consoleId")); ref("operationalUnits", row.opt("uoId"))
            val pipeline = ref("pipelines", row.opt("pipelineId"))
            require(pipeline.opt("consoleId") == row.opt("consoleId") && rows("pipelineOperationalUnits").any { it.opt("pipelineId") == row.opt("pipelineId") && it.opt("uoId") == row.opt("uoId") }) { "Console, duto e UO incompatíveis." }
            if (!row.isNull("equipmentTypeId") && row.opt("equipmentTypeId") != "") require(ref("equipmentTypes", row.opt("equipmentTypeId")).opt("uoId") == row.opt("uoId")) { "Tipo incompatível com UO." }
            if (!row.isNull("tagId") && row.opt("tagId") != "") {
                val tag = ref("equipmentTags", row.opt("tagId"))
                require(tag.opt("uoId") == row.opt("uoId") && tag.opt("equipmentTypeId") == row.opt("equipmentTypeId")) { "TAG incompatível com tipo ou UO." }
            }
            val local = localTime(row.opt("scheduledDate"), row.opt("scheduledTime"))
            val scheduled = iso(row.opt("scheduledAt"), "Horário previsto").toInstant()
            // Legacy v1 has no source timezone. Preserve the original instant and
            // local labels, allowing only a real, whole-minute timezone difference.
            val offset = Duration.between(scheduled, local.toInstant(ZoneOffset.UTC))
            require(abs(offset.seconds) <= 14 * 3600 && offset.seconds % 60 == 0L && offset.nano == 0) { "Horário previsto inconsistente." }
            require(row.opt("status") in setOf("pendente", "concluido")) { "Situação do evento inválida." }
            require(row.opt("alarmState") in setOf("idle", "triggered", "snoozed", "acknowledged")) { "Situação do alarme inválida." }
            require(row.opt("priority") in setOf("Baixa", "Normal", "Alta", "Crítica", "Urgente")) { "Prioridade inválida." }
            integer(row.opt("alarmMinutesBefore"), 0, 525600, "Antecedência")
            integer(row.opt("alarmRepeatInterval"), 1, 1440, "Intervalo")
            integer(row.opt("alarmMaxRepeats"), 0, 1000, "Repetições")
            integer(row.opt("alarmTriggerCount"), 0, MAX_SAFE_INTEGER, "Disparos")
            if (!row.isNull("alarmSnoozedUntil")) require(number(row.opt("alarmSnoozedUntil"), "Adiamento") >= 0) { "Adiamento inválido." }
            if (!row.isNull("completedTimeDiffMinutes")) number(row.opt("completedTimeDiffMinutes"), "Diferença de conclusão")
            if (row.opt("status") == "concluido") iso(row.opt("completedAt"), "Data de conclusão")
        }
        for (row in rows("eventHistory")) { ref("events", row.opt("eventId")); text(row.opt("action"), "Ação do histórico"); iso(row.opt("timestamp"), "Data do histórico") }
        validateRanges(rows("colorRanges").toList())
        require(rows("settings").size == 1) { "Configuração principal obrigatória." }
        for (row in rows("settings")) {
            require(row.opt("key") == "app_settings") { "Chave de configuração desconhecida." }
            val settings = row.opt("value") as? JSONObject ?: invalid("Configurações inválidas.")
            validateSettings(settings)
            if (!settings.isNull("activeConsoleId")) ref("consoles", settings.opt("activeConsoleId"))
        }
        return copy
    }

    fun merge(existing: JSONObject, incoming: JSONObject): MergeResult {
        val original = validate(existing)
        val imported = validate(incoming)
        val candidate = copyJson(original) as JSONObject
        var inserted = 0; var updated = 0; var skipped = 0
        val conflicts = mutableListOf<String>()
        for (store in stores) {
            val target = candidate.getJSONObject("data").getJSONArray(store)
            val key = if (store == "settings") "key" else "id"
            val indexed = rows(target).associateBy { it.getString(key) }.toMutableMap()
            for (newRow in rows(imported.getJSONObject("data").getJSONArray(store))) {
                val id = newRow.getString(key)
                val current = indexed[id]
                if (current == null) {
                    val business = businessKey(store, newRow)
                    if (business != null && indexed.values.any { businessKey(store, it) == business }) {
                        conflicts += "$store/$id: duplicate-business-key"; continue
                    }
                    val detached = copyJson(newRow) as JSONObject
                    target.put(detached); indexed[id] = detached; inserted++; continue
                }
                if (sameJson(current, newRow)) { skipped++; continue }
                val oldVersion = if (current.has("version")) integer(current.opt("version"), 1, MAX_SAFE_INTEGER, "Versão") else 0
                val newVersion = if (newRow.has("version")) integer(newRow.opt("version"), 1, MAX_SAFE_INTEGER, "Versão") else 0
                val oldTime = revisionTime(current); val newTime = revisionTime(newRow)
                // Never allow an older timestamp OR revision to overwrite current data.
                if (newVersion < oldVersion || newTime < oldTime) { skipped++; continue }
                if (newVersion == oldVersion && newTime == oldTime) {
                    conflicts += "$store/$id: same-revision-different-content"; continue
                }
                for (field in keys(newRow)) current.put(field, copyJson(newRow.get(field)))
                updated++
            }
        }
        if (conflicts.isEmpty()) {
            try { validate(candidate) } catch (error: IllegalArgumentException) { conflicts += "data: ${error.message}" }
        }
        return if (conflicts.isEmpty()) MergeResult(candidate, inserted, updated, skipped, emptyList(), true)
        else MergeResult(original, 0, 0, skipped, conflicts.toList(), false)
    }

    /** Excel-compatible UTF-8 text (caller encodes UTF-8), BOM, CRLF and semicolons. */
    fun csv(snapshot: JSONObject, kind: String): String {
        val normalized = when (kind) { "pendente" -> "pending"; "concluido" -> "completed"; "todos" -> "all"; "master" -> "cadastros"; else -> kind }
        require(normalized in setOf("pending", "completed", "all", "cadastros")) { "Tipo de CSV inválido." }
        val data = validate(snapshot).getJSONObject("data")
        fun records(store: String) = rows(data.getJSONArray(store))
        fun names(store: String, field: String = "name") = records(store).associate { it.getString("id") to it.getString(field) }
        val consoles = names("consoles"); val pipelines = names("pipelines"); val units = names("operationalUnits")
        val types = names("equipmentTypes"); val tags = names("equipmentTags", "tag")
        val output = mutableListOf<List<Any?>>()
        if (normalized == "cadastros") {
            output += listOf("Tipo de Registro", "ID", "Nome / Código", "Console / UO Vinculada", "Situação", "Data Criação")
            for ((store, label) in listOf("consoles" to "Console", "pipelines" to "Duto", "operationalUnits" to "UO", "equipmentTypes" to "Tipo Equipamento", "equipmentTags" to "TAG")) {
                for (row in records(store)) {
                    val linked = when (store) { "pipelines" -> consoles[row.opt("consoleId")]; "equipmentTypes", "equipmentTags" -> units[row.opt("uoId")]; else -> "-" }
                    output += listOf(label, row.getString("id"), row.getString(if (store == "equipmentTags") "tag" else "name"), linked ?: "", if (row.getBoolean("active")) "Ativo" else "Inativo", dateTime(row.getString("createdAt")))
                }
            }
        } else {
            output += listOf("ID", "Situação", "Console", "Duto", "UO", "Tipo de Equipamento", "TAG", "Data Prevista", "Hora Prevista", "Descrição", "Observações", "Alarme Ativo", "Antecedência (min)", "Data Conclusão", "Hora Conclusão", "Diferença Efetiva", "Observação Conclusão", "Data Criação", "Data Atualização")
            for (row in records("events")) {
                if (!row.getBoolean("active") || normalized == "pending" && row.getString("status") != "pendente" || normalized == "completed" && row.getString("status") != "concluido") continue
                val completed = if (row.isNull("completedAt")) null else iso(row.getString("completedAt"), "Conclusão").atZoneSameInstant(ZoneId.systemDefault())
                val difference = if (row.isNull("completedTimeDiffMinutes")) "--" else {
                    val rounded = floor(row.getDouble("completedTimeDiffMinutes") + 0.5)
                    when { rounded > 0 -> "Com atraso de ${plainNumber(rounded)} min"; rounded < 0 -> "Com antecedência de ${plainNumber(-rounded)} min"; else -> "Exatamente no horário" }
                }
                output += listOf(row.getString("id"), if (row.getString("status") == "concluido") "Concluído" else "Pendente", consoles[row.opt("consoleId")] ?: "", pipelines[row.opt("pipelineId")] ?: "", units[row.opt("uoId")] ?: "", types[row.opt("equipmentTypeId")] ?: "", tags[row.opt("tagId")] ?: "", LocalDate.parse(row.getString("scheduledDate")).format(DATE), row.getString("scheduledTime"), row.getString("description"), row.getString("notes"), if (row.getBoolean("hasAlarm")) "Sim" else "Não", row.get("alarmMinutesBefore"), completed?.format(DATE) ?: "", completed?.format(TIME) ?: "", difference, row.getString("completionNote"), dateTime(row.getString("createdAt")), dateTime(row.getString("updatedAt")))
            }
        }
        return "\uFEFF" + output.joinToString("\r\n") { row -> row.joinToString(";") { csvCell(it) } }
    }

    private fun validateRanges(rows: List<JSONObject>) {
        require(rows.isNotEmpty()) { "Pelo menos uma faixa é obrigatória." }
        val ordered = rows.sortedBy { integer(it.opt("minMinutes"), 0, 999999999, "Limite inicial") }
        var end = 0L
        for (row in ordered) {
            text(row.opt("name"), "Faixa")
            require(row.opt("color") is String && Regex("#[0-9a-fA-F]{6}").matches(row.getString("color"))) { "Cor inválida." }
            val start = integer(row.opt("minMinutes"), 0, 999999999, "Limite inicial")
            val next = integer(row.opt("maxMinutes"), 1, 999999999, "Limite final")
            integer(row.opt("priority"), 0, 1000, "Prioridade")
            require(start == end && next > start) { "Faixas com lacuna, sobreposição ou limite inválido." }
            end = next
        }
    }
    private fun validateSettings(value: JSONObject) {
        for (key in listOf("localUserName", "soundEnabled", "soundType", "soundVolume", "visualAlertEnabled", "notificationEnabled", "repeatAlarm", "repeatIntervalMinutes", "maxRepeats", "defaultLeadTimeMinutes")) require(value.has(key) && !value.isNull(key)) { "Configuração obrigatória ausente: $key." }
        val enums = mapOf("soundType" to setOf("chime", "beep", "siren", "blip"), "theme" to setOf("dark", "light", "industrial"), "viewMode" to setOf("cards", "table"), "responsiveLayoutMode" to setOf("auto", "compact", "mobile", "tablet", "conventional", "widescreen", "ultrawide"))
        for ((key, options) in enums) if (value.has(key)) require(value.opt(key) in options) { "Configuração $key inválida." }
        for ((key, range) in mapOf("soundVolume" to 0L..100L, "defaultLeadTimeMinutes" to 0L..525600L, "repeatIntervalMinutes" to 1L..1440L, "maxRepeats" to 0L..1000L, "backupReminderDays" to 1L..3650L)) if (value.has(key)) integer(value.opt(key), range.first, range.last, key)
        for (key in listOf("soundEnabled", "visualAlertEnabled", "highlightCardEnabled", "pulsingEnabled", "changeTitleEnabled", "notificationEnabled", "repeatAlarm", "firstMobileNoticeShown", "keepDutoUOPrefilled")) if (value.has(key)) require(value.opt(key) is Boolean) { "Configuração $key inválida." }
        text(value.opt("localUserName"), "Nome do usuário")
        if (!value.isNull("lastBackupAt")) iso(value.opt("lastBackupAt"), "Data de backup")
    }
    private fun drawing(value: Any?) {
        if (value == null || value === JSONObject.NULL || value == "") return
        require(value is String && value.length <= 3000000 && pngPattern.matches(value)) { "Desenho deve ser uma imagem PNG segura." }
        val bytes = try { Base64.getDecoder().decode(value.substringAfter(',')) } catch (_: IllegalArgumentException) { invalid("PNG base64 inválido.") }
        require(bytes.size >= 8 && bytes.copyOfRange(0, 8).contentEquals(byteArrayOf(-119,80,78,71,13,10,26,10))) { "Assinatura PNG inválida." }
        // A tiny compressed PNG can otherwise request gigabytes in BitmapFactory.
        // Validate the mandatory first chunk before any platform image decoding.
        require(bytes.size >= 33) { "Cabeçalho PNG incompleto." }
        val header = ByteBuffer.wrap(bytes)
        require(header.getInt(8) == 13 && header.getInt(12) == 0x49484452) { "Cabeçalho IHDR inválido." }
        val width = header.getInt(16); val height = header.getInt(20)
        require(width in 1..8192 && height in 1..8192 && width.toLong() * height <= 4_194_304L) {
            "Desenho PNG excede o limite seguro: 8192 por dimensão e 4.194.304 pixels."
        }
        val checksum = CRC32().apply { update(bytes, 12, 17) }.value.toInt()
        require(header.getInt(29) == checksum) { "Cabeçalho PNG corrompido." }
    }
    private fun businessKey(store: String, row: JSONObject): String? {
        fun clean(field: String) = browserTrim((row.opt(field) as? String).orEmpty()).lowercase(Locale.ROOT)
        return when (store) {
            "consoles", "operationalUnits", "colorRanges" -> clean("name")
            "pipelines" -> "${row.opt("consoleId")}|${clean("name")}"
            "equipmentTypes" -> "${row.opt("uoId")}|${clean("name")}"
            "equipmentTags" -> clean("tag")
            "pipelineOperationalUnits" -> "${row.opt("pipelineId")}|${row.opt("uoId")}"
            else -> null
        }
    }
    private fun integer(value: Any?, min: Long, max: Long, label: String): Long {
        require(value is Number) { "$label deve ser numérico." }
        val number = decimal(value)
        require(number.scale() <= 0 && number >= BigDecimal.valueOf(min) && number <= BigDecimal.valueOf(max)) { "$label: número inteiro entre $min e $max." }
        return number.toLong()
    }
    private fun decimal(value: Number): BigDecimal = try { BigDecimal(value.toString()).stripTrailingZeros() } catch (_: NumberFormatException) { invalid("Número inválido.") }
    private fun number(value: Any?, label: String): Double {
        require(value is Number && value.toDouble().isFinite()) { "$label deve ser um número finito." }
        return value.toDouble()
    }
    private fun text(value: Any?, label: String): String {
        require(value is String && browserTrim(value).isNotEmpty()) { "$label obrigatório." }
        return browserTrim(value)
    }
    private fun browserTrim(value: String): String = value.trim { it.isWhitespace() || Character.isSpaceChar(it) || it == '\uFEFF' }
    private fun iso(value: Any?, label: String): OffsetDateTime {
        require(value is String && isoPattern.matches(value)) { "$label inválida." }
        val parsed = try { OffsetDateTime.parse(value) } catch (_: java.time.DateTimeException) { invalid("$label inválida.") }
        require(parsed.year >= 100) { "$label inválida." }
        return parsed
    }
    private fun localTime(date: Any?, time: Any?): LocalDateTime {
        require(date is String && Regex("\\d{4}-\\d{2}-\\d{2}").matches(date) && time is String && Regex("\\d{2}:\\d{2}").matches(time)) { "Data ou hora inválida." }
        val parsed = try { LocalDateTime.of(LocalDate.parse(date), LocalTime.parse(time)) } catch (_: java.time.DateTimeException) { invalid("Data ou hora inválida.") }
        require(parsed.year >= 100) { "Data ou hora inválida." }
        return parsed
    }
    private fun revisionTime(row: JSONObject): java.time.Instant = listOf("updatedAt", "createdAt", "timestamp").firstOrNull { !row.isNull(it) }?.let { iso(row.opt(it), it).toInstant() } ?: java.time.Instant.EPOCH
    private fun keys(value: JSONObject) = value.keys().asSequence().toList()
    private fun rows(value: JSONArray) = (0 until value.length()).map { value.getJSONObject(it) }
    private fun copyJson(value: Any?, depth: Int = 0): Any {
        require(depth <= 128) { "Estrutura JSON excessivamente profunda." }
        return when (value) {
            null, JSONObject.NULL -> JSONObject.NULL
            is JSONObject -> JSONObject().also { result ->
                for (key in keys(value)) {
                    StrictJson.requireValidUnicode(key)
                    result.put(key, copyJson(value.get(key), depth + 1))
                }
            }
            is JSONArray -> JSONArray().also { result -> for (index in 0 until value.length()) result.put(copyJson(value.get(index), depth + 1)) }
            is String -> value.also(StrictJson::requireValidUnicode)
            is Boolean -> value
            is Number -> value.also { require(it.toDouble().isFinite()) { "Número não finito no backup." } }
            else -> invalid("Valor não JSON no backup.")
        }
    }
    private fun sameJson(a: Any?, b: Any?): Boolean = when {
        a is JSONObject && b is JSONObject -> keys(a).toSet() == keys(b).toSet() && keys(a).all { sameJson(a.get(it), b.get(it)) }
        a is JSONArray && b is JSONArray -> a.length() == b.length() && (0 until a.length()).all { sameJson(a.get(it), b.get(it)) }
        a is Number && b is Number -> decimal(a) == decimal(b)
        else -> a == b
    }
    private val DATE = DateTimeFormatter.ofPattern("dd/MM/uuuu", Locale.ROOT)
    private val TIME = DateTimeFormatter.ofPattern("HH:mm", Locale.ROOT)
    private fun dateTime(value: String): String = iso(value, "Data").atZoneSameInstant(ZoneId.systemDefault()).let { "${it.format(DATE)} ${it.format(TIME)}" }
    private fun plainNumber(value: Double) = BigDecimal.valueOf(value).stripTrailingZeros().toPlainString()
    private fun csvCell(value: Any?): String {
        if (value == null || value === JSONObject.NULL) return "\"\""
        var text = value.toString()
        if (value is String) {
            val prefix = text.takeWhile { it.isWhitespace() || Character.isSpaceChar(it) || it == '\uFEFF' }
            val trimmed = text.substring(prefix.length)
            if (prefix.any { it == '\t' || it == '\r' } || trimmed.firstOrNull() in listOf('=', '+', '-', '@')) text = "'$text"
        }
        return if (text.any { it in ";\"\n\r" }) "\"${text.replace("\"", "\"\"")}\"" else text
    }
    private fun invalid(message: String): Nothing = throw IllegalArgumentException(message)
}
