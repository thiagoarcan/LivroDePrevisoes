package br.com.livrodeprevisoes.domain

import java.time.LocalDate
import java.time.LocalTime

data class EntradaPrevisao(val consoleId: String, val dutoId: String, val uoId: String, val data: LocalDate?, val hora: LocalTime?, val descricao: String, val temAlarme: Boolean, val antecedenciaMinutos: Int?)
fun validar(entrada: EntradaPrevisao): String? = when {
    entrada.consoleId.isBlank() -> "O Console é obrigatório."
    entrada.dutoId.isBlank() -> "O Duto é obrigatório."
    entrada.uoId.isBlank() -> "A UO é obrigatória."
    entrada.data == null -> "A data do evento é obrigatória."
    entrada.hora == null -> "A hora do evento é obrigatória."
    entrada.descricao.isBlank() -> "A descrição da atividade é obrigatória."
    entrada.temAlarme && (entrada.antecedenciaMinutos == null || entrada.antecedenciaMinutos < 0) -> "A antecedência do alarme deve ser igual ou superior a 0 minutos."
    else -> null
}

data class Faixa(val nome: String, val minimoMinutos: Long, val maximoMinutos: Long, val cor: String, val prioridade: Int, val pisca: Boolean, val som: Boolean)
fun faixasPadrao() = listOf(
    Faixa("Crítico", 0, 15, "#dc2626", 1, true, true),
    Faixa("Urgente", 15, 30, "#ea580c", 2, false, false),
    Faixa("Atenção", 30, 45, "#ca8a04", 3, false, false),
    Faixa("Monitoramento", 45, 60, "#2563eb", 4, false, false),
    Faixa("Normal", 60, 999999, "#16a34a", 5, false, false)
)
fun classificar(diferencaMillis: Long, faixas: List<Faixa>): Faixa {
    require(faixas.isNotEmpty()) { "Ao menos uma faixa é necessária." }
    if (diferencaMillis < 0) return Faixa("Atrasado", 0, 0, "#991b1b", 0, true, true)
    val ordenadas = faixas.sortedBy { it.minimoMinutos }
    return ordenadas.firstOrNull { diferencaMillis >= it.minimoMinutos * 60000 && diferencaMillis < it.maximoMinutos * 60000 } ?: ordenadas.last()
}
