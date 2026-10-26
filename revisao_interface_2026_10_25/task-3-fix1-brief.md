# Task 3 — fix round 1/5

Leia primeiro `revisoes/task-3-review.md`. Os achados I1–I6 são a lista de correções, com reproduções e recomendações verbatim nesse arquivo. Corrija todos, sem substituir a proposta aprovada por outra arquitetura. Preserve core/service/UI, salvo a concatenação Python já autorizada. O fix da autoria na UI foi aprovado separadamente; não o reverta.

O usuário autorizou **todas** as correções. O coordenador confirmou que M1–M3 também conflitam com a proposta: console deve identificar o valor completo, recomendações devem ser legíveis e filtros de concluídos devem ser recolhíveis no celular. A decisão está no ledger. Trate-os nesta mesma alteração delimitada; não crie tarefas novas nem adie defeito visual conhecido. Use disclosure nativo com summary “Filtros” em Concluídos, preservando IDs/valores/listeners e um resumo do escopo aplicado.

Achado adicional X1 confirmado pela raiz: `parts_js_presentation.py` detail(completed=true) usa `event.completedBy || 'Não informado'`; um responsável composto apenas de espaços gera campo vazio. A UI foi corrigida para não inferir autoria, e a nova prévia deve ser coerente: string real não branca ou “Não informado”. A regressão ampliada `test_missing_completion_actor_is_not_replaced_with_creator` verifica tabela, detalhe e cards com null/vazio/espaços/ator real. RED atual em `resultados/ator_presentation_red.log`. Corrija só Presentation neste ponto, não altere a UI aprovada.

Cobertura RED da raiz: `tests/test_layout_quality_browser.py`, **10 testes, 10 falhas, zero erros**, `resultados/layout_quality_red.log`. Cada teste reproduz um dos nove achados (I5 tem diagnóstico e TAG separados). Critérios medem regiões úteis, comprimento de leitura e contraste; não relaxe asserts para manter composições quebradas. Se uma expectativa estiver incorreta, reporte evidência antes de alterá-la.

Cobertura obrigatória da rodada:

- `python tests/test_layout_quality_browser.py`
- edição 2, apresentação 5, UI 24, acessibilidade 5, workflows 12 e controlador 18.
- matriz completa `python tests/test_layout_browser.py --screenshots` com relógio real do novo browser_support; todas as regiões/temas/modais.
- Compilação Python das fontes alteradas.

UI deve continuar única autoridade para modais, gravação, alarmes, importação e navegação. Presentation usa somente snapshot e relações `pipelineOperationalUnits`; testar as duas direções M:N, inclusive uma UO em mais de um duto. Não adicionar polling, persistência, dados de preenchimento ou recursos remotos. Corrigir largura mínima de tabelas/representação móvel sem ocultar controles nem quebrar número/caractere; a rolagem interna deve ser identificável e operável por teclado.

Base de revisão em `revisoes/task3_r1_base/` para CSS/HTML/Presentation. Não gere index ainda. Append relatório da rodada no `task-3-report.md` com achados, arquivos, comandos, saídas, capturas e diffs. Retorne contrato curto e congele fontes para re-review escopada. Não spawn.
