package br.com.livrodeprevisoes.domain

import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject
import java.math.BigDecimal
import java.math.BigInteger

/**
 * Portable strict JSON text boundary for import and persistence.
 *
 * Android/JVM JSONObject(String) accept non-JSON syntax and ignore trailing data.
 * This parser owns the grammar instead. Duplicate keys deliberately retain the
 * last value, like browser JSON.parse, including keys spelled with escapes.
 * A single leading UTF-8 BOM is tolerated; only RFC whitespace is allowed after
 * it. Container depth is at most 128. Numbers must be finite in the common
 * Android/JVM numeric range; schema-specific integer limits remain in BackupCodec.
 * Unpaired UTF-16 surrogates are rejected, not normalized: Android JSON emits
 * them unescaped and UTF-8 persistence would silently replace them with '?'.
 */
object StrictJson {
    fun parseObject(text: String): JSONObject = try {
        Parser(text).objectRoot()
    } catch (error: JSONException) {
        throw IllegalArgumentException("JSON inválido: ${error.message}", error)
    }

    internal fun requireValidUnicode(value: String) {
        var index = 0
        while (index < value.length) {
            val current = value[index]
            when {
                Character.isHighSurrogate(current) -> {
                    require(index + 1 < value.length && Character.isLowSurrogate(value[index + 1])) {
                        "Unicode inválido: caractere UTF-16 sem par."
                    }
                    index += 2
                }
                Character.isLowSurrogate(current) -> throw IllegalArgumentException("Unicode inválido: caractere UTF-16 sem par.")
                else -> index++
            }
        }
    }

    private class Parser(private val source: String) {
        private var position = 0

        fun objectRoot(): JSONObject {
            if (source.startsWith('\uFEFF')) position++
            whitespace()
            require(peek() == '{') { "O documento JSON deve conter um objeto." }
            val result = objectValue(1)
            whitespace()
            require(position == source.length) { "Conteúdo após o objeto JSON na posição $position." }
            return result
        }

        private fun value(depth: Int): Any {
            whitespace()
            return when (peek()) {
                '{' -> objectValue(depth + 1)
                '[' -> arrayValue(depth + 1)
                '"' -> string()
                't' -> literal("true", true)
                'f' -> literal("false", false)
                'n' -> literal("null", JSONObject.NULL)
                '-', in '0'..'9' -> number()
                else -> invalid("Valor JSON esperado")
            }
        }

        private fun objectValue(depth: Int): JSONObject {
            boundedDepth(depth)
            consume('{')
            val result = JSONObject()
            whitespace()
            if (take('}')) return result
            while (true) {
                whitespace()
                if (peek() != '"') invalid("Nome de propriedade entre aspas duplas esperado")
                val key = string()
                whitespace(); consume(':')
                result.put(key, value(depth))
                whitespace()
                if (take('}')) return result
                consume(',')
            }
        }

        private fun arrayValue(depth: Int): JSONArray {
            boundedDepth(depth)
            consume('[')
            val result = JSONArray()
            whitespace()
            if (take(']')) return result
            while (true) {
                result.put(value(depth))
                whitespace()
                if (take(']')) return result
                consume(',')
            }
        }

        private fun string(): String {
            consume('"')
            val result = StringBuilder()
            while (position < source.length) {
                val char = source[position++]
                when {
                    char == '"' -> return result.toString().also(::requireValidUnicode)
                    char == '\\' -> {
                        if (position == source.length) invalid("Escape incompleto")
                        when (val escaped = source[position++]) {
                            '"', '\\', '/' -> result.append(escaped)
                            'b' -> result.append('\b')
                            'f' -> result.append('\u000c')
                            'n' -> result.append('\n')
                            'r' -> result.append('\r')
                            't' -> result.append('\t')
                            'u' -> {
                                if (source.length - position < 4) invalid("Escape Unicode incompleto")
                                var code = 0
                                repeat(4) {
                                    val digit = when (val hex = source[position++]) {
                                        in '0'..'9' -> hex - '0'
                                        in 'a'..'f' -> hex - 'a' + 10
                                        in 'A'..'F' -> hex - 'A' + 10
                                        else -> invalid("Escape Unicode inválido")
                                    }
                                    code = code * 16 + digit
                                }
                                result.append(code.toChar())
                            }
                            else -> invalid("Escape inválido")
                        }
                    }
                    char.code < 0x20 -> invalid("Caractere de controle não escapado")
                    else -> result.append(char)
                }
            }
            invalid("Texto sem aspas de fechamento")
        }

        private fun number(): Number {
            val start = position
            take('-')
            if (!take('0')) {
                if (peek() !in '1'..'9') invalid("Número inválido")
                digits()
            }
            var fractional = false
            if (take('.')) {
                fractional = true
                if (peek() !in '0'..'9') invalid("Fração incompleta")
                digits()
            }
            if (peek() == 'e' || peek() == 'E') {
                fractional = true; position++
                if (peek() == '+' || peek() == '-') position++
                if (peek() !in '0'..'9') invalid("Expoente incompleto")
                digits()
            }
            val token = source.substring(start, position)
            val result = try {
                if (fractional) BigDecimal(token)
                else token.toLongOrNull()?.let { if (it in Int.MIN_VALUE..Int.MAX_VALUE) it.toInt() else it } ?: BigInteger(token)
            } catch (_: NumberFormatException) { invalid("Número fora do intervalo suportado") }
            require(result.toDouble().isFinite()) { "Número não finito na posição $start." }
            return result
        }

        private fun digits() { while (peek() in '0'..'9') position++ }
        private fun literal(token: String, value: Any): Any {
            if (!source.startsWith(token, position)) invalid("Literal inválido")
            position += token.length
            return value
        }
        private fun boundedDepth(depth: Int) {
            require(depth <= 128) { "Estrutura JSON excede a profundidade máxima de 128." }
        }
        private fun whitespace() { while (peek() in listOf(' ', '\t', '\r', '\n')) position++ }
        private fun peek(): Char? = source.getOrNull(position)
        private fun take(char: Char): Boolean = if (peek() == char) { position++; true } else false
        private fun consume(char: Char) { if (!take(char)) invalid("Esperado '$char'") }
        private fun invalid(message: String): Nothing = throw IllegalArgumentException("$message na posição $position.")
    }
}
