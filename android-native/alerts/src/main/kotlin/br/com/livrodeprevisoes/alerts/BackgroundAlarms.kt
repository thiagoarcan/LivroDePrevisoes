package br.com.livrodeprevisoes.alerts

import android.Manifest
import android.app.*
import android.content.*
import android.content.pm.PackageManager
import android.media.*
import android.os.*
import br.com.livrodeprevisoes.data.FileSnapshotStore
import br.com.livrodeprevisoes.domain.LivroService
import java.io.File
import java.util.concurrent.Executors

/** One process-wide store is the transaction lock used by Activity and receivers alike. */
object AlarmRuntime {
    private var instance: State?=null
    @Synchronized fun get(context:Context):State {
        instance?.let{return it}
        val app=context.applicationContext
        val store=FileSnapshotStore(File(app.filesDir,"livro-data.json"))
        val service=LivroService(store)
        return State(app,store,service).also { state ->
            instance=state
            store.onSaved={state.requestSchedule()}
            state.requestSchedule()
        }
    }
    class State(val context:Context,val store:FileSnapshotStore,val service:LivroService) {
        private val handler=Handler(Looper.getMainLooper())
        @Volatile var foreground=false
            private set
        private var visibleControllers=0
        fun enterForeground(){synchronized(store){visibleControllers++;foreground=true}}
        fun leaveForeground(){synchronized(store){visibleControllers=(visibleControllers-1).coerceAtLeast(0);foreground=visibleControllers>0}}
        private val reconcile=Runnable{runCatching{schedule()}.onFailure{android.util.Log.e("LivroAlarms","Agendamento",it)}}
        fun requestSchedule(){handler.removeCallbacks(reconcile);handler.post(reconcile)}
        private val recovery=context.getSharedPreferences("alarm-recovery",Context.MODE_PRIVATE)
        private fun key(event:org.json.JSONObject)=event.getString("id")+"|"+event.getString("lastAlarmTriggeredAt")
        fun eligible(event:org.json.JSONObject):Boolean {
            val manager=context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            val allowed=(Build.VERSION.SDK_INT<33 || context.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)==PackageManager.PERMISSION_GRANTED) && manager.areNotificationsEnabled() && manager.getNotificationChannel("operational-alerts")?.importance!=NotificationManager.IMPORTANCE_NONE
            val channels=AlarmChannels.resolve(event,service.settings(),allowed)
            return channels.audio || channels.notification
        }
        private fun emptyClaims():List<org.json.JSONObject> {
            val data=service.snapshot().getJSONObject("data")
            fun rows(name:String)=data.getJSONArray(name).let{a->(0 until a.length()).map{a.getJSONObject(it)}}
            return AlarmDeliveryPolicy.undelivered(rows("events"),rows("eventHistory"))
        }
        private fun recoveryDeadline():Long? {
            val claims=emptyClaims()
            val valid=claims.map{key(it)}.toSet()
            val obsolete=recovery.all.keys.filter{it !in valid}
            if(obsolete.isNotEmpty())recovery.edit().also{editor->obsolete.forEach{editor.remove(it)}}.apply()
            return claims.filter{eligible(it)}.mapNotNull{event->
                val record=org.json.JSONObject(recovery.getString(key(event),"{}") ?: "{}")
                if(record.optInt("attempts")>=3)null
                else maxOf(System.currentTimeMillis()+1000,record.optLong("at",System.currentTimeMillis())+30000)
            }.minOrNull()
        }
        fun recoverable(event:org.json.JSONObject):Boolean = mayAttempt(event) && emptyClaims().any{it.getString("id")==event.getString("id") && it.getString("lastAlarmTriggeredAt")==event.getString("lastAlarmTriggeredAt")}
        fun mayAttempt(event:org.json.JSONObject):Boolean {
            val record=org.json.JSONObject(recovery.getString(key(event),"{}") ?: "{}")
            return record.optInt("attempts")<3 && (record.optInt("attempts")==0 || System.currentTimeMillis()>=record.optLong("at")+30000)
        }
        fun noteAttempt(event:org.json.JSONObject){
            if(!eligible(event))return
            val name=key(event)
            val old=org.json.JSONObject(recovery.getString(name,"{}") ?: "{}")
            val attempts=old.optInt("attempts")+1
            // commit is synchronous: a killed process cannot reset the retry budget.
            check(recovery.edit().putString(name,org.json.JSONObject().put("attempts",attempts).put("at",System.currentTimeMillis()).toString()).commit())
            if(attempts==3)store.logError("Entrega de alarme","Última tentativa automática de entrega: ${event.getString("id")}. Confira permissões e áudio se não receber o aviso.")
        }
        private fun arm(whenMillis:Long){
            val manager=context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
            val pending=PendingIntent.getBroadcast(context,7300,Intent(context,BackgroundAlarmReceiver::class.java).setAction(ACTION_FIRE),PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
            try{if(exactAllowed())manager.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP,whenMillis,pending)
                else manager.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP,whenMillis,pending)}
            catch(_:SecurityException){manager.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP,whenMillis,pending)}
        }
        fun armSafety(){arm(System.currentTimeMillis()+30000)}
        fun exactAllowed():Boolean=Build.VERSION.SDK_INT<31 || (context.getSystemService(Context.ALARM_SERVICE) as AlarmManager).canScheduleExactAlarms()
        fun schedule(){
            synchronized(store){
                val manager=context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
                val pending=PendingIntent.getBroadcast(context,7300,Intent(context,BackgroundAlarmReceiver::class.java).setAction(ACTION_FIRE),PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
                manager.cancel(pending)
                cancelStale()
                val next=listOfNotNull(service.nextAlarmAt()?.toEpochMilli(),recoveryDeadline()).minOrNull() ?: return
                arm(maxOf(System.currentTimeMillis()+1000,next))
            }
        }
        fun cancelStale(){
            synchronized(store){
                val manager=context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
                val posted=manager.activeNotifications.mapNotNull{n->n.notification.extras?.getString("livro.claim")?.let{stamp->n.tag?.let{it to stamp}}}.toMap()
                AlarmDeliveryPolicy.staleNotifications(posted,service.rows("events")).forEach{manager.cancel(it,0)}
            }
        }
    }
    const val ACTION_FIRE="br.com.livrodeprevisoes.FIRE_ALARM"
}

/** Explicit RTC wakeup also runs after process death. Never opens an Activity over the lockscreen. */
class BackgroundAlarmReceiver:BroadcastReceiver() {
    override fun onReceive(context:Context,intent:Intent){
        val pending=goAsync()
        executor.execute{
            val wake=(context.getSystemService(Context.POWER_SERVICE) as PowerManager).newWakeLock(PowerManager.PARTIAL_WAKE_LOCK,"Livro:alarm-delivery")
            var track:AudioTrack?=null
            try{
                wake.acquire(9000)
                val state=AlarmRuntime.get(context)
                val started=SystemClock.elapsedRealtime()
                val service=state.service
                val manager=context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
                createChannel(manager)
                if(!state.foreground){
                    val snapshot=service.snapshot().getJSONObject("data")
                    fun rows(name:String)=snapshot.getJSONArray(name).let{array->(0 until array.length()).map{array.getJSONObject(it)}}
                    val candidates=linkedMapOf<String,org.json.JSONObject>()
                    AlarmDeliveryPolicy.undelivered(rows("events"),rows("eventHistory")).filter{state.mayAttempt(it) && state.eligible(it)}.take(4).forEach{candidates[it.getString("id")]=it}
                    service.dueAlarms().take(4).forEach{candidates[it.getString("id")]=it}
                    // One safety wakeup precedes claims and side effects, even if the process dies.
                    if(candidates.isNotEmpty())state.armSafety()
                    for(candidate in candidates.values.take(4)){
                        if(SystemClock.elapsedRealtime()-started>2500)break
                        // Release the transaction lock between events so an Activity can resume.
                        synchronized(state.store){
                            if(!state.foreground){
                                val id=candidate.getString("id")
                                val latest=service.rows("events").firstOrNull{it.getString("id")==id}
                                val event=service.fireAlarm(id,emptyList()) ?: latest?.takeIf{AlarmDeliveryPolicy.current(it,id,candidate.optString("lastAlarmTriggeredAt")) && state.recoverable(it)}
                                if(event!=null){
                                    state.noteAttempt(event)
                                    state.schedule()
                                    val allowed=(Build.VERSION.SDK_INT<33 || context.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)==PackageManager.PERMISSION_GRANTED) && manager.areNotificationsEnabled() && manager.getNotificationChannel(CHANNEL)?.importance!=NotificationManager.IMPORTANCE_NONE
                                    val channels=AlarmChannels.resolve(event,service.settings(),allowed)
                                    val actual=mutableListOf<String>()
                                    if(channels.audio){
                                        if(track==null)track=play(channels.sound,channels.volume)
                                        if(track!=null)actual.add("audio")
                                    }
                                    if(channels.notification && notify(context,manager,event))actual.add("notification")
                                    if(actual.isNotEmpty())service.recordAlarmDelivery(id,event.getString("lastAlarmTriggeredAt"),actual)
                                }
                            }
                        }
                    }
                }
                state.cancelStale()
                // Bounded sound playback keeps this receiver alive, including on a locked device.
                if(track!=null)Thread.sleep(1400)
                state.schedule()
            }catch(error:Exception){android.util.Log.e("LivroAlarms","Entrega em segundo plano",error)}
            finally{runCatching{track?.stop();track?.release()};if(wake.isHeld)wake.release();pending.finish()}
        }
    }
    companion object {
        private val executor=Executors.newSingleThreadExecutor{r->Thread(r,"livro-background-alarms").apply{isDaemon=true}}
        private const val CHANNEL="operational-alerts"
        fun createChannel(manager:NotificationManager){
            val channel=NotificationChannel(CHANNEL,"Previsões operacionais",NotificationManager.IMPORTANCE_DEFAULT)
            channel.description="Avisos de previsões, inclusive em segundo plano. Som configurado no aplicativo."
            channel.setSound(null,null);channel.enableVibration(false);channel.lockscreenVisibility=Notification.VISIBILITY_PRIVATE
            manager.createNotificationChannel(channel)
        }
        private fun notify(context:Context,manager:NotificationManager,event:org.json.JSONObject):Boolean=try{
            val launch=context.packageManager.getLaunchIntentForPackage(context.packageName)
                ?: Intent().setClassName(context.packageName,"br.com.livrodeprevisoes.app.MainActivity")
            run {
                val pending=PendingIntent.getActivity(context,0,launch.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP),PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
                val body="${event.getString("scheduledDate")} ${event.getString("scheduledTime")} · Abra para reconhecer ou adiar."
                manager.notify(event.getString("id"),0,Notification.Builder(context,CHANNEL).setSmallIcon(android.R.drawable.ic_dialog_alert)
                    .setContentTitle("Previsão operacional: ${event.getString("description")}".take(200)).setContentText(body)
                    .setContentIntent(pending).setAutoCancel(true).setCategory(Notification.CATEGORY_REMINDER)
                    .setVisibility(Notification.VISIBILITY_PRIVATE).addExtras(Bundle().apply{putString("livro.claim",event.getString("lastAlarmTriggeredAt"))}).build())
                true
            }
        }catch(_:Exception){false}
        private fun play(type:String,volume:Int):AudioTrack? {
            var audio:AudioTrack?=null
            return try{
                val samples=SoundSynthesis.samples(type,volume)
                audio=AudioTrack.Builder().setAudioAttributes(AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_ALARM).setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION).build())
                    .setAudioFormat(AudioFormat.Builder().setSampleRate(SoundSynthesis.SAMPLE_RATE).setEncoding(AudioFormat.ENCODING_PCM_16BIT).setChannelMask(AudioFormat.CHANNEL_OUT_MONO).build())
                    .setBufferSizeInBytes(samples.size*2).setTransferMode(AudioTrack.MODE_STATIC).build()
                if(audio.state!=AudioTrack.STATE_INITIALIZED || audio.write(samples,0,samples.size)!=samples.size){audio.release();null}else{audio.play();audio}
            }catch(_:Exception){runCatching{audio?.release()};null}
        }
    }
}
