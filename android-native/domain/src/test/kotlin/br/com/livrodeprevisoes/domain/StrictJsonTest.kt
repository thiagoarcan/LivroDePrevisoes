package br.com.livrodeprevisoes.domain

import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test

class StrictJsonTest {
    private fun rejected(text: String) {
        try { StrictJson.parseObject(text); fail("Accepted malformed JSON: ${text.take(120)}") }
        catch (_: IllegalArgumentException) { }
    }
    @Test fun strictTokensAndExactlyOneObjectRootAreRequired() {
        for (text in listOf("", "[]", "null", "true", "1", "\"text\"", "{} trailing", "{}{}", "{}[]", "{}\u0000", "{a:1}", "{'a':1}", "{\"a\":'text'}", "{\"a\":1,}", "{\"a\":[1,]}", "{\"a\":[,1]}", "{\"a\":undefined}", "{\"a\":NaN}", "{\"a\":Infinity}", "{/* comment */}", "{\"a\":true false}", "{\"a\"=1}", "{\"a\":1;\"b\":2}", "{}\u00a0")) rejected(text)
    }
    @Test fun strictNumberGrammarRejectsLenientParserExtensions() {
        for (token in listOf("+1", "01", "-01", ".1", "1.", "1e", "1e+", "--1", "0x10", "1_000", "-", "00", "1E--2")) rejected("{\"n\":$token}")
    }
    @Test fun stringsRejectBadEscapesAndUnescapedControlCharacters() {
        for (text in listOf("{\"a\":\"\\x20\"}", "{\"a\":\"\\u123\"}", "{\"a\":\"\\uZZZZ\"}", "{\"a\":\"\\q\"}", "{\"a\":\"unterminated}", "{\"a\":\"line\nbreak\"}", "{\"a\":\"null\u0000byte\"}", "{\"a\":\"tab\there\"}")) rejected(text)
    }
    @Test fun unpairedSurrogatesAreRejectedBeforeUtf8CanReplaceThem() {
        for (source in listOf(
            """{"text":"\ud800"}""", """{"text":"\udfff"}""",
            """{"\ud800":"value"}""", """{"nested":["x\udfffy"]}""",
            """{"text":"\ud800\ud800\udfff"}""", """{"text":"\udfff\ud800"}""",
            "{\"text\":\"\uD800\"}", "{\"\uDFFF\":1}"
        )) {
            val error=assertThrows(IllegalArgumentException::class.java) { StrictJson.parseObject(source) }
            assertTrue(error.message.orEmpty().contains("Unicode"))
        }
    }
    @Test fun validEmojiPairsInKeysAndValuesSurviveUtf8WithoutNormalization() {
        val source="""{"\ud83d\ude00":"á\ud83d\ude00é","nested":["\ud834\udd1e"]}"""
        val parsed=StrictJson.parseObject(source)
        val reencoded=String(parsed.toString().toByteArray(Charsets.UTF_8),Charsets.UTF_8)
        val restored=StrictJson.parseObject(reencoded)
        assertEquals("á😀é",restored.getString("😀"))
        assertEquals("𝄞",restored.getJSONArray("nested").getString(0))
    }
    @Test fun escapedStringsScientificNumbersWhitespaceAndNestedValuesArePreserved() {
        val parsed=StrictJson.parseObject("\uFEFF \r\n\t" + """{"text":"{[\"\n\t\b\f\r\/\\\u00e1\uD83D\uDE00]}","n":-1.25e+2,"tiny":0.01,"array":[true,false,null,{"key":"value"}]}""" + "\r\n ")
        assertEquals("{[\"\n\t\b\u000c\r/\\á😀]}",parsed.getString("text"))
        assertEquals(-125.0,parsed.getDouble("n"),0.0)
        assertEquals(0.01,parsed.getDouble("tiny"),0.0)
        assertEquals(true,parsed.getJSONArray("array").get(0))
        assertEquals(false,parsed.getJSONArray("array").get(1))
        assertTrue(parsed.getJSONArray("array").isNull(2))
        assertEquals("value",parsed.getJSONArray("array").getJSONObject(3).getString("key"))
    }
    @Test fun duplicateObjectKeysMatchBrowserLastValueWinsIncludingUnicodeEscapes() {
        val parsed=StrictJson.parseObject("""{"a":1,"\u0061":2,"nested":{"x":true,"x":false}}""")
        assertEquals(2,parsed.getInt("a"))
        assertFalse(parsed.getJSONObject("nested").getBoolean("x"))
        assertEquals(2,parsed.length())
    }
    @Test fun depthIsBoundedBeforeObjectConstructionAndStringBracesDoNotCount() {
        val boundary="{\"nested\":"+"[".repeat(127)+"0"+"]".repeat(127)+"}"
        assertTrue(StrictJson.parseObject(boundary).has("nested"))
        rejected("{\"nested\":"+"[".repeat(128)+"0"+"]".repeat(128)+"}")
        assertEquals("[".repeat(1000),StrictJson.parseObject("{\"text\":\""+"[".repeat(1000)+"\"}").getString("text"))
    }
    @Test fun backupTextParsingRejectsTrailingDataBeforeValidation() {
        val json=BackupCodecTest.fixture().toString()
        assertEquals(10,BackupCodec.parse(json).getJSONObject("data").length())
        for (suffix in listOf(" TRAILING", "{}", "\u0000")) {
            try { BackupCodec.parse(json+suffix); fail("Backup accepted suffix") } catch (_: IllegalArgumentException) { }
        }
        try { BackupCodec.parse("{}"); fail("Backup skipped schema validation") } catch (_: IllegalArgumentException) { }
    }
}
