# Task 3 — Proposta concreta de composição responsiva

Data: 25/10/2026. Escopo desta entrega: desenho de implementação e brief, sem alteração de produto ou testes. As decisões abaixo concretizam o desenho já autorizado em `docs/superpowers/specs/2026-10-25-correcao-integral-design.md`; não solicitam nova escolha ao usuário.

## 1. Fontes e decisão de composição

Fontes examinadas: Task 3 do plano `docs/superpowers/plans/2026-10-25-correcao-integral.md`; `auditoria_interface/dados/analise_referencias.md`; os 40 itens de `achados_consolidados.json`; `parts_html.py` e `parts_css.py`; trechos de integração de `parts_js_ui.py`; recomendações dimensionais de `requisitos_extraidos.txt`. Foram inspecionadas as três imagens renderizadas dos PDFs em `auditoria_interface/referencias`, incluindo a prancha convencional/wide/ultra.

O desenho adotado é um shell que ocupa o viewport, com navegação lateral em monitores e regiões coordenadas que acrescentam informação operacional. Formulários, descrições e cartões continuam com medidas de leitura. A área adicional recebe listas, detalhe selecionado, contexto do console e resumos calculados com os dados existentes. Não há conteúdo fictício nem exigência de reproduzir os gráficos ilustrativos dos PDFs.

Alternativas descartadas nesta concretização: apenas remover `max-width` esticaria cartões e campos; manter um formulário central estreito com margens enormes repetiria as áreas mortas atuais. A solução distribui regiões úteis, com alturas determinadas pelo conteúdo, e usa espaço restante para mais linhas reais de listas. Se não houver dados suficientes, um estado vazio curto e honesto é correto; não se cria um painel alto vazio para preencher a tela.

As linhas citadas neste documento correspondem ao produto lido antes da implementação das Tasks 2/3. IDs/classes são o contrato durável, pois as linhas mudarão.

## 2. Cinco tiers, sete modos e altura disponível

| Tier automático proposto | Largura CSS | Navegação e estrutura |
| --- | --- | --- |
| Celular | 320–767 px | Cabeçalho em duas faixas compactas; conteúdo em uma coluna; barra inferior com Painel, Pendentes, Novo e Mais. Drawer para demais destinos. |
| Tablet | 768–1199 px | Retrato/estreito: rail de 64 px ou drawer, conteúdo de uma/duas regiões conforme largura útil. Paisagem/área útil suficiente: rail de 72 px, lista e detalhe simultâneos. Sem barra inferior concorrente. |
| Convencional | 1200–1919 px | Navegação lateral de 208–224 px; cabeçalho compacto; região principal e contexto lateral de 300–380 px quando houver conteúdo útil. |
| Wide | 1920–2559 px | Navegação de 224 px; três regiões operacionais simultâneas no painel: foco/alarmes, lista, contexto. Nas outras telas, distribuir editor, lista e contexto conforme tarefa. |
| Ultra | ≥2560 px | Navegação de 232–240 px; quatro regiões operacionais no painel: foco/alarmes, lista, detalhe, panorama/ações. Outras telas usam regiões próprias, sem repetir um formulário até preencher a largura. |

Os limites acima usam P0032 e estão definidos no contrato de integração: 768/1200/1920/2560. O JS lido ainda usa 1600/2200 para wide/ultra; isso não era, isoladamente, um defeito documental (GUI-38), mas deve ser atualizado para a decisão adotada. Centralizar os limites na Task 2 e reutilizá-los no CSS/Task 3, sem duas definições contraditórias.

`auto` sempre precisa escrever o tier efetivo no DOM, inclusive mobile/tablet/conventional. `compact` é densidade sobre o tier automático, não um sexto layout. Os cinco modos manuais mantêm a escolha do usuário; a largura real limita colunas e move contexto secundário para baixo ou abas. Um ultra manual em 390 px não pode impor uma grade de 2500 px, esconder alarmes ou reduzir botões a ícones minúsculos. Mostrar o aviso de viabilidade existente e manter o acesso às mesmas regiões.

O limiar para duas regiões no tablet deve considerar espaço real: mestre ≥300 px + detalhe ≥320 px + gap 16 px, além de rail e margens. Com 768–820 px úteis insuficientes ou zoom elevado, detalhe abre sob demanda; com 1024×768, lista/detalhe cabem. Não usar apenas `orientation` nem resolução física para decidir. Em altura útil <600 px, retirar sticky de painéis secundários e priorizar rolagem normal; modais continuam com cabeçalho/ações e corpo rolável.

## 3. Shell e dimensões de trabalho

### Navegação e cabeçalho

- Converter `.app-nav` em navegação vertical persistente no desktop; reaproveitar seus botões e `data-view`, sem clonar IDs. Dar nome acessível à navegação. Se tratada como navegação de páginas, remover `role=tablist/tab` e marcar o destino atual com `aria-current=page`; se Task 2 mantiver tabs, implementar o padrão completo de tabs, não misturar semânticas.
- O shell desktop pode usar grid com coluna de navegação e uma coluna `minmax(0,1fr)`. Cabeçalho, banners e conteúdo pertencem à área de trabalho. `.app-main` passa a `width:100%; max-width:none; min-width:0`, com padding de 16–24 px, sem margem central monumental.
- Cabeçalho móvel: primeira faixa com menu, título curto da tela e sino; segunda faixa com label e seletor do console. Relógio compacto pode compartilhar a segunda faixa se couber, nunca reduzir a largura mínima do seletor. Modo, tema, usuário, notificações e status já têm destinos no drawer/modal; não repetir todos no cabeçalho. Objetivo normal: 96–112 px mais safe-area, sem altura fixa que corte texto a 200% de zoom.
- Desktop: console, relógio, sino e ações essenciais em uma faixa; status de áudio visível quando requer interação. Nome de usuário longo pode ocupar duas linhas limitadas ou aparecer completo no controle/modal; não empurrar o sino para fora. Se faltar espaço, mover controles auxiliares para menu, em vez de comprimir todos os grupos.
- Criar um grupo de topo que contenha cabeçalho e faixa de alarmes, ou medir o cabeçalho por `ResizeObserver` e alimentar `--header-height`. Nunca repetir o `top:52px` atual. A faixa deve usar altura natural, permitir quebra e permanecer abaixo do cabeçalho. Avisos de backup/layout são secundários e não precisam competir como três barras sticky.
- Barra inferior: usar as classes já presentes no HTML (`bottom-nav-item`, `bottom-nav-fab`, `bottom-nav-badge`). Quatro slots equivalentes; Novo com ícone e rótulo visível. Um único botão Novo visível nessa região; `btnFabNewEvent` legado continua inacessível/oculto ou é removido após verificar bindings. Na tela de formulário, o slot Novo indica a tela atual; os comandos de salvar pertencem ao formulário.

### Medidas, leitura e densidade

| Elemento | Regra proposta |
| --- | --- |
| Espaçamento | Celular 16 px nas laterais; 12 px apenas onde indispensável em 320 px, registrando a exceção. Gaps 12–16 px; desktop 16–24 px. |
| Texto operacional | 16 px base, line-height 1,45–1,55; descrições e valores essenciais nunca menores que 16 px no modo normal. |
| Rótulos auxiliares | 14 px, reservados para metadados; evitar os atuais 11–12 px. Título de seção 18–22 px; título de tela 20–26 px. |
| Contadores | 28–36 px no spotlight, 40–56 px no alarme, com tabular-nums; tamanho limitado por `clamp`, sem crescer com todo o monitor. |
| Campos | Altura mínima 48 px em mobile/tablet; 44–48 px no desktop; fonte 16 px. Datas e horas com tipos nativos. |
| Ações principais | Altura 48–56 px; alvos de ícone/fechar ≥44×44 px; labels de checkbox/radio também clicáveis nessa altura. |
| Texto livre | Linha de leitura de 45–75 caracteres; limite aproximado de 65ch para explicações. Descrições longas podem usar até 80ch em detalhe amplo. |
| Formulário | Editor principal 640–900 px; cada grupo/coluna 280–440 px. Área total maior recebe outros grupos ou contexto; um select não ganha 1800 px. |
| Cartões de evento | 300–440 px quando em grade; 280 px somente em área realmente restrita. Lista mestre pode ser mais ampla, mas description tem max-inline-size de leitura. |
| Contexto lateral | 280–380 px; detalhe 360–560 px. Se sobrar mais largura, acrescentar região real, não aumentar a fonte ou a altura. |
| Métricas | Altura natural aproximada 80–100 px, numeral 24–32 px; grade de sete itens pode quebrar em duas linhas. Não impor sete colunas se os rótulos não couberem. |

`min-width:0` em todos os filhos grid/flex e `overflow-wrap:anywhere` para identificadores/texto importado. Aplicar quebra seletiva: horários curtos não quebram, descrição e hierarquia quebram. Tabelas têm wrapper próprio com `overflow:auto`, cabeçalho sticky e região nomeada quando rolável por teclado. Não usar `body{overflow-x:hidden}` como prova de correção: isso pode apenas cortar botões. O aceite mede os retângulos dos controles e a largura do documento.

## 4. Composição das nove telas nos cinco tiers

As tabelas definem ordem visual e conteúdo. A ordem DOM deve seguir a prioridade operacional e continuar compreensível no teclado; evitar reordenação CSS que torne o foco imprevisível.

### 4.1 Painel — `viewDashboard`

| Tier | Composição concreta |
| --- | --- |
| Celular | Faixa de alarmes quando ativa → spotlight com estado e contador juntos no topo → lista curta de atenção imediata → métricas em duas colunas → acesso ao restante. Description e hierarquia abaixo do estado/tempo. Sem painel lateral vazio. |
| Tablet | Métricas compactas no topo, spotlight e alarmes lado a lado quando couberem; lista urgente abaixo. No retrato estreito, spotlight vem primeiro e alarmes ficam em seção curta adjacente/aba acessível, sem tirar a faixa persistente. |
| Convencional | Métricas no topo; coluna principal com spotlight e lista urgente; à direita alarmes reais e resumo do console. A lista recebe a maior parte da altura disponível, não o spotlight. |
| Wide | Foco + alarmes em coluna de 340–420 px; pendentes/urgentes em tabela central legível; contexto do console de 300–380 px com métricas e distribuição por estado/duto. Filtro do panorama claramente indicado. |
| Ultra | Foco + alarmes 340–420 px; lista central com descrições limitadas; detalhe selecionado de 400–560 px; panorama com métricas, distribuição e ações de contexto de 300–380 px. Não duplicar todos os sete cards numa faixa gigante superior. |

A lista central do painel pode começar reutilizando a lista urgente existente; se o novo painel exibir todos os pendentes, o título deve dizer “Pendentes do console” e o usuário deve poder alternar para “Atenção imediata”. Não alterar silenciosamente o significado de `cardDashboardUrgent`. O spotlight permanece vinculado ao próprio ID, independentemente da seleção da lista. No ultra, o detalhe é do evento selecionado; título e borda de seleção tornam isso explícito.

### 4.2 Nova previsão/edição — `viewNewEvent`

| Tier | Composição concreta |
| --- | --- |
| Celular | Grupos: Localização operacional → Programação e descrição → Alarme → Anotação/lousa. Data/hora lado a lado se couberem; descrição textarea de 3 linhas iniciais. Alarme/lousa recolhíveis com resumo e estado, sem perder valores. Salvar e Salvar e criar outra em rodapé com duas colunas; Limpar secundário fora da dupla principal. |
| Tablet | Localização/programação em duas colunas de campos; descrição em largura total do editor. Em paisagem, editor à esquerda e lousa/contexto à direita. A lousa mantém proporção, não ocupa toda a altura de uma coluna vazia. |
| Convencional | Editor de 720–900 px e painel de resumo de 300–380 px: console/duto/UO/TAG, horário, prioridade e alarme efetivo. Ações no fim do editor, acessíveis sem percorrer uma coluna contextual alta. |
| Wide | Localização/programação e descrição em duas regiões do mesmo form; anotação/lousa em terceira região. Contexto abaixo da programação inclui eventos já cadastrados para o duto/UO selecionado, se existirem. |
| Ultra | Localização/programação, descrição + alarme, lousa e contexto do duto em quatro regiões com leitura limitada. O resumo não vira segunda cópia editável dos mesmos campos. Sem seleção de duto, contexto mostra instrução curta. |

Preservar todos os IDs de campos e um único `formEvent`. Wrapper de grupos/fieldsets pode ser novo; botão externo ao form, se houver, usa `form=formEvent`. Rascunho do resumo deve ser marcado “Prévia — ainda não salva”, nunca contaminar métricas de eventos persistidos. A opção manter Duto/UO fica antes das ações, não no meio dos campos de programação. Para 320 px, os dois comandos podem usar rótulos em duas linhas sem truncamento.

### 4.3 Pendentes — `viewPendingEvents`

| Tier | Composição concreta |
| --- | --- |
| Celular | Busca em largura útil; linha de console ativo/filtros; ordenar em linha própria se preciso. Cartões compactos com estado/tempo, hierarquia, descrição e ações essenciais. Filtros em sheet; detalhes e demais ações sob demanda. Se usuário pedir tabela, ela rola internamente. |
| Tablet | Lista mestre e detalhe quando a área mínima couber. Retrato insuficiente conserva lista e abre detalhe sem perder posição. Toolbar quebra em linhas lógicas; filtros em sheet/painel, nunca antes da lista com 665 px de altura. |
| Convencional | Lista/tabela na região principal e detalhe de 360–440 px; filtros recolhíveis acima ou em seção estreita própria. Seleção inicial deve mostrar conteúdo. |
| Wide | Lista central + detalhe + resumo da seleção/filtros e próximos eventos do mesmo duto. O contexto distingue conjunto filtrado e console ativo. |
| Ultra | Filtros/panorama estreitos + lista + detalhe completo + histórico/alarme/relacionados do evento selecionado. Sem duplicar as ações de concluir/editar em todas as colunas. |

Mover `containerPendingTable` para um novo wrapper mestre junto de `containerPendingCards`, dentro da grade; hoje a tabela fica fora de `.pending-master-detail-grid`. Manter IDs, delegação de eventos e apenas a representação necessária renderizada/visível. `pendingDetailPane` passa a existir em conventional/wide além de tablet/ultra. Nenhum painel lateral deve selecionar outro evento em segundo plano ao atualizar o relógio.

### 4.4 Concluídos — `viewCompletedEvents`

| Tier | Composição concreta |
| --- | --- |
| Celular | Busca, resumo dos filtros e cards expansíveis. Cabeçalho do card: descrição, conclusão, diferença e responsável real; expansão: notas/histórico/alarmes/ações. Filtros detalhados recolhíveis. CSV em ação nomeada. |
| Tablet | Cards em uma/duas colunas ou tabela em wrapper conforme largura útil; filtro compacto. Seleção pode abrir detalhe sob demanda para evitar nove colunas comprimidas. |
| Convencional | Tabela legível com filtros e resumo de quantidade/período; detalhe selecionado lateral apenas quando couber. Coluna de notas tem largura de leitura e expansão. |
| Wide | Tabela + detalhe/histórico + resumo calculado do conjunto filtrado: quantidade, no horário/antecipado/atrasado, intervalo efetivamente aplicado. |
| Ultra | Filtros/contexto do período + tabela + detalhe com anotação + trilha de auditoria. Ações reabrir/excluir pertencem ao evento selecionado e ficam separadas. |

Não rotular como “Hoje” uma consulta baseada em data prevista se o atalho promete conclusão hoje. Resumo e filtros usam exatamente a semântica implementada na Task 2. Não derivar taxa de produtividade, desempenho de controlador ou tendência de dados sem requisito/modelo.

### 4.5 Cadastros — `viewCadastros`

| Tier | Composição concreta |
| --- | --- |
| Celular | Seletor de categoria compacto → lista da categoria → formulário de novo/editar sob demanda. Ao editar, mostrar Voltar à lista; preservar categoria, ID e valores. Evitar mostrar cinco formulários na mesma rolagem. |
| Tablet | Categoria como rail ou lista estreita; lista/formulário da categoria selecionada na região principal. Em paisagem, lista e editor simultâneos. |
| Convencional | Categorias 180–220 px dentro da tela; lista 320–460 px; editor restante limitado por grupo. Relações reais em resumo adjacente/aba. |
| Wide | Categorias + lista + editor + vínculos do registro (console/dutos/UOs/TAGs existentes). Ativos/inativos explícitos; pendências de seleção com estado vazio curto. |
| Ultra | Manter o fluxo da categoria selecionada; área extra recebe mapa textual/árvore de vínculos e registros relacionados. “Ver todos” é visão de consulta em colunas por grupo, não modo que abre todos os editores e perde a seleção. |

Os hubs atuais agrupam consoles/pipelines, UOs/types e TAGs. Ocultar apenas o hub por `data-cat-group` não resolve a separação de categoria dentro do hub. Criar wrappers por categoria e por lista/editor, preservando `formConsole`, `formPipeline`, `formUO`, `formEquipmentType`, `formEquipmentTag` e todos os tbody/IDs usados pelo JS. Relações lidas da base devem respeitar a multiplicidade real; não redesenhar o modelo como árvore estrita se um duto possuir várias UOs.

### 4.6 Configurações de alertas — `viewConfigAlerts`

| Tier | Composição concreta |
| --- | --- |
| Celular | Seções expansíveis: Operador/exibição, Alarme padrão, Som, Notificações/visual, Repetição. Resumo no título de cada grupo. Uma ação de salvar clara no fim; testes junto do grupo correspondente. |
| Tablet | Duas colunas de grupos quando houver espaço; testes/prévia em faixa lateral ou inferior. Salvar não depende da altura da maior coluna. |
| Convencional | Editor em duas colunas + resumo dos valores efetivos e status real de áudio/notificação. |
| Wide | Grupos de parâmetros, meios de aviso e prévia/estado em três regiões; explicar junto do campo o efeito de zero e da repetição. |
| Ultra | Quatro regiões de conteúdo real: parâmetros/operador, som/repetição, visual/notificação, prévia/status/testes. Cada região usa largura limitada e altura natural. |

Manter um `formAlertSettings`. Não duplicar sliders/checkboxes em prévias. Prévia visual usa edição atual e distingue “não salvo”; status usa permissão real do navegador. Ações de testar podem usar valores de edição, mas isso precisa estar expresso na ação. Preferência de movimento reduzido prevalece sobre pulsação salva.

### 4.7 Configurações de cores — `viewConfigColors`

| Tier | Composição concreta |
| --- | --- |
| Celular | Resumo da cadeia → cards de faixas → editor da faixa selecionada → prévia. Cadeia quebra ou rola só internamente; nome/limites nunca dependem exclusivamente da cor. |
| Tablet | Lista/cards à esquerda, editor e prévia à direita se couber; em retrato estreito, editor abaixo da seleção. |
| Convencional | Tabela/lista de faixas + editor + prévia pequena, sem um único cartão de largura total contendo longos vazios. |
| Wide | Lista/cadeia + edição + prévia de estado/timer, com resumo dos limites adjacentes. |
| Ultra | Lista/cadeia, editor, prévia atual e contexto de validação (continuidade, limites, nomes). Comparação salvo/edição somente se ambas origens forem identificadas. |

Preservar `colorPreviewBar`, `colorChainPreview`, `formColorRange` e campos. Prévia usa a faixa em edição e tem texto “Exemplo de aparência”; não exibir contagem fictícia de eventos como se viesse da base. Restaurar padrões permanece ação separada do salvar faixa.

### 4.8 Backup e dados — `viewBackup`

| Tier | Composição concreta |
| --- | --- |
| Celular | Último backup → exportar JSON → importar/validar → exportações CSV → demonstração e limpeza em seção separada. Arquivo e resumo de validação quebram linhas; ação destrutiva fora do caminho do exportar. |
| Tablet | Exportar e importar lado a lado; CSV abaixo. Status/contagens acompanham as operações; demonstração/limpeza em seção inferior compacta. |
| Convencional | Operações 640–900 px + estado do backup e contagens locais em lateral de 300–380 px. |
| Wide | Exportação, importação/prévia e estado da base em três regiões. Resumo de conflitos real aparece na região de importação e permanece acessível na confirmação. |
| Ultra | Exportação/CSV, importação, resumo validado/conflitos e estado local. Sem arquivo selecionado, a região de prévia mostra orientação curta e não reserva uma tela inteira vazia. |

Não prometer histórico de backups se só existe timestamp do último exportado. Não antecipar “validado com sucesso” antes do serviço confirmar. Toda prévia usa texto seguro e o resultado das Tasks 1/2; o layout nunca relê e injeta HTML do arquivo. Preservar uma única ação final de executar importação dentro do diálogo previsto.

### 4.9 Diagnóstico — `viewDiagnostic`

| Tier | Composição concreta |
| --- | --- |
| Celular | Estados reais em lista de termos/valores → coleções/contagens em linhas → logs em cards com mensagem quebrável → copiar diagnóstico. Limpar logs separado. |
| Tablet | Estados e coleções em duas regiões; logs na largura útil abaixo. |
| Convencional | Estados/coleções em coluna de 320–380 px; log ocupa região principal com rolagem interna quando necessário. |
| Wide | Estado de APIs/versão, coleções e log em três regiões; a largura adicional permite ler mensagens completas sem aumentar cards de status. |
| Ultra | Estado + coleções + lista de logs + detalhe do log selecionado, se a estrutura dos logs justificar. Se não houver campos adicionais, manter lista legível e remover região inútil. |

Não acrescentar números de latência, uso de memória ou garantias de alarmes em segundo plano sem fonte real. `diagAppVersion`, `diagDBStatus`, `diagAudioStatus`, `diagNotifStatus`, `tbodyDiagCollections`, `tbodyDiagLogs` continuam sendo saídas únicas dos dados oficiais.

## 5. Painéis úteis e contrato com Task 2

Um módulo adicional, por exemplo `parts_js_layout.py`, pode ser incorporado ao build após a UI. Sua função é composição/contexto; não criar um segundo motor de eventos, segundo cache de status ou segundo conjunto de regras de prazo.

| Painel novo sugerido | Fonte permitida e interação |
| --- | --- |
| `dashboardContextPanel` | Snapshot atual de eventos/cadastros, console ativo e classificação oficial. Quantidades por estado e duto; barras horizontais simples opcionais com rótulo e valor. Zero registros produz mensagem curta. |
| `dashboardSelectedDetail` | ID selecionado na lista do dashboard, resolvido no snapshot atual. Renderização compartilhada com o detalhe existente, com IDs únicos ou atributos data-role. Não modifica ID do spotlight. |
| `pendingContextPanel` | Mesmo conjunto filtrado da lista + contexto do evento selecionado. Quantidades explicam o filtro; relacionados usam a relação real e indicam se estão fora do filtro atual. |
| `completedContextPanel` / `completedDetailPane` | Conjunto de concluídos filtrado e evento selecionado. Datas, diferenças e responsável vêm dos dados/formatadores corrigidos. |
| `eventDraftSummary` / `eventRelatedList` | Valores vivos do único `formEvent`; lista existente do duto/UO selecionado. Prévia identificada; nenhuma gravação automática. |
| `cadastrosRelationsPanel` | Registro em edição/seleção e vínculos do snapshot. Mostrar quantidade e nomes reais; não escolher outro registro ao redimensionar. |
| `settingsPreviewPanel` / `rangeLivePreview` | Valores da edição, separados dos valores efetivos salvos; sem disparar som/notificação automaticamente. |
| `backupContextPanel` | Metadado real do último backup, contagens atuais e resultado oficial da validação. |
| `diagnosticLogDetail` | Objeto de log selecionado já disponível. Nunca inventar stack/causa quando ausentes. |

IDs acima são propostos e devem ser criados uma única vez. Reutilizar as funções públicas de ação do App.UI/App.Service, sem copiar botões com o mesmo ID e sem mover elementos que estejam sendo editados entre árvores a cada segundo.

Integração preferencial: Task 2 expõe notificações/hooks após alteração de dados, filtros, console, seleção e rascunho. O módulo pode oferecer `App.Layout.refresh(snapshot, reason)` e `App.Layout.syncSelection(viewId, eventId)`; nomes são proposta, não APIs já existentes. Atualização temporal usa a classificação/tempo oficial e altera apenas nós textuais/classes necessários. Em ausência de hook, envolver um ponto único de atualização com contrato explícito; não instalar polling paralelo nem reatribuir vários métodos fragilmente.

Preservar seleção, aba, foco, scroll e valores no resize; não regenerar formulários. Quando um evento some por conclusão/filtro, mostrar seleção vazia ou selecionar próximo item com política explícita, sem deixar detalhe stale. Gráficos opcionais devem ter equivalente textual e no máximo uma agregação clara por contexto; não são condição para cumprir GUI-32.

## 6. Seletores e HTML a corrigir

| Área | Seletores/IDs existentes | Alteração requerida |
| --- | --- | --- |
| Shell | `.app-header`, `.header-left`, `.header-status-bar`, `.header-actions`, `.app-nav`, `.app-main` | Grid/flex com `min-width:0`, lateral no desktop, controles compactos no móvel, retirar limites globais de 1650/2100 px. |
| Topo | `mobileActiveAlarmsBanner`, `backupOverdueBanner`, `viewModeWarningBanner` | Deslocamento real do cabeçalho, quebras de conteúdo, prioridade e camadas coerentes. |
| Menu | `appMobileDrawer`, `mobileDrawerOverlay`, `btnToggleMobileMenu` | Fechado fora da interação; nome, estado expandido e política modal coordenados com Task 2. Rever alias vazio `mobileDrawer` sem quebrar bindings. |
| Barra móvel | `mobileBottomNav`, `.bottom-nav-item`, `.bottom-nav-fab`, `.bottom-nav-badge` | Trocar seletores CSS antigos `.bottom-nav-btn`, `.mobile-fab`, `.bottom-badge`; estado atual/foco e Novo com label. |
| Dashboard | `.dashboard-metrics`, `.metric-card`, `.dashboard-highlight-grid`, `spotlightCard`, `.spotlight-header`, `.spotlight-timer` | Métricas como botões nativos; estado/contador juntos; regiões por grid; descrição limitada. |
| Alarmes laterais | `tabletActiveAlarmsPanel`, `tabletAlarmsCount`, `tabletAlarmsList` | Nomear segundo semântica definida pela Task 2; ampliar disponibilidade para desktop; não mostrar zero com lista preenchida. |
| Formulário | `formEvent`, `inputEventDescription`, `.form-grid`, `.form-sticky-submit-bar`, `boxStylusCanvas`, `stylusDrawingCanvas` | Textarea, fieldsets/legends, grupos expansíveis, footer seguro, desenho proporcional. |
| Pendentes | `.events-toolbar`, `.toolbar-primary`, `.search-box`, `filterDrawer`, `.pending-master-detail-grid`, `containerPendingCards`, `containerPendingTable`, `pendingDetailPane` | Remover min-width rígido da busca; sheet modal mobile; wrapper mestre compartilhado; detalhe preenchido em todos os tiers aplicáveis. |
| Concluídos | `.completed-event-card`, `.completed-card-details`, `containerCompletedCards`, `tableCompletedWrapper` | CSS deve usar a classe renderizada `.completed-card-details`, substituindo `.completed-card-extra`; expansão acessível e tabela contida. |
| Cadastros | `.cadastros-category-btn`, `.cat-count`, `.cadastros-unified-grid`, `.cadastro-hub-card`, `cadastrosCategoryBar` | Substituir `.cad-cat-btn`; wrappers reais por categoria/lista/editor; respeitar estado único da Task 2. |
| Cores | `containerColorRangeCards`, `tableColorRangesWrapper`, `colorChainPreview`, `colorPreviewBar`, `formColorRange` | Limites de leitura, editor/prévia coordenados, nomes associados e ação selecionar. |
| Modais | `.modal-overlay`, `.modal-box`, `.modal-header`, `.modal-body`, `.modal-footer`, `.modal-close` | Altura dinâmica, corpo rolável, ações acessíveis, título ligado por aria-labelledby em todos os dez. |
| Desenho em detalhes | `detailsModalDrawingBox`, `detailsStylusContainer`, `detailsModalDrawingImg` | Task 2 decide container visível único; CSS da imagem conserva proporção e não força fundo escuro no tema claro. |
| Status | `pillAudio`, `chipHeaderAudioWarning`, `pillDB`, `pillNotif`, `pillBackup` | Elementos clicáveis como button; status não interativos como texto. Substituir cores inline/fixas por tokens de estado. |

Não acrescentar somente uma camada extensa de `!important` ao fim do CSS. Consolidar regras por componente e tier e remover inline de dimensão/cor que esteja causando conflito. Preservar inline de visibilidade que ainda faça parte do contrato JS até substituição coordenada por estado semântico.

## 7. Acessibilidade, temas, overlays e áreas seguras

- Adicionar link “Ir para conteúdo” e alvo `mainContent`; cada visão ativa tem título identificável. Visões inativas não recebem foco. Labels visíveis associados por `for`; busca, ordenar, filtros, cores/largura da caneta e inputs de arquivo recebem nome. Placeholder/title sozinho não é o nome principal.
- Toda ação de ícone tem aria-label contextual (por exemplo “Mais ações de [descrição]”, com texto sanitizado). Fechar modal deve informar o diálogo. SVG decorativo tem `aria-hidden=true`. Métricas clicáveis são button e anunciam nome/quantidade, sem depender de listener numa div.
- Foco visível com contorno ≥2 px e offset, mantido em todos os temas; nunca `outline:none` sem alternativa. Alarme/erro/seleção combinam texto/ícone/borda; cor sozinha não comunica estado.
- A Task 2 gerencia foco, inert, retorno, Escape e empilhamento. A Task 3 fornece títulos, labels e containers corretos. `filterDrawer` no mobile e drawer devem participar do mesmo gerenciamento; o contexto de fundo fica inerte enquanto modal/sheet aberto.
- Definir tokens para texto de destaque, aviso, sucesso, perigo, superfície de spotlight, timer, seleção, borda, foco e texto de botão primário. Eliminar ciano/verde/amarelo claros hardcoded no tema claro. O industrial mantém ação primária amarela com texto preto, conforme evidência estabilizada; não registrar novamente a falsa falha de botão azul.
- Validar contraste efetivo de texto normal ≥4,5:1 e texto grande ≥3:1, além de limites/foco de controles ≥3:1 quando aplicável. Medir combinações reais, incluindo overlays/transparências, estado hover/disabled/selected e faixa customizada; não declarar conformidade só pela existência dos tokens.
- `prefers-reduced-motion` retira pulsação e transições não essenciais mesmo se usuário salvou pulsar. A indicação de alarme permanece por texto, ícone e borda. O relógio não usa live region a cada segundo; anunciar mudanças importantes de estado, não cada tick.
- Modal mobile de alarme/detalhes usa viewport disponível com `100dvh` e fallback; snooze/ações/filtros usam bottom sheet. Modais de conclusão/adiamento em telas amplas mantêm aproximadamente 480–560 px; detalhe 760–960 px se necessário, sem cobrir 3000 px.
- Aplicar `env(safe-area-inset-top/right/bottom/left)` aos elementos de borda, além do `viewport-fit=cover` no documento gerado quando adequado. Fundo pode alcançar a borda; ações/texto não. Padding inferior do main considera barra inferior + safe-area; form footer considera a mesma reserva, sem contar safe-area duas vezes.
- Com teclado aberto, campo ativo e ações precisam permanecer alcançáveis. Preferir footer sticky dentro da região do formulário; não uma barra fixed que cubra o meio do card. Se `visualViewport` indicar redução forte de altura, recolher temporariamente navegação inferior e usar footer no fluxo/área visível; restaurar ao fechar. Isso é comportamento dependente da Task 2, não CSS garantido em todos os aparelhos.
- Ordem de camadas única: conteúdo < navegação/topo < faixa/elementos sticky < backdrop/drawer < diálogo ativo < feedback pertinente ao diálogo. Evitar toasts cobrindo ações de confirmação; região de status pode ficar dentro do modal ativo.
- Canvas usa dimensão lógica e aspecto definidos pela Task 2; CSS só limita apresentação com `max-inline-size:100%`, altura proporcional e controles com quebra. Fullscreen conserva ferramenta, desenho, foco e botão sair visível.

## 8. Sequência de implementação e aceite da Task 3

1. Ler o handoff da Task 2 e reconciliar IDs/classes e fonte dos tiers. Escrever a regressão de layout solicitada no plano, sem duplicar testes comportamentais já aprovados.
2. Resolver shell, navegação, header/banners e largura global. Verificar os extremos 320/768/1200/1920/2560/3440 antes de adicionar painéis.
3. Corrigir HTML semântico, nomes, classes divergentes e grupos. Preservar IDs e formulários únicos; mover a tabela pendente para wrapper mestre compartilhado.
4. Implementar as nove composições por regiões. Adicionar somente painéis com fonte real disponível e ligação de seleção clara. Reduzir rolagem com disposição paralela e grupos recolhíveis; nunca cortar conteúdo com alturas fixas.
5. Ajustar temas, modais/sheets, canvas e safe-area. Reconciliar mínimos de toque e tamanho de fonte com Compacto sem reduzir ações essenciais.
6. Executar a matriz completa e capturar versões finais. Registrar exceções documentais e testes físicos indisponíveis de forma distinta.

Larguras da matriz existente: 320, 360, 390, 480, 600, 767, 768, 820, 1024, 1199, 1200, 1440, 1600, 1919, 1920, 2200, 2559, 2560 e 3440 px. Cobrir nove visões, dez modais, sete modos e três temas com amostras representativas de altura curta/longa e zoom; não presumir que toda combinação do produto cartesiano foi testada se não foi executada.

Contrato de regressão recebido do integrador: `tests/test_layout_browser.py` cobre 19 larguras e sete modos, sem overflow nas nove visões; a navegação lateral desktop tem altura de pelo menos 500 px e largura de no máximo 300 px no viewport de teste; o spotlight ultrawide tem largura máxima de 1100 px; a área main alcança a borda útil com distância máxima de 40 px. Esses limites são pisos/tetos de aceitação, não metas para esticar o spotlight. Os IDs HTML existentes permanecem. Task 2 fornecerá hooks/contextdata; esta entrega não cria runtime.

Critérios mensuráveis: sem overflow global nem controles cortados; sidebar real desktop; quatro destinos móveis estilizados; faixa de alarme abaixo do header; filtros como sheet no móvel; ações alcançáveis; textos longos quebram; editor/seleção/lousa sobrevivem a resize; contexto acrescenta informação verdadeira; tabelas/listas podem rolar internamente; nenhum card cresce de altura só para preencher um monitor; regiões ocultas não recebem Tab. Verificar estados vazio, poucos registros, 500 eventos, textos extensos, alarmes simultâneos e erro de importação.

Mapeamento principal: GUI-01/02/03/04/05, GUI-23/24/25/26/27, GUI-30/31/32/33/34/36/38/39; integração necessária com GUI-06/07/08/11/12/14/15/21/22/28/29/35/37/40. A aceitação funcional permanece com as Tasks 1/2/4; esta proposta não declara achados resolvidos nem validação de navegador executada.

## 9. Brief curto para quem implementar

Entregar primeiro o shell de largura total com sidebar desktop e topo móvel compacto. Depois distribuir conteúdo em cinco tiers, com tablet guiado por largura útil. Reusar IDs/métodos da Task 2, preservar rascunhos e seleção, trocar os três conjuntos de classes incompatíveis e tornar tabela/detalhe pendentes uma só composição. Em wide, acrescentar contexto real; em ultra, acrescentar detalhe/relacionados/histórico conforme a tela. Limitar linhas de leitura e campos, não a largura do shell. Não gerar dados de demonstração para preencher tela, não criar gráficos sem fonte e não alongar cartões. Cada região nova deve ter origem de dados, estado vazio curto, nome acessível e regra explícita de atualização.
