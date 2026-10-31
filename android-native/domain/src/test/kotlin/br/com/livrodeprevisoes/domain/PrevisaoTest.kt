package br.com.livrodeprevisoes.domain

import org.junit.Assert.*
import org.junit.Test
import java.time.LocalDate
import java.time.LocalTime

class PrevisaoTest {
    private fun entrada() = EntradaPrevisao("c", "d", "u", LocalDate.of(2026, 10, 31), LocalTime.of(12, 0), " Atividade ", true, 15)
    @Test fun camposObrigatorios() {
        assertEquals("O Console é obrigatório.", validar(entrada().copy(consoleId = "")))
        assertEquals("O Duto é obrigatório.", validar(entrada().copy(dutoId = "")))
        assertEquals("A UO é obrigatória.", validar(entrada().copy(uoId = "")))
        assertEquals("A descrição da atividade é obrigatória.", validar(entrada().copy(descricao = "  ")))
        assertEquals("A antecedência do alarme deve ser igual ou superior a 0 minutos.", validar(entrada().copy(antecedenciaMinutos = -1)))
        assertNull(validar(entrada()))
    }
    @Test fun limitesDeClassificacao() {
        val faixas = faixasPadrao()
        assertEquals("Atrasado", classificar(-1, faixas).nome)
        assertEquals("Crítico", classificar(0, faixas).nome)
        assertEquals("Crítico", classificar(899999, faixas).nome)
        assertEquals("Urgente", classificar(900000, faixas).nome)
        assertEquals("Atenção", classificar(1800000, faixas).nome)
        assertEquals("Monitoramento", classificar(2700000, faixas).nome)
        assertEquals("Normal", classificar(3600000, faixas).nome)
    }
}
