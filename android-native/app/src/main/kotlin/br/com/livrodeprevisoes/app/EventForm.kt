package br.com.livrodeprevisoes.app

import android.app.DatePickerDialog
import android.app.TimePickerDialog
import android.view.View
import android.widget.LinearLayout
import org.json.JSONObject
import java.time.*
import java.time.format.DateTimeFormatter

fun MainActivity.eventForm(initial: JSONObject) {
    val editing = initial.optString("id").isNotBlank()
    heading(page, if (editing) "Editar previsão" else "Nova previsão", "Campos obrigatórios marcados com *. Horários usam o fuso ${ZoneId.systemDefault().id}.")
    val hierarchyBox = card(page)
    label(hierarchyBox, "01  Contexto operacional", 18f, true)
    val selectors = column(hierarchyBox)
    var consoleId = initial.optString("consoleId", activeConsole).takeUnless { it == "null" }.orEmpty()
    var pipelineId = initial.optString("pipelineId")
    var uoId = initial.optString("uoId")
    var typeId = initial.optString("equipmentTypeId").takeUnless { it == "null" }.orEmpty()
    var tagId = initial.optString("tagId").takeUnless { it == "null" }.orEmpty()
    fun original(field: String) = if (editing) setOf(initial.optString(field)) else emptySet()
    fun rebuild() {
        selectors.removeAllViews()
        val consoleOptions = options("consoles", original("consoleId"))
        val pipelineOptions = options("pipelines", original("pipelineId")) { it.optString("consoleId") == consoleId }
        val linkedUos = rows("pipelineOperationalUnits").filter { it.optString("pipelineId") == pipelineId && it.optBoolean("active", true) }.map { it.optString("uoId") }.toSet()
        val uoOptions = options("operationalUnits", original("uoId")) { it.optString("id") in linkedUos }
        val types = options("equipmentTypes", original("equipmentTypeId")) { it.optString("uoId") == uoId }
        val tags = options("equipmentTags", original("tagId")) { it.optString("uoId") == uoId && it.optString("equipmentTypeId") == typeId }
        val c = picker(selectors, "Console *", listOf(Choice("", "Selecione o console")) + consoleOptions, consoleId)
        val p = picker(selectors, "Duto *", listOf(Choice("", "Selecione o duto")) + pipelineOptions, pipelineId)
        val u = picker(selectors, "Unidade operacional *", listOf(Choice("", "Selecione a UO")) + uoOptions, uoId)
        val t = picker(selectors, "Tipo de equipamento", listOf(Choice("", "Geral da UO")) + types, typeId)
        val tag = picker(selectors, "TAG", listOf(Choice("", "Sem TAG")) + tags, tagId)
        c.onChange { if (it != consoleId) { consoleId = it; pipelineId = ""; uoId = ""; typeId = ""; tagId = ""; rebuild() } }
        p.onChange { if (it != pipelineId) { pipelineId = it; uoId = ""; typeId = ""; tagId = ""; rebuild() } }
        u.onChange { if (it != uoId) { uoId = it; typeId = ""; tagId = ""; rebuild() } }
        t.onChange { if (it != typeId) { typeId = it; tagId = ""; rebuild() } }
        tag.onChange { tagId = it }
    }
    rebuild()
    label(hierarchyBox, "Não encontrou um item? Salve seus cadastros antes de iniciar esta previsão. Dutos precisam de ao menos duas UOs vinculadas.", 12f, muted = true)
    val content = card(page)
    label(content, "02  Atividade e prazo", 18f, true)
    val now = LocalDateTime.now().plusMinutes(30)
    val date = input(content, "Data * (AAAA-MM-DD)", initial.optString("scheduledDate", now.toLocalDate().toString()))
    button(content, "Selecionar data") {
        val parsed = runCatching { LocalDate.parse(date.text.toString()) }.getOrDefault(now.toLocalDate())
        DatePickerDialog(this, { _, year, month, day -> date.setText(LocalDate.of(year, month + 1, day).toString()) }, parsed.year, parsed.monthValue - 1, parsed.dayOfMonth).show()
    }
    val time = input(content, "Horário * (HH:mm)", initial.optString("scheduledTime", now.toLocalTime().format(DateTimeFormatter.ofPattern("HH:mm"))))
    button(content, "Selecionar horário") {
        val parsed = runCatching { LocalTime.parse(time.text.toString()) }.getOrDefault(now.toLocalTime())
        TimePickerDialog(this, { _, hour, minute -> time.setText(String.format(java.util.Locale.ROOT, "%02d:%02d", hour, minute)) }, parsed.hour, parsed.minute, true).show()
    }
    val description = input(content, "Descrição da atividade *", initial.optString("description"), multiline = true)
    val priority = picker(content, "Prioridade", listOf("Baixa", "Normal", "Alta", "Crítica", "Urgente").map { Choice(it, it) }, initial.optString("priority", "Normal"))
    val notes = input(content, "Notas complementares", initial.optString("notes"), multiline = true)
    val alarmBox = card(page)
    label(alarmBox, "03  Alarme", 18f, true)
    label(alarmBox, "Monitoramento apenas com o app aberto e ativo.", 13f, muted = true)
    val enabled = toggle(alarmBox, "Habilitar alarme desta previsão", initial.optBoolean("hasAlarm", true))
    val default = toggle(alarmBox, "Usar configurações padrão", initial.optBoolean("useDefaultAlarmSettings", true))
    val custom = column(alarmBox)
    val settings = service.settings()
    val lead = input(custom, "Antecedência (minutos)", initial.optInt("alarmMinutesBefore", settings.optInt("defaultLeadTimeMinutes", 15)).toString(), numeric = true)
    val audio = toggle(custom, "Tocar som", initial.optBoolean("alarmAudio", true))
    val visual = toggle(custom, "Abrir alerta visual", initial.optBoolean("alarmVisual", true))
    val notification = toggle(custom, "Notificação Android", initial.optBoolean("alarmNotification", false))
    val repeat = toggle(custom, "Repetir até reconhecer", initial.optBoolean("alarmRepeat", true))
    val interval = input(custom, "Intervalo da repetição (minutos)", initial.optInt("alarmRepeatInterval", 2).toString(), numeric = true)
    val max = input(custom, "Máximo de repetições adicionais", initial.optInt("alarmMaxRepeats", 5).toString(), numeric = true)
    fun showAlarmOptions() { default.visibility = if (enabled.isChecked) View.VISIBLE else View.GONE; custom.visibility = if (enabled.isChecked && !default.isChecked) View.VISIBLE else View.GONE }
    enabled.setOnCheckedChangeListener { _, _ -> showAlarmOptions() }; default.setOnCheckedChangeListener { _, _ -> showAlarmOptions() }; showAlarmOptions()
    val drawingBox = card(page)
    label(drawingBox, "04  Anotação à mão", 18f, true)
    label(drawingBox, "Opcional. Desenhe com o dedo ou caneta. O PNG acompanha o backup.", 13f, muted = true)
    space(drawingBox)
    val drawing = DrawingView(this, initial.optString("stylusDrawing"))
    drawingBox.addView(drawing, LinearLayout.LayoutParams(-1, dp(220)))
    button(drawingBox, "Desfazer último traço") { drawing.undo() }
    button(drawingBox, "Limpar desenho") { confirm("Limpar desenho?", "Você pode desfazer esta limpeza antes de salvar.", "Limpar") { drawing.clear() } }
    val reader: () -> JSONObject = {
        JSONObject(initial.toString()).apply {
            put("consoleId", consoleId); put("pipelineId", pipelineId); put("uoId", uoId)
            put("equipmentTypeId", typeId.ifBlank { null }); put("tagId", tagId.ifBlank { null })
            put("scheduledDate", date.text.toString().trim()); put("scheduledTime", time.text.toString().trim())
            put("description", description.text.toString()); put("notes", notes.text.toString()); put("priority", priority.value)
            put("hasAlarm", enabled.isChecked); put("useDefaultAlarmSettings", default.isChecked)
            put("alarmMinutesBefore", lead.text.toString().toIntOrNull() ?: -1)
            put("alarmAudio", audio.isChecked); put("alarmVisual", visual.isChecked); put("alarmNotification", notification.isChecked)
            put("alarmRepeat", repeat.isChecked); put("alarmRepeatInterval", interval.text.toString().toIntOrNull() ?: -1)
            put("alarmMaxRepeats", max.text.toString().toIntOrNull() ?: -1)
            put("stylusDrawing", drawing.png())
        }
    }
    draftReader = reader
    draftBaseline = if (restoredDraft) null else reader().toString()
    button(page, if (editing) "Salvar alterações" else "Salvar previsão", true) {
        service.saveEvent(reader())
        draftReader = null; draftBaseline = null; draft = null; draftFile.delete()
        notice("Previsão salva neste aparelho"); screen = "pending"; detailId = null; render()
    }
    button(page, "Cancelar") { navigate("dashboard") }
    space(page, 16)
}
