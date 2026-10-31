package br.com.livrodeprevisoes.alerts

import kotlin.math.*

/** Offline PCM counterparts of the web app's four synthesized patterns. */
object SoundSynthesis {
    const val SAMPLE_RATE=22050
    fun samples(type:String,volume:Int):ShortArray {
        if(volume<=0)return ShortArray(0)
        val duration=when(type){"beep"->.32;"siren"->1.1;"blip"->.16;else->.8}
        val gain=.3*volume.coerceAtMost(100)/100
        var phase=0.0
        return ShortArray((duration*SAMPLE_RATE).toInt()){index->
            val t=index.toDouble()/SAMPLE_RATE
            val signal=when(type){
                "beep"->{val x=if(t>=.18)t-.18 else t;if(x>.14)0.0 else sin(2*PI*880*t).sign*envelope(x,.02,.14)}
                "siren"->{val halfCycle=(t%.5)/.25;val frequency=if(halfCycle<=1)650+300*halfCycle else 950-300*(halfCycle-1);phase+=frequency/SAMPLE_RATE;((phase%1)*2-1)*exp(-5*t/1.1)*.7}
                "blip"->sin(2*PI*1046.5*t)*exp(-5*t/.15)
                else->{listOf(523.25,659.25,783.99).mapIndexed{note,frequency->val x=t-note*.15;if(x<0||x>.5)0.0 else sin(2*PI*frequency*x)*envelope(x,.03,.5)}.sum()/3}
            }
            (signal.coerceIn(-1.0,1.0)*gain*32767).roundToInt().toShort()
        }
    }
    private fun envelope(t:Double,attack:Double,end:Double)=if(t<attack)t/attack else exp(-5*(t-attack)/(end-attack))
}
