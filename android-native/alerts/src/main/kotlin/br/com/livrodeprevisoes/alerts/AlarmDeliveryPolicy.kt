package br.com.livrodeprevisoes.alerts

import org.json.JSONObject

/** Pure delivery boundary: stale claims never produce native side effects. */
object AlarmDeliveryPolicy {
    fun current(event:JSONObject?,id:String,stamp:String):Boolean = event!=null &&
        event.optString("id")==id && event.optBoolean("active",true) && event.optBoolean("hasAlarm",false) &&
        event.optString("status")=="pendente" && event.optString("alarmState")=="triggered" &&
        event.optString("lastAlarmTriggeredAt")==stamp

    /** A paused/killed activity may have persisted a claim before delivering any channel. */
    fun undelivered(events:List<JSONObject>,history:List<JSONObject>):List<JSONObject> {
        val claims=history.filter{it.optString("action")=="disparo_alarme"}
            .associateBy{it.optString("eventId")+"|"+it.optString("timestamp")}
        return events.filter{event->
            val id=event.optString("id");val stamp=event.optString("lastAlarmTriggeredAt")
            current(event,id,stamp) && claims[id+"|"+stamp]?.optJSONArray("channels")?.length()==0
        }
    }

    fun missingVisual(events:List<JSONObject>,history:List<JSONObject>,shown:Map<String,String>):List<JSONObject> {
        val claims=history.filter{it.optString("action")=="disparo_alarme"}
            .associateBy{it.optString("eventId")+"|"+it.optString("timestamp")}
        return events.filter{event->
            val id=event.optString("id");val stamp=event.optString("lastAlarmTriggeredAt")
            val channels=claims[id+"|"+stamp]?.optJSONArray("channels")
            current(event,id,stamp)&&shown[id]!=stamp&&channels!=null&&
                (0 until channels.length()).none{channels.optString(it)=="visual"}
        }
    }

    fun staleNotifications(posted:Map<String,String>,events:List<JSONObject>):Set<String> {
        val byId=events.associateBy{it.optString("id")}
        return posted.filter{(id,stamp)->!current(byId[id],id,stamp)}.keys
    }
}
