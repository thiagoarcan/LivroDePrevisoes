# Task 3 — composição integral implementada

Status: **DONE, aguardando revisão independente/integração da raiz**. Produto estabilizado em `parts_css.py`, `parts_html.py` e novo `parts_js_presentation.py`; `parts_js_ui.py` recebeu exclusivamente o import Python e a concatenação de `JS_PRESENTATION` ao final de `JS_UI`. Não alterei núcleo, serviço, build, `index.html`, dados do usuário ou referências.

## Resultado

Shell utiliza a largura útil, sidebar de 224 px nos tiers desktop, drawer em tablet, cabeçalho móvel de duas linhas e quatro destinos inferiores com Novo nomeado. Banners de backup/layout ficam no fluxo; alarme fica sticky abaixo da altura real do cabeçalho medida pelo controlador. A matriz inclui banner ativo após rolagem e reconhecimento em lote.

O CSS anterior foi substituído por um sistema consolidado de tokens e componentes, com cinco tiers e proteção da largura física. Não existe `overflow-x:hidden` no body ou raiz. Tabelas têm rolagem própria; tamanho de leitura, campos e contadores permanecem limitados pelos painéis. Modo ultrawide forçado em 768–1199 px conserva a preferência, mas degrada a composição do dashboard para regiões empilhadas que cabem fisicamente.

| Visão | Composição implementada |
| --- | --- |
| Dashboard | Spotlight + alarmes, urgentes, detalhe selecionado e panorama real do console. No ultra, métricas compactas ficam na quarta região com panorama; não formam sete cartões gigantes. Métricas/urgentes abrangem todos os consoles, explicitado no título; panorama identifica o console ativo. |
| Nova previsão | Textarea inicial vazia, fieldsets Localização/Programação/Atividade/Lousa/Alarme, observações expansíveis, preview não salvo e eventos reais do duto/UO. Em wide, atividade e lousa ocupam regiões paralelas. |
| Pendentes | Cards e tabela no mesmo wrapper mestre; detalhe único e contexto do conjunto filtrado, relacionados do duto e histórico. Filtros móveis continuam na sheet gerida pelo controlador. |
| Concluídos | Cards expansíveis móveis e tabela interna desktop; resumo do período filtrado, seleção e histórico/observação/controlador da conclusão. |
| Cadastros | Categoria, lista e editor preservam os IDs existentes. Mobile alterna lista/editor por Novo, Editar e Voltar à lista; voltar preserva rascunho. Telas amplas apresentam lista/editor/vínculos reais. |
| Alertas | Grupos details/summary no mesmo form; testes de som junto do timbre/volume, testes de notificações junto dos canais; preview da edição e estado real das APIs. |
| Cores | Lista/cadeia, editor e exemplo de aparência marcado como exemplo. Faixa usa marcador/borda com texto legível; cores customizadas não viram texto ilegível. |
| Backup | Exportar/importar, CSV, inventário local e manutenção separados; validação/importação permanecem exclusivamente no diálogo oficial. Orientação explícita sobre dispositivo/navegador/perfil, risco de limpar dados e ausência de sincronização automática. |
| Diagnóstico | Estado, coleções e logs em regiões próprias, com tabelas contidas e mensagens quebráveis. Saídas oficiais da UI preservadas. |

Regiões contextuais secundárias ficam ocultas no celular quando já existe o equivalente por card/modal, evitando duplicar detalhes e alongar o fluxo principal. Nenhum dado fictício, leitura paralela do banco, gráfico inventado ou conteúdo de preenchimento foi criado.

## Contratos e semântica

- `App.Presentation.init()` idempotente; escuta `app-ui-update`, input/change/click e mudanças locais do editor cadastral. Não tem timer, polling, persistência, motor próprio nem substituição de métodos da UI.
- Lê somente `getPresentationState()`. Ordenações usam cópias. Dashboard usa `snapshot.events`, nunca uma listagem pendente anteriormente filtrada. Seleção visual do dashboard pertence à apresentação e não altera spotlight/timestamp.
- Ações usam `App.UI.showDetailsModal`, `showCompleteModal`, `acknowledgeAlarm` e `selectCompletedEvent`. Foco dos botões de contexto é restabelecido se a atualização substitui seu nó; formulários não são regenerados no resize.
- IDs únicos, dez diálogos nomeados em fonte, nomes reais associados aos controles, SVGs decorativos ocultos, métricas button nativas e navegação com aria-current. Descrição é textarea de verdade e começa vazia; Enter não envia o formulário.
- Tema escuro/claro/industrial usa tokens legíveis. Primário industrial amarelo/preto; demais primários azul/branco. Texto auxiliar de 14 px e campos de 16 px; campos mobile/tablet de 48 px e ícones de 44 px. Preferências de pulsação/destaque e redução de movimento preservadas.
- Lousa conserva bitmap/aspecto 1200×440, toolbar sticky no fullscreen e stack/foco/Escape oficiais. Safe-area, corpo rolável de modais e footer acessível; importação móvel tem apresentação de bottom sheet com altura natural limitada ao viewport.
- Rodapé de salvar é sticky em mobile/tablet, com somente as duas ações de salvar; Manter Duto/UO e Limpar ficam antes. Teclado aberto o recoloca no fluxo. No desktop, ações ficam no fluxo para não cobrir campos nem o checkbox ao capturar/consultar o formulário inteiro. A decisão mantém os comandos alcançáveis e elimina sobreposição desnecessária em monitores.

## Verificação executada

Todos os testes usam HTML/IndexedDB temporários; capturas usam a massa oficial de demonstração isolada, não a base do usuário.

| Comando/evidência | Resultado |
| --- | --- |
| RED `tests/test_layout_browser.py --quick` | 37 falhas em 102, preservado em `resultados/task3-layout-red.json` |
| `tests/test_presentation_browser.py` | 5/5: snapshot do dashboard, rascunho sem persistência, fieldsets, wrapper mestre e lista/editor/retorno mobile |
| `run_task3_suite.py` | **101/101**, zero falhas/erros/skips, 69,855 s |
| `tests/test_layout_browser.py --quick` | **102/102** |
| `tests/test_layout_browser.py --screenshots` final | **1651/1651**, `sources_stable:true`, 70 capturas |
| `capture_task3_focus.py` | Checkboxes de alarme e Manter Duto/UO alcançáveis por hit test em 390×844 e 3440×1000; quatro capturas viewport |
| `verify_task3_header.py` | Relógio com data real, console e sino dentro da tela em 320/768/1200/3440; quatro capturas viewport |
| `python -m compileall -q parts_css.py parts_html.py parts_js_presentation.py parts_js_ui.py` | Sucesso |

Os 101 testes incluem UI 24, controlador 18, acessibilidade 5, workflows 12, core 33, compatibilidade 3, apresentação 5 e edição 1. Os cinco problemas HTML/CSS deixados pela Task 2 passaram: textarea, Enter, nomes acessíveis, alvos de toque e contraste dos componentes amostrados nos três temas.

A matriz completa cobre 19 larguras × 7 modos × 9 visões, auto tiers/sidebar/navigation, temas em três tamanhos, dez modais em cinco tamanhos, redução de movimento e alarmes ativos. Não afirma testar o produto cartesiano inteiro de temas × modos × modais. As 70 capturas estão nomeadas `final_<largura>_<visao>.png`, `final_tema_*`, `final_modal_*`, `final_alarme_ativo_*`.

Após a rodada completa, a raiz identificou que o harness parava o motor antes do primeiro tick e o relógio nas capturas mostrava `--:--:--`. O harness foi corrigido pela raiz; `verify_task3_header.py` confirma a geometria **com texto real** em quatro extremos. A matriz final distribuída da raiz fará a cobertura completa com esse harness atualizado. O screenshot da Task 3 é evidência de composição, não de funcionamento contínuo do relógio; os testes funcionais cobrem os contadores separadamente.

Reruns intermediários: houve timeout de startup sem page errors e timeout de screenshot com orçamento de 5 s. A suíte sequencial final fechou sem erros. Somente o orçamento de **captura** foi explicitamente ampliado para 15 s, autorizado pelo coordenador; asserts, ações de usuário e critérios de aceite não foram relaxados. Um overflow de 7 px em 768 + ultrawide forçado foi corrigido e a matriz final passou. A inspeção visual também identificou serialização inicial incorreta da textarea; foi corrigida na fonte e uma regressão agora exige valor inicial vazio e textarea de observações presente.

## Arquivos de evidência e revisão

- `resultados/task3-suite-green.log/.json`, `layout_quick.json`, `layout_completo.json`.
- `resultados/task3-controls-viewport.json`, `task3-header-real.json` e oito capturas viewport complementares.
- `resultados/task3-parts_css.py.diff`, `task3-parts_html.py.diff`, `task3-parts_js_presentation.py.diff` contra originais; `task3-ui-concatenacao.diff` isola exclusivamente a integração Python da Task 3.
- `resultados/task3-source-hashes.json` registra fontes congeladas. O script de composição HTML e a cópia do CSS em revisão são artefatos de implementação; **BeautifulSoup não é dependência do build ou do runtime**.
- `tests/test_workflows_browser.py` recebeu somente abertura explícita do disclosure de observações antes de preencher o campo; interação real, sem force. O novo teste de edição foi criado pela raiz.
- A primeira execução integrada utilizou o runner antigo e atualizou `task2-suite-final.*` para 100/100; essa evidência foi copiada. O runner dedicado da Task 3 agora preserva seu resultado em arquivos próprios. Demais evidências fix1 da Task 2 não foram alteradas.

## Pendências reais

Não há falha conhecida aberta nas verificações executadas desta tarefa. A integração/build de `index.html`, revisão independente, validação do HTML distribuído e matriz Firefox pertencem à raiz e ainda não são declaradas concluídas aqui. Caneta/palma reais, teclado móvel físico, som audível do sistema, suspensão do navegador e permissões do sistema não são demonstrados por emulação. A aprovação dos testes de contraste não equivale a certificação formal WCAG de todos os estados possíveis.

## Revisão Task 3 — fix round 1/5

Esta seção registra a correção do lote aceito em `task-3-fix1-brief.md` e `revisoes/task-3-review.md`, incluindo os três Minor por exigência do usuário de resolver todas as correções e o achado adicional X1. A primeira entrega acima foi submetida à revisão; os resultados desta seção a sucedem. A base imutável desta rodada é `revisoes/task3_r1_base`.

### Correções implementadas

| Achado | Correção e evidência |
| --- | --- |
| I1 — contraste dos modais no tema claro | Aliases de superfícies definidos também no escopo de `body`, resolvendo as variáveis com o tema efetivamente aplicado. Título, mensagem, fechar e ações dos modais de confirmação e conclusão verificados nos três temas; capturas dos três temas também incluem a recomendação de dependências. |
| I2 — composição do painel | Foco, urgentes e panorama começam na mesma linha em widescreen. O panorama ocupa a largura integral de sua coluna; métricas e detalhes formam contexto organizado. No ultrawide os detalhes têm coluna própria. Em tablet e desktop convencional as métricas ficam antes do foco. A tabela central tem largura útil para seus dados e ações, sem quebrar nomes por caractere. |
| I3 — configuração de alertas | Aviso com altura natural em uma linha própria do grid; editor principal e prévia iniciam juntos abaixo. Campos em duas colunas no widescreen e três no ultrawide. O texto do aviso mantém comprimento de leitura limitado, sem esticar verticalmente o painel. |
| I4 — relações de cadastros | Contexto lê o snapshot atual e as junções reais de `pipelineOperationalUnits` em ambos os sentidos; remove duplicatas e identifica relacionados inativos. Rascunho da TAG usa `inputTagCode`. Testes comprovam OSCAN com duas UOs, REFAP em dois ou mais dutos pela API do serviço, relação TEDEP em dois dutos e atualização do rascunho. |
| I5 — legibilidade de tabelas | Larguras mínimas por tabela/coluna e quebra de texto aplicada às células adequadas. Diagnóstico, cadastros e cores oferecem região de rolagem local nomeada, focável pelo teclado, com orientação visível quando há overflow; rolagem por seta foi exercitada no navegador. Contêineres do diagnóstico permitem encolhimento sem causar overflow da página. |
| I6 — backup móvel | Removido o grid inline que impedia a coluna única em mobile. Seleção de arquivo permanece nativa e exibe o nome completo em texto separado; arquivo JSON real de nome longo selecionado e botão Validar alcançável em 320/390 px. |
| M1 — console no cabeçalho | Seletor com largura adequada para `Console: C04`; matriz executada com relógio/data reais. |
| M2 — recomendação de dependências | Texto e trecho em negrito no mesmo parágrafo, preservando a frase contínua em mobile e os três temas. |
| M3 — filtros de concluídos | Disclosure nativo compacto no mobile e aberto inicialmente no desktop; resumo inclui filtros atuais e contagem oficial. Fechar, abrir e redimensionar preservam valores e controles em edição. |
| X1 — ator de conclusão em branco | Presentation normaliza espaços e exibe `Não informado` para ator ausente/branco, sem atribuir a conclusão ao criador. Jornada existente confirma tabela, detalhe e cartões. |

### RED, GREEN e cobertura final

Todos os comandos abaixo foram executados no workspace, usando bancos temporários isolados. O runner `--baseline` carrega em memória somente CSS/HTML/Presentation da base da revisão, mantendo UI/core/service atuais; não reverte arquivos no disco. Isso permite reproduzir as falhas específicas da camada em revisão com a UI fix2 aprovada.

| Comando | Saída final |
| --- | --- |
| `python revisao_interface_2026_10_25/run_task3_fix1.py --baseline` | 18 testes, **17 falhas, zero erros**, 19,124 s; a jornada de edição preexistente passa. |
| `python revisao_interface_2026_10_25/run_task3_fix1.py` | **18/18**, zero falhas/erros/skips, 17,845 s. |
| `python revisao_interface_2026_10_25/run_task3_fix1.py --all` | **120/120**, zero falhas/erros/skips, 85,851 s. |
| `python tests/test_layout_browser.py --screenshots` | **1651/1651**, `sources_stable:true`, 70 capturas. |
| `python revisao_interface_2026_10_25/capture_task3_fix1.py` | **34 capturas complementares**, zero page errors. |
| `python -m compileall -q parts_css.py parts_html.py parts_js_presentation.py` | Sucesso. |
| `python revisao_interface_2026_10_25/make_task3_fix1_diffs.py` | Diffs contra a base da revisão e hashes das fontes gerados. |

A suíte completa possui os 114 casos coordenados pela raiz e seis regressões complementares em `tests/test_layout_review_browser.py`. Os seis novos testes cobrem contraste efetivo das partes dos modais, junções reais e inativos, rolagem acessível/leitura das tabelas, nome de arquivo móvel, posição das métricas e preservação/resumo dos filtros. Os dez testes de qualidade fornecidos pela revisão e as duas jornadas de edição estão incluídos. Não houve redução de asserts ou aumento do prazo de ações de usuário.

Uma execução intermediária da matriz encontrou três overflows em Diagnóstico a 768 px (auto, compact e tablet). A causa era a largura intrínseca dos filhos do grid; `min-width:0` nos filhos e tracks `minmax(0,1fr)` corrigiram o problema. A matriz inteira foi repetida após a correção e passou. A matriz final desta rodada já usa o harness com relógio real, substituindo a limitação de relógio-placeholder da primeira entrega.

### Evidências e contratos

- `resultados/task3-fix1-baseline.log/.json`, `task3-fix1-focused.log/.json` e `task3-fix1-suite.log/.json` contêm as saídas completas.
- `resultados/task3-fix1-layout-completo.json` registra os 1651 resultados e hashes estáveis; a validação usa HTML montado das fontes (`distributed_html:false`).
- `resultados/task3-fix1-captures.json` lista as 34 capturas específicas e medidas. Junto das 70 capturas da matriz são **104 capturas nesta rodada**. Incluem painel/alertas em 768/1024/1440/1920/3440, modais em três temas, backup em 320/390, tabelas em 390/1024/1440, filtros abertos/fechados e junções duto/UO.
- `resultados/task3-fix1-parts_css.py.diff`, `task3-fix1-parts_html.py.diff` e `task3-fix1-parts_js_presentation.py.diff` registram exatamente o delta frente a `revisoes/task3_r1_base`.
- `resultados/task3-fix1-source-hashes.json` registra as fontes congeladas para re-revisão.

Nesta rodada somente `parts_css.py`, `parts_html.py` e `parts_js_presentation.py` foram alterados no produto. UI fix2, core, serviço, build e `index.html` não foram modificados. IDs e seletores de workflows foram preservados. Presentation continua consumindo o contrato somente leitura de `getPresentationState` e `app-ui-update`, sem persistência, polling, substituição de métodos UI ou gerenciamento de modais/cache/foco. Disclosure e regiões de rolagem usam comportamento nativo. Não foi usado `body { overflow-x:hidden }` para ocultar falhas.

**Estado ao entregar:** fontes congeladas; nenhuma falha conhecida aberta nos testes desta rodada. A aceitação independente dos achados, build/HTML distribuído e matriz Firefox continuam sob responsabilidade da raiz e não são declarados concluídos por esta implementação. A emulação continua sem comprovar hardware físico, comportamento de suspensão, som audível ou permissões externas.
