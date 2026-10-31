package br.com.livrodeprevisoes.app

import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import br.com.livrodeprevisoes.domain.BackupCodec
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.io.InputStream
import java.time.Instant
import java.time.LocalDate

private const val CREATE_DOCUMENT = 701
private const val OPEN_DOCUMENT = 702
private const val MAX_IMPORT_BYTES = 32 * 1024 * 1024

fun MainActivity.freshBackup(): String = service.snapshot().put("exportedAt", Instant.now().toString()).toString(2)

fun MainActivity.backupScreen() {
    heading(page, "Backup e migração", "Arquivos escolhidos por você. Nenhuma conexão com servidores.")
    val export = card(page); label(export, "Exportar", 20f, true)
    val currentSettings = service.settings()
    val lastBackup = currentSettings.optString("lastBackupAt").takeUnless { it == "null" || it.isBlank() }
    label(export, "Último backup JSON: ${lastBackup?.let(::formatted) ?: "ainda não registrado"}", 14f, true)
    if (backupIsDue(currentSettings)) label(export, "Lembrete: salve uma cópia atualizada fora deste aparelho.", 14f, true)
    val reminder = input(export, "Lembrar a cada quantos dias? (1–3650)", currentSettings.optInt("backupReminderDays", 7).toString(), numeric = true)
    button(export, "Salvar frequência do lembrete") { service.saveSettings(service.settings().put("backupReminderDays", reminder.text.toString().toInt())); notice("Lembrete configurado"); render() }
    label(export, "O JSON contém as 10 coleções, configurações, desenhos e histórico. Guarde uma cópia fora deste aparelho. CSV é para consulta, não restauração.", muted = true)
    button(export, "Salvar backup JSON completo", true) { beginExport("json", freshBackup(), "application/json", "livro-backup-${LocalDate.now()}.json") }
    val csv = picker(export, "Conteúdo do CSV", listOf(Choice("pending", "Previsões pendentes"), Choice("completed", "Previsões concluídas"), Choice("all", "Todas as previsões"), Choice("cadastros", "Cadastros")))
    button(export, "Exportar CSV (UTF-8, ponto e vírgula)") { beginExport("csv", BackupCodec.csv(service.snapshot(), csv.value), "text/csv", "livro-${csv.value}-${LocalDate.now()}.csv") }
    val restore = card(page); label(restore, "Importar JSON", 20f, true)
    label(restore, "Para migrar do navegador, exporte o JSON no site e selecione esse arquivo aqui. O conteúdo é validado integralmente antes de alterar os dados.", muted = true)
    button(restore, "Importar e mesclar") { chooseImport("merge") }
    label(restore, "Mesclar combina IDs e versões. Conflitos impedem a aplicação; nenhuma coleção fica parcialmente importada.", 12f, muted = true)
    button(restore, "Substituir todos os dados", danger = true) { chooseImport("replace") }
    label(restore, "Substituir, carregar demonstração ou limpar só acontece depois que um backup preventivo é salvo com sucesso. Cancelar o seletor não altera seus dados.", 12f, muted = true)
    val maintenance = card(page); label(maintenance, "Ambiente local", 20f, true)
    button(maintenance, "Carregar dados de demonstração") { preventiveAction("demo", "Carregar demonstração?", "Dados de exemplo serão carregados conforme as regras do aplicativo. Primeiro será obrigatório salvar seu backup atual.") }
    button(maintenance, "Limpar todos os dados", danger = true) { preventiveAction("clear", "Limpar todos os dados?", "Todas as previsões, cadastros e histórico deste aparelho serão removidos. Primeiro será obrigatório salvar um backup preventivo.") }
}

fun MainActivity.chooseImport(mode: String) {
    check(exportGate.pending == null) { "Conclua ou cancele a exportação em andamento." }
    importMode = mode
    startActivityForResult(Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
        addCategory(Intent.CATEGORY_OPENABLE); type = "*/*"
        putExtra(Intent.EXTRA_MIME_TYPES, arrayOf("application/json", "text/json", "text/plain", "application/octet-stream"))
    }, OPEN_DOCUMENT)
}

fun MainActivity.beginExport(action: String, payload: String, mime: String, name: String) {
    check(exportGate.pending == null) { "Já existe uma exportação em andamento." }
    exportFile.writeText(payload, Charsets.UTF_8)
    launchPreparedExport(action, mime, name)
}

/** Recovery must copy bytes, never decode or repair a corrupt source document. */
fun MainActivity.beginRawExport(source: java.io.File) {
    check(exportGate.pending == null) { "Já existe uma exportação em andamento." }
    try {
        source.inputStream().use { input -> exportFile.outputStream().use { output -> input.copyTo(output) } }
        launchPreparedExport("raw", "application/json", "livro-original.json")
    } catch (e: Exception) { exportFile.delete(); throw e }
}

private fun MainActivity.launchPreparedExport(action: String, mime: String, name: String) {
    exportGate.begin(action)
    try {
        startActivityForResult(Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE); type = mime; putExtra(Intent.EXTRA_TITLE, name)
        }, CREATE_DOCUMENT)
    } catch (e: Exception) { exportGate.finished(false); exportFile.delete(); throw e }
}

fun MainActivity.preventiveAction(action: String, title: String, message: String) {
    confirm(title, message, "Salvar backup e continuar") {
        beginExport(action, freshBackup(), "application/json", "livro-preventivo-${LocalDate.now()}.json")
    }
}


fun MainActivity.handleDocumentResult(request: Int, result: Int, intent: Intent?) {
    if (request == CREATE_DOCUMENT) {
        if (result != Activity.RESULT_OK || intent?.data == null) {
            exportGate.finished(false); exportFile.delete()
            notice("Exportação cancelada. Os dados não foram alterados.")
            return
        }
        var written = false
        try {
            require(exportFile.exists()) { "Não foi possível recuperar o arquivo preparado. Nenhum dado foi alterado." }
            val output = contentResolver.openOutputStream(intent.data!!, "wt") ?: error("Não foi possível abrir o documento para gravação.")
            output.use { stream -> exportFile.inputStream().use { it.copyTo(stream) }; stream.flush() }
            written = true
        } catch (e: Exception) {
            exportGate.finished(false)
            report(IllegalStateException("O backup não foi concluído. Nenhum dado foi alterado; o documento escolhido pode estar incompleto. ${e.message}"))
        } finally { exportFile.delete() }
        if (!written) return
        val action = exportGate.finished(true) ?: return
        safe {
            when (action) {
                "replace" -> {
                    require(importFile.exists()) { "Arquivo de importação não encontrado. Seu backup foi salvo e os dados atuais foram preservados." }
                    applyRestore(BackupCodec.parse(importFile.inputStream().use { readBounded(it) }), "replace", true)
                }
                "demo" -> { service.loadDemoData(true); activeConsole = ""; notice("Demonstração carregada; backup preventivo salvo"); render() }
                "clear" -> { service.clearAllData(true); activeConsole = ""; notice("Dados limpos; backup preventivo salvo"); render() }
                "json" -> {
                    try { service.saveSettings(successfulBackupSettings(action, service.settings())!!) }
                    catch (e: Exception) { notice("Backup salvo. Não foi possível registrar a data no aparelho."); runCatching { store.logError("data do backup", e.message.orEmpty()) } }
                    notice("Backup JSON salvo com sucesso"); render()
                }
                else -> notice("Arquivo salvo com sucesso")
            }
        }
    } else if (request == OPEN_DOCUMENT) {
        if (result != Activity.RESULT_OK || intent?.data == null) { notice("Importação cancelada. Nenhum dado foi alterado."); return }
        safe {
            val input = contentResolver.openInputStream(intent.data!!) ?: error("Não foi possível abrir o arquivo.")
            val text = input.use { readBounded(it) }
            val backup = BackupCodec.parse(text)
            importFile.writeText(backup.toString())
            val data = backup.getJSONObject("data")
            val summary = "Backup validado: ${data.getJSONArray("events").length()} previsões e ${data.getJSONArray("eventHistory").length()} registros de histórico."
            if (importMode == "replace") {
                preventiveAction("replace", "Substituir todos os dados?", "$summary\n\nOs dados atuais serão substituídos. Salve primeiro o backup preventivo obrigatório.")
            } else confirm("Mesclar backup?", "$summary\n\nIDs e versões serão comparados. Conflitos não serão aplicados.", "Mesclar") { applyRestore(backup, "merge", false) }
        }
    }
}

fun MainActivity.applyRestore(backup: JSONObject, mode: String, preventive: Boolean) {
    val result = service.restore(backup, mode, preventive)
    if (!result.applied) {
        AlertDialog.Builder(this).setTitle("Importação não aplicada")
            .setMessage("Nenhum dado foi alterado.\n\n" + result.conflicts.joinToString("\n"))
            .setPositiveButton("Entendi", null).show()
        return
    }
    importFile.delete(); activeConsole = ""
    notice("Importação concluída: ${result.inserted} novos, ${result.updated} atualizados, ${result.skipped} preservados.")
    render()
}
