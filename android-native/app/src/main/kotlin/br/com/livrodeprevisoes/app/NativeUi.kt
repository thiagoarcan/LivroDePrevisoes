package br.com.livrodeprevisoes.app

import android.app.AlertDialog
import android.content.Context
import android.content.res.ColorStateList
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.text.InputType
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.*

class Palette(theme: String) {
    val light = theme == "light"
    val industrial = theme == "industrial"
    val app = Color.parseColor(if (light) "#f0f3ef" else if (industrial) "#000000" else "#101719")
    val surface = Color.parseColor(if (light) "#ffffff" else if (industrial) "#101010" else "#192326")
    val text = Color.parseColor(if (light) "#1b3029" else "#f0f5f3")
    val muted = Color.parseColor(if (light) "#43594f" else "#c0ceca")
    val primary = Color.parseColor(if (industrial) "#ffdb44" else if (light) "#17664f" else "#1c7460")
    val onPrimary = if (industrial) Color.BLACK else Color.WHITE
    val border = Color.parseColor(if (light) "#91a79a" else "#657d75")
    val danger = Color.parseColor(if (light) "#a92132" else "#ff9ba6")
    val focus = Color.parseColor(if (industrial) "#ffdb44" else if (light) "#17664f" else "#84d8c2")
}

fun Context.dp(n: Int): Int = (n * resources.displayMetrics.density + .5f).toInt()
fun MainActivity.shape(color: Int = palette.surface, radius: Int = 12, border: Boolean = false) = GradientDrawable().apply {
    setColor(color); cornerRadius = dp(radius).toFloat(); if (border) setStroke(dp(1), palette.border)
}
fun MainActivity.column(parent: ViewGroup? = null, padding: Int = 0): LinearLayout = LinearLayout(this).apply {
    orientation = LinearLayout.VERTICAL; setPadding(dp(padding), dp(padding), dp(padding), dp(padding))
    parent?.addView(this, ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT))
}
fun MainActivity.row(parent: ViewGroup): LinearLayout = LinearLayout(this).apply {
    orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL
    parent.addView(this, ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT))
}
fun MainActivity.space(parent: ViewGroup, n: Int = 12) { parent.addView(View(this), ViewGroup.LayoutParams(1, dp(n))) }
fun MainActivity.label(parent: ViewGroup, text: String, size: Float = 15f, bold: Boolean = false, muted: Boolean = false): TextView = TextView(this).apply {
    this.text = text; textSize = size; setTextColor(if (muted) palette.muted else palette.text)
    if (bold) setTypeface(typeface, Typeface.BOLD)
    setLineSpacing(dp(3).toFloat(), 1f); setTextIsSelectable(true)
    parent.addView(this, ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT))
}
fun MainActivity.heading(parent: ViewGroup, title: String, subtitle: String = "") {
    label(parent, title, 25f, true)
    if (subtitle.isNotEmpty()) { space(parent, 5); label(parent, subtitle, 14f, muted = true) }
    space(parent, 20)
}
fun MainActivity.card(parent: ViewGroup): LinearLayout = column().apply {
    background = shape(); setPadding(dp(16), dp(16), dp(16), dp(16))
    parent.addView(this, LinearLayout.LayoutParams(-1, -2).apply { bottomMargin = dp(12) })
}
fun MainActivity.button(parent: ViewGroup, title: String, primary: Boolean = false, danger: Boolean = false, action: () -> Unit): Button = Button(this).apply {
    text = title; textSize = 14f; isAllCaps = false; minHeight = dp(48)
    setTextColor(if (primary) palette.onPrimary else if (danger) palette.danger else palette.text)
    background = shape(if (primary) palette.primary else palette.app, 8, !primary)
    setPadding(dp(12), dp(8), dp(12), dp(8))
    contentDescription = title
    setOnClickListener { safe(action) }
    val params = LinearLayout.LayoutParams(-1, -2).apply { topMargin = dp(8) }
    parent.addView(this, params)
}
fun MainActivity.input(parent: ViewGroup, title: String, value: String = "", multiline: Boolean = false, numeric: Boolean = false): EditText {
    space(parent, 10); val caption = label(parent, title, 13f, true, true)
    return EditText(this).apply {
        id = View.generateViewId(); caption.labelFor = id
        setText(value); setTextColor(palette.text); setHintTextColor(palette.muted); textSize = 16f
        minHeight = dp(52); setPadding(dp(12), dp(9), dp(12), dp(9))
        background = shape(palette.app, 8, true)
        inputType = if (numeric) InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_SIGNED else if (multiline) InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_MULTI_LINE or InputType.TYPE_TEXT_FLAG_CAP_SENTENCES else InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_CAP_SENTENCES
        if (multiline) { minLines = 3; gravity = Gravity.TOP } else setSingleLine(true)
        parent.addView(this, ViewGroup.LayoutParams(-1, -2))
    }
}
fun MainActivity.toggle(parent: ViewGroup, title: String, checked: Boolean): CheckBox = CheckBox(this).apply {
    text = title; textSize = 15f; setTextColor(palette.text); isChecked = checked; minHeight = dp(48)
    buttonTintList = ColorStateList.valueOf(palette.focus)
    parent.addView(this, ViewGroup.LayoutParams(-1, -2))
}

class Choice(val id: String, val title: String) { override fun toString() = title }
class Picker(val spinner: Spinner, val options: List<Choice>) {
    val value: String get() = options.getOrNull(spinner.selectedItemPosition)?.id.orEmpty()
    fun onChange(action: (String) -> Unit) { spinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
        override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) { action(value) }
        override fun onNothingSelected(parent: AdapterView<*>?) {}
    } }
}
fun MainActivity.picker(parent: ViewGroup, title: String, options: List<Choice>, selected: String = ""): Picker {
    space(parent, 10); val caption = label(parent, title, 13f, true, true)
    val spinner = Spinner(this).apply {
        id = View.generateViewId(); caption.labelFor = id; contentDescription = title
        minimumHeight = dp(52); background = shape(palette.app, 8, true)
        val items = if (options.isEmpty()) listOf(Choice("", "Nenhum disponível")) else options
        adapter = object : ArrayAdapter<Choice>(this@picker, android.R.layout.simple_spinner_item, items) {
            override fun getView(position: Int, convertView: View?, parent: ViewGroup): View = super.getView(position, convertView, parent).apply {
                (this as TextView).setTextColor(palette.text); setPadding(dp(12), dp(10), dp(12), dp(10)); textSize = 16f; setSingleLine(false)
            }
            override fun getDropDownView(position: Int, convertView: View?, parent: ViewGroup): View = super.getDropDownView(position, convertView, parent).apply {
                (this as TextView).setTextColor(palette.text); setBackgroundColor(palette.surface); minHeight = dp(48); setPadding(dp(12), dp(10), dp(12), dp(10)); setSingleLine(false)
            }
        }.also { it.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item) }
        setSelection(options.indexOfFirst { it.id == selected }.coerceAtLeast(0))
        parent.addView(this, ViewGroup.LayoutParams(-1, -2))
    }
    return Picker(spinner, options)
}
fun MainActivity.confirm(title: String, message: String, positive: String = "Confirmar", action: () -> Unit) {
    AlertDialog.Builder(this).setTitle(title).setMessage(message).setNegativeButton("Cancelar", null)
        .setPositiveButton(positive) { _, _ -> safe(action) }.show()
}
fun MainActivity.formDialog(title: String, build: (LinearLayout) -> (() -> Unit)) {
    val body = column(padding = 20)
    val action = build(body)
    val scroll = ScrollView(this).apply { addView(body); setBackgroundColor(palette.surface) }
    val dialog = AlertDialog.Builder(this).setTitle(title).setView(scroll).setNegativeButton("Cancelar", null).setPositiveButton("Salvar", null).create()
    dialog.setOnShowListener { dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
        try { action(); dialog.dismiss() } catch (e: Exception) { report(e) }
    } }
    dialog.show()
}
