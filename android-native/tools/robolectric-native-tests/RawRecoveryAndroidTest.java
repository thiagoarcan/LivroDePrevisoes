package br.com.livrodeprevisoes.app;

import android.app.Activity;
import android.app.AlertDialog;
import android.os.Looper;
import android.content.Intent;
import android.net.Uri;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import java.io.ByteArrayOutputStream;
import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import org.json.JSONObject;
import org.robolectric.shadows.ShadowAlertDialog;
import java.io.File;
import java.nio.file.Files;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.Robolectric;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.Shadows;
import org.robolectric.android.controller.ActivityController;
import org.robolectric.annotation.Config;
import org.robolectric.annotation.GraphicsMode;
import org.robolectric.shadows.ShadowActivity;
import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
@Config(manifest = Config.NONE, sdk = 36)
@GraphicsMode(GraphicsMode.Mode.LEGACY)
public class RawRecoveryAndroidTest {
    @Test public void rawRecoveryExportPreservesMalformedUtf8BytesExactly() throws Exception {
        byte[] damaged = {123, 34, 120, 34, 58, 34, (byte) 0xc3, 0x28, 34, 125};
        File database = new File(RuntimeEnvironment.getApplication().getFilesDir(), "livro-data.json");
        Files.write(database.toPath(), damaged);
        RuntimeEnvironment.getApplication().getApplicationInfo().targetSdkVersion = 36;
        try (ActivityController<MainActivity> controller = Robolectric.buildActivity(MainActivity.class).create().start()) {
            MainActivity activity = controller.get();
            assertFalse("Malformed UTF-8 must show preservation recovery, not initialize", activity.getInitialized());
            Button export = findButton(activity.findViewById(android.R.id.content), "Salvar cópia original");
            assertNotNull(export);
            assertTrue(export.performClick());
            ShadowActivity.IntentForResult started = Shadows.shadowOf(activity).getNextStartedActivityForResult();
            assertNotNull(started);
            assertEquals(701, started.requestCode);
            assertEquals(Intent.ACTION_CREATE_DOCUMENT, started.intent.getAction());
            assertEquals("raw", activity.getExportGate().getPending());
            Uri destination = Uri.parse("content://fixture.documents/original-damaged.json");
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            Shadows.shadowOf(activity.getContentResolver()).registerOutputStream(destination, output);
            Shadows.shadowOf(activity).receiveResult(started.intent, Activity.RESULT_OK, new Intent().setData(destination));
            assertArrayEquals("Recovery export must not replace malformed UTF-8 or normalize original bytes", damaged, output.toByteArray());
            assertArrayEquals("Private original must remain untouched", damaged, Files.readAllBytes(database.toPath()));
            assertFalse(activity.getInitialized());
            assertNull(activity.getExportGate().getPending());
            assertFalse(activity.getExportFile().exists());
        }
    }
    @Test public void malformedUtf8InValidatedStagedReplaceCannotMutateLiveDataAfterPreventiveBackup() throws Exception {
        RuntimeEnvironment.getApplication().getApplicationInfo().targetSdkVersion = 36;
        try (ActivityController<MainActivity> controller = Robolectric.buildActivity(MainActivity.class).create().start()) {
            MainActivity activity = controller.get();
            assertTrue(activity.getInitialized());
            AlertDialog onboarding = ShadowAlertDialog.getLatestAlertDialog();
            if (onboarding != null) onboarding.dismiss();
            activity.getService().loadDemoData(true);
            activity.setActiveConsole("");
            activity.navigate("backup", null);
            File live = new File(activity.getFilesDir(), "livro-data.json");
            byte[] original = Files.readAllBytes(live.toPath());
            JSONObject incoming = activity.getService().snapshot();
            incoming.getJSONObject("data").getJSONArray("events").getJSONObject(0).put("description", "STAGED_UTF8_SENTINEL");
            Button replace = findButton(activity.findViewById(android.R.id.content), "Substituir todos os dados");
            assertNotNull(replace);
            assertTrue(replace.performClick());
            ShadowActivity.IntentForResult selected = Shadows.shadowOf(activity).getNextStartedActivityForResult();
            assertEquals(Intent.ACTION_OPEN_DOCUMENT, selected.intent.getAction());
            Uri imported = Uri.parse("content://fixture.documents/valid-before-staging.json");
            Shadows.shadowOf(activity.getContentResolver()).registerInputStream(imported,
                    new ByteArrayInputStream(incoming.toString().getBytes(StandardCharsets.UTF_8)));
            Shadows.shadowOf(activity).receiveResult(selected.intent, Activity.RESULT_OK, new Intent().setData(imported));
            assertTrue("Validated import is staged before preventive confirmation", activity.getImportFile().exists());
            String staged = new String(Files.readAllBytes(activity.getImportFile().toPath()), StandardCharsets.UTF_8);
            int marker = staged.indexOf("STAGED_UTF8_SENTINEL");
            assertTrue(marker >= 0);
            ByteArrayOutputStream corrupt = new ByteArrayOutputStream();
            corrupt.write(staged.substring(0, marker).getBytes(StandardCharsets.UTF_8));
            corrupt.write(0xc3); corrupt.write(0x28);
            corrupt.write(staged.substring(marker + "STAGED_UTF8_SENTINEL".length()).getBytes(StandardCharsets.UTF_8));
            Files.write(activity.getImportFile().toPath(), corrupt.toByteArray());
            AlertDialog confirmation = ShadowAlertDialog.getLatestAlertDialog();
            confirmation.getButton(AlertDialog.BUTTON_POSITIVE).performClick();
            Shadows.shadowOf(Looper.getMainLooper()).idle();
            ShadowActivity.IntentForResult exported = Shadows.shadowOf(activity).getNextStartedActivityForResult();
            assertNotNull(exported);
            assertEquals(Intent.ACTION_CREATE_DOCUMENT, exported.intent.getAction());
            assertEquals("replace", activity.getExportGate().getPending());
            Uri preventive = Uri.parse("content://fixture.documents/preventive-before-invalid-stage.json");
            ByteArrayOutputStream backup = new ByteArrayOutputStream();
            Shadows.shadowOf(activity.getContentResolver()).registerOutputStream(preventive, backup);
            Shadows.shadowOf(activity).receiveResult(exported.intent, Activity.RESULT_OK, new Intent().setData(preventive));
            assertNotNull("Preventive backup itself completed successfully", new JSONObject(backup.toString("UTF-8")).getJSONObject("data"));
            assertArrayEquals("A changed staged document must be strictly decoded again before replacement", original, Files.readAllBytes(live.toPath()));
            assertTrue(activity.getImportFile().exists());
            assertArrayEquals(corrupt.toByteArray(), Files.readAllBytes(activity.getImportFile().toPath()));
            assertNull(activity.getExportGate().getPending());
            assertFalse(activity.getExportFile().exists());
            assertTrue(activity.getInitialized());
        }
    }

    private static Button findButton(View view, String caption) {
        if (view instanceof Button && caption.equals(((Button) view).getText().toString())) return (Button) view;
        if (view instanceof ViewGroup) {
            ViewGroup group = (ViewGroup) view;
            for (int i = 0; i < group.getChildCount(); i++) {
                Button result = findButton(group.getChildAt(i), caption);
                if (result != null) return result;
            }
        }
        return null;
    }
}
