package br.com.livrodeprevisoes.alerts
import org.junit.Assert.*
import org.junit.Test
import kotlin.math.abs

class SoundSynthesisTest {
    @Test fun zeroAndNegativeVolumesProduceNoSound() {
        assertTrue(SoundSynthesis.samples("beep",0).isEmpty())
        assertTrue(SoundSynthesis.samples("siren",-4).isEmpty())
    }
    @Test fun fourPatternsProduceDifferentBoundedPcm() {
        val sounds=listOf("beep","chime","siren","blip").map{SoundSynthesis.samples(it,100)}
        assertEquals(listOf(7056,17640,24255,3528),sounds.map{it.size})
        sounds.forEach{assertTrue(it.any{sample->sample!=0.toShort()});assertTrue(it.all{sample->abs(sample.toInt())<=9831})}
        assertFalse(sounds[0].contentEquals(sounds[1]))
    }
    @Test fun volumeScalesOutputAndAbove100IsClamped() {
        val loud=SoundSynthesis.samples("blip",100);val quiet=SoundSynthesis.samples("blip",25)
        assertTrue(quiet.maxOf{abs(it.toInt())}<loud.maxOf{abs(it.toInt())}/3)
        assertArrayEquals(loud,SoundSynthesis.samples("blip",200))
    }
}
