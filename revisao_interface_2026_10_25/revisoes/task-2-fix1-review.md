# Re-review Task 2 — fix round 1

Veredito de especificação desta rodada: **APROVADO**. Veredito de qualidade do patch: **APPROVE**. C1, I1, I2 e M1 estão **ADDRESSED**. Não identifiquei nova quebra Critical/Important introduzida pelo patch.

Escopo restrito a `revisoes/task2-fix1.diff`, seção final de `task-2-report.md` e evidências `revisoes/task2-fix1-*`. A aprovação se refere às correções da rodada, não à conclusão da Task 3 ou à conformidade visual integral. Não reexecutei testes, não ampliei a revisão do legado e não alterei produto.

## Achados anteriores

| Achado | Veredito | Fundamentação |
| --- | --- | --- |
| C1 — conclusão atingia evento diferente do exibido | **ADDRESSED** | `beginModalRequest` captura eventId e foco antes de awaits e incrementa geração por diálogo (`parts_js_ui.py:155`). `openModal` recebe explicitamente o evento local (`parts_js_ui.py:164`); os confirmadores usam somente a entrada de sua stack, sem fallback global (`parts_js_ui.py:3659`). Conclusão, reabertura, detalhes, action sheet e alarme conferem geração antes de preencher a interface. Close invalida aberturas pendentes. O probe original agora registra boundId=expectedId e A concluído/B pendente; os testes intercalam A lento/B rápido nos seis diálogos e invalidam abertura cancelada. |
| I1 — concluídos desapareciam após cruzar mobile/desktop | **ADDRESSED** | `getListModality` e `syncActiveListModality` (`parts_js_ui.py:15`, `parts_js_ui.py:19`) verificam a modalidade efetivamente renderizada no resize e na preferência manual. Só a lista ativa divergente é reconstruída. Concluídos atualizam cards/tabela e seus displays; expansão fica por ID. Testes usam 110 registros/página 2, busca, seleção e expansão em mobile→desktop→mobile e tiers manuais. Pendentes mantêm a modalidade escolhida, página/filtro/seleção e tabela acessível. Probe original: após resize, cards=0/rows=1, substituindo o antigo cards ocultos=1/rows=0. |
| I2 — cache e notificação cadastral não acompanhavam gravação | **ADDRESSED** | `publishCatalogChange` (`parts_js_ui.py:57`) aguarda snapshot, repovoa filtros e só então notifica. O patch coloca sua chamada após await do serviço em criar/editar, cinco toggles, exclusões e inativações por dependência. Nos cinco métodos delete, a publicação está **dentro do callback confirmado**, depois de await delete, não após o método que apenas abre a confirmação (`parts_js_ui.py:3192`, `parts_js_ui.py:3244`, `parts_js_ui.py:3286`, `parts_js_ui.py:3330`, `parts_js_ui.py:3373`). Regressões cobrem os cinco toggles, CRUD dos cinco formulários e exclusão real com barreira assíncrona: nenhum sinal antes de liberar; depois do commit, DB/cache ausentes e notificação consistente. |
| M1 — pinch zoom ativava keyboard-open | **ADDRESSED** | `updateKeyboardState` (`parts_js_ui.py:209`) exige foco editável e normaliza altura por escala; acompanha resize/foco. CDP com escala 2, BODY focado e visualViewport=422/innerHeight=844 resulta em keyboardOpen=false. O trecho de getters controlados cobre shrink com editável, zoom e perda de foco. Continua uma heurística, sem alegação de teclado físico testado. |

## Pontos de concorrência conferidos

O snooze chamado diretamente por ID continua reconsultando o evento, com ID local e guarda geracional (`parts_js_ui.py:3709`). No caminho Alarme→Adiar, recebe a cópia do evento da entrada modalAlarmTrigger e abre sincronamente, preservando Escape imediato. Os botões de conclusão/detalhes do alarme também capturam o ID dessa entrada antes de fechar ou aguardar outra abertura. `showAlarmModal` captura sua requisição e copia o evento antes das leituras (`parts_js_ui.py:3679`). O estado global legado não decide mais o alvo dos confirmadores críticos.

A publicação cadastral não antecipa commit: todas as adições vistas no patch sucedem o await de escrita, incluindo callbacks de dependência. O teste específico de exclusão observa banco ainda preenchido, zero sinais e modal busy antes de liberar o serviço real. Isso cobre a distinção entre abrir uma confirmação e concluir a operação.

## Evidências e limites

Conferidos `task2-fix1-probe.log`, `task2-fix1-controller.log/.json`, testes adicionados no diff e resumo estruturado `task2-fix1-suite.json`. Controller: **18 testes, zero falhas/erros/skips**. Discovery entregue: **94 testes, 89 passam, cinco falhas HTML/CSS previstas, zero erros/skips**. As cinco falhas continuam exatamente descrição multiline/Enter, nomes acessíveis estáticos, tamanho touch e contraste; não são regressões deste patch.

Sem novos achados Minor nesta rodada. Testes de aparelhos físicos e a integração visual/semântica continuam com os limites já documentados.
