# Revisão independente — Task 3

Data: 25/10/2026. **Veredito: REPROVADO para integração final. Critical: 0; Important: 6; Minor: 3. Há seis Important abertos.**

## Escopo e evidência

Revisados `parts_css.py`, `parts_html.py`, `parts_js_presentation.py` e somente a concatenação Python de `parts_js_ui.py`, conforme `resultados/task3-ui-concatenacao.diff`. Comparação com brief, proposta de composição, especificação, contrato final da Task 2 e diff contra originais, sem Git. Não foram modificados arquivos de produto. A correção paralela do controlador de conclusão é externa a esta revisão.

Inspecionadas diretamente as três pranchas `auditoria_interface/referencias/*pagina_01.png`, as 45 capturas das nove visões em 390/1024/1440/1920/3440, os dez modais finais e amostras de temas claro/industrial, além do escuro das capturas gerais. As capturas revelam problemas que as verificações de overflow não medem.

Reprodução independente no Edge headless, HTML e IndexedDB temporários, demonstração oficial isolada, relógio real inicializado. Comando: `python revisao_interface_2026_10_25/revisoes/task-3-review-probe.py`. Resultado detalhado: [task-3-review-probe.json](task-3-review-probe.json); zero `pageerror`. O probe registra medidas e estados observados, não é uma suíte de aceitação cujo exit 0 signifique ausência de defeitos. Nenhuma base/perfil real foi acessada.

Reruns independentes: `python tests/test_presentation_browser.py`: **5/5**; `python tests/test_accessibility_browser.py`: **5/5**. A suíte 101/101 e matriz 1651/1651 do implementador foram consultadas como evidências anteriores; não foram reexecutadas integralmente nesta revisão. O contraste automatizado existente amostra componentes de quatro visões, sem abrir modais, explicando por que não detecta I1 abaixo. A matriz mede limites dos modais, mas não sua legibilidade, e mede overflow sem verificar a organização das regiões.

SHA256 dos três arquivos da Task 3 conferidos ao fim: CSS `adc80db3f0121b60d1fbae314924da38143ae50f054906a7555a62f2c22f4e9d`; HTML `830be0f27f27ad3381cb690c65f2d5a4726dd0dc599e9311019e85adcca23b40`; Presentation `8385724476043f8aec5e2f6fb840dbd60065176f6473d0e2d513c6b709d53410`. Correspondem ao congelamento informado.

## Important abertos

### I1 — Modais ficam praticamente ilegíveis no tema claro

**Local:** `parts_css.py:4`, `parts_css.py:5`, `parts_css.py:237`.

**Reprodução:** aplicar tema claro e abrir confirmação de exclusão, conclusão ou outro modal. O probe usa `App.UI.applyTheme('light')` e `showConfirmModal`. A caixa herda fundo `rgb(24,37,54)` e texto `rgb(24,40,59)`: **contraste 1,036:1**. Título, mensagem e símbolo de fechar ficam quase invisíveis. Captura: [review-modal-light-390.png](review-modal-light-390.png). Não é um efeito de imagem escurecida pelo overlay: são as cores computadas da própria caixa.

**Causa:** `--bg-elevated:var(--bg-surface)` é definido em `:root`; o alias é herdado já resolvido para a superfície escura. `body.theme-light` redefine `--bg-surface` e texto, mas não esse alias. `.modal-box` continua usando a superfície escura. O mesmo problema de herança afeta `--bg-surface-elevated` quando consumido.

**Recomendação:** fazer os aliases resolverem no mesmo escopo dos tokens por tema, ou consumir a superfície adequada diretamente. Acrescentar regressão de contraste efetivo de título/corpo/fechar e ações em todos os três temas, incluindo confirmação destrutiva e conclusão. A correção deve preservar fundo e foco legíveis no industrial.

### I2 — Grade widescreen deixa urgentes, panorama e métricas fora da primeira região útil

**Local:** `parts_css.py:281–287`, `parts_html.py:646`.

**Reprodução:** demonstração, Painel, automático, 1920×1000. Spotlight inicia em **y196**, urgentes e panorama em **y776**, detalhe em **y1160**, métricas em **y1881**. A área à direita do Spotlight fica vazia durante aproximadamente 580 px, embora existam três urgências e um panorama real. A captura `resultados/final_1920_viewDashboard.png` mostra o mesmo resultado; o probe confirmou contra as fontes congeladas. Em 2560/3440 os overrides ultrawide colocam urgentes na linha correta.

**Causa:** foco ocupa a linha 2 automática, mas urgentes/contexto são explicitamente colocados na linha 3 e detalhe na 4. `dashboardOverview` está em `display:contents` fora de ultra, e a grade deixa as métricas autoalocadas no fim. A organização em três regiões simultâneas aprovada não se concretiza no tier widescreen.

**Recomendação:** definir áreas/linhas coerentes para todos os componentes do dashboard em widescreen, com foco, lista e contexto no mesmo início de trabalho e métricas no contexto/topo previsto. Verificar também a ordem e posição das métricas em convencional/tablet, que nas capturas aparecem depois de detalhes altos, contrariando a ordem aprovada. Regressão deve comparar coordenadas e uso simultâneo das regiões, não apenas largura do documento.

### I3 — Configurações de alertas aloca a maior região a um aviso vazio

**Local:** `parts_css.py:310`, `parts_html.py:2278`, `parts_html.py:2310`.

**Reprodução:** Alertas, auto, 1920/2560/3440. Em **3440**, o aviso de cinco itens ocupa **2103×1049 px**, o formulário fica nos **1052 px** à direita e a prévia começa em **y1261**. Em **1920**, aviso **1090×1455 px**, formulário **545 px**, prévia **y1667**. Capturas independentes: [review-alerts-1920.png](review-alerts-1920.png), [review-alerts-3440.png](review-alerts-3440.png).

**Causa:** a grade de duas colunas 2:1 recebe aviso, editor e prévia como três filhos autoalocados. O aviso pega a coluna maior e estica até a altura do editor; a prévia cai na linha seguinte. Trata-se justamente de grande área morta havendo conteúdo útil, proibida no brief.

**Recomendação:** atribuir região curta de aviso, região principal aos grupos editáveis e região de leitura à prévia/status, mantendo altura natural dos grupos. Garantir que ampliar de convencional para wide não comprima o formulário nem alongue o aviso. Testar a geometria desses três elementos em 1920 e 3440.

### I4 — Painel cadastral informa ausência de vínculos que existem

**Local:** `parts_js_presentation.py:159`, `parts_js_presentation.py:168`, `parts_js_presentation.py:170`.

**Reprodução:** Cadastros → Dutos → Editar OSCAN. O painel mostra **UOs vinculadas: Nenhuma**, enquanto o snapshot tem duas associações OSCAN→REFAP/TEDEP. Cadastros → UOs → Editar REFAP mostra **Dutos vinculados: Nenhum**, apesar de OSCAN. O probe navega pelas categorias oficiais e aguarda os editores; JSON inclui o registro, as associações e os textos produzidos.

**Causa:** a apresentação procura `pipeline.uoIds`, propriedade inexistente nos registros persistidos. A relação M:N real está em `snapshot.pipelineOperationalUnits`, já disponível no contrato readonly.

**Recomendação:** resolver ambas as direções pelo junction do snapshot, preservando a multiplicidade e o tratamento de ativos/inativos aplicável. Cobrir duto com duas UOs e UO ligada a mais de um duto. No mesmo mapa cadastral há um erro de contrato menor: TAG usa `inputTagName`, mas o campo real é `inputTagCode` (`parts_html.py:2194`). Ao preencher `TAG-PROBE-123` em Novo TAG, “Edição atual” permanece “Novo registro”; corrigir e cobrir a prévia desse rascunho na mesma rodada.

### I5 — Tabelas comprimem palavras e números por caractere em regiões estreitas

**Local:** `parts_css.py:171–178`, `parts_css.py:223`, `parts_css.py:279–280`; tabelas cadastrais/coleções no HTML.

**Reprodução:** Diagnóstico, auto, 390×844. A seção de somente onze coleções tem **3340 px de altura**; “Finalidade” tem célula de **45 px**, aproximadamente **21 px úteis** após padding. “Consoles Operacionais” quebra quase letra a letra, e a linha de eventos tem **387 px** de altura. [review-diagnostic-390.png](review-diagnostic-390.png). Em 1440 a captura final também mostra a tabela comprimida na coluna lateral, com números de dois dígitos partidos verticalmente. Cadastros em390 mostra “Ativo” em três linhas e “0 duto(s)” em várias; Cores em1024 apresenta problema semelhante nos cabeçalhos/valores.

**Causa:** quebra `anywhere` aplicada indiscriminadamente, larguras mínimas de 110 px da primeira/última coluna e ausência de largura mínima legível/representação móvel para essas tabelas. O wrapper com `overflow:auto` não ajuda porque a tabela encolhe para caber em vez de rolar. Em Diagnóstico, “Inativos” recebe os 110 px da regra genérica destinada a ações.

**Recomendação:** distinguir texto longo de campos curtos/números, usar cards/linhas de termos no mobile ou tabela com colunas mínimas legíveis e rolagem interna nomeada/acessível. Ajustar a coluna de coleções convencional para esse conteúdo real. Validar palavras, números e alturas, além de overflow global, em 320/390/768/1024/1440.

### I6 — Backup não passa para uma coluna no celular e corta o seletor de arquivo

**Local:** `parts_html.py:2780`, `parts_css.py:220`, `parts_css.py:390`.

**Reprodução:** Backup, automático, 390×844. Exportação e importação continuam lado a lado, cada painel com **160 px**, e input de arquivo com **118 px**. O seletor nativo e seu nome ficam cortados; títulos, orientação e botão de exportar se fragmentam em muitas linhas. Captura final `resultados/final_390_viewBackup.png`; medidas em `backup_390` do probe.

**Causa:** `style="display:grid"` no HTML prevalece sobre a regra móvel `display:flex; flex-direction:column`. As duas colunas `1fr 1fr` da regra base permanecem em vigor. Isso viola a sequência móvel exportar→importar da proposta, sem benefício funcional.

**Recomendação:** retirar a declaração inline de layout conflitante e aplicar a composição móvel no CSS de componente; conferir botão de escolher arquivo, nome selecionado e ações em320/390 com arquivo real de teste, sem truncar comandos. A validação e execução continuam pertencendo ao diálogo oficial.

## Minor abertos

### M1 — Identificador do console ativo é cortado em tablet/desktop

**Local:** `parts_css.py:36`.

O select fixo de130 px não acomoda “Console: C04” (91,75 px de texto), padding e seta nativa. Nas capturas1024/1440/1920 o último dígito é cortado, tornando C04/C08 indistinguíveis com o seletor fechado. A seleção funciona ao abrir. Dar espaço suficiente ao valor ou encurtar somente o prefixo redundante, preservando o identificador completo. Evidência adicional: `review-header-1920.png` e `header_console` no JSON.

### M2 — Recomendação do diálogo de dependência fragmenta “Inativação”

**Local:** `parts_html.py:3518–3523`, `parts_css.py:217`.

Em390, `.notice-banner` é flex e recebe texto solto, `<strong>` e mais texto como três itens. “Inativação” fica em caixa de **16,98 px** de largura e101 px de altura. A captura `final_modal_dependency.png` mostra a frase cortada em colunas verticais, também reproduzida em `review-dependency-light-390.png`. Envolver a frase em um único bloco textual ou usar o layout adequado para aviso sem ícone. Não mudar a ação de inativar.

### M3 — Filtros de concluídos continuam sempre expandidos no mobile

**Local:** `parts_html.py:1486` e regras móveis da toolbar em `parts_css.py:378`.

Em390×844, a toolbar tem **676 px** de altura e o primeiro evento só começa em **y1019**. Não existe disclosure/sheet para os seis filtros detalhados, apesar da seção4.4 da proposta prever filtros recolhíveis e resumo. Usar disclosure com resumo dos filtros aplicados, preservando IDs/valores e o controlador aprovado. Evidência: `completed_mobile` no JSON e `final_390_viewCompletedEvents.png`.

## Conformidade e qualidade

Há avanços concretos: sidebar real, barra inferior com quatro destinos, uso útil do ultrawide no dashboard, wrapper mestre correto em Pendentes, descrição textarea inicialmente vazia, fieldsets e disclosures nativos, prévia não salva, ações delegadas à UI, tabelas com wrappers e modais com corpo rolável. O novo módulo consome o snapshot sem ordená-lo in-place, não persiste, não instala polling e não substitui métodos da UI. O panorama usa `snapshot.events` filtrado explicitamente pelo console e não herda `state.pending`; a regressão independente passou. A concatenação preserva o build de cinco blocos.

Entretanto, a conformidade visual e semântica ainda é parcial pelos nove achados. Os componentes centralizados são uma base melhor, mas regras genéricas de tabela/flex, inline remanescente de layout e autoalocação de grids impedem o resultado aprovado. A camada de apresentação também precisa usar os nomes e relações reais do modelo, em vez de propriedades presumidas.

Nenhuma exigência de gráfico decorativo ou dado fictício foi acrescentada; estados vazios curtos foram aceitos. Não foram abertos achados pela ausência de dados para preencher monitores. As recomendações acima tratam regiões com conteúdo existente, controles legíveis e informação correta. Caneta/palma física, teclado móvel físico, som audível e execução em navegador suspenso não são certificados por esta revisão. A integração final deve permanecer pendente até corrigir/revisar os seis Important, além de considerar os três Minor na rodada solicitada.
