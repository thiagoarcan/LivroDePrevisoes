package br.com.livrodeprevisoes.app;

import android.app.AlertDialog;
import android.os.Handler;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.window.OnBackInvokedCallback;
import android.util.Pair;
import org.robolectric.shadows.ShadowWindowOnBackInvokedDispatcher;
import br.com.livrodeprevisoes.domain.BackupCodec;
import br.com.livrodeprevisoes.domain.LivroService;
import br.com.livrodeprevisoes.domain.SnapshotStore;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.LockSupport;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.Robolectric;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.android.controller.ActivityController;
import org.robolectric.annotation.Config;
import org.robolectric.annotation.GraphicsMode;
import org.robolectric.shadows.ShadowAlertDialog;
import org.robolectric.util.ReflectionHelpers;
import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
@Config(manifest = Config.NONE, sdk = 36)
@GraphicsMode(GraphicsMode.Mode.LEGACY)
public class NativeRenderCacheTest {
    @Test public void fiveHundredEventRenderUsesOneRowsAndNamesCacheAndNoPerCardStoreReads() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            CountingStore store = installBulkService(activity);
            store.loads = 0;
            long start = System.nanoTime();
            activity.navigate("pending", null);
            long renderMillis = TimeUnit.NANOSECONDS.toMillis(System.nanoTime() - start);
            assertEquals("One snapshot plus palette settings, independent of 500 total results", 2, store.loads);
            assertNotNull(findText(activity, "500 registros"));
            assertEquals("Only first-page cards may be inflated from the 500-result cache", 100, clockViews(activity).size());
            Map<?, ?> rowCache = ReflectionHelpers.getField(activity, "renderRows");
            Map<?, ?> nameCache = ReflectionHelpers.getField(activity, "renderNames");
            List<JSONObject> events = activity.rows("events");
            assertSame(rowCache.get("events"), events);
            EditText search = input(activity, "Buscar");
            EditText dateFrom = input(activity, "Data prevista de (AAAA-MM-DD)");
            Set<String> visited = new HashSet<>();
            store.loads = 0;
            for (int page = 0; page < 5; page++) {
                assertEquals(page, activity.getListPage());
                assertNotNull(findText(activity, "Exibindo " + (page * 100 + 1) + "–" + ((page + 1) * 100) + " de 500"));
                List<String> descriptions = visibleBulkDescriptions(activity);
                assertEquals(100, descriptions.size());
                for (String description : descriptions) assertTrue("Each card appears on one page only: " + description, visited.add(description));
                assertEquals(100, clockViews(activity).size());
                assertSame(search, input(activity, "Buscar"));
                assertSame(dateFrom, input(activity, "Data prevista de (AAAA-MM-DD)"));
                assertSame(rowCache, ReflectionHelpers.getField(activity, "renderRows"));
                assertSame(nameCache, ReflectionHelpers.getField(activity, "renderNames"));
                assertSame(events, activity.rows("events"));
                List<Button> previous = buttons(activity, "Anterior");
                List<Button> next = buttons(activity, "Próxima");
                assertEquals("Previous controls at top and bottom", 2, previous.size());
                assertEquals("Next controls at top and bottom", 2, next.size());
                for (Button button : previous) assertEquals(page > 0, button.isEnabled());
                for (Button button : next) assertEquals(page < 4, button.isEnabled());
                if (page < 4) assertTrue(next.get(0).performClick());
            }
            assertEquals(500, visited.size());
            for (int i = 0; i < 500; i++) assertTrue(visited.contains(String.format(java.util.Locale.ROOT, "Bulk event %04d", i)));
            for (JSONObject event : events) {
                assertFalse(activity.hierarchy(event).isEmpty());
                assertEquals("C04", activity.name("consoles", event.getString("consoleId"), "missing"));
            }
            assertEquals("All five pages and 500 hierarchy/name lookups reuse caches", 0, store.loads);

            click(activity, "Anterior");
            click(activity, "Anterior");
            assertEquals(2, activity.getListPage());
            assertFalse(visibleBulkDescriptions(activity).contains("Bulk event 0499"));
            search.setText("Bulk event 0499");
            assertEquals("Search resets page and includes off-page results", 0, activity.getListPage());
            assertNotNull(findText(activity, "1 registros"));
            assertEquals(java.util.Collections.singletonList("Bulk event 0499"), visibleBulkDescriptions(activity));
            assertEquals(1, clockViews(activity).size());
            search.setText("Bulk event");
            click(activity, "Próxima"); click(activity, "Próxima"); click(activity, "Próxima");
            assertEquals(3, activity.getListPage());
            click(activity, "Mostrar / ocultar filtros avançados");
            dateFrom.setText("2030-01-01");
            click(activity, "Aplicar filtros");
            assertEquals("Applying a filter resets the first page", 0, activity.getListPage());
            assertSame(search, input(activity, "Buscar"));
            assertSame(dateFrom, input(activity, "Data prevista de (AAAA-MM-DD)"));
            assertEquals(0, store.loads);
            for (int i = 0; i < 4; i++) click(activity, "Próxima");
            JSONObject shrunk = activity.getService().snapshot();
            JSONArray survivors = new JSONArray();
            for (int i = 0; i < 250; i++) survivors.put(shrunk.getJSONObject("data").getJSONArray("events").getJSONObject(i));
            shrunk.getJSONObject("data").put("events", survivors);
            store.save(BackupCodec.INSTANCE.validate(shrunk));
            store.loads = 0;
            activity.refreshAfterMutation();
            assertEquals("Refresh reads one new snapshot, never once per card", 1, store.loads);
            assertEquals("A vanished last page clamps to the new last page", 2, activity.getListPage());
            assertNotNull(findText(activity, "Exibindo 201–250 de 250"));
            assertEquals(50, visibleBulkDescriptions(activity).size());
            assertEquals(50, clockViews(activity).size());
            assertSame(search, input(activity, "Buscar"));
            assertSame(dateFrom, input(activity, "Data prevista de (AAAA-MM-DD)"));
            System.out.println("Native 500-result first page: " + renderMillis + " ms; 100 live cards, all 500 unique across 5 pages, 2 initial loads then 0 paging/search/name reads (informative timing only)");
            activity.navigate("alerts", null);
            assertEquals("Navigation releases old event-card watchers", 0, clockViews(activity).size());
            activity.navigate("new", null);
            assertEquals(0, clockViews(activity).size());
        }
    }

    @Test public void pagedListReturnsFromDetailAndRestoresPageAndQueryAfterActivityRecreation() throws Exception {
        ActivityController<MainActivity> original = launch();
        MainActivity activity = original.get();
        installBulkService(activity);
        activity.navigate("pending", null);
        input(activity, "Buscar").setText("Bulk event");
        click(activity, "Próxima"); click(activity, "Próxima");
        assertEquals(2, activity.getListPage());
        click(activity, "Detalhes e ações");
        assertNotNull(activity.getDetailId());
        assertEquals(2, activity.getListPage());
        click(activity, "Voltar à lista");
        assertNull(activity.getDetailId());
        assertEquals(2, activity.getListPage());
        assertNotNull(findText(activity, "Exibindo 201–300 de 500"));
        assertEquals("Bulk event", input(activity, "Buscar").getText().toString());
        // Recreated Activity uses the actual file-backed store, not the counting fixture adapter.
        activity.getStore().save(activity.getService().snapshot());
        Bundle state = new Bundle();
        original.saveInstanceState(state).stop().destroy();
        try (ActivityController<MainActivity> recreated = Robolectric.buildActivity(MainActivity.class).create(state).start()) {
            MainActivity restored = recreated.get();
            assertTrue(restored.getInitialized());
            assertEquals("pending", restored.getScreen());
            assertEquals(2, restored.getListPage());
            assertEquals("Bulk event", input(restored, "Buscar").getText().toString());
            assertNotNull(findText(restored, "500 registros"));
            assertNotNull(findText(restored, "Exibindo 201–300 de 500"));
            assertEquals(100, visibleBulkDescriptions(restored).size());
            assertEquals(100, clockViews(restored).size());
        }
    }

    @Test public void predictiveBackFromPagedDetailsRetainsPendingAndCompletedListState() throws Exception {
        RuntimeEnvironment.getApplication().getApplicationInfo().targetSdkVersion = 36;
        ReflectionHelpers.callInstanceMethod(RuntimeEnvironment.getApplication().getApplicationInfo(), "setEnableOnBackInvokedCallback", ReflectionHelpers.ClassParameter.from(boolean.class, true));
        ReflectionHelpers.callStaticMethod(ShadowWindowOnBackInvokedDispatcher.class, "setEnablePredictiveBack", ReflectionHelpers.ClassParameter.from(boolean.class, true));
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            CountingStore store = installBulkService(activity);
            List<Pair<OnBackInvokedCallback, Integer>> callbacks = ReflectionHelpers.getField(activity.getOnBackInvokedDispatcher(), "mCallbacks");
            assertFalse("Actual platform callback must be registered", callbacks.isEmpty());
            OnBackInvokedCallback back = callbacks.get(callbacks.size() - 1).first;
            for (String screen : new String[] {"pending", "completed"}) {
                if (screen.equals("completed")) {
                    JSONObject snapshot = activity.getService().snapshot();
                    JSONArray events = snapshot.getJSONObject("data").getJSONArray("events");
                    String completedAt = Instant.now().toString();
                    for (int i = 0; i < events.length(); i++) {
                        events.getJSONObject(i).put("status", "concluido").put("completedAt", completedAt)
                                .put("completedBy", "Native fixture").put("completedTimeDiffMinutes", -1)
                                .put("alarmState", "acknowledged");
                    }
                    store.save(BackupCodec.INSTANCE.validate(snapshot));
                }
                activity.navigate(screen, null);
                input(activity, "Buscar").setText("Bulk event");
                click(activity, "Mostrar / ocultar filtros avançados");
                input(activity, "Data prevista de (AAAA-MM-DD)").setText("2030-01-01");
                click(activity, "Aplicar filtros");
                click(activity, "Próxima"); click(activity, "Próxima");
                assertEquals(2, activity.getListPage());
                click(activity, "Detalhes e ações");
                assertNotNull(activity.getDetailId());
                assertEquals(screen, activity.getScreen());
                back.onBackInvoked();
                assertEquals("Predictive Back from details returns to its list, not dashboard", screen, activity.getScreen());
                assertNull(activity.getDetailId());
                assertEquals(2, activity.getListPage());
                assertEquals("Bulk event", activity.getListQuery());
                assertEquals("Bulk event", input(activity, "Buscar").getText().toString());
                assertEquals("2030-01-01", activity.getListFilters().getDateFrom());
                assertEquals("2030-01-01", input(activity, "Data prevista de (AAAA-MM-DD)").getText().toString());
                assertNotNull(findText(activity, "Exibindo 201–300 de 500"));
                assertEquals(100, clockViews(activity).size());
                assertFalse(activity.isFinishing());
            }
        }
    }

    @Test public void repeatedRealFilterEditsBoundClockWatchersAndDeadlineTickPreservesForm() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            CountingStore store = installBulkService(activity);
            activity.navigate("pending", null);
            EditText search = input(activity, "Buscar");
            EditText dateFrom = input(activity, "Data prevista de (AAAA-MM-DD)");
            click(activity, "Mostrar / ocultar filtros avançados");
            Button apply = (Button) findText(activity, "Aplicar filtros");
            assertNotNull(apply);
            store.loads = 0;
            Map<?, ?> rowCache = ReflectionHelpers.getField(activity, "renderRows");
            int maxWatchers = 0;
            for (int i = 0; i < 20; i++) {
                search.setText(String.format(java.util.Locale.ROOT, "Bulk event %04d", 480 + i));
                dateFrom.setText(i % 2 == 0 ? "2020-01-01" : "2021-01-01");
                assertTrue(apply.performClick());
                assertSame("Filtering must preserve the search field", search, input(activity, "Buscar"));
                assertSame("Filtering must preserve advanced filter fields", dateFrom, input(activity, "Data prevista de (AAAA-MM-DD)"));
                assertNotNull("Expected one result for query=" + activity.getListQuery() + " console=" + activity.getActiveConsole() + " filters=" + activity.getListFilters() + " watches=" + clockViews(activity).size(), findText(activity, "1 registros"));
                int current = clockViews(activity).size();
                maxWatchers = Math.max(maxWatchers, current);
                assertEquals("Only the currently visible card retains a clock watcher", 1, current);
                assertEquals(0, activity.getListPage());
                assertSame(rowCache, ReflectionHelpers.getField(activity, "renderRows"));
            }
            assertEquals("Twenty actual text/filter edits cannot introduce per-card store reads", 0, store.loads);

            // Use a schema-valid minute-aligned real deadline, rather than a fake +2-second record.
            Instant now = Instant.now();
            Instant deadline = now.truncatedTo(ChronoUnit.MINUTES).plusSeconds(60);
            if (Duration.between(now, deadline).toMillis() < 5000) deadline = deadline.plusSeconds(60);
            JSONObject event = null;
            for (JSONObject candidate : activity.getService().rows("events")) if (candidate.getString("description").equals("Bulk event 0499")) event = candidate;
            assertNotNull(event);
            event.put("scheduledDate", deadline.atZone(ZoneOffset.UTC).toLocalDate().toString())
                    .put("scheduledTime", deadline.atZone(ZoneOffset.UTC).format(DateTimeFormatter.ofPattern("HH:mm")));
            activity.getService().saveEvent(event);
            dateFrom.setText("draft filter text must remain untouched");
            activity.refreshAfterMutation();
            assertSame(search, input(activity, "Buscar"));
            assertSame(dateFrom, input(activity, "Data prevista de (AAAA-MM-DD)"));
            assertEquals("draft filter text must remain untouched", dateFrom.getText().toString());
            assertEquals(1, clockViews(activity).size());
            TextView status = (TextView) clockViews(activity).keySet().iterator().next();
            assertFalse("Deadline begins in the future", status.getText().toString().startsWith("Atrasado"));
            View page = activity.getPage();
            while (!Instant.now().isAfter(deadline)) {
                long remaining = Math.max(1, Duration.between(Instant.now(), deadline).toNanos());
                LockSupport.parkNanos(Math.min(remaining, TimeUnit.MILLISECONDS.toNanos(50)));
            }
            Runnable tick = ReflectionHelpers.getField(activity, "clockTick");
            tick.run();
            Handler handler = ReflectionHelpers.getField(activity, "clockHandler");
            handler.removeCallbacks(tick);
            assertTrue("Same live native label crosses to overdue without render", status.getText().toString().startsWith("Atrasado"));
            assertSame(page, activity.getPage());
            assertSame(status, clockViews(activity).keySet().iterator().next());
            assertSame(search, input(activity, "Buscar"));
            assertSame(dateFrom, input(activity, "Data prevista de (AAAA-MM-DD)"));
            assertEquals("Bulk event 0499", search.getText().toString());
            assertEquals("draft filter text must remain untouched", dateFrom.getText().toString());
            assertEquals(1, clockViews(activity).size());
            System.out.println("20 real search/filter edits: max clock watchers=" + maxWatchers + "; live deadline advanced at " + deadline + " without replacing fields/page");
        }
    }

    private static ActivityController<MainActivity> launch() {
        RuntimeEnvironment.getApplication().getApplicationInfo().targetSdkVersion = 36;
        ActivityController<MainActivity> controller = Robolectric.buildActivity(MainActivity.class).create().start();
        assertTrue(controller.get().getInitialized());
        AlertDialog dialog = ShadowAlertDialog.getLatestAlertDialog();
        if (dialog != null) dialog.dismiss();
        return controller;
    }
    private static void click(MainActivity activity, String caption) {
        List<Button> choices = buttons(activity, caption);
        assertFalse("Missing button " + caption, choices.isEmpty());
        assertTrue("Button must be enabled: " + caption, choices.get(0).isEnabled());
        assertTrue(choices.get(0).performClick());
    }
    private static List<Button> buttons(MainActivity activity, String caption) {
        List<Button> result = new ArrayList<>();
        for (View view : views(activity)) if (view instanceof Button && caption.equals(((Button) view).getText().toString())) result.add((Button) view);
        return result;
    }
    private static List<String> visibleBulkDescriptions(MainActivity activity) {
        List<String> result = new ArrayList<>();
        for (View view : views(activity)) {
            if (view instanceof TextView && !(view instanceof EditText)) {
                String text = ((TextView) view).getText().toString();
                if (text.matches("Bulk event [0-9]{4}")) result.add(text);
            }
        }
        return result;
    }
    private static List<View> views(MainActivity activity) {
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
    private static CountingStore installBulkService(MainActivity activity) throws Exception {
        activity.getService().loadDemoData(true);
        JSONObject snapshot = activity.getService().snapshot();
        JSONObject template = activity.getService().rows("events").get(0);
        // Explicitly select the C04 pending fixture, with consistent original master references.
        for (JSONObject candidate : activity.getService().rows("events")) {
            if (candidate.optString("status").equals("pendente") && candidate.optString("description").contains("BB-101A")) template = candidate;
        }
        JSONArray events = new JSONArray();
        for (int i = 0; i < 500; i++) {
            JSONObject event = new JSONObject(template.toString());
            event.put("id", UUID.nameUUIDFromBytes(("native-bulk-" + i).getBytes(StandardCharsets.UTF_8)).toString())
                    .put("description", String.format(java.util.Locale.ROOT, "Bulk event %04d", i))
                    .put("scheduledDate", "2030-01-02").put("scheduledTime", "12:00").put("scheduledAt", "2030-01-02T12:00:00Z")
                    .put("hasAlarm", false).put("alarmAudio", false).put("alarmVisual", false).put("alarmNotification", false)
                    .put("status", "pendente").put("alarmState", "idle").put("alarmTriggerCount", 0)
                    .put("lastAlarmTriggeredAt", JSONObject.NULL).put("completedAt", JSONObject.NULL).put("completedBy", JSONObject.NULL)
                    .put("completedTimeDiffMinutes", JSONObject.NULL).put("completionNote", "");
            events.put(event);
        }
        snapshot.getJSONObject("data").put("events", events).put("eventHistory", new JSONArray());
        CountingStore store = new CountingStore(BackupCodec.INSTANCE.validate(snapshot));
        LivroService realService = new LivroService(store, () -> Instant.now(), ZoneOffset.UTC);
        activity.setService(realService);
        // Like the production demo-import flow, clear references to the replaced old store.
        activity.setActiveConsole("");
        return store;
    }
    private static Map<View, ?> clockViews(MainActivity activity) { return ReflectionHelpers.getField(activity, "clockViews"); }
    private static EditText input(MainActivity activity, String label) {
        TextView caption = findText(activity, label);
        assertNotNull("Missing caption " + label, caption);
        View view = activity.findViewById(caption.getLabelFor());
        assertTrue("Caption must label an EditText: " + label, view instanceof EditText);
        return (EditText) view;
    }
    private static TextView findText(MainActivity activity, String text) { return findText(activity.findViewById(android.R.id.content), text); }
    private static TextView findText(View view, String text) {
        if (view instanceof TextView && text.equals(((TextView) view).getText().toString())) return (TextView) view;
        if (view instanceof ViewGroup) {
            ViewGroup group = (ViewGroup) view;
            for (int i = 0; i < group.getChildCount(); i++) {
                TextView found = findText(group.getChildAt(i), text);
                if (found != null) return found;
            }
        }
        return null;
    }
    private static final class CountingStore implements SnapshotStore {
        private JSONObject snapshot;
        int loads;
        CountingStore(JSONObject snapshot) { this.snapshot = snapshot; }
        @Override public synchronized JSONObject load() { loads++; return copy(snapshot); }
        @Override public synchronized void save(JSONObject value) { snapshot = copy(value); }
        private static JSONObject copy(JSONObject value) {
            try { return new JSONObject(value.toString()); }
            catch (JSONException error) { throw new IllegalArgumentException(error); }
        }
    }
}
