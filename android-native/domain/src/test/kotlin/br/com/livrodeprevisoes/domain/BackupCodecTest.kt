package br.com.livrodeprevisoes.domain

import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import java.nio.ByteBuffer
import java.util.Base64
import java.util.zip.CRC32

/** Real schema-v1 fixtures, not a service-generated expectation. */
class BackupCodecTest {
    private fun rows(snapshot: JSONObject, store: String) = snapshot.getJSONObject("data").getJSONArray(store)
    private fun first(snapshot: JSONObject, store: String) = rows(snapshot, store).getJSONObject(0)
    private fun invalid(label: String, change: (JSONObject) -> Unit) {
        val input = fixture(); change(input)
        try { BackupCodec.validate(input); fail("Accepted invalid backup: $label") }
        catch (_: IllegalArgumentException) { }
    }
    @Test fun validationDetachesEveryNestedValueAndPreservesAuditDrawingAndExtensions() {
        val input = fixture()
        val result = BackupCodec.validate(input)
        assertEquals(PNG, first(result,"events").getString("stylusDrawing"))
        assertEquals("Operador", first(result,"events").getString("createdBy"))
        assertEquals("literal", first(result,"events").getJSONObject("extension").getString("retained"))
        assertEquals("before", first(result,"eventHistory").getString("previousValue"))
        first(result,"events").getJSONObject("extension").put("retained","changed")
        assertEquals("literal", first(input,"events").getJSONObject("extension").getString("retained"))
        assertEquals(10, result.getJSONObject("data").length())
    }
    @Test fun programmaticSnapshotsRejectUnpairedUnicodeInEveryStringAndKey() {
        val mutations: List<(JSONObject)->Unit> = listOf(
            { it.put("application","Broken\uD800") },
            { it.put("\uDFFF","extension") },
            { first(it,"events").put("description","Broken\uDFFF") },
            { first(it,"events").put("extension",JSONObject().put("\uD800","value")) },
            { first(it,"events").put("extension",JSONArray().put("Broken\uD800")) }
        )
        for (change in mutations) {
            val input=fixture(); change(input)
            val before=input.toString()
            val error=assertThrows(IllegalArgumentException::class.java) { BackupCodec.validate(input) }
            assertTrue(error.message.orEmpty().contains("Unicode"))
            assertEquals(before,input.toString())
        }
        val valid=fixture(); first(valid,"events").put("description","Inspecionar 😀").put("extension",JSONObject().put("😀","á𝄞é"))
        val restored=BackupCodec.parse(String(BackupCodec.validate(valid).toString().toByteArray(Charsets.UTF_8),Charsets.UTF_8))
        assertEquals("Inspecionar 😀",first(restored,"events").getString("description"))
        assertEquals("á𝄞é",first(restored,"events").getJSONObject("extension").getString("😀"))
    }
    @Test fun malformedUnicodeRestorePreservesEveryCollectionAndPerformsNoSave() {
        for (mode in listOf("merge","replace")) {
            val store=MemorySnapshotStore(fixture())
            val service=LivroService(store)
            val original=store.value.toString()
            val incoming=fixture(); first(incoming,"events").put("description","Broken\uD800").put("version",2)
            val error=assertThrows(IllegalArgumentException::class.java) { service.restore(incoming,mode,preventiveBackupConfirmed=true) }
            assertTrue(error.message.orEmpty().contains("Unicode"))
            assertEquals(original,store.value.toString())
            assertEquals(0,store.saves)
        }
    }
    @Test fun unknownMissingStoresAndUnsupportedVersionsAreRejected() {
        invalid("unknown") { it.getJSONObject("data").put("errorLogs", JSONArray()) }
        invalid("missing") { it.getJSONObject("data").remove("events") }
        for (value in listOf<Any>(2, true, "01", 1.5)) invalid("schema $value") { it.put("schemaVersion", value) }
        val legacy=fixture().put("schemaVersion","1")
        assertEquals("1", BackupCodec.validate(legacy).get("schemaVersion"))
    }
    @Test fun requiredFunctionalFieldsCannotBeSilentlyDefaulted() {
        val schema=mapOf(
            "consoles" to "id name active createdAt updatedAt version synchronizationStatus",
            "operationalUnits" to "id name active createdAt updatedAt version synchronizationStatus",
            "pipelines" to "id name active createdAt updatedAt version synchronizationStatus consoleId",
            "pipelineOperationalUnits" to "id pipelineId uoId createdAt version synchronizationStatus",
            "equipmentTypes" to "id name active createdAt updatedAt version synchronizationStatus uoId",
            "equipmentTags" to "id tag uoId equipmentTypeId active createdAt updatedAt version synchronizationStatus",
            "events" to "id consoleId pipelineId uoId equipmentTypeId tagId scheduledDate scheduledTime scheduledAt description notes priority status hasAlarm useDefaultAlarmSettings alarmMinutesBefore alarmAudio alarmVisual alarmNotification alarmRepeat alarmRepeatInterval alarmMaxRepeats alarmState alarmSnoozedUntil alarmTriggerCount lastAlarmTriggeredAt completedAt completedTimeDiffMinutes completionNote active createdAt updatedAt version synchronizationStatus",
            "eventHistory" to "id eventId action timestamp description previousValue newValue localUser",
            "colorRanges" to "id name color minMinutes maxMinutes priority blink sound active",
            "settings" to "key value")
        for ((store,fields) in schema) for (field in fields.split(' ')) invalid("$store.$field") { first(it,store).remove(field) }
    }
    @Test fun stringsAndBooleansCannotMasqueradeAsNumbersOrOtherTypes() {
        for (key in listOf("version","alarmMinutesBefore","alarmRepeatInterval","alarmMaxRepeats","alarmTriggerCount")) {
            invalid("string $key") { first(it,"events").put(key,"1") }
            invalid("boolean $key") { first(it,"events").put(key,true) }
            invalid("fraction $key") { first(it,"events").put(key,1.5) }
        }
        for (key in listOf("active","hasAlarm","alarmAudio","alarmVisual","alarmNotification","alarmRepeat","useDefaultAlarmSettings")) invalid(key) { first(it,"events").put(key,1) }
        for (key in listOf("description","notes","completionNote","createdBy","localUser","synchronizationStatus")) invalid(key) { first(it,"events").put(key,JSONObject()) }
        invalid("snooze string") { first(it,"events").put("alarmSnoozedUntil","123") }
        invalid("completion string") { first(it,"events").put("completedTimeDiffMinutes","3") }
        invalid("unsafe integer") { first(it,"events").put("version",9007199254740992L) }
    }
    @Test fun datesUseStrictCalendarAndTimeParsing() {
        for (date in listOf("2026-02-31T00:00:00Z","2026-13-01T00:00:00Z","2026-01-01T24:00:00Z","2026-01-01")) invalid(date) { it.put("exportedAt",date) }
        invalid("impossible local") { first(it,"events").put("scheduledDate","2026-02-31") }
        invalid("invalid local time") { first(it,"events").put("scheduledTime","24:00") }
        invalid("invalid scheduled ISO") { first(it,"events").put("scheduledAt","2026-02-31T12:00:00Z") }
        invalid("completion required") { first(it,"events").put("status","concluido") }
        invalid("history timestamp") { first(it,"eventHistory").put("timestamp","yesterday") }
        invalid("negative snooze") { first(it,"events").put("alarmSnoozedUntil",-1) }
    }
    @Test fun portableBackupsKeepOriginalInstantWithoutAssumingImporterTimeZone() {
        val incoming=fixture()
        first(incoming,"events").put("scheduledAt","2026-10-31T15:00:00Z")
        val retained=first(BackupCodec.validate(incoming),"events")
        assertEquals("2026-10-31T15:00:00Z",retained.getString("scheduledAt"))
        assertEquals("12:00",retained.getString("scheduledTime"))
        invalid("outside legal zone") { first(it,"events").put("scheduledAt","2026-11-02T12:00:00Z") }
        invalid("non-minute offset") { first(it,"events").put("scheduledAt","2026-10-31T12:00:01Z") }
    }
    @Test fun unsafePngLinksIdentifiersAndInvalidEnumsAreRejected() {
        invalid("svg") { first(it,"events").put("stylusDrawing","data:image/svg+xml,<svg onload=alert(1)>") }
        invalid("invalid base64") { first(it,"events").put("stylusDrawing","data:image/png;base64,iVBORw0KGgo!!!") }
        invalid("javascript") { first(it,"events").put("href","javascript:alert(1)") }
        invalid("id") { first(it,"events").put("id","__proto__") }
        invalid("status") { first(it,"events").put("status","unknown") }
        invalid("priority") { first(it,"events").put("priority","unknown") }
        invalid("state") { first(it,"events").put("alarmState","unknown") }
        invalid("color") { first(it,"colorRanges").put("color","red;display:none") }
    }
    @Test fun pngHeadersCannotRequestUnboundedNativeBitmapAllocations() {
        invalid("truncated PNG") { first(it,"events").put("stylusDrawing","data:image/png;base64,iVBORw0KGgo=") }
        for ((width,height) in listOf(100000 to 100000,8193 to 1,4096 to 4096,0 to 1)) {
            val bytes=Base64.getDecoder().decode(PNG.substringAfter(','))
            ByteBuffer.wrap(bytes).putInt(16,width).putInt(20,height)
            val checksum=CRC32().apply { update(bytes,12,17) }.value.toInt()
            ByteBuffer.wrap(bytes).putInt(29,checksum)
            invalid("PNG ${width}x$height") { first(it,"events").put("stylusDrawing","data:image/png;base64,"+Base64.getEncoder().encodeToString(bytes)) }
        }
        val corrupted=Base64.getDecoder().decode(PNG.substringAfter(',')); corrupted[12]='J'.code.toByte()
        invalid("not IHDR") { first(it,"events").put("stylusDrawing","data:image/png;base64,"+Base64.getEncoder().encodeToString(corrupted)) }
    }
    @Test fun duplicateAndOrphanOrIncompatibleRelationshipsAreRejected() {
        invalid("duplicate id") { rows(it,"consoles").put(JSONObject(first(it,"consoles").toString())) }
        invalid("duplicate name") { rows(it,"consoles").put(JSONObject(first(it,"consoles").toString()).put("id","other").put("name"," c04 ")) }
        invalid("missing console") { first(it,"pipelines").put("consoleId","missing") }
        invalid("one linked UO") { rows(it,"pipelineOperationalUnits").remove(1) }
        invalid("duplicate relationship") { rows(it,"pipelineOperationalUnits").put(JSONObject(first(it,"pipelineOperationalUnits").toString()).put("id","other")) }
        invalid("tag type UO mismatch") { first(it,"equipmentTags").put("uoId","u2") }
        invalid("event hierarchy") { first(it,"events").put("uoId","u2") }
        invalid("history orphan") { first(it,"eventHistory").put("eventId","missing") }
        invalid("active console") { first(it,"settings").getJSONObject("value").put("activeConsoleId","missing") }
        val inactive=fixture(); first(inactive,"operationalUnits").put("active",false)
        assertFalse(first(BackupCodec.validate(inactive),"operationalUnits").getBoolean("active"))
    }
    @Test fun browserWhitespaceCannotHideBlankTextOrDuplicateBusinessKeys() {
        invalid("BOM description") { first(it,"events").put("description","\uFEFF \uFEFF") }
        invalid("BOM catalogue key") {
            rows(it,"consoles").put(JSONObject(first(it,"consoles").toString()).put("id","other").put("name","\uFEFFC04\uFEFF"))
        }
    }
    @Test fun rangesAndSettingsAreBoundedAndStrictWhileLegacyMetadataStaysOptional() {
        invalid("range gap") { first(it,"colorRanges").put("minMinutes",1) }
        invalid("empty ranges") { it.getJSONObject("data").put("colorRanges",JSONArray()) }
        invalid("zero span") { first(it,"colorRanges").put("maxMinutes",0) }
        for ((key,value) in listOf("soundVolume" to 101,"soundVolume" to "50","repeatIntervalMinutes" to 0,"maxRepeats" to -1,"defaultLeadTimeMinutes" to -1,"soundEnabled" to "true","theme" to "other","soundType" to "other","viewMode" to "other","responsiveLayoutMode" to "other","lastBackupAt" to "today")) invalid(key) { first(it,"settings").getJSONObject("value").put(key,value) }
        invalid("unknown settings key") { first(it,"settings").put("key","other") }
        invalid("missing settings value") { first(it,"settings").getJSONObject("value").remove("soundEnabled") }
        val legacy=fixture()
        for (key in listOf("stylusDrawing","createdBy","completedBy")) first(legacy,"events").remove(key)
        assertEquals(1, rows(BackupCodec.validate(legacy),"settings").length())
    }
    @Test fun mergeInsertsAndUpdatesWithoutMutatingEitherInput() {
        val current=fixture(); val incoming=fixture()
        first(incoming,"events").put("description","Revised").put("version",2).put("updatedAt","2026-11-01T00:00:00Z")
        rows(incoming,"consoles").put(JSONObject(first(incoming,"consoles").toString()).put("id","c2").put("name","C08"))
        val original=current.toString(); val imported=incoming.toString()
        val result=BackupCodec.merge(current,incoming)
        assertTrue(result.applied); assertTrue(result.conflicts.isEmpty()); assertEquals(1,result.inserted); assertEquals(1,result.updated)
        assertEquals("Revised",first(result.snapshot,"events").getString("description"))
        assertEquals(2,rows(result.snapshot,"consoles").length())
        assertEquals(original,current.toString()); assertEquals(imported,incoming.toString())
    }
    @Test fun sameRevisionConflictRollsBackInsertionsInEveryStore() {
        val current=fixture(); val incoming=fixture()
        rows(incoming,"consoles").put(JSONObject(first(incoming,"consoles").toString()).put("id","c2").put("name","C08"))
        first(incoming,"events").put("description","Conflict")
        val result=BackupCodec.merge(current,incoming)
        assertFalse(result.applied); assertEquals(0,result.inserted); assertEquals(0,result.updated)
        assertTrue(result.conflicts.any { it.contains("same-revision-different-content") })
        assertEquals(current.toString(),result.snapshot.toString())
        first(result.snapshot,"events").put("description","Detached")
        assertEquals("Inspecionar",first(current,"events").getString("description"))
    }
    @Test fun olderVersionsOrOlderTimestampsNeverOverwriteCurrent() {
        for ((version,timestamp) in listOf(1 to "2026-11-01T00:00:00Z", 3 to "2026-10-30T00:00:00Z")) {
            val current=fixture(); first(current,"events").put("version",2)
            val incoming=fixture(); first(incoming,"events").put("version",version).put("updatedAt",timestamp).put("description","Old")
            val result=BackupCodec.merge(current,incoming)
            assertTrue(result.applied); assertEquals(0,result.updated); assertEquals("Inspecionar",first(result.snapshot,"events").getString("description"))
        }
    }
    @Test fun businessKeyConflictsAreAllOrNothingEvenWhenEachInputIsValid() {
        val current=fixture(); val incoming=fixture()
        rows(incoming,"consoles").put(JSONObject(first(incoming,"consoles").toString()).put("id","new").put("name","C08"))
        rows(current,"consoles").put(JSONObject(first(current,"consoles").toString()).put("id","old").put("name","c08"))
        val result=BackupCodec.merge(current,incoming)
        assertFalse(result.applied); assertEquals(0,result.inserted); assertTrue(result.conflicts.any { it.contains("duplicate-business-key") })
        assertEquals(current.toString(),result.snapshot.toString())
    }
    @Test fun csvHasBomSemicolonsEscapingFormulaDefenceAndActiveStatusFilters() {
        val snapshot=fixture(); val event=first(snapshot,"events")
        event.put("description","  =SUM(1;2)").put("notes","Linha 1\n\"Linha 2\"")
        val pending=BackupCodec.csv(snapshot,"pending")
        assertTrue(pending.startsWith("\uFEFFID;Situação;Console;Duto;UO;"))
        assertTrue(pending.contains("\"'  =SUM(1;2)\"")); assertTrue(pending.contains("\"Linha 1\n\"\"Linha 2\"\"\""))
        assertEquals(1,BackupCodec.csv(snapshot,"completed").split("\r\n").size)
        event.put("active",false)
        assertEquals(1,BackupCodec.csv(snapshot,"all").split("\r\n").size)
        first(snapshot,"consoles").put("name","@command")
        val cadastros=BackupCodec.csv(snapshot,"cadastros")
        assertTrue(cadastros.startsWith("\uFEFFTipo de Registro;")); assertTrue(cadastros.contains("'@command"))
        try { BackupCodec.csv(snapshot,"unknown"); fail("Unknown CSV type accepted") } catch (_: IllegalArgumentException) { }
    }
    companion object {
        private const val PNG="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        fun fixture(): JSONObject = JSONObject("""{
          "application":"Controle de Previsões em Dutos","schemaVersion":1,"exportedAt":"2026-10-31T12:00:00Z","data":{
            "consoles":[{"id":"c1","name":"C04","active":true,"createdAt":"2026-10-31T12:00:00Z","updatedAt":"2026-10-31T12:00:00Z","version":1,"synchronizationStatus":"local-only"}],
            "operationalUnits":[{"id":"u1","name":"REFAP","active":true,"createdAt":"2026-10-31T12:00:00Z","updatedAt":"2026-10-31T12:00:00Z","version":1,"synchronizationStatus":"local-only"},{"id":"u2","name":"TEDEP","active":true,"createdAt":"2026-10-31T12:00:00Z","updatedAt":"2026-10-31T12:00:00Z","version":1,"synchronizationStatus":"local-only"}],
            "pipelines":[{"id":"p1","name":"OSCAN","consoleId":"c1","active":true,"createdAt":"2026-10-31T12:00:00Z","updatedAt":"2026-10-31T12:00:00Z","version":1,"synchronizationStatus":"local-only"}],
            "pipelineOperationalUnits":[{"id":"l1","pipelineId":"p1","uoId":"u1","createdAt":"2026-10-31T12:00:00Z","version":1,"synchronizationStatus":"local-only"},{"id":"l2","pipelineId":"p1","uoId":"u2","createdAt":"2026-10-31T12:00:00Z","version":1,"synchronizationStatus":"local-only"}],
            "equipmentTypes":[{"id":"t1","name":"Bomba","uoId":"u1","active":true,"createdAt":"2026-10-31T12:00:00Z","updatedAt":"2026-10-31T12:00:00Z","version":1,"synchronizationStatus":"local-only"}],
            "equipmentTags":[{"id":"tag1","tag":"BB-101A","uoId":"u1","equipmentTypeId":"t1","active":true,"createdAt":"2026-10-31T12:00:00Z","updatedAt":"2026-10-31T12:00:00Z","version":1,"synchronizationStatus":"local-only"}],
            "events":[{"id":"e1","consoleId":"c1","pipelineId":"p1","uoId":"u1","equipmentTypeId":"t1","tagId":"tag1","scheduledDate":"2026-10-31","scheduledTime":"12:00","scheduledAt":"2026-10-31T12:00:00Z","description":"Inspecionar","notes":"","priority":"Normal","status":"pendente","hasAlarm":true,"useDefaultAlarmSettings":false,"alarmMinutesBefore":0,"alarmAudio":true,"alarmVisual":true,"alarmNotification":false,"alarmRepeat":false,"alarmRepeatInterval":2,"alarmMaxRepeats":0,"alarmState":"idle","alarmSnoozedUntil":null,"alarmTriggerCount":0,"lastAlarmTriggeredAt":null,"completedAt":null,"completedTimeDiffMinutes":null,"completionNote":"","active":true,"createdAt":"2026-10-31T12:00:00Z","updatedAt":"2026-10-31T12:00:00Z","version":1,"synchronizationStatus":"local-only","stylusDrawing":"$PNG","createdBy":"Operador","extension":{"retained":"literal"}}],
            "eventHistory":[{"id":"h1","eventId":"e1","action":"criacao","timestamp":"2026-10-31T12:00:00Z","description":"Criada","previousValue":"before","newValue":"after","localUser":"Operador"}],
            "colorRanges":[{"id":"range","name":"Normal","color":"#16a34a","minMinutes":0,"maxMinutes":999999,"priority":1,"blink":false,"sound":false,"active":true}],
            "settings":[{"key":"app_settings","value":{"localUserName":"Operador","soundEnabled":true,"soundType":"chime","soundVolume":80,"visualAlertEnabled":true,"notificationEnabled":false,"repeatAlarm":true,"repeatIntervalMinutes":2,"maxRepeats":5,"defaultLeadTimeMinutes":15,"activeConsoleId":"c1"}}]
          }}""")
    }
}
