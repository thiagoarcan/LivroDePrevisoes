package br.com.livrodeprevisoes.alerts

import android.Manifest
import android.app.Activity
import android.app.AlertDialog
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import android.os.Build
import android.os.Bundle
import java.util.concurrent.CompletableFuture
import java.util.concurrent.Executors
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.atomic.AtomicBoolean
import android.os.Handler
import android.os.Looper
import android.widget.Toast
import br.com.livrodeprevisoes.domain.LivroService
import org.json.JSONObject

/** Foreground monitoring only. No service, receiver, exact alarm, or hidden operational action. */
class AndroidAlerts(private val activity:Activity,private val service:LivroService,private val onChanged:()->Unit) {
    private val handler=Handler(Looper.getMainLooper())
    private val gate=ForegroundGate()
    private val manager=activity.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
    private val preferences=activity.getSharedPreferences("native-alert-permission",Context.MODE_PRIVATE)
    private var track:AudioTrack?=null
    @Volatile private var dialog:AlertDialog?=null
    private var visibleId:String?=null
    private val shown=ConcurrentHashMap<String,String>()
    private var lastError:String?=null
    private val worker=Executors.newSingleThreadExecutor{task->Thread(task,"livro-foreground-alerts").apply{isDaemon=true}}
    private val busy=AtomicBoolean(false)
    private val refreshPending=AtomicBoolean(false)
    private var destroyed=false
    private val posted=mutableMapOf<String,String>()
    var onError:(String,Throwable)->Unit={context,error->android.util.Log.e("LivroAlerts",context,error)}
    private val pulse=object:Runnable {
        override fun run(){
            if(gate.isActive()&&busy.compareAndSet(false,true)){
                val token=gate.token()
                worker.execute{try{if(gate.isCurrent(token))tick(token)}finally{busy.set(false)}}
            }
            if(gate.isActive())handler.postDelayed(this,1000)
        }
    }

    init {
        val channel=NotificationChannel(CHANNEL,"Previsões operacionais",NotificationManager.IMPORTANCE_DEFAULT)
        channel.description="Avisos gerados enquanto o aplicativo está aberto. O som é controlado separadamente no aplicativo."
        channel.setSound(null,null);channel.enableVibration(false)
        channel.lockscreenVisibility=Notification.VISIBILITY_PRIVATE
        manager.createNotificationChannel(channel)
    }

    fun start(){if(destroyed||gate.isActive())return;gate.resume();restorePosted();handler.post(pulse)}
    fun stop(){
        gate.pause();handler.removeCallbacks(pulse);stopSound();dialog?.dismiss();dialog=null;visibleId=null
        // Operator actions can be followed immediately by leaving the screen; clear stale notices now.
        if(posted.isNotEmpty())try{cancelStale(service.rows("events"))}catch(error:Exception){report("Atualização de notificações",error)}
    }
    fun destroy(){if(destroyed)return;stop();destroyed=true;worker.shutdownNow()}

    fun permissionState():String {
        val granted=Build.VERSION.SDK_INT<33||activity.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)==PackageManager.PERMISSION_GRANTED
        if(granted&&manager.areNotificationsEnabled()&&manager.getNotificationChannel(CHANNEL)?.importance!=NotificationManager.IMPORTANCE_NONE)return "concedida"
        if(Build.VERSION.SDK_INT>=33&&!preferences.getBoolean("requested",false)&&!granted)return "nao_solicitada"
        return "negada"
    }

    fun requestPermission(){
        if(Build.VERSION.SDK_INT>=33&&activity.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)!=PackageManager.PERMISSION_GRANTED){
            preferences.edit().putBoolean("requested",true).apply()
            activity.requestPermissions(arrayOf(Manifest.permission.POST_NOTIFICATIONS),REQUEST_PERMISSION)
        }else if(permissionState()!="concedida"){
            activity.startActivity(Intent(android.provider.Settings.ACTION_APP_NOTIFICATION_SETTINGS).putExtra(android.provider.Settings.EXTRA_APP_PACKAGE,activity.packageName))
        }else toast("Notificações autorizadas. Alertas só são monitorados com o aplicativo aberto.")
    }

    fun testSound(){
        val settings=service.settings()
        if(!playSound(settings.optString("soundType","chime"),settings.optInt("soundVolume",80)))toast("Som não iniciado: confira volume e disponibilidade de áudio.")
    }

    fun testNotification(){
        if(!sendNotification("native-test","Teste de alerta operacional","Teste manual. O monitoramento funciona com o aplicativo aberto."))toast("Notificações não autorizadas. Use Autorizar notificações.")
        else toast("Notificação de teste enviada ao Android.")
    }

    private fun tick(token:Long){
        try{
            var changed=false
            val attempted=mutableSetOf<String>()
            for(candidate in service.dueAlarms()){
                if(!gate.isCurrent(token))break
                val event=service.fireAlarm(candidate.getString("id"),emptyList())?:continue
                attempted.add(event.getString("id"));changed=true
                val actual=deliverOnMain(event,token)
                if(actual.isNotEmpty())service.recordAlarmDelivery(event.getString("id"),event.getString("lastAlarmTriggeredAt"),actual)
            }
            if(!gate.isCurrent(token))return
            val snapshot=service.snapshot().getJSONObject("data")
            fun rows(name:String)=snapshot.getJSONArray(name).let{a->(0 until a.length()).map{a.getJSONObject(it)}}
            val events=rows("events")
            // Retry an undelivered persisted claim without incrementing trigger/repeat counters.
            // This also recovers a no-repeat alarm interrupted by pause or process death.
            for(event in AlarmDeliveryPolicy.undelivered(events,rows("eventHistory"))){
                if(!gate.isCurrent(token))break
                if(event.getString("id") in attempted)continue
                val settings=service.settings()
                val options=AlarmChannels.resolve(event,settings,permissionState()=="concedida")
                if(!options.audio&&!options.notification&&(!options.visual||dialog!=null))continue
                val actual=deliverOnMain(event,token)
                if(actual.isNotEmpty()){
                    service.recordAlarmDelivery(event.getString("id"),event.getString("lastAlarmTriggeredAt"),actual);changed=true
                }
            }
            // A delivered sound/notification must not discard a visual queued behind another dialog.
            if(dialog==null&&gate.isCurrent(token)){
                val settings=service.settings()
                val queued=AlarmDeliveryPolicy.missingVisual(events,rows("eventHistory"),shown)
                    .firstOrNull{AlarmChannels.resolve(it,settings,permissionState()=="concedida").visual}
                if(queued!=null){
                    val visual=deliverOnMain(queued,token,true)
                    if(visual.isNotEmpty()){
                        val claim=service.rows("eventHistory").lastOrNull{it.optString("eventId")==queued.getString("id")&&it.optString("action")=="disparo_alarme"&&it.optString("timestamp")==queued.getString("lastAlarmTriggeredAt")}
                        val previous=claim?.optJSONArray("channels")
                        val combined=(if(previous==null)emptyList() else (0 until previous.length()).map{previous.getString(it)})+visual
                        service.recordAlarmDelivery(queued.getString("id"),queued.getString("lastAlarmTriggeredAt"),combined.distinct());changed=true
                    }
                }
            }
            handler.post{if(gate.isCurrent(token)){
                cancelStale(events)
                if(visibleId!=null&&events.none{it.optString("id")==visibleId&&it.optString("status")=="pendente"&&it.optBoolean("active",true)&&it.optString("alarmState")=="triggered"}){dialog?.dismiss();dialog=null;visibleId=null}
            }}
            if(changed)requestRefresh(token)
            lastError=null
        }catch(error:InterruptedException){Thread.currentThread().interrupt()}
        catch(error:Exception){report("Monitoramento de alarmes",error)}
    }

    private fun deliverOnMain(claim:JSONObject,token:Long,visualOnly:Boolean=false):List<String>{
        val outcome=CompletableFuture<List<String>>()
        handler.post{
            val actual=mutableListOf<String>()
            try{
                if(gate.isCurrent(token)&&!activity.isFinishing&&!activity.isDestroyed){
                    val id=claim.getString("id");val stamp=claim.getString("lastAlarmTriggeredAt")
                    val latest=service.rows("events").firstOrNull{it.optString("id")==id}
                    // Native commands are synchronous on this main thread: no operator action can
                    // interleave between this final claim check and the three platform calls.
                    if(AlarmDeliveryPolicy.current(latest,id,stamp)){
                        val options=AlarmChannels.resolve(latest!!,service.settings(),permissionState()=="concedida")
                        if(!visualOnly&&options.audio&&playSound(options.sound,options.volume))actual.add("audio")
                        if(options.visual&&showVisual(latest))actual.add("visual")
                        if(!visualOnly&&options.notification&&sendNotification(id,"Previsão operacional: ${latest.getString("description")}","${latest.getString("scheduledDate")} ${latest.getString("scheduledTime")}",stamp))actual.add("notification")
                    }
                }
            }catch(error:Exception){report("Entrega do alarme",error)}
            finally{outcome.complete(actual)}
        }
        // Do not block the UI thread. stop() leaves this tiny guarded callback queued so it
        // completes empty after pause; destroy() interrupts this worker wait.
        return outcome.get()
    }

    private fun requestRefresh(token:Long){
        if(!refreshPending.compareAndSet(false,true))return
        handler.postDelayed({refreshPending.set(false);if(gate.isCurrent(token))onChanged()},250)
    }

    private fun restorePosted(){
        for(item in manager.activeNotifications){
            val stamp=item.notification.extras?.getString("livro.claim")?:continue
            val id=item.tag?:continue;posted[id]=stamp
        }
    }

    private fun cancelStale(events:List<JSONObject>){
        for(id in AlarmDeliveryPolicy.staleNotifications(posted,events)){manager.cancel(id,0);posted.remove(id)}
    }

    private fun showVisual(event:JSONObject):Boolean {
        if(!gate.isActive()||activity.isFinishing||activity.isDestroyed)return false
        if(dialog!=null)return visibleId==event.getString("id")
        val id=event.getString("id")
        val popup=AlertDialog.Builder(activity)
            .setTitle("Alarme operacional")
            .setMessage("${event.getString("description")}\n\nPrevisto: ${event.getString("scheduledDate")} ${event.getString("scheduledTime")}\nO reconhecimento silencia o alarme, mas não conclui a previsão.")
            .setPositiveButton("Reconhecer"){_,_->action{id.let(service::acknowledgeAlarm);manager.cancel(id,0)}}
            .setNeutralButton("Adiar 10 min"){_,_->action{service.snoozeAlarm(id,10);manager.cancel(id,0)}}
            .setNegativeButton("Fechar",null).create()
        popup.setOnDismissListener{dialog=null;visibleId=null}
        popup.show();dialog=popup;visibleId=id;shown[id]=event.optString("lastAlarmTriggeredAt")
        return true
    }

    private fun action(block:()->Unit){try{block();stopSound();onChanged()}catch(error:Exception){report("Ação no alarme",error);toast(error.message?:"Não foi possível concluir a ação.")}}

    private fun sendNotification(id:String,title:String,body:String,stamp:String?=null):Boolean {
        if(permissionState()!="concedida")return false
        return try{
            val launch=activity.packageManager.getLaunchIntentForPackage(activity.packageName)?:Intent(activity,activity.javaClass)
            launch.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP)
            val pending=PendingIntent.getActivity(activity,0,launch,PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
            val notification=Notification.Builder(activity,CHANNEL).setSmallIcon(android.R.drawable.ic_dialog_alert)
                .setContentTitle(title.take(200)).setContentText(body.take(1000))
                .setStyle(Notification.BigTextStyle().bigText(body.take(4000)))
                .setContentIntent(pending).setAutoCancel(true).setVisibility(Notification.VISIBILITY_PRIVATE)
                .setCategory(Notification.CATEGORY_REMINDER).setOnlyAlertOnce(false)
                .addExtras(Bundle().apply{if(stamp!=null)putString("livro.claim",stamp)}).build()
            manager.notify(id,0,notification);if(stamp!=null)posted[id]=stamp;true
        }catch(error:Exception){report("Notificação",error);false}
    }

    private fun playSound(type:String,volume:Int):Boolean {
        val samples=SoundSynthesis.samples(type,volume)
        if(samples.isEmpty())return false
        return try{
            stopSound()
            val audio=AudioTrack.Builder()
                .setAudioAttributes(AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_ALARM).setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION).build())
                .setAudioFormat(AudioFormat.Builder().setSampleRate(SoundSynthesis.SAMPLE_RATE).setEncoding(AudioFormat.ENCODING_PCM_16BIT).setChannelMask(AudioFormat.CHANNEL_OUT_MONO).build())
                .setBufferSizeInBytes(samples.size*2).setTransferMode(AudioTrack.MODE_STATIC).build()
            if(audio.state!=AudioTrack.STATE_INITIALIZED){audio.release();return false}
            if(audio.write(samples,0,samples.size)!=samples.size){audio.release();return false}
            track=audio;audio.play()
            handler.postDelayed({if(track===audio)stopSound()},samples.size*1000L/SoundSynthesis.SAMPLE_RATE+200)
            true
        }catch(error:Exception){report("Áudio",error);false}
    }

    private fun stopSound(){val old=track;track=null;try{old?.pause();old?.flush();old?.release()}catch(_:Exception){}}
    private fun toast(text:String){Toast.makeText(activity,text,Toast.LENGTH_LONG).show()}
    private fun report(context:String,error:Throwable){val key="$context: ${error.message}";if(lastError!=key){lastError=key;handler.post{if(!destroyed)onError(context,error)}}}
    companion object{const val REQUEST_PERMISSION=7401;private const val CHANNEL="operational-alerts"}
}
