# Task 2 — controlador integral de interface

**Status: DONE_WITH_CONCERNS.** Fix round 1 concluído e verificado: **94 testes, 89 passam, as mesmas cinco falhas HTML/CSS, zero erros**, em 72,851 s. UIController: **18/18**, workflows: **11/11**. Composição/semântica HTML e CSS seguem com a Task 3. As seções iniciais preservam a evidência da primeira entrega (84 testes); a seção de revisão ao final documenta os contratos corrigidos e os resultados atuais. Nenhuma alteração em core/service, HTML/CSS, build ou index.html; nenhum perfil real ou dependência remota utilizada.

## Comportamento entregue

- Confirmação, dependência e importação mantêm uma única ação atual. Cancelar/Escape/backdrop descartam a ação. Botão crítico fica desabilitado durante a Promise; Escape e backdrop não interrompem a operação nem permitem duplo envio. Erros permanecem visíveis e são registrados; a ação pode ser repetida após erro/conflito.
- Todos os caminhos de abrir/fechar diálogos passam por `openModal`/`closeModal`. Stack, foco inicial, Tab/Shift+Tab, retorno, fundo inert e Escape apenas no topo. Alarme→snooze conserva o alarme inferior e seu evento; cada operação crítica resolve o evento do próprio diálogo. Drawer fechado fica inert, abre com foco e retorna ao botão ao fechar. Filtros móveis usam o mesmo controlador e `active-sheet`.
- Prévia revalida o envelope completo antes de usar os campos. Resultado da importação distingue aplicada/não aplicada e mostra inseridos/atualizados/ignorados/conflitos. Replace deixa o backup preventivo para o serviço. Importação aplicada recarrega tema, densidade/tier, modo de lista, usuário, console e seletores. Demonstração exporta backup preventivo, limpa a base e carrega a massa original completa; o texto informa a substituição. Limpeza também reinicializa preferências/console. Exclusão informa preservação do histórico.
- Auto expõe sempre os cinco tiers em `data-layout-mode`: mobile <768, tablet <1200, conventional <1920, widescreen <2560, ultrawide a partir de 2560. Compacto é `density-compact`; preferência manual persiste; `layout-narrow` reflete largura física <768. Resize não regenera formulários; reconstrói somente a lista ativa quando muda sua modalidade e mantém rascunho, filtros, categoria, seleção e desenho.
- Spotlight e alarme mantêm seus próprios timestamps/IDs. Todos os contadores usam segundos. A cache vem de snapshot transacional em atividade de render/gravação; ticks ociosos só atualizam texto. Transição de faixa/janela/dia e mudança de alarmes invalidam a apresentação. Não há polling paralelo de dados nem render de todas as telas a cada segundo. O motor continua a autoridade do estado triggered e do título.
- Métricas aplicam janelas disjuntas 0–15, >15–30 e >30–60; total limpa filtros; atrasados usa prazo; não reconhecidos usa triggered. Métrica de concluídos usa data local de conclusão, com filtro explícito removível. Banner/sino também filtram triggered. Badge conta filtros ativos, incluindo console atual e filtro temporal. Combos são repovoados preservando valores ainda válidos.
- Detalhe inicial usa `detalhes`, antecedência efetiva usa alarmMinutesBefore/default. Desenhos PNG seguros mostram também o ancestral correto; evento sem desenho limpa src e oculta a região. Sheet mostra console/duto/UO/horário. Categorias cadastrais usam somente `currentCadastrosCategory`.
- Zeros são preservados ao salvar, reabrir configurações, editar e duplicar eventos. Snooze valida inteiro 1–1440. Lembrete de backup é editável em 1–3650 dias. Preferências de pulsação/destaque geram flags e retiram classes animadas; redução de movimento também é respeitada. Texto de countdown deixa contraste para os tokens do tema, mantendo a faixa configurada em `--event-color` e nas bordas.
- Canvas tem bitmap lógico 1200×440 e proporção CSS correspondente; resize/rotação não reamostram nem esticam o desenho. Captura identifica pointerId, rejeita ponteiros concorrentes e preserva prioridade de caneta. Touch fora do desenho continua rolável. Ferramentas ficam dentro da região fullscreen, que agora participa da stack/foco/Escape. Undo, borracha e limpeza confirmada continuam funcionais.
- Pendentes/concluídos renderizam **até 50 registros de uma única modalidade** por página. Resultados completos continuam em memória para filtros e detalhe. Paginação informa total, página e ações Anterior/Próxima; detalhe navega o conjunto filtrado completo independentemente da página. Lista urgente do dashboard também é limitada a 50, com acesso à lista completa. Não reduzimos a massa de demonstração nem as expectativas.
- Cards concluídos realmente alternam `.completed-card-details`, hidden/display e aria-expanded; cards/métricas têm teclado. Diagnóstico exibe APP_VERSION, estado local e erros reais; relatório copiado inclui logs. Aviso inicial mobile é uma nota dispensável no fluxo normal, sem bloquear consulta ou alarme.

## Contrato público para Task 3

`window` recebe `CustomEvent('app-ui-update', {detail:{reason,view,eventId}})`. Reasons atuais: init, navigation, dashboard, filters, completed, selection, catalog, settings, ranges, diagnostic, console, layout, crud, import e time. São notificações de estado; o módulo de apresentação pode ler a cache sem criar polling. Eventos iniciais podem ocorrer antes da primeira cache; a inicialização formal acontece depois de `renderDashboard` e `refreshPresentationCache`.

`App.UI.getPresentationState()` retorna:

```js
{
  snapshot, settings, ranges, view, activeConsoleId,
  pending, completed, selectedEventId,
  selections: {pending, completed, dashboard}, spotlightEventId,
  category, tier, metricFilter, filters,
  classifyEvent: event => App.Service.classifyEvent(event, ranges)
}
```

`snapshot` contém as dez coleções oficiais; errorLogs é acrescentada quando diagnóstico é carregado. pending/completed são resultados filtrados completos, não apenas a página. selectedEventId é específico da visão: spotlight no dashboard, seleção de concluídos ou seleção de pendentes. Ao desaparecer um selecionado do filtro, pendentes/concluídos escolhem o primeiro resultado ou null. `selectPendingDetailEvent`, `movePendingSelection` e `selectCompletedEvent` são ações públicas. `App.UI.formatCountdown(timestamp)` retorna `{text,isOverdue}`, com segundos; `localDate(value?)` retorna YYYY-MM-DD no fuso local.

`if (App.Presentation) await App.Presentation.init()` é chamado antes de iniciar o motor. O módulo extra pode ser carregado antes de DOMContentLoaded. Não precisa envolver métodos ou criar um segundo cache/motor. Formulários permanecem únicos; input/change são fontes adequadas para suas prévias.

Hooks/IDs realmente usados:

| Hook | Contrato |
| --- | --- |
| body[data-layout-mode], .density-compact, .layout-narrow | Tier efetivo, densidade independente e segurança de largura física |
| body.disable-pulsing, body.disable-highlight | Preferências visuais salvas; CSS deve neutralizar efeitos correspondentes |
| body.keyboard-open | Exige foco editável e visualViewport.height × visualViewport.scale menor que 70% de innerHeight; pinch isolado não ativa a classe |
| --app-header-height | Altura real do header atualizada por ResizeObserver |
| #pendingPagination / #completedPagination, .events-pagination | Nav criada uma vez, total + Anterior/Próxima, botões nativos |
| #btnClearCompletedScope | Botão nativo para remover filtro “Concluídos hoje”; hidden quando inativo |
| .detail-navigation | Navegação anterior/próxima no detalhe de pendentes |
| .completed-card-details | hidden/display geridos pela UI; raiz tem aria-expanded e classe expanded |
| #filterDrawer.active-sheet | Sheet móvel, aria-modal e foco geridos pelo controlador |
| #appMobileDrawer.open | Drawer ativo; fechado inert; botão publica aria-expanded |
| #inputBackupReminderDays | Number 1–3650, label associado; injetado apenas se HTML ainda não tiver o ID |
| #appRuntimeNotice.runtime-notice | Nota mobile inicial não bloqueante; botão Entendi persiste preferência |
| #boxStylusCanvas.fullscreen-lousa | Mesma stack modal; toolbar dentro; proporção de canvas preservada |
| --event-color nos countdowns | Cor da faixa original disponível para apresentação; texto herda cor legível do tema |
| #spotlightTimeLeft[data-timestamp], #alarmModalCountdown[data-timestamp] | Timestamps próprios, sem depender do filtro pendente |

Preferir as classes HTML existentes bottom-nav-item, bottom-nav-fab, bottom-nav-badge e cadastros-category-btn. Não duplicar IDs. O HTML da Task 3 ainda deve fornecer textarea/labels/nomes em fonte; o controlador já nomeia diálogos como reforço.

## RED/GREEN e evidências

RED original: `resultados/ui_red_original.log`, 23 regressões falhando antes da correção. O coordenador acrescentou a 24ª regressão, precisão por segundo, que também passa agora. Fixture de cancelamento de importação foi corrigida pelo coordenador para utilizar snapshot completo e o retorno oficial applied do serviço, preservando a expectativa A cancelado/B executado.

Novos nove testes em `tests/test_ui_controller_browser.py`: busy/duplo clique/Escape, alarme→snooze empilhados, 503 registros/50 nós/modalidade única/página seguinte, urgentes limitados, tick ocioso sem leitura/render, dia local/remover filtro, fullscreen/Escape, conflito sem falso sucesso, zeros na reabertura/edição. `resultados/task2-controller-red.log` registra falhas de escopo de hoje, urgentes ilimitados e fullscreen. O primeiro teste de escala tinha duas suposições incorretas no harness novo: fixture podia escolher outro console quando o filtro atual estava ligado, e IDs de mesma data não têm ordem numérica no IndexedDB. Fixture foi alinhada ao console ativo e a comparação usa o 51º item da ordenação real, sem reduzir 503 registros. RED adicional de zeros mostrou 15/80/5 em lugar de zero; GREEN final registra todos os nove passando.

Comandos executados, sempre com HTML e IndexedDB temporários no Edge headless:

| Comando | Resultado final |
| --- | --- |
| python tests/test_ui_browser.py | 24 testes: 22 passam, 2 falhas HTML |
| python tests/test_workflows_browser.py | 10/10 passam |
| python tests/test_ui_controller_browser.py | 9/9 passam |
| python tests/test_accessibility_browser.py | 5 testes: 2 passam, 3 falhas HTML/CSS |
| python revisao_interface_2026_10_25/run_task2_suite.py | Discovery completo: 84 testes, 79 passam, 5 falhas, 0 erros, 0 skips |
| python -m compileall -q parts_js_ui.py | Sucesso |

Logs: `task2-ui-final.log`, `task2-workflows-final.log`, `task2-controller-green.log`, `task2-a11y-final.log`, `task2-suite-final.log` e `task2-suite-final.json` em resultados. Discovery inclui também os 33 testes core e 3 compatibility, todos passando. Não executa os runners standalone de geometria/Firefox; essa matriz cabe à Task 3/integração.

Houve timeout intermitente de startup em contextos frios durante execução concorrente; o coordenador ajustou o orçamento inicial do harness. Houve também um erro de diagnóstico introduzido durante a troca para snapshot: DATA_STORES não inclui errorLogs. A leitura explícita foi restaurada e o rerun completo confirma zero erros. Esses runs intermediários não são apresentados como GREEN.

## Cinco falhas restantes atribuídas à Task 3

1. `test_description_is_multiline`: inputEventDescription ainda é INPUT no HTML fonte; converter para TEXTAREA com o mesmo ID.
2. `test_all_dialogs_and_controls_have_accessible_names`: nomes dos diálogos passam; 34 inputs/selects HTML ainda não têm labels associados/nome acessível. Corrigir fonte, incluindo ferramentas de caneta, filtros e arquivos.
3. `test_description_enter_does_not_submit`: Enter ainda envia o formulário porque descrição é INPUT; mesma correção textarea.
4. `test_mobile_fields_and_main_actions_have_touch_size`: campos/ações ainda têm dimensões/fontes antigas abaixo da aceitação de 44 px/14 px no mobile. Corrigir CSS/inline do HTML.
5. `test_rendered_text_contrast_key_components`: contrastes estáticos ainda falham, principalmente texto auxiliar, navegação e botão primário no tema claro. Detalhes de cores/razões estão no log/JSON. Texto countdown deixou de forçar cores de faixa de baixo contraste.

## Self-review e limites

Conferidos caminhos de fechamento, callback único, validação antes da prévia, resultado applied, backup preventivo único em replace, preservação da massa demo, zeros em salvamento/edição/reapresentação, classificação oficial, fuso local, modalidade única e paginação. Diff contra o snapshot original está em `resultados/task2-ui.diff`. Nenhum arquivo de produto fora da UI foi alterado.

Proporção/rotação, pointerId e fullscreen foram verificados em navegador desktop com emulação de viewport; palma física, caneta real, teclado móvel real, som audível do sistema, suspensão/tela bloqueada e permissões do sistema não são declarados testados. A aplicação não promete alarmes em navegador suspenso. A composição visual dos hooks e o contraste de todo o produto dependem da Task 3; não há declaração de conformidade formal de acessibilidade neste relatório.

## Revisão Task 2 — fix round 1/5

Revisão recebida em `revisoes/task-2-review.md` e conferida com o probe original. Foram tratados somente C1, I1, I2 e M1. Base imutável desta rodada: `revisoes/task2_r1_base/parts_js_ui.py` e `test_ui_controller_browser.py`. Patch exclusivo desta rodada: `revisoes/task2-fix1.diff`; não confundir com o diff inicial contra originais. Nenhuma alteração no HTML, CSS, núcleo, serviço, build ou index. O coordenador acrescentou o 11º workflow do canvas; esse arquivo não integra o patch da UI desta rodada.

### C1 — identidade do evento e requisições obsoletas

`beginModalRequest(dialogId, eventId)` captura o ID e o foco de retorno **antes de qualquer await**, atribuindo uma geração por diálogo. Conclusão, reabertura, snooze, detalhes, sheet de ações e alarme só escrevem a interface após `isModalRequestCurrent(request)`. Chamadas antigas da mesma modalidade não sobrescrevem a mais recente. `closeModal` invalida a geração, inclusive se a abertura ainda estiver lendo o banco. Busy continua impedindo rebind/fechamento da operação crítica.

Contrato atualizado: `openModal(id, event = null, request = null)` recebe o contexto local explícito. A stack não captura mais o global selectedEventForAction; confirmadores críticos não têm fallback para esse global. A propriedade legada permanece para compatibilidade de leitura, sem decidir o alvo de gravações. Todos os dados de detalhe/histórico são obtidos antes de preencher o diálogo, evitando também mistura de textos de duas requisições.

O botão Alarme→Adiar passa o evento da própria stack diretamente a `showSnoozeModal(id, currentAlarm)`, abrindo o topo sincronamente sem nova leitura desnecessária. Chamadas diretas por ID continuam consultando o banco com guarda geracional. Isso preserva Escape imediato no snooze; a gravação continua validada/releita pelo serviço.

Regressões: conclusão de A suspensa numa leitura real de catálogo, chegada de alarme B e confirmação persistem **A concluído/B pendente**. Outra regressão intercala A lento/B rápido nos seis diálogos, conferindo evento vinculado e textos quando existentes. Fechamento durante abertura lenta impede reabertura posterior. O teste do probe original agora mostra descrição e boundId de A.

### I1 — modalidade ativa no resize e na preferência manual

`getListModality('pending'|'completed')` é a autoridade da modalidade. Pendentes conserva viewMode escolhido; concluídos usa cards em tier mobile ou largura física estreita, tabela nos demais. `renderedListModalities` registra o DOM efetivamente criado. `syncActiveListModality` é chamado no resize e na aplicação manual; só renderiza a lista ativa quando a modalidade diverge. Trabalhos simultâneos de sincronização compartilham uma Promise e a modalidade é conferida novamente após o render.

Página, filtro e seleção não são reiniciados. `expandedCompletedIds` conserva a expansão por ID quando cards são omitidos em favor da tabela e os restaura no retorno. A posição da janela e das regiões de lista é reaplicada se a visão continuar a mesma. O controlador publica display coerente em containerCompletedCards/tableCompletedWrapper, sem depender de CSS para criar os nós omitidos.

Regressões usam **110 registros e página 2**, com busca, seleção e expansão. Cobrem resize físico mobile→desktop→mobile sem chamar applyResponsiveLayoutMode, depois preferência mobile/conventional em largura desktop. Pendentes conserva a tabela escolhida, página, busca e seleção ao atravessar larguras/tiers. O probe original passou de cards1/rows0 para cards0/rows1 após resize.

### I2 — snapshot e evento após commit cadastral

`publishCatalogChange()` aguarda snapshot consistente, repovoa seletores preservando valores válidos e só então emite `app-ui-update` com reason catalog. Está imediatamente após **22 chamadas de escrita** da UI: criar/editar dos cinco cadastros, lote/adição inline de UO, cinco toggles, cinco exclusões e suas inativações por dependência. O fluxo correto de UO foi conservado. Nenhum método do serviço foi envolvido e a apresentação não precisa de polling.

Regressões conferem banco, cache e sinal publicado para os cinco toggles e create→update→delete dos cinco formulários, com serviços/IndexedDB reais. A exclusão confirmada tem ainda uma barreira assíncrona antes de chamar o serviço real: antes de liberar, não há sinal e o registro existe; depois de commit, DB/cache não contêm o registro e o sinal apresenta sua ausência. A Promise externa de delete que apenas abre confirmação não é tratada como commit. O probe de duto agora observa DB=false/cache=false e reason catalog.

### M1 — teclado sem falso positivo por zoom

`updateKeyboardState()` exige foco em input editável, textarea ou contenteditable, excluindo disabled/readOnly. Compara `visualViewport.height * visualViewport.scale` a innerHeight; eventos resize/focusin/focusout atualizam o sinal. Pinch muda altura e escala juntas e não representa teclado. O contrato continua sendo uma heurística de viewport, sem alegação de teste de teclado físico/móvel real.

Regressão usa CDP Emulation.setPageScaleFactor=2 real, em 390×844 e foco BODY, e exige keyboard-open false. Um segundo trecho controla getters de altura/escala para provar shrink com campo editável=true, mesmo shrink por zoom=false e ausência de foco=false. O probe original também retorna keyboardOpen=false com scale2/height422/innerHeight844.

### RED, GREEN e comandos desta rodada

`revisoes/task2-fix1-red.log`: 17 testes na primeira execução, cinco falhas e cinco erros de expectativa não satisfeita (quatro subtests CRUD e resize aguardavam sinais/nós inexistentes). RED reproduziu boundId incorreto, reabertura obsoleta, cache antigo, resize vazio e falso teclado. Os erros de espera são das regressões dos comportamentos ausentes, não de startup do harness.

`run_task2_fix1.py --baseline ...` carrega somente a UI de task2_r1_base em um módulo separado, mantendo o núcleo/serviço atuais, sem substituir arquivos de produto. A regressão adicional de exclusão assíncrona e as versões fortalecidas de latest-request/resize também falham nesse snapshot: três testes, duas falhas e um timeout por ausência dos nós da modalidade nova. Evidência: `task2-fix1-baseline.log/.json`.

Resultados focados, posteriores às correções: diálogos 4/4, modalidade 2/2, catálogo 2/2 e teclado 1/1. O primeiro standalone ampliado encontrou uma corrida de Escape após o novo await do snooze; a passagem local explícita do evento já carregado removeu essa janela, e o teste agora exige abertura síncrona antes de enviar Escape. Não foi ocultada nem enfraquecida a expectativa.

Comandos reproduzíveis:

```text
python revisao_interface_2026_10_25/revisoes/task-2-review-probe.py
python revisao_interface_2026_10_25/revisoes/run_task2_fix1.py
python revisao_interface_2026_10_25/revisoes/run_task2_fix1.py --all
python -m compileall -q parts_js_ui.py tests/test_ui_controller_browser.py
```

O runner registra stdout/resultado estruturado e logs UTF-8 em `revisoes/task2-fix1-{probe,controller,suite}`. UIController ampliado tem **18 testes**; a suíte discovery tem **94** incluindo os 11 workflows do coordenador. Os cinco casos HTML/CSS da primeira entrega continuam explicitamente atribuídos à Task 3; não se modificou expectativa, massa demo ou semântica via remendo para fazê-los passar. Snapshot de apresentação permanece readonly para consumidores. Os limites físicos da primeira entrega permanecem.

Verificação final após a última alteração de produto: **18/18 UIController em 12,463 s** e **94 testes discovery em 72,851 s: 89 passam, cinco falhas, zero erros e zero skips**. Core33, compatibility3 e workflows11 passam integralmente. UI24 conserva 22 passes e as duas pendências de textarea/labels; accessibility5 conserva dois passes e as três pendências de Enter/touch/contraste. A lista nominal das cinco falhas é idêntica à seção da Task 3 acima. Compileall concluiu com sucesso. `task2-fix1-suite.json` e `.log` são a evidência atual; arquivos task2-suite-final da primeira entrega permanecem históricos.

Self-review da rodada conferiu os seis pontos de captura local antes de await, guardas antes de preencher DOM, ausência de fallback global nos confirmadores, invalidação ao fechar, 22 publicações pós-commit, uma modalidade no DOM e preservação de expansão por ID. O patch escopado contém apenas `parts_js_ui.py` e `tests/test_ui_controller_browser.py`; relatório e runners são documentação/evidência. Nenhuma coleta adicional ou alteração de produto fica pendente desta rodada.

## Revisão Task 2 — fix round 2/5

**Status: DONE.** I3/GUI-37 corrigido exclusivamente na exibição do controlador de conclusão em cards e tabela. A UI utiliza completedBy real quando é string não branca; para campo ausente, null, vazio ou espaços mostra **Não informado**. Não utiliza createdBy nem Usuário local como autoria inferida. Nenhum dado persistido foi alterado.

Arquivo de produto alterado: `parts_js_ui.py`, somente as duas expressões controllerName. Busca dirigida encontrou essas duas ocorrências equivalentes no controlador. Núcleo, serviço, HTML, CSS, Presentation e testes não foram alterados nesta rodada. A concatenação Python `JS_UI += JS_PRESENTATION` da Task 3 foi preservada: a verificação compara o arquivo inteiro à base `revisoes/task2_r2_base/parts_js_ui.py` e exige igualdade após apenas as duas substituições previstas.

RED da raiz: `resultados/ator_conclusao_red.log`; o teste `EditJourney.test_missing_completion_actor_is_not_replaced_with_creator` mostrava Pessoa que apenas criou na autoria de conclusão. A raiz ampliou a mesma regressão para null/vazio/espaços→Não informado e ator real→preservado, em tabela e cards. Expectativas mantidas.

Comandos e saídas desta rodada:

```text
python revisao_interface_2026_10_25/revisoes/run_task2_fix2.py
Ran 44 tests in 37.175s — OK

python -m compileall -q parts_js_ui.py
exit 0

python revisao_interface_2026_10_25/revisoes/make_task2_fix2_diff.py
Only two completion-actor expressions changed; Task3 concatenation preserved.
```

Cobertura específica solicitada: **edição 2/2, UI 24/24 e controlador 18/18 — 44/44, zero falhas, zero erros, zero skips**. Inclui os quatro estados de autoria nas duas modalidades e a jornada real de edição com preservação de registro/histórico. Logs/resultado estruturado: `revisoes/task2-fix2-tests.log` e `task2-fix2-tests.json`. Patch escopado exclusivamente às duas linhas da UI: `revisoes/task2-fix2.diff`. Runners são artefatos de verificação; não integram o produto.

Os números de 94 testes/falhas HTML-CSS acima são históricos da rodada 1. Esta rodada verificou os 44 testes solicitados sobre a composição atual da Task 3; a integração completa permanece sob a raiz. Não foi regenerado index.html. Self-review confirmou ausência de fallback ao criador, tratamento de string branca e preservação de todo o restante da fonte contra a base desta rodada.
