package br.com.livrodeprevisoes.alerts

import org.json.JSONObject

data class AlarmChannels(val audio:Boolean,val visual:Boolean,val notification:Boolean,val volume:Int,val sound:String) {
    companion object {
        fun resolve(event:JSONObject,settings:JSONObject,notificationAllowed:Boolean):AlarmChannels {
            val defaults=event.optBoolean("useDefaultAlarmSettings",false)
            val volume=settings.optInt("soundVolume",80).coerceIn(0,100)
            fun enabled(global:String,custom:String,default:Boolean)=if(defaults)settings.optBoolean(global,default) else event.optBoolean(custom,default)
            return AlarmChannels(enabled("soundEnabled","alarmAudio",true)&&volume>0,
                enabled("visualAlertEnabled","alarmVisual",true),
                enabled("notificationEnabled","alarmNotification",false)&&notificationAllowed,
                volume,settings.optString("soundType","chime"))
        }
    }
}

/** Scope control, not a background scheduler. Paused activities cannot begin new deliveries. */
class ForegroundGate {
    @Volatile private var active=false
    private var busy=false
    private var generation=0L
    @Synchronized fun resume(){if(!active){generation++;active=true}}
    @Synchronized fun pause(){generation++;active=false}
    @Synchronized fun token()=generation
    @Synchronized fun isCurrent(token:Long)=active&&generation==token
    fun isActive()=active
    fun runIfActive(action:()->Unit){
        synchronized(this){if(!active||busy)return;busy=true}
        try{action()}finally{synchronized(this){busy=false}}
    }
}
