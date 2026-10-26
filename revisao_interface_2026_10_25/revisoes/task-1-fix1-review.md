# Revisão Task 1 — fix round 1

Status: APPROVED_WITH_CONCERNS. Os três achados Important da primeira revisão estão ADDRESSED. Nenhum novo Critical/Important identificado no patch.

Spec verdict: APROVADO no escopo das três correções, com a decisão explícita de lease advisory registrada abaixo. Quality verdict: APROVADO no escopo deste patch.

## Escopo e evidência

Revisão restrita a `revisoes/task1-fix1.diff` contra `revisoes/task1_r1_base`, seção final de `task-1-report.md` e evidências RED/GREEN correspondentes. Foram consultados somente os produtores legados pertinentes aos novos campos obrigatórios: criação de catálogos, vínculos e histórico em `originais/parts_js_service.py`. Não houve alteração de produto, nova varredura do legado, probe adicional ou reexecução das suítes.

Os logs conferidos mostram: `resultados/task1-fix1-red.txt`, três testes com três falhas anteriores às correções; `resultados/task1-fix1-green.txt`, 33 testes GREEN em 85.700 s; `resultados/task1-fix1-compatibility.txt`, três testes GREEN em 9.911 s, incluindo duas abas sem navigator.locks. Esses são resultados executados pelo implementador e conferidos nesta revisão, não novas execuções do revisor.

## Veredito por achado

1. **Backup preventivo em replace — ADDRESSED.** `parts_js_service.py:1859` aguarda exportJSON({preventive:true}) depois da validação completa e antes da abertura da transação. `parts_js_service.py:1847`–1854 aguarda downloadBlob e, no modo preventivo, retorna antes de alterar settings/lastBackupAt ou chamar UI. O teste novo cobre rejeição da API de exportação, rejeição assíncrona do download e comparação das onze coleções antes/depois. Também confirma que o snapshot preventivo contém o evento original e que esse evento ainda existe quando o download termina. O contrato sem argumentos de exportJSON permanece compatível. A limitação da API de navegador, que não confirma a gravação física final do arquivo, está corretamente documentada.

2. **Omissão de campos funcionais em backup — ADDRESSED.** `parts_js_service.py:1686`–1703 define o esquema obrigatório e nullable; `parts_js_service.py:1728` exige propriedades próprias presentes, sem undefined/null indevido. hasAlarm e alarmTriggerCount passam a ser obrigatórios, eliminando a desativação silenciosa reproduzida anteriormente. O teste remove os campos por coleção e exige rejeição, verifica preservação da base na importação inválida e mantém aceitação de metadados legitimamente opcionais. Os campos adicionais exigidos em catálogos, vínculos e histórico correspondem aos produtores legados consultados: especialmente pipelineOperationalUnits sem active/updatedAt obrigatórios e histórico com previousValue/newValue nullable. Não identifiquei incompatibilidade nova com esses produtores.

3. **Tick ocioso com regravações quadráticas — ADDRESSED.** `parts_js_service.py:1935`–1937 pré-filtra candidatos elegíveis por snapshot consistente de events/settings. fireAlarm continua revalidando due dentro da transação final; a otimização não transfere a autoridade para um snapshot potencialmente obsoleto. `parts_js_core.py:725`–729 compara os arrays JSON antes/depois e não emite clear/add para coleções inalteradas, cobrindo também claim invalidado por concorrência e callbacks no-op. O teste instrumenta add/put/clear/delete nativos e confirma zero escritas no tick ocioso, atomic no-op e fireAlarm de evento concluído. A representação JSON é adequada ao contrato documentado de registros JSON deste aplicativo. Operações que alteram coleções continuam podendo regravar arrays inteiros; isso é custo conhecido de uma operação efetiva, separado do defeito corrigido de regravar por linha a cada segundo.

## Lease e limitações remanescentes

A decisão agora é coerente entre comentário do código (`parts_js_service.py:1902`–1903), relatório e mecanismo real: navigator.locks exclui callbacks quando disponível; localStorage apenas reduz concorrência. O fallback continua permitindo o interleaving A/B descrito na primeira revisão, portanto não há promessa de exclusividade de callbacks ou de entregas de eventos diferentes.

A transação IndexedDB permanece a autoridade de exclusão de claims do mesmo ciclo: a segunda aba relê o estado/contador/último disparo antes de decidir. Conclusão e reconhecimento usam stores concorrentes e não são substituídos pelo snapshot anterior ao claim. O teste de duas abas sem navigator.locks comprova seu cenário de claim; não comprova todos os interleavings externos. A decisão aceita nesta rodada substitui a exigência anterior de mutex no fallback e deve continuar explicitamente documentada. Não há evidência nova de disparo duplicado ou perda de conclusão causada pelo patch.

A integração da UI com applied/conflicts e as demais revisões de UI/layout continuam fora deste parecer. A manutenção dos overrides finais sobre métodos legados permanece um concern de legibilidade já apontado, sem novo bloqueio introduzido nesta rodada.
