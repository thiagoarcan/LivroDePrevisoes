package br.com.livrodeprevisoes.app

import android.app.DatePickerDialog
import android.app.TimePickerDialog
import android.graphics.Color
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.LinearLayout
import org.json.JSONObject
import java.time.*
import java.time.format.DateTimeFormatter

fun MainActivity.consoleFilter(parent: LinearLayout, onChange: () -> Unit) {
    val choose = picker(parent, "Console", listOf(Choice("", "Todos os consoles")) + options("consoles"), activeConsole)
    choose.onChange { value -> if (activeConsole != value) {
        activeConsole = value
        safe { service.saveSettings(service.settings().put("activeConsoleId", value.ifBlank { null })); onChange() }
    } }
}
fun MainActivity.pendingEvents() = filterEvents(rows("events"), "pendente", activeConsole, "", "", ::hierarchy)
fun MainActivity.eventStatus(e: JSONObject): Pair<String, Int> {
    if (e.optString("status") == "concluido") return "Concluído" to palette.focus
    val minutes = try { Duration.between(Instant.now(), Instant.parse(e.getString("scheduledAt"))).toMinutes() } catch (_: Exception) { 0L }
    if (deadlineIsLate(e.optString("scheduledAt"))) return "Atrasado · ${(-minutes).coerceAtLeast(0)} min" to palette.danger
    val ranges = rows("colorRanges").filter { it.optBoolean("active", true) }.sortedBy { it.optLong("minMinutes") }
    val range = ranges.firstOrNull { minutes >= it.optLong("minMinutes") && minutes < it.optLong("maxMinutes") } ?: ranges.lastOrNull()
    val color = try { Color.parseColor(range?.optString("color")) } catch (_: Exception) { palette.focus }
    return "${range?.optString("name") ?: "Previsto"} · em $minutes min" to color
}
fun MainActivity.dashboard() {
    heading(page, "Painel operacional", "Prazos, próximos eventos e ações do turno.")
    consoleFilter(page) { render() }
    space(page)
    val pending = pendingEvents()
    val late = pending.count { runCatching { Instant.parse(it.getString("scheduledAt")).isBefore(Instant.now()) }.getOrDefault(false) }
    val alarms = pending.count { it.optString("alarmState") == "triggered" }
    val done = filterEvents(rows("events"), "concluido", activeConsole, "", "", ::hierarchy).size
    val metrics = row(page)
    listOf(pending.size to "Pendentes", late to "Atrasados", done to "Concluídos", alarms to "Alarmes").forEach { (count, name) ->
        val box = column(padding = 10).apply { background = shape(); metrics.addView(this, LinearLayout.LayoutParams(0, -2, 1f).apply { marginEnd = dp(6) }) }
        val countLabel = label(box, count.toString(), 29f, true)
        if (name == "Atrasados") watchClock(countLabel) { countLabel.text = pending.count { deadlineIsLate(it.optString("scheduledAt")) }.toString() }
        label(box, name, 12f, muted = true)
    }
    if (alarms > 0) button(page, "Reconhecer $alarms alarmes do console") {
        confirm("Reconhecer todos os alarmes exibidos?", "As previsões continuarão pendentes. Esta ação será registrada no histórico.", "Reconhecer") {
            pending.filter { it.optString("alarmState") == "triggered" }.forEach { service.acknowledgeAlarm(it.getString("id")) }; render()
        }
    }
    space(page, 20)
    if (pending.isEmpty()) {
        val empty = card(page); label(empty, "Nenhuma previsão pendente", 19f, true)
        label(empty, "Cadastre a hierarquia operacional e programe sua primeira atividade. Dados de exemplo só são carregados com sua confirmação.", muted = true)
        button(empty, "Criar previsão", true) { navigate("new") }
        button(empty, "Abrir cadastros") { navigate("registry") }
    } else {
        label(page, "PRÓXIMO EVENTO", 12f, true, true); space(page, 8)
        eventCard(page, pending.first(), true)
        if (pending.size > 1) { label(page, "Na sequência", 18f, true); space(page, 10); pending.drop(1).take(4).forEach { eventCard(page, it) } }
        button(page, "Ver todas as ${pending.size} pendentes") { navigate("pending") }
    }
    val note = card(page); label(note, "Monitoramento em primeiro plano", 14f, true)
    label(note, "Alertas funcionam com este aplicativo aberto e ativo. Ao sair, o monitoramento é pausado. Faça backups em Backup.", 13f, muted = true)
    if (backupIsDue(service.settings())) {
        space(note); label(note, "Backup pendente de atualização", 14f, true)
        button(note, "Salvar uma cópia de segurança") { navigate("backup") }
    }
}
fun MainActivity.eventCard(parent: LinearLayout, e: JSONObject, featured: Boolean = false) {
    val box = card(parent)
    liveStatus(box, e)
    space(box, 6); label(box, e.optString("description"), if (featured) 22f else 18f, true)
    space(box, 6); label(box, formatted(e.optString("scheduledAt")), 15f, true)
    label(box, hierarchy(e), 13f, muted = true)
    if (e.optString("status") == "concluido") {
        label(box, "Concluído: ${formatted(e.optString("completedAt"))}", 13f, muted = true)
        val diff = runCatching { Duration.between(Instant.parse(e.getString("scheduledAt")), Instant.parse(e.getString("completedAt"))).toMinutes() }.getOrNull()
        if (diff != null) label(box, "Real − previsto: ${if (diff > 0) "+" else ""}$diff min", 13f, muted = true)
    }
    label(box, "Prioridade: ${e.optString("priority", "Normal")}" + if (e.optBoolean("hasAlarm")) "  •  Alarme" else "", 12f, muted = true)
    button(box, "Detalhes e ações", featured) { detailId = e.getString("id"); screen = if (e.optString("status") == "concluido") "completed" else "pending"; render() }
}
fun MainActivity.eventList(completed: Boolean) {
    heading(page, if (completed) "Concluídos" else "Pendentes", if (completed) "Registros, diferença de horário e histórico." else "Busque por atividade, notas, duto, UO ou TAG.")
    val controls = card(page)
    val search = input(controls, "Buscar", listQuery)
    val priorities = picker(controls, "Prioridade", listOf(Choice("", "Todas")) + listOf("Baixa", "Normal", "Alta", "Crítica", "Urgente").map { Choice(it, it) }, listPriority)
    val console = picker(controls, "Console", listOf(Choice("", "Todos os consoles")) + options("consoles"), activeConsole)
    val results = column(page)
    fun fill() {
        forgetClockChildren(results)
        results.removeAllViews()
        val matching = filterEvents(rows("events"), if (completed) "concluido" else "pendente", activeConsole, listQuery, listPriority, ::hierarchy, listFilters)
        val bounds = pageBounds(matching.size, listPage)
        listPage = bounds.page
        label(results, "${matching.size} registros", 13f, true, true)
        fun pager() {
            space(results, 10)
            label(results, "Exibindo ${if (bounds.total == 0) 0 else bounds.start + 1}–${bounds.endExclusive} de ${bounds.total}", 13f, true, true)
            val navigation = row(results)
            fun pageButton(title: String, enabled: Boolean, target: Int, trailingMargin: Int) {
                val control = button(navigation, title) {
                    listPage = target
                    fill()
                    results.post { results.requestRectangleOnScreen(android.graphics.Rect(0, 0, results.width, dp(72)), false) }
                }
                control.layoutParams = LinearLayout.LayoutParams(0, -2, 1f).apply { topMargin = dp(8); marginEnd = dp(trailingMargin) }
                control.isEnabled = enabled
                control.alpha = if (enabled) 1f else .45f
            }
            pageButton("Anterior", bounds.page > 0, bounds.page - 1, 6)
            pageButton("Próxima", bounds.endExclusive < bounds.total, bounds.page + 1, 0)
            space(results, 12)
        }
        pager()
        if (matching.isEmpty()) label(results, "Nenhum registro corresponde a estes filtros.", muted = true)
        matching.subList(bounds.start, bounds.endExclusive).forEach { eventCard(results, it) }
        if (matching.isNotEmpty()) pager()
    }
    val advanced = column(controls).apply { visibility = View.GONE }
    button(controls, "Mostrar / ocultar filtros avançados") { advanced.visibility = if (advanced.visibility == View.VISIBLE) View.GONE else View.VISIBLE }
    val all = listOf(Choice("", "Todos"))
    val pipelineFilter = picker(advanced, "Duto", all + options("pipelines"), listFilters.pipeline)
    val unitFilter = picker(advanced, "UO", all + options("operationalUnits"), listFilters.unit)
    val equipmentFilter = picker(advanced, "Tipo de equipamento", all + options("equipmentTypes"), listFilters.equipment)
    val tagFilter = picker(advanced, "TAG", all + options("equipmentTags"), listFilters.tag)
    val dateFrom = input(advanced, "Data prevista de (AAAA-MM-DD)", listFilters.dateFrom)
    val dateTo = input(advanced, "Data prevista até (AAAA-MM-DD)", listFilters.dateTo)
    val alarmFilter = picker(advanced, "Presença de alarme", all + listOf(Choice("on", "Com alarme"), Choice("off", "Sem alarme")), listFilters.alarm)
    val alarmState = picker(advanced, "Situação do alarme", all + listOf(Choice("idle", "Aguardando"), Choice("triggered", "Disparado"), Choice("snoozed", "Adiado"), Choice("acknowledged", "Reconhecido")), listFilters.alarmState)
    val window = picker(advanced, "Prazo", all + listOf(Choice("overdue", "Atrasados"), Choice("15", "Próximos 15 minutos"), Choice("30", "Próximos 30 minutos"), Choice("60", "Próximos 60 minutos")), listFilters.window)
    button(advanced, "Aplicar filtros", true) {
        val from = dateFrom.text.toString().trim(); val to = dateTo.text.toString().trim()
        if (from.isNotBlank()) LocalDate.parse(from)
        if (to.isNotBlank()) LocalDate.parse(to)
        require(from.isBlank() || to.isBlank() || from <= to) { "A data inicial deve ser anterior ou igual à final." }
        listFilters = EventFilters(pipelineFilter.value, unitFilter.value, equipmentFilter.value, tagFilter.value, from, to, alarmFilter.value, alarmState.value, window.value)
        listPage = 0
        fill()
    }
    button(advanced, "Limpar todos os filtros") { listFilters = EventFilters(); listQuery = ""; listPriority = ""; listPage = 0; activeConsole = ""; render() }
    search.addTextChangedListener(object : TextWatcher {
        override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
        override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) { listQuery = s.toString(); listPage = 0; fill() }
        override fun afterTextChanged(s: Editable?) {}
    })
    priorities.onChange { if (listPriority != it) { listPriority = it; listPage = 0; fill() } }
    console.onChange { if (activeConsole != it) { activeConsole = it; listPage = 0; fill() } }
    mutationRefresh = { fill() }
    fill()
}
fun MainActivity.eventDetails(id: String) {
    val e = rows("events").firstOrNull { it.optString("id") == id } ?: return
    heading(page, "Detalhes da previsão", hierarchy(e))
    val box = card(page)
    liveStatus(box, e)
    label(box, e.optString("description"), 22f, true)
    space(box); label(box, "Previsto neste aparelho: ${formatted(e.optString("scheduledAt"))}")
    label(box, "Data/hora registrada: ${e.optString("scheduledDate")} ${e.optString("scheduledTime")}", 13f, muted = true)
    label(box, "Instante: ${e.optString("scheduledAt")}", 12f, muted = true)
    if (e.optString("status") == "concluido") {
        label(box, "Concluído: ${formatted(e.optString("completedAt"))}", 13f, muted = true)
        val diff = runCatching { Duration.between(Instant.parse(e.getString("scheduledAt")), Instant.parse(e.getString("completedAt"))).toMinutes() }.getOrNull()
        if (diff != null) label(box, "Real − previsto: ${if (diff > 0) "+" else ""}$diff min", 13f, muted = true)
    }
    label(box, "Prioridade: ${e.optString("priority", "Normal")}")
    if (e.optString("notes").isNotBlank()) { space(box); label(box, "Notas", 13f, true); label(box, e.optString("notes")) }
    val alarmStateLabel = when (e.optString("alarmState")) {
        "triggered" -> "disparado"
        "snoozed" -> "adiado até ${formatted(e.optString("alarmSnoozedUntil"))}"
        "acknowledged" -> "reconhecido"
        else -> "aguardando"
    }
    label(box, if (e.optBoolean("hasAlarm")) "Alarme: $alarmStateLabel" else "Sem alarme", 13f, muted = true)
    if (e.optBoolean("hasAlarm")) label(box, "Configuração: ${if (e.optBoolean("useDefaultAlarmSettings", true)) "padrão" else "personalizada"} • Disparos: ${e.optInt("alarmTriggerCount")}", 13f, muted = true)
    val drawing = e.optString("stylusDrawing")
    if (drawing.isNotBlank() && drawing != "null") { space(box); box.addView(DrawingView(this, drawing, false), LinearLayout.LayoutParams(-1, dp(220))) }
    if (e.optString("status") == "concluido") {
        label(box, "Concluído: ${formatted(e.optString("completedAt"))}")
        if (e.optString("completionNote").isNotBlank()) { label(box, "Nota de conclusão", 13f, true); label(box, e.optString("completionNote")) }
        val difference = runCatching { Duration.between(Instant.parse(e.getString("scheduledAt")), Instant.parse(e.getString("completedAt"))).toMinutes() }.getOrNull()
        if (difference != null) label(box, "Diferença real − prevista: ${if (difference > 0) "+" else ""}$difference min")
        button(box, "Reabrir com novo horário") { reopenDialog(e) }
    } else {
        button(box, "Concluir atividade", true) { completionDialog(e) }
        button(box, "Editar previsão") { navigate("new", JSONObject(e.toString())) }
        if (e.optBoolean("hasAlarm")) {
            button(box, "Reconhecer alarme") { confirm("Reconhecer alarme?", "A previsão continuará pendente.", "Reconhecer") { service.acknowledgeAlarm(id); notice("Alarme reconhecido"); render() } }
            button(box, "Adiar alarme") {
                formDialog("Adiar alarme") { form ->
                    val minutes = input(form, "Adiar por quantos minutos?", "10", numeric = true)
                    val save: () -> Unit = { service.snoozeAlarm(id, minutes.text.toString().toInt()); render() }; save
                }
            }
        }
    }
    button(box, "Duplicar como nova previsão") { navigate("new", service.duplicateDraft(id)) }
    button(box, "Excluir previsão", danger = true) { confirm("Excluir previsão?", "A previsão será inativada. O histórico será preservado.", "Excluir") { service.deleteEvent(id); detailId = null; render() } }
    val history = card(page); label(history, "Histórico de auditoria", 18f, true)
    val rows = sortHistory(rows("eventHistory").filter { it.optString("eventId") == id })
    if (rows.isEmpty()) label(history, "Sem movimentações registradas.", muted = true)
    rows.forEach { h ->
        space(history, 12)
        label(history, h.optString("action", "Movimentação"), 14f, true)
        label(history, formatted(h.optString("timestamp", h.optString("createdAt"))) + " • " + h.optString("localUser", "Usuário local"), 12f, muted = true)
        label(history, h.optString("details", h.optString("description", h.optString("notes"))), 14f)
    }
    button(page, "Voltar à lista") { detailId = null; render() }
}
fun MainActivity.completionDialog(e: JSONObject) {
    formDialog("Concluir atividade") { form ->
        label(form, "Será registrado o horário atual deste aparelho.", muted = true)
        val note = input(form, "Nota de conclusão (opcional)", multiline = true)
        val save: () -> Unit = { service.completeEvent(e.getString("id"), note.text.toString()); notice("Atividade concluída"); detailId = null; screen = "completed"; render() }; save
    }
}
fun MainActivity.reopenDialog(e: JSONObject) {
    formDialog("Reabrir previsão") { form ->
        val schedule = LocalDateTime.now().plusMinutes(30)
        val date = input(form, "Nova data (AAAA-MM-DD)", schedule.toLocalDate().toString())
        val time = input(form, "Novo horário (HH:mm)", schedule.toLocalTime().format(DateTimeFormatter.ofPattern("HH:mm")))
        val save: () -> Unit = { service.reopenEvent(e.getString("id"), date.text.toString(), time.text.toString()); screen = "pending"; detailId = e.getString("id"); render() }; save
    }
}

fun MainActivity.liveStatus(parent: LinearLayout, event: JSONObject) {
    val statusLabel = label(parent, "", 13f, true)
    statusLabel.setPadding(dp(8), dp(5), dp(8), dp(5))
    watchClock(statusLabel) {
        val (title, color) = eventStatus(event)
        if (statusLabel.text.toString() != title) {
            statusLabel.text = title
            statusLabel.background = shape(color, 6)
            fun linear(component: Int): Double { val n = component / 255.0; return if (n <= .04045) n / 12.92 else Math.pow((n + .055) / 1.055, 2.4) }
            val luminance = .2126 * linear(Color.red(color)) + .7152 * linear(Color.green(color)) + .0722 * linear(Color.blue(color))
            statusLabel.setTextColor(if (luminance > .179) Color.BLACK else Color.WHITE)
        }
    }
}
