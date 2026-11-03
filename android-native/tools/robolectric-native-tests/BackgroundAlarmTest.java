package br.com.livrodeprevisoes.app;

import android.Manifest;
import android.app.*;
import android.content.*;
import android.os.Looper;
import br.com.livrodeprevisoes.alerts.*;
import br.com.livrodeprevisoes.domain.LivroService;
import java.time.Instant;
import java.util.concurrent.TimeUnit;
import org.json.*;
import org.junit.*;
import org.junit.runner.RunWith;
import org.robolectric.*;
import org.robolectric.annotation.*;
import org.robolectric.util.ReflectionHelpers;
import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
@Config(manifest=Config.NONE,sdk=36)
@GraphicsMode(GraphicsMode.Mode.LEGACY)
public class BackgroundAlarmTest {
    private Context context;
    private AlarmRuntime.State state;
    @Before public void setup() {
        context=RuntimeEnvironment.getApplication();
        context.getApplicationInfo().targetSdkVersion=36;
        Shadows.shadowOf(RuntimeEnvironment.getApplication()).grantPermissions(Manifest.permission.POST_NOTIFICATIONS);
        context.registerReceiver(new BackgroundAlarmReceiver(),new IntentFilter(AlarmRuntime.ACTION_FIRE),Context.RECEIVER_NOT_EXPORTED);
        state=AlarmRuntime.INSTANCE.get(context);
    }
    @Test public void backgroundWakeDeliversNotificationOnceAndCancelsAfterAcknowledgement() throws Exception {
        String id=due();
        wake(); awaitCount(id,1);
        assertEquals(1,manager().getActiveNotifications().length);
        wake(); Thread.sleep(50); Shadows.shadowOf(Looper.getMainLooper()).idle();
        assertEquals(1,event(id).getInt("alarmTriggerCount"));
        assertEquals(1,manager().getActiveNotifications().length);
        state.getService().acknowledgeAlarm(id);
        state.schedule();
        assertEquals(0,manager().getActiveNotifications().length);
        assertNull(state.getService().nextAlarmAt());
    }
    @Test public void persistedEmptyClaimRecoversAfterRuntimeRecreationWithoutIncrementingCount() throws Exception {
        String id=due();
        state.getService().fireAlarm(id,java.util.Collections.emptyList());
        state.retire(); // Process death removes the old process callbacks, but preserves files and system alarm.
        ReflectionHelpers.setStaticField(AlarmRuntime.class,"instance",null);
        state=AlarmRuntime.INSTANCE.get(context);
        state.schedule();
        org.robolectric.shadows.ShadowAlarmManager.ScheduledAlarm recovery=Shadows.shadowOf((AlarmManager)context.getSystemService(Context.ALARM_SERVICE)).getNextScheduledAlarm();
        assertNotNull("Persisted empty claim must automatically retain a system recovery wakeup",recovery);
        assertTrue(recovery.triggerAtTime>=System.currentTimeMillis()+20000);
        recovery.operation.send();
        Shadows.shadowOf(Looper.getMainLooper()).idle();
        awaitCount(id,1);
        assertEquals(1,manager().getActiveNotifications().length);
        assertEquals(1,event(id).getInt("alarmTriggerCount"));
    }
    @Test public void foregroundOwnsClaimUntilPausedThenReceiverDelivers() throws Exception {
        String id=due();
        state.enterForeground();
        wake(); Thread.sleep(60); Shadows.shadowOf(Looper.getMainLooper()).idle();
        assertEquals(0,event(id).getInt("alarmTriggerCount"));
        assertEquals(0,manager().getActiveNotifications().length);
        state.leaveForeground();
        wake(); awaitCount(id,1);
        assertEquals(1,manager().getActiveNotifications().length);
    }
    @Test public void visualOnlyClaimDoesNotScheduleAnEndlessRecoveryWake() throws Exception {
        String id=due();
        JSONObject snapshot=state.getService().snapshot();
        JSONArray events=snapshot.getJSONObject("data").getJSONArray("events");
        for(int i=0;i<events.length();i++)if(id.equals(events.getJSONObject(i).getString("id")))events.getJSONObject(i).put("alarmNotification",false).put("alarmVisual",true);
        state.getStore().save(snapshot);
        wake();
        long deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(5);
        while(event(id).getInt("alarmTriggerCount")!=1 && System.nanoTime()<deadline){Shadows.shadowOf(Looper.getMainLooper()).idle();Thread.sleep(10);}
        assertEquals(1,event(id).getInt("alarmTriggerCount"));
        state.schedule();
        assertNull(state.getService().nextAlarmAt());
        assertEquals(0,manager().getActiveNotifications().length);
    }
    @Test public void runtimeDoesNotReuseStoreAcrossApplicationStorageContexts() throws Exception {
        state.getService().loadDemoData(true);
        assertEquals(6,state.getService().rows("events").size());
        final java.io.File alternate=new java.io.File(context.getCacheDir(),"isolated-application-files");
        assertTrue(alternate.mkdirs() || alternate.isDirectory());
        Context isolated=new android.content.ContextWrapper(context){
            @Override public Context getApplicationContext(){return this;}
            @Override public java.io.File getFilesDir(){return alternate;}
        };
        AlarmRuntime.State replacement=AlarmRuntime.INSTANCE.get(isolated);
        assertNotSame(state,replacement);
        assertTrue(state.getRetired());
        assertEquals(0,replacement.getService().rows("events").size());
        assertTrue(new java.io.File(alternate,"livro-data.json").isFile());
        assertSame(replacement,AlarmRuntime.INSTANCE.get(isolated));
    }
    @Test public void unrelatedEarlyBroadcastDoesNotConsumeRetryBudget() throws Exception {
        String id=due();
        JSONObject claim=state.getService().fireAlarm(id,java.util.Collections.emptyList());
        String key=id+"|"+claim.getString("lastAlarmTriggeredAt");
        android.content.SharedPreferences ledger=context.getSharedPreferences("alarm-recovery",Context.MODE_PRIVATE);
        ledger.edit().putString(key,new JSONObject().put("attempts",1).put("at",System.currentTimeMillis()).toString()).commit();
        wake();Thread.sleep(80);Shadows.shadowOf(Looper.getMainLooper()).idle();
        assertEquals(1,new JSONObject(ledger.getString(key,"{}")).getInt("attempts"));
        assertEquals(0,manager().getActiveNotifications().length);
        assertEquals(1,event(id).getInt("alarmTriggerCount"));
        state.schedule();
        assertTrue(Shadows.shadowOf((AlarmManager)context.getSystemService(Context.ALARM_SERVICE)).getNextScheduledAlarm().triggerAtTime>=System.currentTimeMillis()+20000);
    }
    @Test public void exhaustedRecoveryBudgetStopsAutomaticWakesForAnEmptyClaim() throws Exception {
        String id=due();
        JSONObject claim=state.getService().fireAlarm(id,java.util.Collections.emptyList());
        String key=id+"|"+claim.getString("lastAlarmTriggeredAt");
        context.getSharedPreferences("alarm-recovery",Context.MODE_PRIVATE).edit().putString(key,new JSONObject().put("attempts",3).put("at",System.currentTimeMillis()).toString()).commit();
        state.schedule();
        assertNull(Shadows.shadowOf((AlarmManager)context.getSystemService(Context.ALARM_SERVICE)).getNextScheduledAlarm());
        assertEquals(1,event(id).getInt("alarmTriggerCount"));
    }
    @Test public void exactPermissionDeniedStillSchedulesAndAcknowledgementCancels() throws Exception {
        String id=due();
        AlarmManager alarms=(AlarmManager)context.getSystemService(Context.ALARM_SERVICE);
        Shadows.shadowOf(alarms).setCanScheduleExactAlarms(false);
        assertFalse(state.exactAllowed());
        state.schedule();
        assertNotNull(Shadows.shadowOf(alarms).getNextScheduledAlarm());
        state.getService().acknowledgeAlarm(id);state.schedule();
        assertNull(Shadows.shadowOf(alarms).getNextScheduledAlarm());
    }
    @Test public void exactPermissionGrantedSchedulesADeadline() throws Exception {
        due();
        AlarmManager alarms=(AlarmManager)context.getSystemService(Context.ALARM_SERVICE);
        Shadows.shadowOf(alarms).setCanScheduleExactAlarms(true);
        assertTrue(state.exactAllowed());state.schedule();
        assertNotNull(Shadows.shadowOf(alarms).getNextScheduledAlarm());
    }
    private void wake(){context.sendBroadcast(new Intent(AlarmRuntime.ACTION_FIRE).setPackage(context.getPackageName()));Shadows.shadowOf(Looper.getMainLooper()).idle();}
    private NotificationManager manager(){return (NotificationManager)context.getSystemService(Context.NOTIFICATION_SERVICE);}
    private JSONObject event(String id){for(JSONObject e:state.getService().rows("events"))if(id.equals(e.optString("id")))return e;throw new AssertionError(id);}
    private void awaitCount(String id,int count)throws Exception{
        long deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(5);
        while(System.nanoTime()<deadline){Shadows.shadowOf(Looper.getMainLooper()).idle();if(event(id).getInt("alarmTriggerCount")==count && manager().getActiveNotifications().length==1)return;Thread.sleep(10);}
        fail("Background delivery did not finish");
    }
    private String due()throws Exception{
        state.getService().loadDemoData(true);
        JSONObject snapshot=state.getService().snapshot();JSONArray events=snapshot.getJSONObject("data").getJSONArray("events");String id=null;
        for(int i=0;i<events.length();i++){
            JSONObject e=events.getJSONObject(i);e.put("hasAlarm",false).put("alarmAudio",false).put("alarmVisual",false).put("alarmNotification",true).put("useDefaultAlarmSettings",false).put("alarmRepeat",false).put("alarmMinutesBefore",0);
            if(id==null && "pendente".equals(e.getString("status")) && Instant.parse(e.getString("scheduledAt")).isBefore(Instant.now())){id=e.getString("id");e.put("hasAlarm",true).put("alarmState","idle").put("alarmTriggerCount",0).put("lastAlarmTriggeredAt",JSONObject.NULL).put("alarmSnoozedUntil",JSONObject.NULL);}
        }
        assertNotNull(id);state.getStore().save(snapshot);BackgroundAlarmReceiver.Companion.createChannel(manager());return id;
    }
}
