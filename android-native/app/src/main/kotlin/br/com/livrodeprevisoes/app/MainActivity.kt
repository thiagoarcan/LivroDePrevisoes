package br.com.livrodeprevisoes.app

import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import android.content.res.Configuration
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.Gravity
import android.view.View
import android.view.WindowInsets
import android.widget.*
import br.com.livrodeprevisoes.domain.LivroService
import br.com.livrodeprevisoes.data.FileSnapshotStore
import br.com.livrodeprevisoes.alerts.AndroidAlerts
import org.json.JSONObject
import java.io.File
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter

class MainActivity : Activity() {
    lateinit var service: LivroService
    lateinit var store: FileSnapshotStore
    var alerts: AndroidAlerts? = null
    var palette = Palette("dark")
    lateinit var page: LinearLayout
    var screen = "dashboard"
    var activeConsole = ""
    var draftReader: (() -> JSONObject)? = null
    var draftBaseline: String? = null
    var draft: JSONObject? = null
    var exportGate = ExportGate()
    val exportFile get() = File(filesDir, "pending-export.txt")
    val importFile get() = File(filesDir, "pending-import.json")
    val draftFile get() = File(filesDir, "native-draft.json")
    var importMode = "merge"
    var detailId: String? = null
    var listQuery = ""
    var listPriority = ""
    var listPage = 0
    var listFilters = EventFilters()
    var restoredDraft = false
    var registryCategory = "consoles"
    private var platformBackCallback: android.window.OnBackInvokedCallback? = null
    var initialized = false
    private var renderRows: Map<String, List<JSONObject>> = emptyMap()
    private var renderNames: Map<String, Map<String, String>> = emptyMap()
    fun rows(name: String): List<JSONObject> = renderRows[name].orEmpty()
    private val clockHandler = Handler(Looper.getMainLooper())
    private val clockViews = linkedMapOf<View, () -> Unit>()
    var mutationRefresh: (() -> Unit)? = null
    private val clockTick = object : Runnable {
        override fun run() {
            clockViews.values.toList().forEach { update -> runCatching(update) }
            clockHandler.postDelayed(this, 1000L)
        }
    }
    fun watchClock(view: View, update: () -> Unit) { clockViews[view] = update; update() }
    fun forgetClockChildren(parent: View) {
        clockViews.keys.removeAll { child ->
            var current: android.view.ViewParent? = child.parent
            var found = child === parent
            while (current is View && !found) { found = current === parent; current = (current as View).parent }
            found
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        if (Build.VERSION.SDK_INT >= 33) {
            platformBackCallback = android.window.OnBackInvokedCallback { handleBack() }.also { callback ->
                onBackInvokedDispatcher.registerOnBackInvokedCallback(android.window.OnBackInvokedDispatcher.PRIORITY_DEFAULT, callback)
            }
        }
        store = FileSnapshotStore(File(filesDir, "livro-data.json"))
        try {
            service = LivroService(store)
            initialized = true
            activeConsole = savedInstanceState?.getString("console") ?: service.settings().optString("activeConsoleId").takeUnless { it == "null" }.orEmpty()
            screen = savedInstanceState?.getString("screen") ?: "dashboard"
            detailId = savedInstanceState?.getString("detailId")
            listQuery = savedInstanceState?.getString("query").orEmpty()
            listPriority = savedInstanceState?.getString("priority").orEmpty()
            listPage = savedInstanceState?.getInt("listPage", 0) ?: 0
            savedInstanceState?.getBundle("listFilters")?.let { filters ->
                listFilters = EventFilters(filters.getString("pipeline").orEmpty(), filters.getString("unit").orEmpty(),
                    filters.getString("equipment").orEmpty(), filters.getString("tag").orEmpty(), filters.getString("dateFrom").orEmpty(),
                    filters.getString("dateTo").orEmpty(), filters.getString("alarm").orEmpty(), filters.getString("alarmState").orEmpty(), filters.getString("window").orEmpty())
            }
            registryCategory = savedInstanceState?.getString("registry") ?: "consoles"
            importMode = savedInstanceState?.getString("importMode") ?: "merge"
            exportGate = ExportGate(savedInstanceState?.getString("exportAction"))
            if (savedInstanceState?.getBoolean("hasDraft") == true && draftFile.exists()) { draft = JSONObject(draftFile.readText()); restoredDraft = true }
            alerts = AndroidAlerts(this, service) { refreshAfterMutation() }.also { controller ->
                controller.onError = { context, error -> runCatching { store.logError(context, error.message ?: error.toString()) } }
            }
            render()
            if (!getPreferences(MODE_PRIVATE).getBoolean("foregroundNotice", false)) {
                AlertDialog.Builder(this).setTitle("Seu caderno, neste aparelho")
                    .setMessage("Tudo funciona offline. Os alertas são monitorados somente enquanto o aplicativo está aberto e ativo; não há garantia com a tela bloqueada ou em segundo plano. Use os procedimentos operacionais da sua equipe. Exporte backups regularmente.")
                    .setPositiveButton("Entendi") { _, _ -> getPreferences(MODE_PRIVATE).edit().putBoolean("foregroundNotice", true).apply() }.show()
            }
        } catch (e: Exception) {
            showLoadFailure(e)
        }
    }

    fun showLoadFailure(e: Exception) {
        initialized = false
        val body = column(padding = 24)
        body.setBackgroundColor(palette.app)
        heading(body, "Dados preservados", "Não foi possível abrir o armazenamento local.")
        label(body, "O arquivo original não foi apagado nem reinicializado. Exporte uma cópia para análise antes de qualquer intervenção.")
        space(body); label(body, e.message ?: "Erro de leitura", muted = true)
        button(body, "Salvar cópia original", true) {
            val file = File(filesDir, "livro-data.json")
            require(file.exists()) { "Arquivo não encontrado." }
            beginRawExport(file)
        }
        setContentView(body)
    }

    override fun onResume() { super.onResume(); if (initialized) { alerts?.start(); clockHandler.removeCallbacks(clockTick); clockHandler.post(clockTick) } }
    override fun onPause() { clockHandler.removeCallbacks(clockTick); alerts?.stop(); super.onPause() }
    override fun onDestroy() {
        clockHandler.removeCallbacks(clockTick); clockViews.clear(); alerts?.destroy()
        if (Build.VERSION.SDK_INT >= 33) platformBackCallback?.let { onBackInvokedDispatcher.unregisterOnBackInvokedCallback(it) }
        super.onDestroy()
    }
    override fun onConfigurationChanged(newConfig: Configuration) {
        super.onConfigurationChanged(newConfig)
        // Keep live Android fields/canvas in place; no rotation discards a draft or dialog.
    }
    override fun onSaveInstanceState(out: Bundle) {
        out.putString("screen", screen); out.putString("console", activeConsole); out.putString("detailId", detailId)
        out.putString("query", listQuery); out.putString("priority", listPriority); out.putString("registry", registryCategory)
        out.putInt("listPage", listPage)
        out.putBundle("listFilters", Bundle().apply {
            putString("pipeline", listFilters.pipeline); putString("unit", listFilters.unit); putString("equipment", listFilters.equipment)
            putString("tag", listFilters.tag); putString("dateFrom", listFilters.dateFrom); putString("dateTo", listFilters.dateTo)
            putString("alarm", listFilters.alarm); putString("alarmState", listFilters.alarmState); putString("window", listFilters.window)
        })
        out.putString("importMode", importMode); out.putString("exportAction", exportGate.pending)
        draftReader?.let { reader ->
            try { draftFile.writeText(reader().toString()); out.putBoolean("hasDraft", true) } catch (e: Exception) { runCatching { store.logError("rascunho", e.message.orEmpty()) } }
        }
        super.onSaveInstanceState(out)
    }
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        handleDocumentResult(requestCode, resultCode, data)
    }
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (initialized && screen == "alerts") render()
    }
    @Suppress("DEPRECATION")
    @Deprecated("Native back compatibility")
    override fun onBackPressed() { handleBack() }
    fun handleBack() {
        if (initialized && detailId != null && screen in listOf("pending", "completed")) safe {
            detailId = null
            render()
        } else if (initialized && (screen != "dashboard" || detailId != null)) safe { navigate("dashboard") }
        else finish()
    }
    fun safe(action: () -> Unit) { try { action() } catch (e: Exception) { report(e) } }
    fun report(e: Exception) {
        runCatching { store.logError(screen, e.message ?: e.javaClass.simpleName) }
        AlertDialog.Builder(this).setTitle("Confira os dados").setMessage(e.message ?: "Não foi possível concluir a operação.")
            .setPositiveButton("Entendi", null).show()
    }
    fun notice(message: String) { Toast.makeText(this, message, Toast.LENGTH_LONG).show() }
    fun refreshAfterMutation() {
        if (screen in listOf("pending", "completed") && detailId == null && mutationRefresh != null) {
            reloadRenderCache(); mutationRefresh?.invoke()
        } else if (screen in listOf("dashboard", "pending", "completed", "diagnostics")) render()
    }
    fun navigate(target: String, newDraft: JSONObject? = null) {
        val act = {
            draftReader = null; draftBaseline = null; draft = newDraft; draftFile.delete()
            detailId = null; screen = target; listQuery = ""; listPriority = ""; listPage = 0; listFilters = EventFilters(); restoredDraft = false; render()
        }
        if (draftReader != null && draftReader!!.invoke().toString() != draftBaseline) {
            confirm("Sair sem salvar?", "O rascunho desta previsão será descartado.", "Descartar", act)
        } else act()
    }
    fun reloadRenderCache() {
        val snapshotData = service.snapshot().getJSONObject("data")
        renderRows = snapshotData.keys().asSequence().associateWith { name ->
            val data = snapshotData.getJSONArray(name)
            (0 until data.length()).map { data.getJSONObject(it) }
        }
        renderNames = renderRows.mapValues { (storeName, records) -> records.associate { record ->
            record.optString("id") to record.optString(if (storeName == "equipmentTags") "tag" else "name")
        } }
    }
    fun render() {
        clockViews.clear(); mutationRefresh = null
        reloadRenderCache()
        palette = Palette(service.settings().optString("theme", "dark"))
        val root = column()
        root.setBackgroundColor(palette.app)
        root.setOnApplyWindowInsetsListener { view, insets ->
            if (Build.VERSION.SDK_INT >= 30) {
                val bars = insets.getInsets(WindowInsets.Type.systemBars() or WindowInsets.Type.displayCutout())
                view.setPadding(bars.left, bars.top, bars.right, bars.bottom)
            } else @Suppress("DEPRECATION") view.setPadding(insets.systemWindowInsetLeft, insets.systemWindowInsetTop, insets.systemWindowInsetRight, insets.systemWindowInsetBottom)
            insets
        }
        val header = row(root).apply { setPadding(dp(20), dp(12), dp(20), dp(10)) }
        val brand = column().apply { header.addView(this, LinearLayout.LayoutParams(0, -2, 1f)) }
        label(brand, "LIVRO DE PREVISÕES", 12f, true, true)
        label(brand, "Operação local", 17f, true)
        val offline = TextView(this).apply { text = "● OFFLINE"; textSize = 11f; setTextColor(palette.focus); contentDescription = "Funciona offline" }
        header.addView(offline)
        val work = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; root.addView(this, LinearLayout.LayoutParams(-1, 0, 1f)) }
        val wide = resources.configuration.screenWidthDp >= 720
        if (wide) {
            val navScroll = ScrollView(this).apply { work.addView(this, LinearLayout.LayoutParams(dp(190), -1)) }
            val nav = column(padding = 12); navScroll.addView(nav)
            destinations.forEach { (id, name) -> button(nav, if (screen == id) "• $name" else name, screen == id) { navigate(id) } }
        }
        val scroll = ScrollView(this).apply { isFillViewport = true; work.addView(this, LinearLayout.LayoutParams(0, -1, 1f)) }
        val outer = column(padding = if (wide) 28 else 18)
        scroll.addView(outer)
        page = column()
        outer.gravity = Gravity.CENTER_HORIZONTAL
        outer.addView(page, LinearLayout.LayoutParams(if (wide) dp(900).coerceAtMost(dp(resources.configuration.screenWidthDp - 250)) else -1, -2))
        when (screen) {
            "dashboard" -> dashboard()
            "new" -> eventForm(draft ?: JSONObject())
            "pending" -> if (detailId != null) eventDetails(detailId!!) else eventList(false)
            "completed" -> if (detailId != null) eventDetails(detailId!!) else eventList(true)
            "registry" -> registry()
            "alerts" -> alertSettings()
            "colors" -> colorSettings()
            "backup" -> backupScreen()
            "diagnostics" -> diagnostics()
            else -> dashboard()
        }
        if (!wide) {
            val bottom = row(root).apply { setPadding(dp(8), dp(6), dp(8), dp(8)); background = shape(palette.surface, 0) }
            listOf("dashboard" to "Painel", "new" to "Nova", "pending" to "Pendentes", "more" to "Mais").forEach { (id, title) ->
                val b = Button(this).apply {
                    text = if (screen == id) "• $title" else title; textSize = 12f; isAllCaps = false; minHeight = dp(52)
                    setPadding(dp(2), dp(6), dp(2), dp(6)); background = shape(if (screen == id) palette.primary else palette.surface, 8)
                    setTextColor(if (screen == id) palette.onPrimary else palette.text)
                    setOnClickListener { if (id == "more") menu() else safe { navigate(id) } }
                }
                bottom.addView(b, LinearLayout.LayoutParams(0, -2, 1f).apply { marginEnd = dp(3) })
            }
        }
        setContentView(root)
        if (Build.VERSION.SDK_INT >= 30) {
            val mask = android.view.WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS or android.view.WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS
            window.insetsController?.setSystemBarsAppearance(if (palette.light) mask else 0, mask)
        } else {
            @Suppress("DEPRECATION")
            window.decorView.systemUiVisibility = if (palette.light) View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR or View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR else 0
        }
        root.requestApplyInsets()
    }
    fun menu() {
        AlertDialog.Builder(this).setTitle("Áreas de trabalho").setItems(destinations.map { it.second }.toTypedArray()) { _, which ->
            safe { navigate(destinations[which].first) }
        }.show()
    }
    fun name(storeName: String, id: String, fallback: String = "—") = renderNames[storeName]?.get(id) ?: fallback
    fun hierarchy(e: JSONObject) = listOf(name("consoles", e.optString("consoleId")), name("pipelines", e.optString("pipelineId")), name("operationalUnits", e.optString("uoId")), name("equipmentTypes", e.optString("equipmentTypeId"), "Geral da UO"), name("equipmentTags", e.optString("tagId"), "Sem TAG")).joinToString(" / ")
    fun options(storeName: String, includeInactiveIds: Set<String> = emptySet(), predicate: (JSONObject) -> Boolean = { true }): List<Choice> = pickableRecords(rows(storeName), includeInactiveIds).filter(predicate).map { Choice(it.optString("id"), it.optString(if (storeName == "equipmentTags") "tag" else "name") + if (!it.optBoolean("active", true)) " (inativo)" else "") }.sortedBy { it.title }
    fun formatted(iso: String): String = try { DateTimeFormatter.ofPattern("dd/MM/yyyy 'às' HH:mm").withZone(ZoneId.systemDefault()).format(Instant.parse(iso)) } catch (_: Exception) { iso.ifBlank { "—" } }
    companion object {
        val destinations = listOf("dashboard" to "Painel", "new" to "Nova previsão", "pending" to "Pendentes", "completed" to "Concluídos", "registry" to "Cadastros", "alerts" to "Alertas", "colors" to "Cores e temas", "backup" to "Backup", "diagnostics" to "Diagnóstico")
    }
}
