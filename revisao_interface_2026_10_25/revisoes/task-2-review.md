# Revisão Task 2 — especificação e qualidade

Veredito de especificação: **REPROVADO nesta rodada**. Veredito de qualidade: **REQUEST_CHANGES**. Há um achado Critical e dois Important reproduzidos em navegador com IndexedDB temporário. As cinco pendências HTML/CSS já entregues à Task 3 não motivam esta reprovação.

Escopo: brief, especificação, contratos Task 1/Task 3, relatório e diff `resultados/task2-ui.diff`. Leituras pontuais da fonte atual somente para conferir os riscos concretos abaixo e construir probes. Nenhum arquivo de produto alterado. Suíte de 84 testes não reexecutada; o resultado entregue continua sendo 79 passam, cinco falhas HTML/CSS, zero erros. Probes em `revisoes/task-2-review-probe.py`, executados com Edge headless, contextos novos e HTML temporário pelos cinco blocos; nenhum perfil real.

## Critical

### C1 — A conclusão pode atingir um evento diferente do exibido

Fonte: `parts_js_ui.py:130` captura `selectedEventForAction` global na entrada da stack; `parts_js_ui.py:3639` atribui esse global antes dos awaits de catálogo em showCompleteModal; `parts_js_ui.py:3664` só abre o diálogo depois deles. `parts_js_ui.py:3601` troca o mesmo global ao chegar um alarme. A confirmação usa o evento capturado em `parts_js_ui.py:3580`.

Cenário reproduzido: iniciar conclusão do evento A; durante a leitura de consoles, chegar alarme de B; terminar a abertura de A. O texto `completeModalEventDesc` descreve A, mas a entrada de modalCompleteEvent contém o ID de B. Clicar Concluir persiste B como `concluido`, mantendo A `pendente`. O probe apenas atrasa uma leitura readonly para tornar determinística uma intercalação possível entre a UI e o motor; os serviços e a gravação de conclusão são reais.

Impacto: alteração operacional do registro errado, com histórico/ator de uma conclusão que o usuário não solicitou. A stack resolve a seleção somente depois da corrida; portanto o teste já existente de alarme→snooze aberto sequencialmente não cobre essa falha.

Correção necessária: vincular explicitamente o objeto/ID local à abertura de cada diálogo, sem recuperá-lo de estado global que pode mudar durante awaits; conferir também caminhos de alarme/snooze/detalhe. Acrescentar regressão com conclusão A e alarme B intercalados e conferir o banco após confirmar.

## Important

### I1 — Concluídos desaparecem ao cruzar mobile/desktop sem nova navegação

Fonte: `parts_js_ui.py:2553` decide a modalidade por tier/largura; `parts_js_ui.py:2568` renderiza apenas cards no mobile e `parts_js_ui.py:2610` deixa a tabela vazia. `parts_js_ui.py:346` atualiza tier/classes no resize, mas não atualiza a modalidade dos concluídos. A aplicação manual de modo também não renderiza concluídos (`parts_js_ui.py:289`).

Cenário reproduzido: abrir Concluídos em 390×844 com um registro, então redimensionar para 1440×1000. Antes: um card, zero linhas. Depois: tier `conventional`, um card com `display:none`, zero linhas. A lista fica visualmente vazia apesar de existir um resultado. A passagem inversa deixa cards vazios com a tabela oculta. O probe confirmou a primeira direção com o CSS entregue, sem depender das cinco falhas de semântica/tamanho/contraste da Task 3.

Correção necessária: ao mudar a modalidade efetiva, atualizar a lista de concluídos preservando filtros, página, seleção e estado de expansão/posição pertinente. Na regressão do fix, cobrir pendentes e concluídos em resize e mudança manual de tier, inclusive página posterior à primeira, verificando a modalidade efetiva e a preservação de filtros/página/seleção. Não exige renderizar todas as telas em cada resize. Uma correção apenas CSS não cria os nós deliberadamente omitidos pela UI.

### I2 — O contrato de apresentação fica desatualizado após CRUD de duto

Fonte: `parts_js_ui.py:35` entrega snapshot em cache; `parts_js_ui.py:3167` executa togglePipelineActive e chama apenas renderPipelinesTable (`parts_js_ui.py:2943`), sem invalidar a cache nem notificar apresentação. O mesmo caminho de tabela é usado após savePipeline (`parts_js_ui.py:2736`). Os novos hooks em renderCadastros/refreshAllMasterDataDropdowns não são atravessados por essa ação.

Cenário reproduzido: navegar para Cadastros; instalar observador de app-ui-update; clicar logicamente na ação pública togglePipelineActive de um duto. Após aguardar a Promise, o registro real está `active:false`, mas `getPresentationState().snapshot.pipelines` ainda informa `active:true`; notificações recebidas: `[]`. A tabela principal acompanha a gravação, enquanto os painéis de contexto sem polling ficam contraditórios até outra ação provocar refresh. Isso viola o requisito de contexto acompanhar CRUD.

Conferência dirigida das cinco ativações: toggleConsoleActive (`parts_js_ui.py:3117`) chama initHeaderConsole, que notifica console sem atualizar snapshot; togglePipelineActive (`parts_js_ui.py:3167`), toggleEquipmentTypeActive (`parts_js_ui.py:3247`) e toggleEquipmentTagActive (`parts_js_ui.py:3287`) só atualizam suas tabelas. toggleUOActive (`parts_js_ui.py:3205`) já passa por refreshAllMasterDataDropdowns, que atualiza cache e notifica. O probe dinâmico foi do duto; os demais caminhos foram conferidos estaticamente, sem alegar uma reprodução independente de todos.

Correção necessária: publicar snapshot atualizado e notificação após commit de todas as operações cadastrais, incluindo salvar/excluir/ativar/inativar. A apresentação da Task 3 deve continuar consumidora dos hooks; não deve precisar envolver métodos ou fazer polling para reparar essa lacuna. A regressão deve cobrir os cinco toggles e CRUD assíncrono, conferindo simultaneamente DB, snapshot e evento publicado após a Promise, preservando o caminho correto de UO.

## Minor / handoff

### M1 — Pinch zoom é anunciado como teclado aberto

Fonte: `parts_js_ui.py:187` liga keyboard-open exclusivamente por visualViewport.height < 70% de innerHeight.

Probe CDP Emulation.setPageScaleFactor=2 em 390×844, sem campo focado: `scale:2`, `height:422`, `innerHeight:844`, foco em BODY e `keyboardOpen:true`. É um falso positivo confirmado. Não há consumidor CSS atual de keyboard-open, então o probe não demonstra navegação perdida no produto desta Task 2. O contrato entregue, porém, autoriza a Task 3 a recolher navegação com essa classe; isso transformaria zoom legítimo em ocultação indevida de ações. Corrigir a detecção considerando foco editável/escala ou garantir que o consumidor não esconda ações apenas por esse sinal. Verificar zoom/pinch no handoff.

## Contratos e pontos conferidos

- Confirmação/dependência/importação usam uma ação atual descartada em closeModal. A confirmação assíncrona desabilita o botão e bloqueia Escape/backdrop enquanto busy; conflito de importação preserva o diálogo e não anuncia aplicação falsa.
- Prévia valida o envelope antes de ler campos; replace deixa backup preventivo no serviço, sem duplicá-lo. Reload após importação aplicada inclui preferências e seletores. Demonstração tem texto destrutivo explícito, export preventivo, clear e loadDemoData.
- Foco inicial/trap/retorno, inert e Escape no topo estão centralizados; drawer/filtro/fullscreen usam a API. O defeito C1 impede aprovar a identidade do evento na stack em concorrência, mesmo com o caminho sequencial alarme→snooze coberto.
- Countdown de spotlight/alarme usa timestamp próprio; janelas de métricas são disjuntas, completedToday usa dia local, temporalSignature evita leitura/render ocioso por segundo. Há paginação explícita e render de uma modalidade por vez. I1 é consequência funcional não coberta dessa otimização.
- Zeros de preferências usam conversão numérica/nullish, snooze valida inteiro 1–1440, e o serviço permanece a autoridade de validação. Diagnóstico usa versão central e logs reais.
- Hooks fornecem dados reais sem polling, mas a invalidação após CRUD é incompleta (I2). getPresentationState entrega referências da cache; o consumidor de apresentação deve tratá-las como readonly.
- Não identifiquei mudança dos IDs públicos, banco, formato de backup ou montagem offline em cinco blocos no diff. As mudanças de CSS/HTML da Task 3 ainda são necessárias e não foram exigidas nesta revisão.

As cinco falhas atribuídas à Task 3 são coerentes com o handoff: textarea e Enter, labels estáticos, dimensões touch e contraste. Elas não cobrem C1/I1/I2. Testes físicos de caneta/palma, teclado móvel e suspensão continuam fora da evidência, como declarado no relatório.
