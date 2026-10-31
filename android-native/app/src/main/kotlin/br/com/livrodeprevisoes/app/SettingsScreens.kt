package br.com.livrodeprevisoes.app

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import org.json.JSONObject
import java.time.Instant
import java.time.ZoneId
import java.util.UUID

fun MainActivity.alertSettings() {
    heading(page, "Alertas", "Preferências locais de som, aviso visual e notificação Android.")
    val scope = card(page)
    label(scope, "Somente com o app aberto e ativo", 18f, true)
    label(scope, "O monitoramento pausa ao sair ou bloquear a tela. Ao retornar, prazos vencidos são reavaliados. Não use este app como único mecanismo de segurança operacional.", muted = true)
    label(scope, "Notificações: ${alerts?.permissionState() ?: "Indisponível"}", 14f, true)
    button(scope, "Permitir notificações Android") { alerts?.requestPermission() }
    val settings = service.settings()
    val identity = card(page); label(identity, "Identificação do operador", 18f, true)
    val actor = input(identity, "Nome no histórico", settings.optString("localUserName", "Usuário local"))
    val sound = card(page); label(sound, "Som e apresentação", 18f, true)
    val enabled = toggle(sound, "Habilitar som", settings.optBoolean("soundEnabled", true))
    val type = picker(sound, "Sinal sonoro", listOf(Choice("chime", "Campainha"), Choice("beep", "Bipe"), Choice("siren", "Sirene"), Choice("blip", "Pulso")), settings.optString("soundType", "chime"))
    val volume = input(sound, "Volume (0 a 100)", settings.optInt("soundVolume", 80).toString(), numeric = true)
    val visual = toggle(sound, "Mostrar diálogo de alarme", settings.optBoolean("visualAlertEnabled", true))
    val notification = toggle(sound, "Enviar notificação Android", settings.optBoolean("notificationEnabled", false))
    val timings = card(page); label(timings, "Tempos padrão", 18f, true)
    val lead = input(timings, "Antecedência (minutos)", settings.optInt("defaultLeadTimeMinutes", 15).toString(), numeric = true)
    val repeat = toggle(timings, "Repetir até reconhecer", settings.optBoolean("repeatAlarm", true))
    val interval = input(timings, "Intervalo (minutos)", settings.optInt("repeatIntervalMinutes", 2).toString(), numeric = true)
    val max = input(timings, "Máximo de repetições adicionais", settings.optInt("maxRepeats", 5).toString(), numeric = true)
    label(timings, "Zero repetições significa um disparo inicial, sem repetição. Reconhecer ou concluir interrompe novos disparos.", 13f, muted = true)
    button(page, "Salvar configurações", true) {
        service.saveSettings(service.settings().apply {
            put("localUserName", actor.text.toString()); put("soundEnabled", enabled.isChecked); put("soundType", type.value)
            put("soundVolume", volume.text.toString().toInt()); put("visualAlertEnabled", visual.isChecked); put("notificationEnabled", notification.isChecked)
            put("defaultLeadTimeMinutes", lead.text.toString().toInt()); put("repeatAlarm", repeat.isChecked)
            put("repeatIntervalMinutes", interval.text.toString().toInt()); put("maxRepeats", max.text.toString().toInt())
        })
        notice("Configurações salvas"); render()
    }
    button(page, "Testar alerta visual") {
        android.app.AlertDialog.Builder(this).setTitle("Teste de alerta visual")
            .setMessage("Este é apenas um teste. Nenhuma previsão, reconhecimento ou histórico foi alterado.")
            .setPositiveButton("Fechar", null).show()
    }
    button(page, "Testar som salvo") { alerts?.testSound() }
    button(page, "Testar notificação salva") { alerts?.testNotification() }
}

fun MainActivity.colorSettings() {
    heading(page, "Cores e temas", "A situação também aparece em texto. Nenhuma decisão depende apenas de cor.")
    val themeBox = card(page)
    val theme = picker(themeBox, "Tema da interface", listOf(Choice("dark", "Grafite e verde"), Choice("light", "Claro"), Choice("industrial", "Industrial · alto contraste")), service.settings().optString("theme", "dark"))
    button(themeBox, "Aplicar tema", true) { service.saveSettings(service.settings().put("theme", theme.value)); render() }
    label(page, "Faixas de prazo", 20f, true)
    label(page, "Minutos restantes até o evento. Comece em 0, sem lacunas nem sobreposição. Atrasados recebem identificação própria.", 14f, muted = true)
    space(page)
    val values = rows("colorRanges").sortedBy { it.optLong("minMinutes") }.map { JSONObject(it.toString()) }.toMutableList()
    val list = column(page)
    var readers = emptyList<() -> JSONObject>()
    fun capture() { val rows = readers.map { it() }; values.clear(); values.addAll(rows) }
    fun drawRows() {
        list.removeAllViews()
        readers = values.mapIndexed { index, original ->
            val box = card(list)
            label(box, "Faixa ${index + 1}", 17f, true)
            val name = input(box, "Nome", original.optString("name"))
            val color = input(box, "Cor hexadecimal (#RRGGBB)", original.optString("color", "#16a34a"))
            val min = input(box, "Início em minutos (inclusivo)", original.optLong("minMinutes").toString(), numeric = true)
            val max = input(box, "Fim em minutos (exclusivo)", original.optLong("maxMinutes").toString(), numeric = true)
            val priority = input(box, "Prioridade da faixa", original.optInt("priority", index + 1).toString(), numeric = true)
            val blink = toggle(box, "Marcação de destaque (compatibilidade do backup)", original.optBoolean("blink"))
            val sound = toggle(box, "Sinal sonoro da faixa (compatibilidade do backup)", original.optBoolean("sound"))
            label(box, "Os disparos nativos seguem o alarme da previsão; estas duas marcações são preservadas para intercâmbio com o navegador.", 12f, muted = true)
            button(box, "Remover esta faixa", danger = true) { capture(); values.removeAt(index); drawRows() }
            val reader: () -> JSONObject = {
                JSONObject(original.toString()).apply {
                    put("name", name.text.toString()); put("color", color.text.toString())
                    put("minMinutes", min.text.toString().toLong()); put("maxMinutes", max.text.toString().toLong())
                    put("priority", priority.text.toString().toInt()); put("blink", blink.isChecked); put("sound", sound.isChecked); put("active", true)
                    if (!has("id")) put("id", UUID.randomUUID().toString())
                }
            }; reader
        }
    }
    drawRows()
    button(page, "Adicionar faixa") {
        capture(); val min = values.lastOrNull()?.optLong("maxMinutes") ?: 0L
        values += JSONObject().put("id", UUID.randomUUID().toString()).put("name", "Nova faixa").put("color", "#16a34a").put("minMinutes", min).put("maxMinutes", min + 60).put("priority", values.size + 1)
        drawRows()
    }
    button(page, "Salvar todas as faixas", true) { capture(); service.saveColorRanges(values); notice("Faixas salvas"); render() }
}

fun MainActivity.diagnostics() {
    heading(page, "Diagnóstico", "Estado local do aplicativo. Relatório sem conteúdo das previsões.")
    val stores = listOf("consoles", "pipelines", "operationalUnits", "pipelineOperationalUnits", "equipmentTypes", "equipmentTags", "events", "eventHistory", "colorRanges", "settings")
    val version = packageManager.getPackageInfo(packageName, 0).versionName ?: "—"
    val errors = store.errors()
    val report = buildString {
        append("Livro de Previsões · Android nativo\nVersão: $version\n")
        append("Android: ${android.os.Build.VERSION.RELEASE} / API ${android.os.Build.VERSION.SDK_INT}\n")
        append("Fuso: ${ZoneId.systemDefault().id}\nGerado: ${Instant.now()}\n")
        append("Persistência: snapshot JSON privado, escrita atômica\nBackup: schemaVersion 1 / 10 coleções\n")
        append("Alertas: somente em primeiro plano\nNotificações: ${alerts?.permissionState()}\n")
        stores.forEach { append("$it: ${rows(it).size}\n") }
        append("Erros técnicos locais: ${errors.size}\n")
        errors.takeLast(20).forEach { append(it.toString()).append('\n') }
    }
    val box = card(page); label(box, report, 14f)
    button(box, "Copiar relatório", true) { (getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).setPrimaryClip(ClipData.newPlainText("Diagnóstico Livro de Previsões", report)); notice("Relatório copiado") }
    button(box, "Atualizar diagnóstico") { render() }
    if (errors.isNotEmpty()) button(box, "Limpar apenas logs técnicos", danger = true) { confirm("Limpar logs técnicos?", "Previsões, cadastros e histórico de auditoria não serão alterados.", "Limpar logs") { store.clearErrors(); render() } }
}
