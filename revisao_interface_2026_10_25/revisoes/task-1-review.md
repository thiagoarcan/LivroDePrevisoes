# Revisão Task 1 — núcleo, persistência e backup

Status: CHANGES_REQUESTED.

Spec verdict: NÃO APROVADO. Há regressão da proteção de substituição e lacuna na validação de linhas de backup. O lease também não implementa a exclusão mútua declarada, embora o claim transacional reduza decisivamente seu impacto.

Quality verdict: NÃO APROVADO. O tick regrava coleções completas para cada evento, inclusive quando nenhum evento é elegível. A integridade transacional do claim, os retornos dos serviços e a preservação do histórico melhoraram, mas os três achados Important abaixo devem ser resolvidos.

## Escopo e evidência

Leitura do brief, spec, relatório, diff Task 1, implementações atuais e callsites originais específicos. Não houve varredura da base real nem nova execução da suíte de 30 testes. O probe `revisoes/task-1-review-probe.py` reutiliza somente a infraestrutura de HTML temporário, perfil temporário, IndexedDB real e Edge headless de `tests/test_core_browser.py`; executou três cenários focados em dúvidas concretas desta revisão. Nenhum arquivo de produto foi alterado.

O resultado externo `resultados/compatibility_ultimo.json` registra 3 testes GREEN, incluindo duas abas sem navigator.locks; isso demonstra o cenário exercitado, sem provar exclusão em todos os interleavings do lease.

## Critical

Nenhum identificado.

## Important

1. **Substituição ignora a proteção de backup preventivo existente.** Fonte: `parts_js_service.py:1831`–1833. O original aguardava `exportJSON()` antes de substituir (`originais/parts_js_service.py:1507`–1510). O novo método valida e abre diretamente a transação de substituição; o callsite original `originais/parts_js_ui.py:3650` também não exporta previamente. Reprodução: criar um evento; obter snapshot válido; retirar eventos e histórico desse snapshot; substituir `App.Backup.exportJSON` por uma função que lança `backup failed`; chamar `importJSON(snapshot,'replace')`. Resultado observado: `{called:0,applied:true,event:null}`. O dado foi removido sem sequer tentar a proteção de backup. Restaurar a garantia no serviço antes da transação; falha de download/backup deve deixar **todo** o banco inalterado, inclusive settings/lastBackupAt. Esse problema é do contrato do serviço, não de layout pendente.

2. **Backup aceita omissão de campos funcionais obrigatórios e desliga alarmes silenciosamente.** Fonte: `parts_js_service.py:1717`–1720 e 1733–1745. A checagem de booleanos percorre apenas as propriedades existentes; não exige `hasAlarm`. Reprodução: exportar snapshot de evento com `hasAlarm:true`, remover `hasAlarm` e importar em replace. O probe também removeu `alarmTriggerCount`; a importação retornou `applied:true` e persistiu a linha sem esses campos. Em `parts_js_service.py:1864`, `!event.hasAlarm` torna esse alarme inelegível permanentemente. O exportador/serviço antigo sempre escrevia `hasAlarm` (`originais/parts_js_service.py:583`), portanto exigir esse campo não quebra a compatibilidade legítima dos metadados opcionais de settings/faixas. Definir explicitamente os campos obrigatórios por coleção, separando os opcionais legados, e rejeitar arquivo incompleto sem escrita.

3. **Tick ocioso regrava eventos e histórico completos N vezes por segundo.** Fonte: `parts_js_service.py:1906`, `parts_js_service.py:1881`–1883 e `parts_js_core.py:727`–729. `tick()` chama `fireAlarm()` para todos os eventos; cada chamada inicia atomic de events/eventHistory/settings. Mesmo quando due retorna false e o callback retorna null, atomic faz clear/add de todos os registros. Reprodução real: carregar a demonstração de seis eventos/sete históricos, desabilitar todos os alarmes e contar chamadas dos métodos nativos add/clear durante um tick. Resultado: **18 clears, 84 adds, zero alarmes elegíveis**. O custo cresce como N×(N+H+1), inclusive para concluídos e tombstones; leitura e escrita de formulários disputam os mesmos stores a cada segundo. Isso não é apenas o custo documentado de uma transação ampla por operação de negócio: há uma operação ampla por linha mesmo sem alteração. Pré-filtrar elegibilidade usando snapshot de eventos/settings e conservar a revalidação final transacional; ou oferecer operação transacional que não regrave quando não há mudança. Adicionar prova focada de que tick ocioso não regrava a base.

## Minor e limite conhecido

- **Lease localStorage não é mutex.** Fonte: `parts_js_service.py:1875`–1878. Interleaving possível: A lê lease vazio; B lê vazio; A escreve owner A, relê A e começa callback; B escreve owner B, relê B e começa callback. Renovação não interrompe A após perder propriedade. Há também perda de exclusão se um callback sobreviver à expiração enquanto seu timer está suspenso. Efeito residual: callbacks/ticks e entregas externas de eventos diferentes podem executar simultaneamente entre abas. Entretanto, `fireAlarm` relê o evento e `due` dentro da transação readwrite antes de incrementá-lo, então esse interleaving **não demonstra** disparo duplicado do mesmo ciclo nem sobrescrita de conclusão/reconhecimento. O teste comum GREEN de duas abas é compatível com essa limitação. Corrigir o mecanismo de exclusão ou declarar que lease apenas reduz concorrência, sem afirmar lock exclusivo; a especificação atual pede exclusividade. Não classificado como perda/duplicação de alarme reproduzida.

- O código novo permanece em overrides ao final de dois grandes blocos legados; leitura inicial dos métodos não revela o comportamento efetivo. Não bloqueia isoladamente, mas consolidar os métodos ativos facilitaria revisões futuras.

## Compatibilidade e requisitos conferidos

- DB_NAME/DB_VERSION mantidos, sem migração destrutiva/dependência remota introduzida neste diff.
- CRUD passa a aguardar commit e rejeitar abort; atomic mantém callback síncrono e snapshot usa transação readonly única. Os callsites internos usam arrays de stores conhecidos e callbacks síncronos.
- saveUOBatch conserva `{created,existing,all}` usado pelos dois formulários originais; cadastros e transições conservam Promises e objetos esperados. deleteEvent conserva true e troca remoção física por tombstone com auditoria.
- importJSON agora retorna resultado estruturado. A UI original ignora applied/conflicts e anuncia sucesso, mas o contrato está explícito no relatório para Task 2; isso é integração pendente, não cobrado novamente como defeito Task 1.
- fireAlarm aceita chamadas antigas com argumentos extras porque passa a reler settings/estado; não usa snapshot obsoleto para claim. Conclusão/reconhecimento são transacionais nos mesmos stores, preservando serialização com claim.
- CSV filtrado exclui tombstones; IDs e PNG têm restrição suficiente para os templates atuais; textos conhecidos são escapados nos callsites originais consultados. A validação de exportedAt antecede a preparação usual do resumo através de validateBackupFile.
- Falhas de modal, menus, contadores, desenho, foco e layout permanecem fora desta revisão de Task 1.
