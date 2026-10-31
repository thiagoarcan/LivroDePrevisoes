package br.com.livrodeprevisoes.app

import android.widget.CheckBox
import org.json.JSONArray
import org.json.JSONObject

private val registryNames = listOf("consoles" to "Consoles", "pipelines" to "Dutos", "operationalUnits" to "Unidades operacionais", "pipelineOperationalUnits" to "Relações duto / UO", "equipmentTypes" to "Tipos de equipamento", "equipmentTags" to "TAGs")

fun MainActivity.registry() {
    heading(page, "Cadastros", "Estruture os consoles, dutos, UOs e equipamentos. Vínculos são validados antes de salvar.")
    val selector = picker(page, "Categoria", registryNames.map { Choice(it.first, it.second) }, registryCategory)
    selector.onChange { if (registryCategory != it) { registryCategory = it; render() } }
    space(page)
    if (registryCategory == "pipelineOperationalUnits") {
        label(page, "Os vínculos são editados junto com o duto. Cada duto requer duas ou mais UOs distintas.", 14f, muted = true)
        rows("pipelines").forEach { pipeline ->
            val box = card(page); label(box, pipeline.optString("name"), 18f, true)
            val ids = rows("pipelineOperationalUnits").filter { it.optString("pipelineId") == pipeline.optString("id") }.map { it.optString("uoId") }
            label(box, ids.joinToString(" • ") { name("operationalUnits", it) }, muted = true)
            button(box, "Editar vínculos") { registryEditor("pipelines", pipeline) }
        }
        return
    }
    button(page, "Adicionar ${registryNames.first { it.first == registryCategory }.second.lowercase()}", true) { registryEditor(registryCategory, null) }
    if (registryCategory == "operationalUnits") button(page, "Cadastrar várias UOs") {
        formDialog("Cadastro em lote de UOs") { form ->
            label(form, "Uma UO por linha. O lote inteiro será validado antes de gravar.", muted = true)
            val names = input(form, "Nomes das UOs", multiline = true)
            val save: () -> Unit = { service.saveUOBatch(names.text.toString()); notice("UOs cadastradas"); render() }; save
        }
    }
    space(page)
    val rows = rows(registryCategory).sortedBy { it.optString(if (registryCategory == "equipmentTags") "tag" else "name") }
    label(page, "${rows.size} registros • ativos e inativos", 13f, true, true); space(page)
    if (rows.isEmpty()) label(page, "Nenhum cadastro nesta categoria.", muted = true)
    rows.forEach { item ->
        val box = card(page)
        val active = item.optBoolean("active", true)
        label(box, item.optString(if (registryCategory == "equipmentTags") "tag" else "name"), 18f, true)
        label(box, if (active) "Ativo" else "Inativo", 13f, true, true)
        when (registryCategory) {
            "pipelines" -> {
                label(box, "Console: ${name("consoles", item.optString("consoleId"))}", 14f)
                val linked = rows("pipelineOperationalUnits").filter { it.optString("pipelineId") == item.optString("id") }.joinToString(" • ") { name("operationalUnits", it.optString("uoId")) }
                label(box, "UOs: $linked", 14f, muted = true)
            }
            "equipmentTypes" -> label(box, "UO: ${name("operationalUnits", item.optString("uoId"))}", 14f, muted = true)
            "equipmentTags" -> label(box, "${name("operationalUnits", item.optString("uoId"))} / ${name("equipmentTypes", item.optString("equipmentTypeId"))}", 14f, muted = true)
        }
        button(box, "Editar") { registryEditor(registryCategory, item) }
        button(box, if (active) "Inativar" else "Reativar") {
            confirm(if (active) "Inativar cadastro?" else "Reativar cadastro?", "Vínculos existentes serão preservados. Dependências ativas podem impedir a alteração.") {
                service.setRecordActive(registryCategory, item.getString("id"), !active); render()
            }
        }
        button(box, "Excluir cadastro", danger = true) {
            confirm("Excluir cadastro?", "Só é possível excluir um cadastro sem dependências. Prefira inativar para preservar referências.", "Excluir") {
                service.deleteRecord(registryCategory, item.getString("id")); render()
            }
        }
    }
}

fun MainActivity.registryEditor(storeName: String, original: JSONObject?) {
    val initial = original ?: JSONObject()
    formDialog(if (original == null) "Novo cadastro" else "Editar cadastro") { form ->
        val textKey = if (storeName == "equipmentTags") "tag" else "name"
        val title = input(form, if (storeName == "equipmentTags") "Código da TAG *" else "Nome *", initial.optString(textKey))
        var console: Picker? = null; var unit: Picker? = null; var type: Picker? = null
        val unitChecks = mutableListOf<Pair<String, CheckBox>>()
        if (storeName == "pipelines") {
            console = picker(form, "Console responsável *", listOf(Choice("", "Selecione")) + options("consoles", setOf(initial.optString("consoleId"))), initial.optString("consoleId"))
            space(form); label(form, "UOs vinculadas * (selecione pelo menos duas)", 14f, true)
            val linked = rows("pipelineOperationalUnits").filter { it.optString("pipelineId") == initial.optString("id") }.map { it.optString("uoId") }.toSet()
            options("operationalUnits", linked).forEach { option -> unitChecks += option.id to toggle(form, option.title, option.id in linked) }
            if (unitChecks.isEmpty()) label(form, "Cadastre UOs antes de adicionar um duto.", muted = true)
        }
        if (storeName in listOf("equipmentTypes", "equipmentTags")) {
            unit = picker(form, "Unidade operacional *", listOf(Choice("", "Selecione")) + options("operationalUnits", setOf(initial.optString("uoId"))), initial.optString("uoId"))
        }
        if (storeName == "equipmentTags") {
            val slot = column(form)
            var selectedUnit = initial.optString("uoId")
            var selectedType = initial.optString("equipmentTypeId")
            fun updateTypes() {
                slot.removeAllViews()
                type = picker(slot, "Tipo de equipamento *", listOf(Choice("", "Selecione")) + options("equipmentTypes", setOf(initial.optString("equipmentTypeId"))) { it.optString("uoId") == selectedUnit }, selectedType)
                type!!.onChange { selectedType = it }
            }
            updateTypes()
            unit!!.onChange { value -> if (selectedUnit != value) { selectedUnit = value; selectedType = ""; updateTypes() } }
        }
        val save: () -> Unit = {
            val row = JSONObject(initial.toString()).put(textKey, title.text.toString())
            console?.let { row.put("consoleId", it.value) }
            unit?.let { row.put("uoId", it.value) }
            type?.let { row.put("equipmentTypeId", it.value) }
            if (storeName == "pipelines") row.put("uoIds", JSONArray(unitChecks.filter { it.second.isChecked }.map { it.first }))
            service.saveRecord(storeName, row); notice("Cadastro salvo"); render()
        }
        save
    }
}
