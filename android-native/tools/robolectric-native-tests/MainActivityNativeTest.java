package br.com.livrodeprevisoes.app;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.res.Configuration;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Spinner;
import android.os.Looper;
import org.json.JSONArray;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import org.json.JSONObject;
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
import org.robolectric.shadows.ShadowAlertDialog;
import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
@Config(manifest = Config.NONE, sdk = 36)
@GraphicsMode(GraphicsMode.Mode.LEGACY)
public class MainActivityNativeTest {
    private static final String PNG = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aCr8AAAAASUVORK5CYII=";

    @Test public void emptyDatabaseLaunchInitializesRealMainActivity() {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            assertEquals("dashboard", activity.getScreen());
            assertEquals(0, activity.getService().rows("events").size());
            assertTrue(texts(activity).contains("LIVRO DE PREVISÕES"));
        }
    }

    @Test @Config(qualifiers = "w800dp")
    public void allNineNativeScreensNavigateWithRealDemoService() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            activity.getService().loadDemoData(true);
            activity.setActiveConsole("");
            activity.render();
            assertTrue(activity.getService().rows("events").size() > 0);
            String[][] screens = {
                {"new", "Nova previsão", "Nova previsão"},
                {"pending", "Pendentes", "Pendentes"},
                {"completed", "Concluídos", "Concluídos"},
                {"registry", "Cadastros", "Cadastros"},
                {"alerts", "Alertas", "Alertas"},
                {"colors", "Cores e temas", "Cores e temas"},
                {"backup", "Backup", "Backup e migração"},
                {"diagnostics", "Diagnóstico", "Diagnóstico"},
                {"dashboard", "Painel", "Painel operacional"}
            };
            for (String[] screen : screens) {
                click(activity, screen[1]);
                assertEquals("Destination: " + screen[1], screen[0], activity.getScreen());
                assertTrue("Missing heading " + screen[2] + ": " + texts(activity), texts(activity).contains(screen[2]));
                assertTrue(activity.getInitialized());
            }
            JSONObject event = activity.getService().rows("events").get(0);
            activity.setScreen(event.optString("status").equals("concluido") ? "completed" : "pending");
            activity.setDetailId(event.getString("id"));
            activity.render();
            assertTrue(texts(activity).contains(event.getString("description")));
        }
    }

    @Test public void safIntentsAndCancellationPreserveStoredDatabase() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            activity.getService().loadDemoData(true);
            activity.navigate("backup", null);
            byte[] before = database(activity);
            click(activity, "Salvar backup JSON completo");
            ShadowActivity.IntentForResult exported = Shadows.shadowOf(activity).getNextStartedActivityForResult();
            assertEquals(701, exported.requestCode);
            assertEquals(Intent.ACTION_CREATE_DOCUMENT, exported.intent.getAction());
            assertEquals("application/json", exported.intent.getType());
            assertTrue(exported.intent.hasCategory(Intent.CATEGORY_OPENABLE));
            Shadows.shadowOf(activity).receiveResult(exported.intent, Activity.RESULT_CANCELED, null);
            assertNull(activity.getExportGate().getPending());
            assertFalse(activity.getExportFile().exists());
            assertArrayEquals(before, database(activity));

            click(activity, "Importar e mesclar");
            ShadowActivity.IntentForResult imported = Shadows.shadowOf(activity).getNextStartedActivityForResult();
            assertEquals(702, imported.requestCode);
            assertEquals(Intent.ACTION_OPEN_DOCUMENT, imported.intent.getAction());
            assertTrue(imported.intent.hasCategory(Intent.CATEGORY_OPENABLE));
            Shadows.shadowOf(activity).receiveResult(imported.intent, Activity.RESULT_CANCELED, null);
            assertArrayEquals(before, database(activity));

            click(activity, "Limpar todos os dados");
            AlertDialog confirm = ShadowAlertDialog.getLatestAlertDialog();
            assertNotNull(confirm);
            confirm.getButton(AlertDialog.BUTTON_POSITIVE).performClick();
            Shadows.shadowOf(Looper.getMainLooper()).idle();
            ShadowActivity.IntentForResult preventive = Shadows.shadowOf(activity).getNextStartedActivityForResult();
            assertEquals(Intent.ACTION_CREATE_DOCUMENT, preventive.intent.getAction());
            assertEquals("clear", activity.getExportGate().getPending());
            Shadows.shadowOf(activity).receiveResult(preventive.intent, Activity.RESULT_CANCELED, null);
            assertNull(activity.getExportGate().getPending());
            assertArrayEquals("Canceled preventive export must not clear data", before, database(activity));
        }
    }

    @Test public void draftSurvivesOrientationAndActivityRecreationWithoutSavingAnEvent() throws Exception {
        ActivityController<MainActivity> original = launch();
        MainActivity activity = original.get();
        activity.navigate("new", new JSONObject().put("stylusDrawing", PNG));
        input(activity, "Descrição da atividade *").setText("Rascunho de inspeção preservado");
        input(activity, "Notas complementares").setText("Não salvar ao girar");
        input(activity, "Data * (AAAA-MM-DD)").setText("2030-01-02");
        input(activity, "Horário * (HH:mm)").setText("13:45");
        byte[] before = database(activity);
        EditText originalDescription = input(activity, "Descrição da atividade *");
        Configuration landscape = new Configuration(activity.getResources().getConfiguration());
        landscape.orientation = Configuration.ORIENTATION_LANDSCAPE;
        activity.onConfigurationChanged(landscape);
        assertSame(originalDescription, input(activity, "Descrição da atividade *"));
        Bundle state = new Bundle();
        original.saveInstanceState(state).stop().destroy();
        try (ActivityController<MainActivity> recreated = Robolectric.buildActivity(MainActivity.class).create(state).start()) {
            MainActivity restored = recreated.get();
            assertTrue(restored.getInitialized());
            assertEquals("new", restored.getScreen());
            assertEquals("Rascunho de inspeção preservado", input(restored, "Descrição da atividade *").getText().toString());
            assertEquals("Não salvar ao girar", input(restored, "Notas complementares").getText().toString());
            assertEquals("2030-01-02", input(restored, "Data * (AAAA-MM-DD)").getText().toString());
            assertEquals("13:45", input(restored, "Horário * (HH:mm)").getText().toString());
            assertEquals(PNG, restored.getDraftReader().invoke().getString("stylusDrawing"));
            assertEquals(0, restored.getService().rows("events").size());
            assertArrayEquals(before, database(restored));
        }
    }

    @Test public void importedDrawingIsUnchangedUntilUserEditsIt() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            DrawingView drawing = new DrawingView(activity, PNG, true);
            drawing.layout(0, 0, 1200, 440);
            assertEquals(PNG, drawing.png());
            drawing.layout(0, 0, 440, 1200);
            assertEquals(PNG, drawing.png());
            activity.navigate("new", new JSONObject().put("stylusDrawing", PNG));
            assertEquals(PNG, activity.getDraftReader().invoke().getString("stylusDrawing"));
            drawing.clear();
            assertEquals("", drawing.png());
        }
    }

    @Test public void deniedNotificationPermissionRendersDeniedStatusWithoutStartingAudio() {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            Shadows.shadowOf(RuntimeEnvironment.getApplication()).denyPermissions(Manifest.permission.POST_NOTIFICATIONS);
            activity.navigate("alerts", null);
            click(activity, "Permitir notificações Android");
            activity.onRequestPermissionsResult(7401, new String[] {Manifest.permission.POST_NOTIFICATIONS}, new int[] {PackageManager.PERMISSION_DENIED});
            assertEquals("negada", activity.getAlerts().permissionState());
            assertTrue(texts(activity).contains("Notificações: negada"));
            assertEquals("alerts", activity.getScreen());
        }
    }

    @Test public void providerWriteAndCloseFailuresNeverClearDataOrMarkBackup() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            activity.getService().loadDemoData(true);
            activity.navigate("backup", null);
            byte[] before = database(activity);
            for (boolean failClose : new boolean[] {false, true}) {
                click(activity, "Limpar todos os dados");
                ShadowAlertDialog.getLatestAlertDialog().getButton(AlertDialog.BUTTON_POSITIVE).performClick();
                Shadows.shadowOf(Looper.getMainLooper()).idle();
                ShadowActivity.IntentForResult started = Shadows.shadowOf(activity).getNextStartedActivityForResult();
                assertNotNull(started);
                assertEquals("clear", activity.getExportGate().getPending());
                Uri document = Uri.parse("content://fixture.documents/failure-" + failClose);
                OutputStream failing = failClose ? new ByteArrayOutputStream() {
                    @Override public void close() throws IOException { throw new IOException("fixture provider close failed"); }
                } : new OutputStream() {
                    @Override public void write(int value) throws IOException { throw new IOException("fixture provider write failed"); }
                };
                Shadows.shadowOf(activity.getContentResolver()).registerOutputStream(document, failing);
                Shadows.shadowOf(activity).receiveResult(started.intent, Activity.RESULT_OK, new Intent().setData(document));
                assertNull(activity.getExportGate().getPending());
                assertFalse(activity.getExportFile().exists());
                assertArrayEquals("Provider failure must preserve database and lastBackupAt", before, database(activity));
                AlertDialog error = ShadowAlertDialog.getLatestAlertDialog();
                assertNotNull(error);
                error.dismiss();
            }
        }
    }

    @Test public void successfulJsonDocumentCloseRecordsBackupTimestamp() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            activity.navigate("backup", null);
            String previous = activity.getService().settings().optString("lastBackupAt");
            click(activity, "Salvar backup JSON completo");
            ShadowActivity.IntentForResult started = Shadows.shadowOf(activity).getNextStartedActivityForResult();
            assertNotNull(started);
            Uri document = Uri.parse("content://fixture.documents/success.json");
            final boolean[] closed = {false};
            ByteArrayOutputStream output = new ByteArrayOutputStream() {
                @Override public void close() throws IOException { closed[0] = true; super.close(); }
            };
            Shadows.shadowOf(activity.getContentResolver()).registerOutputStream(document, output);
            Shadows.shadowOf(activity).receiveResult(started.intent, Activity.RESULT_OK, new Intent().setData(document));
            assertTrue("Provider stream must close successfully", closed[0]);
            assertNotNull(new JSONObject(output.toString("UTF-8")).getJSONObject("data"));
            String recorded = activity.getService().settings().optString("lastBackupAt");
            assertNotEquals("Successful full backup must record a timestamp", previous, recorded);
            assertNotNull(java.time.Instant.parse(recorded));
            assertNull(activity.getExportGate().getPending());
            assertFalse(activity.getExportFile().exists());
        }
    }

    @Test public void inactiveOriginalHierarchyRemainsSelectedInEditForm() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            activity.getService().loadDemoData(true);
            JSONObject event = null;
            for (JSONObject candidate : activity.getService().rows("events")) {
                if (!candidate.optString("tagId").isEmpty() && !candidate.optString("tagId").equals("null")) { event = candidate; break; }
            }
            assertNotNull("Demo event with complete equipment hierarchy", event);
            JSONObject snapshot = activity.getService().snapshot();
            String[][] refs = {{"consoles", "consoleId", "Console *"}, {"pipelines", "pipelineId", "Duto *"},
                {"operationalUnits", "uoId", "Unidade operacional *"}, {"equipmentTypes", "equipmentTypeId", "Tipo de equipamento"},
                {"equipmentTags", "tagId", "TAG"}};
            for (String[] ref : refs) {
                JSONArray rows = snapshot.getJSONObject("data").getJSONArray(ref[0]);
                for (int i = 0; i < rows.length(); i++) {
                    JSONObject row = rows.getJSONObject(i);
                    if (row.getString("id").equals(event.getString(ref[1]))) row.put("active", false);
                }
            }
            activity.getStore().save(snapshot);
            activity.navigate("new", event);
            Shadows.shadowOf(Looper.getMainLooper()).idle();
            for (String[] ref : refs) {
                Spinner spinner = null;
                for (View view : views(activity)) if (view instanceof Spinner && ref[2].contentEquals(view.getContentDescription())) spinner = (Spinner) view;
                assertNotNull("Spinner " + ref[2], spinner);
                assertEquals("Inactive original must remain selected: " + ref[2], event.getString(ref[1]), ((Choice) spinner.getSelectedItem()).getId());
                assertEquals("Draft retains " + ref[1], event.getString(ref[1]), activity.getDraftReader().invoke().getString(ref[1]));
            }
        }
    }

    @Test public void pipelineEditorKeepsExistingInactiveLinkedUnitChecked() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            activity.getService().loadDemoData(true);
            JSONObject pipeline = activity.getService().rows("pipelines").get(0);
            String unitId = null;
            for (JSONObject link : activity.getService().rows("pipelineOperationalUnits")) {
                if (pipeline.getString("id").equals(link.getString("pipelineId"))) { unitId = link.getString("uoId"); break; }
            }
            assertNotNull(unitId);
            JSONObject snapshot = activity.getService().snapshot();
            JSONArray units = snapshot.getJSONObject("data").getJSONArray("operationalUnits");
            String unitName = null;
            for (int i = 0; i < units.length(); i++) {
                JSONObject unit = units.getJSONObject(i);
                if (unit.getString("id").equals(unitId)) { unit.put("active", false); unitName = unit.getString("name"); }
            }
            assertNotNull(unitName);
            activity.getStore().save(snapshot);
            activity.navigate("registry", null);
            RegistryScreensKt.registryEditor(activity, "pipelines", pipeline);
            AlertDialog editor = ShadowAlertDialog.getLatestAlertDialog();
            assertNotNull(editor);
            List<View> dialogViews = new ArrayList<>();
            collect(editor.getWindow().getDecorView(), dialogViews);
            CheckBox originalUnit = null;
            for (View view : dialogViews) {
                if (view instanceof CheckBox && ((CheckBox) view).getText().toString().startsWith(unitName)) originalUnit = (CheckBox) view;
            }
            assertNotNull("Existing inactive linked UO must still be offered", originalUnit);
            assertTrue("Existing inactive linked UO must remain checked", originalUnit.isChecked());
            assertTrue("Inactive option is explicitly labelled", originalUnit.getText().toString().contains("inativo"));
            editor.dismiss();
        }
    }

    private static ActivityController<MainActivity> launch() {
        RuntimeEnvironment.getApplication().getApplicationInfo().targetSdkVersion = 36;
        ActivityController<MainActivity> controller = Robolectric.buildActivity(MainActivity.class).create().start();
        MainActivity activity = controller.get();
        assertTrue("Activity must initialize rather than show data-preservation fallback: " + texts(activity), activity.getInitialized());
        AlertDialog onboarding = ShadowAlertDialog.getLatestAlertDialog();
        if (onboarding != null && onboarding.isShowing()) onboarding.dismiss();
        return controller;
    }
    private static byte[] database(MainActivity activity) throws IOException {
        return Files.readAllBytes(new File(activity.getFilesDir(), "livro-data.json").toPath());
    }
    private static void click(MainActivity activity, String caption) {
        for (View view : views(activity)) {
            if (view instanceof Button && caption.equals(((Button) view).getText().toString())) {
                assertTrue("Click " + caption, view.performClick());
                return;
            }
        }
        fail("Button not found: " + caption + "; visible texts=" + texts(activity));
    }
    private static EditText input(MainActivity activity, String label) {
        for (View view : views(activity)) {
            if (view instanceof TextView && label.equals(((TextView) view).getText().toString()) && view.getLabelFor() != View.NO_ID) {
                View input = activity.findViewById(view.getLabelFor());
                if (input instanceof EditText) return (EditText) input;
            }
        }
        throw new AssertionError("Input label not found: " + label);
    }
    private static List<String> texts(Activity activity) {
        List<String> result = new ArrayList<>();
        for (View view : views(activity)) if (view instanceof TextView) result.add(((TextView) view).getText().toString());
        return result;
    }
    private static List<View> views(Activity activity) {
        List<View> result = new ArrayList<>();
        collect(activity.findViewById(android.R.id.content), result);
        return result;
    }
    private static void collect(View view, List<View> result) {
        result.add(view);
        if (view instanceof ViewGroup) {
            ViewGroup group = (ViewGroup) view;
            for (int i = 0; i < group.getChildCount(); i++) collect(group.getChildAt(i), result);
        }
    }
}
