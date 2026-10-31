package br.com.livrodeprevisoes.alerts
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test

class AlarmChannelsTest {
    private fun settings() = JSONObject().put("soundEnabled",true).put("soundVolume",80).put("soundType","chime").put("visualAlertEnabled",true).put("notificationEnabled",true)
    @Test fun customChannelsOverrideDefaultsAndDeniedNotificationsAreNotReportedAvailable() {
        val event=JSONObject().put("useDefaultAlarmSettings",false).put("alarmAudio",false).put("alarmVisual",true).put("alarmNotification",true)
        val channels=AlarmChannels.resolve(event,settings(),false)
        assertFalse(channels.audio);assertTrue(channels.visual);assertFalse(channels.notification)
    }
    @Test fun defaultChannelsIgnoreCustomFlagsAndZeroVolumeRemainsSilent() {
        val event=JSONObject().put("useDefaultAlarmSettings",true).put("alarmAudio",true).put("alarmVisual",false)
        val channels=AlarmChannels.resolve(event,settings().put("soundVolume",0),true)
        assertFalse(channels.audio);assertTrue(channels.visual);assertTrue(channels.notification);assertEquals(0,channels.volume)
    }
    @Test fun disabledGlobalChannelsStayDisabled() {
        val channels=AlarmChannels.resolve(JSONObject().put("useDefaultAlarmSettings",true),settings().put("soundEnabled",false).put("visualAlertEnabled",false).put("notificationEnabled",false),true)
        assertFalse(channels.audio);assertFalse(channels.visual);assertFalse(channels.notification)
    }
    @Test fun foregroundGateStopsDeliveryAndRejectsReentrantTicks() {
        val gate=ForegroundGate();var calls=0
        gate.runIfActive{calls++};assertEquals(0,calls)
        gate.resume();gate.runIfActive{calls++;gate.runIfActive{calls+=100}}
        assertEquals(1,calls)
        gate.pause();gate.runIfActive{calls++};assertEquals(1,calls)
        gate.resume();try{gate.runIfActive{throw IllegalStateException("delivery failed")}}catch(_:IllegalStateException){}
        gate.runIfActive{calls++};assertEquals(2,calls)
    }
}
