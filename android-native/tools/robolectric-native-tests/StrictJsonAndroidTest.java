package br.com.livrodeprevisoes.app;

import br.com.livrodeprevisoes.data.FileSnapshotStore;
import br.com.livrodeprevisoes.domain.BackupCodec;
import br.com.livrodeprevisoes.domain.LivroService;
import br.com.livrodeprevisoes.domain.StrictJson;
import android.app.Activity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.time.Instant;
import java.time.ZoneOffset;
import org.json.JSONObject;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.Robolectric;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.android.controller.ActivityController;
import org.robolectric.annotation.Config;
import org.robolectric.annotation.GraphicsMode;
import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
@Config(manifest = Config.NONE, sdk = 36)
@GraphicsMode(GraphicsMode.Mode.LEGACY)
public class StrictJsonAndroidTest {
    @Test public void completeBackupParsesButAnyTrailingDocumentDataIsRejectedOnAndroid() throws Exception {
        String valid = fixture().snapshot().toString();
        assertEquals(1, BackupCodec.INSTANCE.parse(valid).getInt("schemaVersion"));
        for (String suffix : new String[] {"TRAILING", "{}", "[]", " false"}) {
            rejectBackup(valid + suffix);
        }
    }
    @Test public void nonJsonSyntaxNeverReachesAndroidPermissiveObjectParser() {
        for (String invalid : new String[] {"{'a':1}", "{a:1}", "{\"a\":1,}", "{\"a\":[1,]}",
                "{\"a\":01}", "{\"a\":NaN}", "{\"a\":Infinity}", "{\"a\":1e9999}", "{\"a\":+1}", "{\"a\":1}/*comment*/"}) {
            try { StrictJson.INSTANCE.parseObject(invalid); fail("Accepted non-JSON: " + invalid); }
            catch (IllegalArgumentException expected) { /* strict boundary */ }
        }
    }
    @Test public void escapedStringsScientificNumbersAndLastDuplicateValueRemainValid() throws Exception {
        JSONObject parsed = StrictJson.INSTANCE.parseObject("\ufeff {\"text\":\"line\\nquote\\\"slash\\\\\\u00e7\",\"n\":-1.25e+2,\"dup\":1,\"d\\u0075p\":2} \r\n");
        assertEquals("line\nquote\"slash\\ç", parsed.getString("text"));
        assertEquals(-125.0, parsed.getDouble("n"), 0.0);
        assertEquals(2, parsed.getInt("dup"));
    }
    @Test public void fileSnapshotStoreRejectsTrailingBytesWithoutOverwritingThem() throws Exception {
        File path = new File(RuntimeEnvironment.getApplication().getFilesDir(), "strict-corrupt.json");
        byte[] corrupt = (fixture().snapshot().toString() + "TRAILING").getBytes(StandardCharsets.UTF_8);
        Files.write(path.toPath(), corrupt);
        try { new FileSnapshotStore(path).load(); fail("Store accepted trailing garbage"); }
        catch (IllegalArgumentException expected) { /* must remain invalid */ }
        assertArrayEquals(corrupt, Files.readAllBytes(path.toPath()));
    }
    @Test public void corruptLocalJsonLaunchShowsPreservationFallbackAndKeepsOriginalBytes() throws Exception {
        File path = new File(RuntimeEnvironment.getApplication().getFilesDir(), "livro-data.json");
        byte[] corrupt = (fixture().snapshot().toString() + "TRAILING").getBytes(StandardCharsets.UTF_8);
        Files.write(path.toPath(), corrupt);
        RuntimeEnvironment.getApplication().getApplicationInfo().targetSdkVersion = 36;
        try (ActivityController<MainActivity> controller = Robolectric.buildActivity(MainActivity.class).create().start()) {
            MainActivity activity = controller.get();
            assertFalse("Invalid local JSON must not initialize a normal dashboard", activity.getInitialized());
            assertTrue(containsText(activity.findViewById(android.R.id.content), "Dados preservados"));
            assertArrayEquals(corrupt, Files.readAllBytes(path.toPath()));
        }
    }
    @Test public void unpairedSurrogatesAreRejectedAndValidEmojiRoundTripThroughNativeUtf8() throws Exception {
        for (String malformed : new String[] {"{\"value\":\"\\uD800\"}", "{\"value\":\"\\uDFFF\"}",
                "{\"\\uD800\":1}", "{\"\\uDFFF\":1}"}) {
            try { StrictJson.INSTANCE.parseObject(malformed); fail("Accepted escaped lone surrogate: " + malformed); }
            catch (IllegalArgumentException expected) { /* lossless UTF-8 boundary */ }
        }
        LivroService service = fixture();
        service.loadDemoData(true);
        for (char lone : new char[] {(char) 0xd800, (char) 0xdfff}) {
            String invalid = new String(new char[] {lone});
            JSONObject invalidValue = service.snapshot();
            invalidValue.getJSONObject("data").getJSONArray("events").getJSONObject(0).put("description", invalid);
            try { BackupCodec.INSTANCE.validate(invalidValue); fail("Accepted in-memory lone-surrogate description"); }
            catch (IllegalArgumentException expected) { /* must reject before persistence */ }
            JSONObject invalidKey = service.snapshot();
            invalidKey.put(invalid, "extension value");
            try { BackupCodec.INSTANCE.validate(invalidKey); fail("Accepted in-memory lone-surrogate object key"); }
            catch (IllegalArgumentException expected) { /* every JSON key is validated */ }
        }

        String rocket = new String(Character.toChars(0x1f680));
        JSONObject parsed = StrictJson.INSTANCE.parseObject("{\"value\":\"\\uD83D\\uDE80\",\"\\uD83D\\uDE80\":\"paired key\"}");
        assertEquals(rocket, parsed.getString("value"));
        assertEquals("paired key", parsed.getString(rocket));
        JSONObject valid = service.snapshot();
        valid.getJSONObject("data").getJSONArray("events").getJSONObject(0).put("description", "Valid emoji " + rocket);
        valid.put(rocket, rocket);
        File path = new File(RuntimeEnvironment.getApplication().getFilesDir(), "emoji-roundtrip.json");
        FileSnapshotStore store = new FileSnapshotStore(path);
        store.save(BackupCodec.INSTANCE.validate(valid));
        JSONObject reloaded = store.load();
        assertEquals("Valid emoji " + rocket, reloaded.getJSONObject("data").getJSONArray("events").getJSONObject(0).getString("description"));
        assertEquals(rocket, reloaded.getString(rocket));
        assertTrue(new String(Files.readAllBytes(path.toPath()), StandardCharsets.UTF_8).contains(rocket));

        JSONObject escapedFile = service.snapshot();
        escapedFile.getJSONObject("data").getJSONArray("events").getJSONObject(0).put("description", "SURROGATE_PLACEHOLDER");
        byte[] original = escapedFile.toString().replace("SURROGATE_PLACEHOLDER", "\\uD800").getBytes(StandardCharsets.UTF_8);
        Files.write(path.toPath(), original);
        try { store.load(); fail("Accepted escaped unpaired surrogate in stored JSON"); }
        catch (IllegalArgumentException expected) { /* preserve original bytes for recovery */ }
        assertArrayEquals(original, Files.readAllBytes(path.toPath()));
    }

    private static LivroService fixture() {
        return new LivroService(new FileSnapshotStore(new File(RuntimeEnvironment.getApplication().getFilesDir(), "strict-fixture.json")),
                () -> Instant.parse("2030-01-01T12:00:00Z"), ZoneOffset.UTC);
    }
    private static void rejectBackup(String text) {
        try { BackupCodec.INSTANCE.parse(text); fail("Accepted trailing backup data"); }
        catch (IllegalArgumentException expected) { /* strict boundary */ }
    }
    private static boolean containsText(View view, String expected) {
        if (view instanceof TextView && expected.equals(((TextView) view).getText().toString())) return true;
        if (view instanceof ViewGroup) {
            ViewGroup group = (ViewGroup) view;
            for (int i = 0; i < group.getChildCount(); i++) if (containsText(group.getChildAt(i), expected)) return true;
        }
        return false;
    }
}
