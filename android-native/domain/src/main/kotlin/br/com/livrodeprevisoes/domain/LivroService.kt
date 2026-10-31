package br.com.livrodeprevisoes.domain

import org.json.JSONArray
import org.json.JSONObject
import java.time.Instant
import java.time.ZoneId
import java.time.LocalDate
import java.time.LocalTime
import java.time.LocalDateTime
import java.time.DateTimeException
import java.time.format.DateTimeFormatter
import java.util.UUID
import java.util.Locale

/** A save must either persist the complete snapshot, or leave the previous one intact. */
interface SnapshotStore {
    fun load(): JSONObject?
    fun save(snapshot: JSONObject)
}

/** Browser-compatible business rules. The persistence boundary never receives a partial change. */
class LivroService(
    private val store: SnapshotStore,
    private val now: () -> Instant = { Instant.now() },
    private val zone: ZoneId = ZoneId.systemDefault()
) {
    init {
        synchronized(store) {
            val current = store.load()
            if (current == null) store.save(BackupCodec.validate(initialSnapshot()))
            else BackupCodec.validate(current)
        }
    }

    fun snapshot(): JSONObject = synchronized(store) { copy(read()).put("exportedAt", now().toString()) }

    fun rows(name: String): List<JSONObject> = synchronized(store) {
        require(name in COLLECTIONS) { "Coleção desconhecida: $name." }
        arrayRows(read().getJSONObject("data"), name).map(::copy)
    }

    fun settings(): JSONObject = synchronized(store) { settingsOf(read().getJSONObject("data")) }

    fun saveRecord(store: String, row: JSONObject): JSONObject = mutate { data -> copy(saveMaster(data, store, row)) }

    fun setRecordActive(store: String, id: String, active: Boolean): JSONObject = mutate { data ->
        requireMaster(store)
        val row = stamp(find(data, store, id), JSONObject().put("active", active))
        putRow(data, store, row)
        copy(row)
    }

    fun deleteRecord(store: String, id: String) {
        mutate { data ->
            requireMaster(store)
            find(data, store, id)
            data.put(store, JSONArray(arrayRows(data, store).filterNot { it.getString("id") == id }))
            if (store == "pipelines") data.put("pipelineOperationalUnits", JSONArray(arrayRows(data, "pipelineOperationalUnits").filterNot { it.getString("pipelineId") == id }))
            // Full validation rejects every orphan, including historical event references.
        }
    }

    fun saveUOBatch(names: String): JSONObject = mutate { data ->
        require(names.isNotBlank()) { "Informe ao menos uma UO." }
        val parsed = names.split(Regex("[,;\\n\\r]+")).map(String::trim).filter(String::isNotEmpty).distinctBy { it.lowercase(Locale.ROOT) }
        require(parsed.isNotEmpty()) { "Informe ao menos uma UO." }
        val created = JSONArray(); val existing = JSONArray()
        for (name in parsed) {
            val old = arrayRows(data, "operationalUnits").firstOrNull { it.getString("name").trim().equals(name, true) }
            if (old == null) created.put(saveMaster(data, "operationalUnits", JSONObject().put("name", name)))
            else {
                val row = if (!old.getBoolean("active")) stamp(old, JSONObject().put("active", true)) else old
                putRow(data, "operationalUnits", row)
                existing.put(row)
            }
        }
        val all = JSONArray()
        for (a in listOf(created, existing)) for (i in 0 until a.length()) all.put(a.getJSONObject(i))
        copy(JSONObject().put("created", created).put("existing", existing).put("all", all))
    }

    fun saveEvent(input: JSONObject): JSONObject = mutate { data -> copy(saveEventIn(data, input)) }
    fun completeEvent(id: String, note: String = ""): JSONObject = transition(id, "conclusao") { row, data ->
        require(row.getString("status") == "pendente") { "Evento já concluído." }
        row.put("status", "concluido").put("completedAt", now().toString()).put("completedBy", actor(data))
            .put("completedTimeDiffMinutes", (now().toEpochMilli() - Instant.parse(row.getString("scheduledAt")).toEpochMilli()) / 60000.0)
            .put("completionNote", note.trim()).put("alarmState", "acknowledged").put("alarmSnoozedUntil", JSONObject.NULL)
    }

    fun reopenEvent(id: String, date: String? = null, time: String? = null): JSONObject = transition(id, "reabertura") { row, _ ->
        require(date.isNullOrEmpty() == time.isNullOrEmpty()) { "Informe data e hora." }
        if (!date.isNullOrEmpty() && !time.isNullOrEmpty()) row.put("scheduledAt", localInstant(date, time).toString()).put("scheduledDate", date).put("scheduledTime", time)
        row.put("status", "pendente").put("completedAt", JSONObject.NULL).put("completedBy", JSONObject.NULL)
            .put("completedTimeDiffMinutes", JSONObject.NULL).put("completionNote", "")
        resetAlarm(row)
    }

    fun duplicateDraft(id: String): JSONObject = synchronized(store) {
        val event = find(read().getJSONObject("data"), "events", id)
        val draft = JSONObject()
        val fields = EVENT_REFERENCES.keys + EVENT_BOOLEAN_DEFAULTS.keys + listOf("description", "notes", "priority", "stylusDrawing", "alarmMinutesBefore", "alarmRepeatInterval", "alarmMaxRepeats")
        fields.forEach { if (event.has(it)) draft.put(it, event.get(it)) }
        val target = now().plusSeconds(30 * 60).atZone(zone)
        copy(draft.put("scheduledDate", target.toLocalDate().toString()).put("scheduledTime", target.toLocalTime().format(DateTimeFormatter.ofPattern("HH:mm"))))
    }

    fun snoozeAlarm(id: String, minutes: Int): JSONObject {
        require(minutes in 1..1440) { "Adiamento deve estar entre 1 e 1440 minutos." }
        return transition(id, "adiamento") { row, _ ->
            require(row.getString("status") == "pendente" && row.getBoolean("hasAlarm")) { "Alarme indisponível." }
            row.put("alarmState", "snoozed").put("alarmSnoozedUntil", now().plusSeconds(minutes * 60L).toEpochMilli())
        }
    }

    fun acknowledgeAlarm(id: String): JSONObject = transition(id, "reconhecimento") { row, _ ->
        require(row.getString("status") == "pendente") { "Evento concluído." }
        row.put("alarmState", "acknowledged").put("alarmSnoozedUntil", JSONObject.NULL)
    }

    fun deleteEvent(id: String) {
        transition(id, "exclusao") { row, _ -> row.put("active", false).put("alarmState", "acknowledged").put("alarmSnoozedUntil", JSONObject.NULL) }
    }

    fun saveSettings(value: JSONObject): JSONObject = mutate { data ->
        val required = listOf("localUserName", "soundEnabled", "soundType", "soundVolume", "visualAlertEnabled", "notificationEnabled", "repeatAlarm", "repeatIntervalMinutes", "maxRepeats", "defaultLeadTimeMinutes")
        require(required.all { value.has(it) && !value.isNull(it) }) { "Configurações obrigatórias ausentes." }
        val merged = defaultSettings()
        value.keys().forEach { merged.put(it, value.get(it)) }
        val old = data.getJSONArray("settings").getJSONObject(0)
        val row = copy(old).put("key", "app_settings").put("value", merged).put("updatedAt", now().toString()).put("version", old.optLong("version", 0) + 1)
        data.put("settings", JSONArray().put(row))
        copy(merged)
    }

    fun saveColorRanges(rows: List<JSONObject>) {
        mutate { data ->
            val prior = arrayRows(data, "colorRanges").associateBy { it.getString("id") }
            val result = rows.map { input ->
                val id = optionalId(input, "id")
                val old = id?.let { prior[it] }
                val values = JSONObject()
                for (key in listOf("name", "color", "minMinutes", "maxMinutes", "priority", "blink", "sound", "active", "unit")) if (input.has(key)) values.put(key, input.get(key))
                if (id != null) values.put("id", id)
                stamp(old, values)
            }
            data.put("colorRanges", JSONArray(result))
        }
    }

    fun saveColorRanges(rows: JSONArray) = saveColorRanges((0 until rows.length()).map { rows.getJSONObject(it) })

    fun dueAlarms(): List<JSONObject> = synchronized(store) {
        val data = read().getJSONObject("data")
        val settings = settingsOf(data)
        val instant = now()
        arrayRows(data, "events").filter { due(it, settings, instant) }.sortedBy { Instant.parse(it.getString("scheduledAt")) }.map(::copy)
    }

    /** Claims an alarm exactly once. Pass no channels until the controller confirms delivery. */
    fun fireAlarm(id: String, channels: List<String>): JSONObject? = synchronized(store) {
        validateChannels(channels)
        val candidate = copy(read())
        val data = candidate.getJSONObject("data")
        val current = arrayRows(data, "events").firstOrNull { it.getString("id") == id } ?: return@synchronized null
        val instant = now()
        if (!due(current, settingsOf(data), instant)) return@synchronized null
        val row = stamp(current, JSONObject().put("alarmState", "triggered").put("lastAlarmTriggeredAt", instant.toString())
            .put("alarmTriggerCount", current.getLong("alarmTriggerCount") + 1).put("alarmSnoozedUntil", JSONObject.NULL))
        putRow(data, "events", row)
        val audit = history(data, row, "disparo_alarme", deliveryDescription(channels), current.toString(), "Sistema de Alarme")
        audit.put("timestamp", instant.toString()).put("channels", JSONArray(channels.distinct()))
        store.save(BackupCodec.validate(candidate))
        copy(row)
    }

    /** Updates only the matching claim's delivery audit; never triggers or changes an event. */
    fun recordAlarmDelivery(id: String, firedAt: String, channels: List<String>) {
        synchronized(store) {
            validateChannels(channels)
            val candidate = copy(read())
            val data = candidate.getJSONObject("data")
            val audit = arrayRows(data, "eventHistory").lastOrNull {
                it.getString("eventId") == id && it.getString("action") == "disparo_alarme" && it.getString("timestamp") == firedAt
            } ?: return@synchronized
            audit.put("channels", JSONArray(channels.distinct())).put("description", deliveryDescription(channels))
            store.save(BackupCodec.validate(candidate))
        }
    }

    fun restore(backup: JSONObject, mode: String, preventiveBackupConfirmed: Boolean = false): MergeResult = synchronized(store) {
        require(mode == "merge" || mode == "replace") { "Modo de importação inválido." }
        require(mode != "replace" || preventiveBackupConfirmed) { "Conclua o backup preventivo antes de substituir os dados." }
        val incoming = BackupCodec.validate(backup)
        val existing = read()
        val result = if (mode == "merge") BackupCodec.merge(existing, incoming)
        else MergeResult(incoming, COLLECTIONS.sumOf { incoming.getJSONObject("data").getJSONArray(it).length() }, 0, 0, emptyList(), true)
        if (result.applied) store.save(BackupCodec.validate(result.snapshot))
        result.copy(snapshot = copy(result.snapshot))
    }

    fun loadDemoData(preventiveBackupConfirmed: Boolean = false) {
        require(preventiveBackupConfirmed) { "Conclua o backup preventivo antes de carregar a demonstração." }
        mutate(fresh = true) { data ->
            val consoles = listOf("C04", "C08", "C10").associateWith { name ->
                val old = arrayRows(data, "consoles").firstOrNull { it.getString("name").equals(name, true) }
                require(old?.optBoolean("active", true) != false) { "Console demonstrativo inativo." }
                old ?: saveMaster(data, "consoles", JSONObject().put("name", name))
            }
            val units = listOf("REFAP", "TEDEP", "REPLAN", "TEBAR").associateWith { saveMaster(data, "operationalUnits", JSONObject().put("name", it)) }
            val pipelines = listOf(
                Triple("OSCAN", "C04", listOf("REFAP", "TEDEP")),
                Triple("OSBRA", "C08", listOf("REPLAN", "TEBAR")),
                Triple("DTCS", "C10", listOf("REPLAN", "TEDEP"))
            ).associate { (name, console, unitNames) ->
                name to saveMaster(data, "pipelines", JSONObject().put("name", name).put("consoleId", consoles.getValue(console).getString("id"))
                    .put("uoIds", JSONArray(unitNames.map { units.getValue(it).getString("id") })))
            }
            val equipment = listOf(
                Triple("Tanque", "REFAP", "TQ-804"), Triple("Bomba", "REFAP", "BB-101A"),
                Triple("Esfera", "REPLAN", "ES-201"), Triple("Válvula de Controle", "TEDEP", "PCV-301")
            ).associate { (name, unit, tag) ->
                val unitId = units.getValue(unit).getString("id")
                val type = saveMaster(data, "equipmentTypes", JSONObject().put("name", name).put("uoId", unitId))
                tag to saveMaster(data, "equipmentTags", JSONObject().put("tag", tag).put("uoId", unitId).put("equipmentTypeId", type.getString("id")))
            }
            for (example in DEMO_EVENTS) {
                val target = now().plusSeconds(example.offset * 60L).atZone(zone)
                val tag = example.tag?.let { equipment.getValue(it) }
                val input = JSONObject().put("consoleId", consoles.getValue(example.console).getString("id"))
                    .put("pipelineId", pipelines.getValue(example.pipeline).getString("id")).put("uoId", units.getValue(example.unit).getString("id"))
                    .put("equipmentTypeId", tag?.getString("equipmentTypeId") ?: JSONObject.NULL).put("tagId", tag?.getString("id") ?: JSONObject.NULL)
                    .put("scheduledDate", target.toLocalDate().toString()).put("scheduledTime", target.toLocalTime().format(DateTimeFormatter.ofPattern("HH:mm")))
                    .put("description", example.description).put("notes", example.notes).put("priority", example.priority).put("hasAlarm", true).put("alarmMinutesBefore", example.lead)
                val event = saveEventIn(data, input)
                if (example.offset == -40) {
                    val completed = stamp(event, JSONObject().put("status", "concluido").put("completedAt", now().toString()).put("completedBy", actor(data))
                        .put("completedTimeDiffMinutes", (now().toEpochMilli() - Instant.parse(event.getString("scheduledAt")).toEpochMilli()) / 60000.0)
                        .put("completionNote", "Manifold aberto e estanqueidade confirmada sem anomalias.").put("alarmState", "acknowledged"))
                    putRow(data, "events", completed)
                    history(data, completed, "conclusao", "Demonstração concluída", event.toString())
                }
            }
        }
    }

    fun clearAllData(preventiveBackupConfirmed: Boolean = false) {
        require(preventiveBackupConfirmed) { "Conclua o backup preventivo antes de limpar os dados." }
        synchronized(store) {
            read() // A damaged live store is never silently reset.
            store.save(BackupCodec.validate(initialSnapshot()))
        }
    }

    private fun due(event: JSONObject, settings: JSONObject, instant: Instant): Boolean {
        if (!event.getBoolean("active") || event.getString("status") != "pendente" || !event.getBoolean("hasAlarm") || event.getString("alarmState") == "acknowledged") return false
        val defaults = event.getBoolean("useDefaultAlarmSettings")
        val lead = if (defaults) settings.getLong("defaultLeadTimeMinutes") else event.getLong("alarmMinutesBefore")
        if (instant.isBefore(Instant.parse(event.getString("scheduledAt")).minusSeconds(lead * 60))) return false
        val snooze = if (event.isNull("alarmSnoozedUntil")) null else event.getLong("alarmSnoozedUntil")
        if (snooze != null && instant.toEpochMilli() < snooze) return false
        if (event.getString("alarmState") == "snoozed" && snooze != null) return true
        if (event.isNull("lastAlarmTriggeredAt")) return true
        val repeat = if (defaults) settings.getBoolean("repeatAlarm") else event.getBoolean("alarmRepeat")
        val limit = if (defaults) settings.getLong("maxRepeats") else event.getLong("alarmMaxRepeats")
        val interval = if (defaults) settings.getLong("repeatIntervalMinutes") else event.getLong("alarmRepeatInterval")
        return repeat && event.getLong("alarmTriggerCount") < 1 + limit &&
            !instant.isBefore(Instant.parse(event.getString("lastAlarmTriggeredAt")).plusSeconds(interval * 60))
    }

    private fun validateChannels(channels: List<String>) {
        require(channels.all { it in setOf("audio", "visual", "notification") }) { "Canal de alarme inválido." }
    }

    private fun deliveryDescription(channels: List<String>) = "Alarme disparado. Canais acionados: ${if (channels.isEmpty()) "nenhum disponível" else channels.distinct().joinToString(", ")}."

    private fun transition(id: String, action: String, block: (JSONObject, JSONObject) -> Unit): JSONObject = mutate { data ->
        val old = find(data, "events", id)
        require(old.optBoolean("active", true)) { "Evento excluído." }
        val previous = old.toString()
        val changed = copy(old)
        block(changed, data)
        val row = stamp(changed, JSONObject())
        putRow(data, "events", row)
        history(data, row, action, action, previous)
        copy(row)
    }

    private fun saveEventIn(data: JSONObject, input: JSONObject): JSONObject {
        val old = optionalId(input, "id")?.let { find(data, "events", it) }
        require(old?.optBoolean("active", true) != false) { "Evento excluído." }
        val fields = JSONObject()
        for ((field, collection) in EVENT_REFERENCES) {
            val id = if (field in listOf("equipmentTypeId", "tagId")) optionalId(input, field) else text(input, field)
            if (id != null) activeRef(data, collection, id, old?.let { optionalId(it, field) })
            fields.put(field, id ?: JSONObject.NULL)
        }
        val date = text(input, "scheduledDate")
        val time = text(input, "scheduledTime")
        // An imported event keeps its source instant on non-scheduling edits.
        val sameLocalSchedule = old != null && old.getString("scheduledDate") == date && old.getString("scheduledTime") == time
        val scheduledAt = if (sameLocalSchedule) old!!.getString("scheduledAt") else localInstant(date, time).toString()
        fields.put("scheduledDate", date).put("scheduledTime", time).put("scheduledAt", scheduledAt)
            .put("description", text(input, "description")).put("notes", input.opt("notes").takeUnless { it == JSONObject.NULL } ?: "")
            .put("priority", input.opt("priority").takeUnless { it == JSONObject.NULL } ?: "Normal")
            .put("stylusDrawing", if (input.has("stylusDrawing")) input.get("stylusDrawing") else old?.opt("stylusDrawing") ?: JSONObject.NULL)
        for ((key, default) in EVENT_BOOLEAN_DEFAULTS) fields.put(key, boolean(input, key, default))
        fields.put("alarmMinutesBefore", integer(input, "alarmMinutesBefore", 0, 525600, 0))
            .put("alarmRepeatInterval", integer(input, "alarmRepeatInterval", 1, 1440, 2))
            .put("alarmMaxRepeats", integer(input, "alarmMaxRepeats", 0, 1000, 5))
        val row = stamp(old, fields)
        if (old == null) {
            row.put("status", "pendente").put("completedAt", JSONObject.NULL).put("completedTimeDiffMinutes", JSONObject.NULL)
                .put("completionNote", "").put("createdBy", actor(data))
            resetAlarm(row)
        } else if (old.getString("scheduledAt") != scheduledAt || old.getBoolean("hasAlarm") != row.getBoolean("hasAlarm")) resetAlarm(row)
        putRow(data, "events", row)
        history(data, row, if (old == null) "criacao" else "edicao", if (old == null) "Previsão criada" else "Evento atualizado", old?.toString())
        return row
    }

    private fun boolean(input: JSONObject, key: String, default: Boolean): Boolean {
        if (!input.has(key)) return default
        val value = input.opt(key)
        require(value is Boolean) { "Booleano inválido: $key." }
        return value
    }

    private fun integer(input: JSONObject, key: String, min: Long, max: Long, default: Long): Long {
        val value = input.opt(key).takeUnless { it == JSONObject.NULL } ?: return default
        val number = when (value) {
            is Number -> value.toDouble()
            is String -> value.toDoubleOrNull()
            else -> null
        }
        require(number != null && number.isFinite() && number >= min && number <= max && number == kotlin.math.floor(number)) { "$key: número inteiro entre $min e $max." }
        return number.toLong()
    }

    private fun localInstant(date: String, time: String): Instant {
        require(Regex("\\d{4}-\\d{2}-\\d{2}").matches(date) && Regex("\\d{2}:\\d{2}").matches(time)) { "Data ou hora inválida." }
        try {
            val local = LocalDateTime.of(LocalDate.parse(date), LocalTime.parse(time))
            val offsets = zone.rules.getValidOffsets(local)
            require(offsets.isNotEmpty()) { "Este horário não existe no fuso selecionado." }
            return local.toInstant(offsets.first())
        } catch (error: DateTimeException) {
            throw IllegalArgumentException("Data ou hora inválida.", error)
        }
    }

    private fun resetAlarm(row: JSONObject) {
        row.put("alarmState", "idle").put("alarmSnoozedUntil", JSONObject.NULL).put("alarmTriggerCount", 0).put("lastAlarmTriggeredAt", JSONObject.NULL)
    }

    private fun actor(data: JSONObject): String = settingsOf(data).getString("localUserName")

    private fun history(data: JSONObject, event: JSONObject, action: String, description: String, previous: String? = null, user: String = actor(data)): JSONObject {
        val record = JSONObject().put("id", UUID.randomUUID().toString()).put("eventId", event.getString("id")).put("action", action)
            .put("description", description).put("timestamp", now().toString()).put("previousValue", previous ?: JSONObject.NULL)
            .put("newValue", event.toString()).put("localUser", user)
        data.getJSONArray("eventHistory").put(record)
        return record
    }

    private fun <T> mutate(fresh: Boolean = false, block: (JSONObject) -> T): T = synchronized(store) {
        val existing = read()
        val candidate = if (fresh) initialSnapshot() else copy(existing)
        val result = block(candidate.getJSONObject("data"))
        store.save(BackupCodec.validate(candidate))
        result
    }

    private fun requireMaster(name: String) {
        require(name in MASTER_STORES) { "Cadastro desconhecido: $name." }
    }

    private fun find(data: JSONObject, collection: String, id: String): JSONObject =
        arrayRows(data, collection).firstOrNull { it.getString("id") == id }
            ?: throw IllegalArgumentException("Registro não encontrado em $collection.")

    private fun text(input: JSONObject, key: String): String {
        val value = input.opt(key)
        require(value is String && value.isNotBlank()) { "Campo obrigatório: $key." }
        return value.trim()
    }

    private fun optionalId(input: JSONObject, key: String): String? {
        if (!input.has(key) || input.isNull(key) || input.opt(key) == "") return null
        return text(input, key)
    }

    private fun activeRef(data: JSONObject, collection: String, id: String, originalId: String?): JSONObject {
        val row = find(data, collection, id)
        require(row.optBoolean("active", true) || id == originalId) { "Não é permitido selecionar cadastro inativo." }
        return row
    }

    private fun putRow(data: JSONObject, collection: String, row: JSONObject) {
        val rows = arrayRows(data, collection).toMutableList()
        val index = rows.indexOfFirst { it.getString("id") == row.getString("id") }
        if (index < 0) rows.add(row) else rows[index] = row
        data.put(collection, JSONArray(rows))
    }

    private fun saveMaster(data: JSONObject, collection: String, input: JSONObject): JSONObject {
        requireMaster(collection)
        val old = optionalId(input, "id")?.let { find(data, collection, it) }
        val label = if (collection == "equipmentTags") "tag" else "name"
        val values = JSONObject().put(label, text(input, label))
        var unitIds = emptyList<String>()
        if (collection == "pipelines") {
            val consoleId = text(input, "consoleId")
            activeRef(data, "consoles", consoleId, old?.optString("consoleId"))
            values.put("consoleId", consoleId)
            val ids = input.opt("uoIds") as? JSONArray ?: throw IllegalArgumentException("Duto exige duas UOs distintas.")
            unitIds = (0 until ids.length()).map { index ->
                val id = ids.opt(index)
                require(id is String && id.isNotBlank()) { "UO inválida." }
                id
            }
            require(unitIds.size >= 2 && unitIds.distinct().size == unitIds.size) { "Duto exige duas UOs distintas." }
            val originals = arrayRows(data, "pipelineOperationalUnits").filter { old != null && it.getString("pipelineId") == old.getString("id") }.map { it.getString("uoId") }
            unitIds.forEach { activeRef(data, "operationalUnits", it, it.takeIf { id -> id in originals }) }
        }
        if (collection == "equipmentTypes" || collection == "equipmentTags") {
            val unitId = text(input, "uoId")
            activeRef(data, "operationalUnits", unitId, old?.optString("uoId"))
            values.put("uoId", unitId)
        }
        if (collection == "equipmentTags") {
            val typeId = text(input, "equipmentTypeId")
            activeRef(data, "equipmentTypes", typeId, old?.optString("equipmentTypeId"))
            values.put("equipmentTypeId", typeId)
        }
        val row = stamp(old, values)
        putRow(data, collection, row)
        if (collection == "pipelines") {
            val prior = arrayRows(data, "pipelineOperationalUnits").filter { it.getString("pipelineId") == row.getString("id") }
            val links = arrayRows(data, "pipelineOperationalUnits").filterNot { it.getString("pipelineId") == row.getString("id") }.toMutableList()
            unitIds.forEach { id ->
                links.add(prior.firstOrNull { it.getString("uoId") == id } ?: JSONObject().put("id", UUID.randomUUID().toString())
                    .put("pipelineId", row.getString("id")).put("uoId", id).put("createdAt", now().toString()).put("version", 1).put("synchronizationStatus", "local-only"))
            }
            data.put("pipelineOperationalUnits", JSONArray(links))
        }
        return row
    }

    private fun read(): JSONObject = BackupCodec.validate(requireNotNull(store.load()) { "Base indisponível; os dados não foram reinicializados." })

    private fun initialSnapshot(): JSONObject {
        val data = JSONObject()
        COLLECTIONS.forEach { data.put(it, JSONArray()) }
        val consoles = INITIAL_CONSOLES.map { stamp(null, JSONObject().put("name", it)) }
        data.put("consoles", JSONArray(consoles))
        val ranges = faixasPadrao().mapIndexed { index, f ->
            JSONObject().put("id", RANGE_IDS[index]).put("name", f.nome).put("color", f.cor)
                .put("minMinutes", f.minimoMinutos).put("maxMinutes", f.maximoMinutos)
                .put("unit", "min").put("priority", f.prioridade).put("blink", f.pisca).put("sound", f.som).put("active", true)
        }
        data.put("colorRanges", JSONArray(ranges))
        val settings = defaultSettings().put("activeConsoleId", consoles.first { it.getString("name") == "C04" }.getString("id"))
        data.put("settings", JSONArray().put(JSONObject().put("key", "app_settings").put("value", settings)))
        return JSONObject().put("application", "Controle de Previsões em Dutos").put("schemaVersion", 1).put("exportedAt", now().toString()).put("data", data)
    }

    private fun stamp(old: JSONObject?, values: JSONObject): JSONObject {
        val row = old?.let(::copy) ?: JSONObject().put("id", UUID.randomUUID().toString()).put("active", true)
            .put("createdAt", now().toString()).put("synchronizationStatus", "local-only")
        values.keys().forEach { row.put(it, values.get(it)) }
        return row.put("updatedAt", now().toString()).put("version", (old?.optLong("version", 0) ?: 0) + 1)
    }

    private fun settingsOf(data: JSONObject): JSONObject {
        val result = defaultSettings()
        val stored = arrayRows(data, "settings").first { it.getString("key") == "app_settings" }.getJSONObject("value")
        stored.keys().forEach { result.put(it, stored.get(it)) }
        return copy(result)
    }

    private fun arrayRows(data: JSONObject, name: String): List<JSONObject> {
        val array = data.getJSONArray(name)
        return (0 until array.length()).map { array.getJSONObject(it) }
    }

    private fun copy(value: JSONObject) = JSONObject(value.toString())

    private data class DemoEvent(val offset: Int, val console: String, val pipeline: String, val unit: String, val tag: String?, val description: String, val notes: String, val priority: String, val lead: Int)

    companion object {
        private val DEMO_EVENTS = listOf(
            DemoEvent(-12, "C04", "OSCAN", "REFAP", "BB-101A", "Verificar alinhamento e término de partida da bomba BB-101A", "Confirmar pressão de sucção e vazão nominal.", "Crítica", 15),
            DemoEvent(8, "C04", "OSCAN", "REFAP", "TQ-804", "Verificar o término do recebimento de MGO no TQ-804", "Monitorar nível máximo seguro de 85% e preparar fechamento de válvula.", "Alta", 15),
            DemoEvent(22, "C08", "OSBRA", "REPLAN", "ES-201", "Acompanhar transferência de GLP para a esfera ES-201", "Vazão prevista de 180 m³/h.", "Normal", 15),
            DemoEvent(50, "C10", "DTCS", "TEDEP", "PCV-301", "Ajuste de controle de contrapressão na PCV-301", "Ajuste fino de setpoint para amortecimento de transiente.", "Normal", 15),
            DemoEvent(150, "C04", "OSCAN", "TEDEP", null, "Chegada estimada de PIG raspador no recebedor de TEDEP", "Aviso prévio à equipe de manutenção para abertura de câmara.", "Baixa", 30),
            DemoEvent(-40, "C08", "OSBRA", "TEBAR", null, "Abertura de manifold de recebimento de Diesel S10", "Operação concluída conforme procedimento operacional padrão.", "Normal", 15)
        )
        val COLLECTIONS = listOf("consoles", "pipelines", "operationalUnits", "pipelineOperationalUnits", "equipmentTypes", "equipmentTags", "events", "eventHistory", "colorRanges", "settings")
        private val EVENT_REFERENCES = linkedMapOf("consoleId" to "consoles", "pipelineId" to "pipelines", "uoId" to "operationalUnits", "equipmentTypeId" to "equipmentTypes", "tagId" to "equipmentTags")
        private val EVENT_BOOLEAN_DEFAULTS = linkedMapOf("hasAlarm" to false, "useDefaultAlarmSettings" to false, "alarmAudio" to true, "alarmVisual" to true, "alarmNotification" to false, "alarmRepeat" to false)
        private val MASTER_STORES = setOf("consoles", "pipelines", "operationalUnits", "equipmentTypes", "equipmentTags")
        private val INITIAL_CONSOLES = listOf("C02", "C03", "C04", "C05", "C06", "C07", "C08", "C10", "C11", "C14", "C15", "C16")
        private val RANGE_IDS = listOf("range_critico", "range_urgente", "range_atencao", "range_monitor", "range_normal")
        private fun defaultSettings() = JSONObject("""{"localUserName":"Usuário local","soundEnabled":true,"soundType":"chime","soundVolume":80,"visualAlertEnabled":true,"highlightCardEnabled":true,"pulsingEnabled":true,"changeTitleEnabled":true,"notificationEnabled":false,"repeatAlarm":true,"repeatIntervalMinutes":2,"maxRepeats":5,"defaultLeadTimeMinutes":15,"theme":"dark","viewMode":"cards","responsiveLayoutMode":"auto","backupReminderDays":7,"firstMobileNoticeShown":false,"lastBackupAt":null,"activeConsoleId":null,"keepDutoUOPrefilled":true}""")
    }
}
