package br.com.livrodeprevisoes.app;

import android.Manifest;
import android.app.AlertDialog;
import android.app.NotificationManager;
import android.app.Notification;
import android.content.Context;
import android.os.Looper;
import br.com.livrodeprevisoes.alerts.AndroidAlerts;
import java.time.Instant;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.locks.LockSupport;
import org.json.JSONArray;
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
import org.robolectric.shadows.ShadowAlertDialog;
import org.robolectric.util.ReflectionHelpers;
import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
@Config(manifest = Config.NONE, sdk = 36)
@GraphicsMode(GraphicsMode.Mode.LEGACY)
public class AndroidAlertsRaceTest {
    @Test public void pauseBeforeMainDeliverySuppressesNotificationThenResumeRetriesSameClaim() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            String eventId = configureOneDueNotificationOnlyEvent(activity);
            AndroidAlerts alerts = activity.getAlerts();
            startWorkerWithoutDeliveringMain(alerts);
            await("persisted alarm claim", () -> event(activity, eventId).optInt("alarmTriggerCount") == 1, false);
            alerts.stop();
            awaitWorkerIdle(alerts);
            assertEquals(0, manager(activity).getActiveNotifications().length);
            assertEquals(0, claimChannels(activity, eventId).length());
            assertNoAudioOrVisual(alerts);

            alerts.start();
            await("resumed delivery audited", () -> claimChannels(activity, eventId).toString().contains("notification"), true);
            awaitWorkerIdle(alerts);
            assertEquals("Undelivered no-repeat claim must not increment trigger count again", 1, event(activity, eventId).optInt("alarmTriggerCount"));
            assertEquals(1, manager(activity).getActiveNotifications().length);
            assertEquals("notification", claimChannels(activity, eventId).getString(0));
            assertNoAudioOrVisual(alerts);
        }
    }

    @Test public void completingClaimBeforeMainDeliveryCreatesNoFalseNotificationOrChannelAudit() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            String eventId = configureOneDueNotificationOnlyEvent(activity);
            AndroidAlerts alerts = activity.getAlerts();
            startWorkerWithoutDeliveringMain(alerts);
            await("persisted alarm claim", () -> event(activity, eventId).optInt("alarmTriggerCount") == 1, false);
            activity.getService().completeEvent(eventId, "Completed before queued main-thread delivery");
            awaitWorkerIdle(alerts);
            assertEquals("concluido", event(activity, eventId).getString("status"));
            assertEquals(0, manager(activity).getActiveNotifications().length);
            assertEquals(0, claimChannels(activity, eventId).length());
            assertNoAudioOrVisual(alerts);
        }
    }

    @Test public void completedEventNotificationIsCanceledImmediatelyWhenMonitoringStops() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            String eventId = configureOneDueNotificationOnlyEvent(activity);
            AndroidAlerts alerts = activity.getAlerts();
            alerts.start();
            await("first delivered notification", () -> manager(activity).getActiveNotifications().length == 1, true);
            awaitWorkerIdle(alerts);
            assertEquals("notification", claimChannels(activity, eventId).getString(0));
            activity.getService().completeEvent(eventId, "Completed then immediately left screen");
            alerts.stop();
            assertEquals("A completed event must not retain a stale operational notification", 0, manager(activity).getActiveNotifications().length);
            assertNoAudioOrVisual(alerts);
        }
    }

    @Test public void secondVisualAlertQueuesWithoutRepeatingItsDeliveredNotification() throws Exception {
        try (ActivityController<MainActivity> controller = launch()) {
            MainActivity activity = controller.get();
            String firstId = configureOneDueNotificationOnlyEvent(activity);
            JSONObject snapshot = activity.getService().snapshot();
            JSONArray events = snapshot.getJSONObject("data").getJSONArray("events");
            String selectedSecond = null;
            for (int i = 0; i < events.length(); i++) {
                JSONObject row = events.getJSONObject(i);
                if (firstId.equals(row.getString("id"))) row.put("alarmVisual", true);
                else if (selectedSecond == null && "pendente".equals(row.getString("status"))) {
                    selectedSecond = row.getString("id");
                    row.put("hasAlarm", true).put("alarmVisual", true).put("alarmNotification", true)
                            .put("alarmMinutesBefore", 1440).put("alarmState", "idle").put("alarmTriggerCount", 0)
                            .put("lastAlarmTriggeredAt", JSONObject.NULL).put("alarmSnoozedUntil", JSONObject.NULL);
                }
            }
            assertNotNull(selectedSecond);
            final String secondId = selectedSecond;
            activity.getStore().save(snapshot);
            assertEquals(2, activity.getService().dueAlarms().size());
            AndroidAlerts alerts = activity.getAlerts();
            alerts.start();
            await("both initial notifications delivered", () -> claimChannels(activity, secondId).toString().contains("notification"), true);
            awaitWorkerIdle(alerts);
            assertTrue(claimChannels(activity, firstId).toString().contains("visual"));
            assertFalse("Second visual must wait for occupied dialog", claimChannels(activity, secondId).toString().contains("visual"));
            assertEquals(2, manager(activity).getActiveNotifications().length);
            Notification secondNotification = Shadows.shadowOf(manager(activity)).getNotification(secondId, 0);
            assertNotNull(secondNotification);
            AlertDialog firstDialog = ReflectionHelpers.getField(alerts, "dialog");
            assertNotNull(firstDialog);
            firstDialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();
            Shadows.shadowOf(Looper.getMainLooper()).idle();
            assertEquals("acknowledged", event(activity, firstId).optString("alarmState"));
            Shadows.shadowOf(Looper.getMainLooper()).idleFor(1, TimeUnit.SECONDS);
            await("queued second visual audited", () -> claimChannels(activity, secondId).toString().contains("visual"), true);
            awaitWorkerIdle(alerts);
            JSONArray channels = claimChannels(activity, secondId);
            assertEquals(2, channels.length());
            assertTrue(channels.toString().contains("notification"));
            assertTrue(channels.toString().contains("visual"));
            assertEquals(1, event(activity, secondId).optInt("alarmTriggerCount"));
            assertEquals(1, manager(activity).getActiveNotifications().length);
            assertSame("Delivering queued visual must not post notification again", secondNotification, Shadows.shadowOf(manager(activity)).getNotification(secondId, 0));
            assertNotNull(ReflectionHelpers.getField(alerts, "dialog"));
            assertNull("Visual/notification fixtures never create AudioTrack", ReflectionHelpers.getField(alerts, "track"));
        }
    }

    private static ActivityController<MainActivity> launch() {
        RuntimeEnvironment.getApplication().getApplicationInfo().targetSdkVersion = 36;
        Shadows.shadowOf(RuntimeEnvironment.getApplication()).grantPermissions(Manifest.permission.POST_NOTIFICATIONS);
        ActivityController<MainActivity> controller = Robolectric.buildActivity(MainActivity.class).create().start();
        assertTrue(controller.get().getInitialized());
        AlertDialog onboarding = ShadowAlertDialog.getLatestAlertDialog();
        if (onboarding != null) onboarding.dismiss();
        Shadows.shadowOf(Looper.getMainLooper()).idle();
        return controller;
    }
    private static String configureOneDueNotificationOnlyEvent(MainActivity activity) throws Exception {
        activity.getService().loadDemoData(true);
        JSONObject snapshot = activity.getService().snapshot();
        JSONArray events = snapshot.getJSONObject("data").getJSONArray("events");
        String selected = null;
        for (int i = 0; i < events.length(); i++) {
            JSONObject event = events.getJSONObject(i);
            event.put("hasAlarm", false).put("useDefaultAlarmSettings", false).put("alarmAudio", false).put("alarmVisual", false)
                    .put("alarmNotification", true).put("alarmRepeat", false).put("alarmMaxRepeats", 0).put("alarmMinutesBefore", 0);
            if (selected == null && event.getString("status").equals("pendente") && Instant.parse(event.getString("scheduledAt")).isBefore(Instant.now())) {
                selected = event.getString("id");
                event.put("hasAlarm", true).put("alarmState", "idle").put("alarmTriggerCount", 0)
                        .put("lastAlarmTriggeredAt", JSONObject.NULL).put("alarmSnoozedUntil", JSONObject.NULL);
            }
        }
        assertNotNull("Demo provides an overdue pending fixture", selected);
        activity.getStore().save(snapshot);
        activity.getService().saveSettings(activity.getService().settings().put("soundEnabled", false).put("soundVolume", 0)
                .put("visualAlertEnabled", false).put("notificationEnabled", true).put("repeatAlarm", false).put("maxRepeats", 0));
        assertEquals("concedida", activity.getAlerts().permissionState());
        assertEquals(1, activity.getService().dueAlarms().size());
        return selected;
    }
    private static void startWorkerWithoutDeliveringMain(AndroidAlerts alerts) {
        alerts.start();
        // Run exactly the pulse, not a delivery callback the worker may enqueue concurrently.
        Shadows.shadowOf(Looper.getMainLooper()).runOneTask();
    }
    private static JSONObject event(MainActivity activity, String id) {
        for (JSONObject row : activity.getService().rows("events")) if (id.equals(row.optString("id"))) return row;
        throw new AssertionError("Missing fixture event " + id);
    }
    private static JSONArray claimChannels(MainActivity activity, String id) {
        for (JSONObject row : activity.getService().rows("eventHistory")) {
            if (id.equals(row.optString("eventId")) && "disparo_alarme".equals(row.optString("action"))) return row.optJSONArray("channels");
        }
        return new JSONArray();
    }
    private static NotificationManager manager(MainActivity activity) {
        return (NotificationManager) activity.getSystemService(Context.NOTIFICATION_SERVICE);
    }
    private static void awaitWorkerIdle(AndroidAlerts alerts) throws Exception {
        AtomicBoolean busy = ReflectionHelpers.getField(alerts, "busy");
        await("worker releases its guarded delivery future", () -> !busy.get(), true);
        Shadows.shadowOf(Looper.getMainLooper()).idle();
    }
    private static void assertNoAudioOrVisual(AndroidAlerts alerts) {
        assertNull("Notification-only fixtures must never create AudioTrack", ReflectionHelpers.getField(alerts, "track"));
        assertNull("Notification-only fixtures must never show alarm dialog", ReflectionHelpers.getField(alerts, "dialog"));
    }
    private interface Condition { boolean holds() throws Exception; }
    private static void await(String reason, Condition condition, boolean drainMain) throws Exception {
        long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(15);
        do {
            if (drainMain) Shadows.shadowOf(Looper.getMainLooper()).idle();
            if (condition.holds()) return;
            // Yield to the real worker while waiting on the actual persisted/result condition.
            LockSupport.parkNanos(TimeUnit.MILLISECONDS.toNanos(5));
        } while (System.nanoTime() < deadline);
        fail("Timed out waiting for " + reason);
    }
}
