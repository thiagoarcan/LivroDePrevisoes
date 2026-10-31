package br.com.livrodeprevisoes.app

import android.content.Context
import android.graphics.*
import android.util.Base64
import android.view.MotionEvent
import android.view.View
import java.io.ByteArrayOutputStream

/** Native Canvas preserves imported PNG bytes until an actual ink edit. */
class DrawingView(context: Context, initial: String = "", val editable: Boolean = true) : View(context) {
    private val snapshot = DrawingSnapshot(initial.takeUnless { it == "null" }.orEmpty())
    private var ink = Bitmap.createBitmap(1200, 440, Bitmap.Config.ARGB_8888)
    private var previous: Bitmap? = null
    private val pen = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.rgb(24, 77, 61); strokeWidth = 4f; strokeCap = Paint.Cap.ROUND; strokeJoin = Paint.Join.ROUND; style = Paint.Style.STROKE }
    private var x = 0f; private var y = 0f
    private var hasInk = false
    init {
        contentDescription = if (editable) "Área de desenho livre. Use o dedo ou uma caneta; botões de desfazer e limpar abaixo." else "Desenho anexado à previsão"
        isFocusable = true; minimumHeight = context.dp(160)
        if (initial.startsWith("data:image/png;base64,")) {
            try {
                val bytes = Base64.decode(initial.substringAfter(','), Base64.DEFAULT)
                val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
                BitmapFactory.decodeByteArray(bytes, 0, bytes.size, bounds)
                if (bounds.outWidth in 1..8192 && bounds.outHeight in 1..8192 && bounds.outWidth.toLong() * bounds.outHeight <= 4_194_304L) {
                    var sample = 1
                    while (bounds.outWidth / sample > 1600 || bounds.outHeight / sample > 1200) sample *= 2
                    val options = BitmapFactory.Options().apply { inSampleSize = sample }
                    val original = BitmapFactory.decodeByteArray(bytes, 0, bytes.size, options)
                    if (original != null) {
                        Canvas(ink).drawBitmap(original, null, fit(original.width.toFloat(), original.height.toFloat(), 1200f, 440f), null)
                        original.recycle(); hasInk = true
                    }
                }
            } catch (_: IllegalArgumentException) { }
        }
    }
    private fun fit(sw: Float, sh: Float, dw: Float, dh: Float): RectF {
        val scale = minOf(dw / sw, dh / sh)
        val w = sw * scale; val h = sh * scale
        return RectF((dw - w) / 2, (dh - h) / 2, (dw + w) / 2, (dh + h) / 2)
    }
    private fun paper() = fit(1200f, 440f, width.toFloat(), height.toFloat())
    override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
        val width = MeasureSpec.getSize(widthMeasureSpec)
        setMeasuredDimension(width, (width * 440 / 1200).coerceAtLeast(context.dp(160)))
    }
    override fun onDraw(canvas: Canvas) {
        canvas.drawColor(Color.rgb(232, 237, 229))
        val paper = paper()
        canvas.drawRect(paper, Paint().apply { color = Color.rgb(248, 250, 247) })
        canvas.drawBitmap(ink, null, paper, null)
    }
    override fun onTouchEvent(event: MotionEvent): Boolean {
        if (!editable) return false
        val paper = paper()
        val nx = ((event.x - paper.left) * 1200f / paper.width().coerceAtLeast(1f)).coerceIn(0f, 1200f)
        val ny = ((event.y - paper.top) * 440f / paper.height().coerceAtLeast(1f)).coerceIn(0f, 440f)
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                if (!paper.contains(event.x, event.y)) return false
                parent?.requestDisallowInterceptTouchEvent(true); previous?.recycle(); previous = ink.copy(Bitmap.Config.ARGB_8888, true)
                x = nx; y = ny; Canvas(ink).drawPoint(nx, ny, pen); hasInk = true; snapshot.changed(); invalidate()
            }
            MotionEvent.ACTION_MOVE -> { Canvas(ink).drawLine(x, y, nx, ny, pen); x = nx; y = ny; hasInk = true; snapshot.changed(); invalidate() }
            MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> { parent?.requestDisallowInterceptTouchEvent(false); performClick() }
        }
        return true
    }
    override fun performClick(): Boolean { super.performClick(); return true }
    fun clear() { previous?.recycle(); previous = ink.copy(Bitmap.Config.ARGB_8888, true); ink.eraseColor(Color.TRANSPARENT); hasInk = false; snapshot.changed(); invalidate() }
    fun undo() { previous?.let { val current = ink; ink = it; previous = current; hasInk = true; snapshot.changed(); invalidate() } }
    fun png(): String = snapshot.encoded {
        if (!hasInk) "" else {
            val output = ByteArrayOutputStream()
            ink.compress(Bitmap.CompressFormat.PNG, 100, output)
            "data:image/png;base64," + Base64.encodeToString(output.toByteArray(), Base64.NO_WRAP)
        }
    }
}
