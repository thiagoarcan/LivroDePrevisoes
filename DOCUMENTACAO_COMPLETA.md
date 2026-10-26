# DOCUMENTAÇÃO TÉCNICA E OPERACIONAL EXAUSTIVA
## Caderno de Previsões Operacionais em Dutos (`index.html`)

---

## Sumário
1. [Objetivo da Aplicação e Contexto Operacional](#1-objetivo-da-aplicação-e-contexto-operacional)
   - [1.1 Objetivo Principal](#11-objetivo-principal)
   - [1.2 Objetivos Secundários](#12-objetivos-secundários)
   - [1.3 Contexto Operacional em Sala de Controle](#13-contexto-operacional-em-sala-de-controle)
2. [Tudo que a Aplicação é Capaz de Realizar (Funcionalidades e Regras de Negócio)](#2-tudo-que-a-aplicação-é-capaz-de-realizar-funcionalidades-e-regras-de-negócio)
   - [2.1 Hierarquia Operacional e Relacionamentos](#21-hierarquia-operacional-e-relacionamentos)
   - [2.2 Regras Estritas de Validação Cadastral e Integridade](#22-regras-estritas-de-validação-cadastral-e-integridade)
   - [2.3 Exclusão Física vs. Exclusão Lógica (Inativação) e Bloqueio por Dependências](#23-exclusão-física-vs-exclusão-lógica-inativação-e-bloqueio-por-dependências)
   - [2.4 Gestão do Ciclo de Vida das Previsões Operacionais (Eventos)](#24-gestão-do-ciclo-de-vida-das-previsões-operacionais-eventos)
   - [2.5 Recursos de Produtividade Operacional (Console Global, Inserção Consecutiva, Duplicação, Lote de UOs, Adição Inline)](#25-recursos-de-produtividade-operacional-console-global-inserção-consecutiva-duplicação-lote-de-uos-adição-inline)
   - [2.6 Lousa Digital / Anotação Manuscrita com Caneta Stylus (Tablets e Touch)](#26-lousa-digital--anotação-manuscrita-com-caneta-stylus-tablets-e-touch)
   - [2.7 Sistema Multicanal de Alarmes e Alertas Operacionais](#27-sistema-multicanal-de-alarmes-e-alertas-operacionais)
   - [2.8 Classificação Dinâmica por Faixas de Tempo e Cores](#28-classificação-dinâmica-por-faixas-de-tempo-e-cores)
   - [2.9 Trilha de Auditoria e Rastreabilidade Completa](#29-trilha-de-auditoria-e-rastreabilidade-completa)
   - [2.10 Backup Completo (JSON), Importação (Substituição / Mesclagem) e Exportação CSV (Excel)](#210-backup-completo-json-importação-substituição--mesclagem-e-exportação-csv-excel)
   - [2.11 Preparação Arquitetural para Sincronização Futura](#211-preparação-arquitetural-para-sincronização-futura)
3. [Como a Aplicação Funciona Tecnicamente (Arquitetura e Engenharia)](#3-como-a-aplicação-funciona-tecnicamente-arquitetura-e-engenharia)
   - [3.1 Arquitetura Single-File 100% Offline e Pipeline de Build](#31-arquitetura-single-file-100-offline-e-pipeline-de-build)
   - [3.2 Arquitetura em Camadas no Namespace `window.App`](#32-arquitetura-em-camadas-no-namespace-windowapp)
   - [3.3 Esquema Completo do Banco de Dados Local IndexedDB (`LivroPrevisoesDutosDB` - 11 Object Stores)](#33-esquema-completo-do-banco-de-dados-local-indexeddb-livroprevisoesdutosdb---11-object-stores)
   - [3.4 Funcionamento do Motor de Monitoramento (`App.AlarmEngine`) e Ciclo de 1 Segundo](#34-funcionamento-do-motor-de-monitoramento-appalarmengine-e-ciclo-de-1-segundo)
   - [3.5 Sintetizador Sonoro Local (`App.Audio` - Web Audio API)](#35-sintetizador-sonoro-local-appaudio---web-audio-api)
   - [3.6 Sistema de 3 Temas Visuais, 7 Modos Responsivos e Adaptação Multi-Dispositivo](#36-sistema-de-3-temas-visuais-7-modos-responsivos-e-adaptação-multi-dispositivo)
   - [3.7 Catálogo de Variáveis CSS (Tokens dos 3 Temas: Controle Escuro, Claro Operacional e Industrial Alto Contraste)](#37-catálogo-de-variáveis-css-tokens-dos-3-temas-controle-escuro-claro-operacional-e-industrial-alto-contraste)
   - [3.8 Catálogo Exaustivo de Todos os Métodos JavaScript por Camada](#38-catálogo-exaustivo-de-todos-os-métodos-javascript-por-camada)
4. [Mapeamento Exaustivo de Todos os Componentes da Interface Gráfica (372 IDs HTML)](#4-mapeamento-exaustivo-de-todos-os-componentes-da-interface-gráfica-372-ids-html)
   - [4.1 Cabeçalho Global (`<header class="app-header">`), Barra de Status e Banners Persistentes](#41-cabeçalho-global-header-classapp-header-barra-de-status-e-banners-persistentes)
   - [4.2 Menu Retrátil Mobile/Tablet (`#appMobileDrawer`), Barra Inferior (`#mobileBottomNav`) e Botões Flutuantes (FAB)](#42-menu-retrátil-mobiletablet-appmobiledrawer-barra-inferior-mobilebottomnav-e-botões-flutuantes-fab)
   - [4.3 Barra de Navegação Desktop (`<nav class="app-nav">`)](#43-barra-de-navegação-desktop-nav-classapp-nav)
   - [4.4 Aba 1: Painel Principal (`#viewDashboard`)](#44-aba-1-painel-principal-viewdashboard)
   - [4.5 Aba 2: Novo Evento / Cadastrar Previsão (`#viewNewEvent`)](#45-aba-2-novo-evento--cadastrar-previsão-viewnewevent)
   - [4.6 Aba 3: Eventos Pendentes (`#viewPendingEvents`)](#46-aba-3-eventos-pendentes-viewpendingevents)
   - [4.7 Aba 4: Eventos Concluídos (`#viewCompletedEvents`)](#47-aba-4-eventos-concluídos-viewcompletedevents)
   - [4.8 Aba 5: Cadastros Operacionais Unificados (`#viewCadastros`)](#48-aba-5-cadastros-operacionais-unificados-viewcadastros)
   - [4.9 Aba 6: Configurações de Alertas (`#viewConfigAlerts`)](#49-aba-6-configurações-de-alertas-viewconfigalerts)
   - [4.10 Aba 7: Configurações de Cores (`#viewConfigColors`)](#410-aba-7-configurações-de-cores-viewconfigcolors)
   - [4.11 Aba 8: Backup e Dados (`#viewBackup`)](#411-aba-8-backup-e-dados-viewbackup)
   - [4.12 Aba 9: Diagnóstico Técnico (`#viewDiagnostic`)](#412-aba-9-diagnóstico-técnico-viewdiagnostic)
   - [4.13 Mapeamento de Todos os 10 Modais do Sistema e Container de Toasts](#413-mapeamento-de-todos-os-10-modais-do-sistema-e-container-de-toasts)
5. [Registro de Auditoria Técnica e Unificação de Bindings (`v1.1.0`)](#5-registro-de-auditoria-técnica-e-unificação-de-bindings-v110)

---

## 1. Objetivo da Aplicação e Contexto Operacional

### 1.1 Objetivo Principal
O **Caderno de Previsões Operacionais em Dutos** tem como objetivo primordial **eliminar ou reduzir drasticamente o risco de esquecimento ou atraso na execução e acompanhamento de atividades operacionais programadas no transporte dutoviário**, oferecendo aos controladores de sala de controle uma ferramenta digital dedicada, estruturada, com monitoramento ativo em tempo real e alarmes multicanais (sonoros, visuais e notificações nativas).

A aplicação substitui anotações informais em papel, blocos de notas ou planilhas estáticas por um sistema ativo que calcula regressivamente o tempo até cada evento operacional (ex.: término de recebimento em tanque, chegada de PIG raspador, fechamento de válvula, ajuste de setpoint de pressão, partida/parada de bombas, abertura de manifold), mudando automaticamente a criticidade visual dos cartões e disparando alertas antes que o horário previsto seja atingido.

### 1.2 Objetivos Secundários
1. **Padronização da Estrutura Operacional**: Garantir que toda previsão seja registrada obedecendo rigorosamente à topologia real da malha dutoviária (`Console Operacional` $\rightarrow$ `Duto` $\rightarrow$ `Unidade Operacional (UO)` $\rightarrow$ `Tipo de Equipamento` $\rightarrow$ `TAG do Equipamento`).
2. **Continuidade na Passagem de Turno**: Permitir que o controlador que assume o console visualize instantaneamente todas as previsões pendentes, os eventos atrasados, os alarmes já disparados ou adiados e o histórico do que foi concluído no turno anterior.
3. **Rastreabilidade e Auditoria Operacional**: Registrar automaticamente toda ação realizada sobre uma previsão (criação, edição, disparo de alarme, reconhecimento, adiamento/snooze, conclusão com cálculo de pontualidade e reabertura), vinculando cada ação ao horário exato e à identificação do controlador local.
4. **Independência de Infraestrutura de Rede (100% Offline)**: Operar integralmente dentro de um único arquivo [`index.html`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/index.html) sem exigir servidor backend, banco de dados externo, instalação de pacotes ou conexão com a internet, garantindo funcionamento em redes isoladas ou estações de trabalho restritas de sala de controle.
5. **Ergonomia para Múltiplos Dispositivos**: Atender tanto estações desktop multi-monitores e video walls em sala de controle (com 3 temas visuais e 7 modos responsivos) quanto tablets e smartphones operacionais com suporte a toque e escrita manual via caneta *stylus*.

### 1.3 Contexto Operacional em Sala de Controle
Na operação de dutos (oleodutos, gasodutos, polidutos), um controlador gerencia um **Console Operacional** (como `C02`, `C04`, `C08`, etc.) que supervisiona diversos **Dutos** (como `OSCAN`, `OSBRA`, `DTCS`), os quais interligam múltiplas **Unidades Operacionais - UOs** (refinarias e terminais como `REFAP`, `TEDEP`, `REPLAN`, `TEBAR`). Durante o turno, dezenas de eventos futuros são estimados com base em vazões, níveis de tanques e janelas operacionais. Como o controlador lida simultaneamente com telas de SCADA, comunicações telefônicas e manobras emergenciais, um evento estimado para ocorrer daqui a 45 minutos ou 2 horas pode ser esquecido se não houver um sistema de aviso prévio com repetição até reconhecimento.

---

## 2. Tudo que a Aplicação é Capaz de Realizar (Funcionalidades e Regras de Negócio)

### 2.1 Hierarquia Operacional e Relacionamentos
A aplicação modela fielmente a hierarquia física e lógica da operação:
1. **Console Operacional (`consoles`)**: Nível superior de supervisão. O sistema já vem pré-populado na primeira inicialização (`App.Config.INITIAL_CONSOLES`) com 12 consoles padrão: **`C02`, `C03`, `C04`, `C05`, `C06`, `C07`, `C08`, `C10`, `C11`, `C14`, `C15`, `C16`** (selecionando `C04` como console ativo padrão inicial).
2. **Duto (`pipelines`)**: Cada duto pertence obrigatoriamente a **1 Console Responsável** (`consoleId`).
3. **Relacionamento M:N entre Duto e UO (`pipelineOperationalUnits`)**:
   - Um duto conecta várias Unidades Operacionais (no mínimo 2 UOs).
   - Uma mesma Unidade Operacional (ex.: `REFAP` ou `REPLAN`) pode estar conectada a múltiplos dutos diferentes.
   - Esse relacionamento muitos-para-muitos é gerido pela tabela associativa `pipelineOperationalUnits`.
4. **Unidade Operacional - UO (`operationalUnits`)**: Instalação física (terminal, refinaria, base, estação intermediária).
5. **Tipo de Equipamento (`equipmentTypes`)**: Categoria de equipamento vinculada a uma UO específica (`uoId`), como *Tanque*, *Bomba*, *Esfera*, *Válvula de Controle*.
6. **TAG do Equipamento (`equipmentTags`)**: Identificador único de um equipamento físico (ex.: `TQ-804`, `BB-101A`, `ES-201`, `PCV-301`), vinculado a uma UO (`uoId`) e a um Tipo de Equipamento (`equipmentTypeId`).

No formulário de Nova Previsão (`#viewNewEvent`), essa hierarquia funciona por **seletores encadeados (cascading dropdowns)** com feedback textual em tempo real (`#cascadeStatusText`):
- O **Console** é herdado automaticamente do seletor global no cabeçalho (`#headerActiveConsole`).
- O seletor de **Duto** (`#selectEventPipeline`) carrega apenas os dutos ativos pertencentes ao Console ativo.
- Ao escolher o Duto, o seletor de **UO** (`#selectEventUO`) é habilitado, exibe apenas as UOs vinculadas àquele duto específico e atualiza `#cascadeStatusText` (`"✓ X UO(s) carregada(s) para o duto selecionado."`).
- Ao escolher a UO, o seletor de **Tipo de Equipamento** (`#selectEventEquipmentType`, opcional) é habilitado com os tipos cadastrados naquela UO e atualiza `#cascadeStatusText` (`"✓ X Tipo(s) de equipamento disponível(is) na UO."`).
- Ao escolher o Tipo de Equipamento, o seletor de **TAG** (`#selectEventTag`, opcional) é habilitado com os TAGs daquele tipo naquela UO e atualiza `#cascadeStatusText` (`"✓ X TAG(s) disponível(is) para o tipo selecionado."`).

*(Nota sobre edição: caso um evento antigo esteja sendo editado e algum de seus itens cadastrais tenha sido inativado posteriormente, os métodos `load*Options` recebem o parâmetro `includeInactiveId` para garantir que o registro inativo continue visível e selecionado durante a edição).*

### 2.2 Regras Estritas de Validação Cadastral e Integridade
Implementadas na camada [`App.Service`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_service.py#L6-L1245):
- **Unicidade de Console**: Não permite criar ou renomear um console com nome já existente (comparação *case-insensitive* e sem espaços extras via `App.Utils.cleanStr`).
- **Regra Mínima de 2 UOs por Duto**: Ao salvar um Duto (`App.Service.savePipeline`), é obrigatório vincular **no mínimo 2 Unidades Operacionais** (`uoIds.length < 2`). Caso contrário, lança erro: *"O duto deve estar associado a no mínimo 2 Unidades Operacionais (UOs)."*
- **Unicidade de Duto no Console**: Não permite dois dutos com o mesmo nome dentro do mesmo console.
- **Unicidade de UO**: Não permite duas UOs com o mesmo nome. No cadastro em lote (`App.Service.saveUOBatch`), caso uma UO informada já exista e esteja inativa, o sistema a reativa automaticamente (`match.active = true`) sem duplicá-la.
- **Unicidade de Tipo por UO**: Não permite dois tipos de equipamento com o mesmo nome na mesma UO.
- **Exclusividade Global de TAG por UO (`App.Service.saveEquipmentTag`)**: Cada código de TAG pertence **exclusivamente a uma única UO em todo o sistema**.
  - Se o controlador tentar cadastrar o TAG `TQ-804` na UO `TEDEP`, mas `TQ-804` já existir na UO `REFAP`, o sistema bloqueia a operação com a mensagem exata: `"O TAG TQ-804 já está cadastrado na UO REFAP e não pode ser associado a outra UO."`
  - Se tentar duplicar na mesma UO, bloqueia informando: `"O TAG <nome> já está cadastrado nesta UO."`

### 2.3 Exclusão Física vs. Exclusão Lógica (Inativação) e Bloqueio por Dependências
Para proteger a integridade referencial do histórico operacional:
- **Verificação prévia antes da exclusão física**:
  - **Console (`deleteConsole`)**: Verifica se há dutos (`pipelines`) ou eventos (`events`) vinculados ao console.
  - **Duto (`deletePipeline`)**: Verifica se há eventos (`events`) vinculados ao duto. (Se não houver eventos, remove também os vínculos em `pipelineOperationalUnits` e exclui o duto).
  - **UO (`deleteUO`)**: Verifica se há dutos associados (`pipelineOperationalUnits`), tipos de equipamentos (`equipmentTypes`), TAGs (`equipmentTags`) ou eventos (`events`) vinculados à UO.
  - **Tipo de Equipamento (`deleteEquipmentType`)**: Verifica se há TAGs (`equipmentTags`) ou eventos (`events`) vinculados ao tipo.
  - **TAG (`deleteEquipmentTag`)**: Verifica se há eventos (`events`) vinculados ao TAG.
- **Acionamento do Modal de Dependências (`#modalDependency`)**: Quando qualquer uma das verificações acima encontra vínculos, o serviço lança um erro com `error.isDependencyError = true` e a lista exata de quantidades (`error.dependencies`). A UI captura esse erro e abre automaticamente o modal **Registro com Dependências**, listando os vínculos e oferecendo o botão **"Inativar Registro"** (`#btnDependencyInactivate`), que executa a exclusão lógica (`active = false`).
- **Comportamento de Registros Inativos e Filtros de Situação**: Registros com `active: false` deixam de aparecer nos seletores de criação de novas previsões, mas permanecem salvos no banco para que os eventos históricos (pendentes ou concluídos) continuem exibindo seus nomes corretamente e são contabilizados na coluna `Inativos` do Diagnóstico Técnico (`#viewDiagnostic`). Na Aba 5 (`#viewCadastros`), cada uma das 5 sub-seções possui um seletor de situação dedicado (`#filterActiveConsoles`, `#filterActivePipelines`, `#filterActiveUOs`, `#filterActiveEquipmentTypes`, `#filterActiveTags`) com opções `Todos` (`all`, padrão), `Ativos` (`active`) e `Inativos` (`inactive`), permitindo visualizar e reativar qualquer item inativo a qualquer momento com 1 clique no botão `Ativar` (além da reativação automática ao informar o nome de uma UO inativa em `saveUOBatch`).

### 2.4 Gestão do Ciclo de Vida das Previsões Operacionais (Eventos)
1. **Criação (`App.Service.saveEvent`)**:
   - Valida campos obrigatórios: Console, Duto, UO, Data, Hora, Descrição da atividade e antecedência de alarme ($\ge 0$).
   - Constrói o timestamp ISO (`scheduledAt`) a partir da data e hora locais informadas.
   - Define prioridades (`Baixa`, `Normal`, `Alta`, `Crítica`), observações opcionais, desenho de caneta opcional (`stylusDrawing`) e parâmetros de alarme (padrão global ou customizado por evento).
   - Inicializa `status: 'pendente'`, `alarmState: 'idle'`, `alarmTriggerCount: 0`.
2. **Edição**:
   - Permite alterar qualquer dado da previsão.
   - Detecta mudanças de horário, descrição e estado de alarme para gravar o resumo das alterações na auditoria.
   - Caso o horário previsto (`scheduledAt`) seja alterado, redefine automaticamente `alarmState = 'idle'` e `alarmSnoozedUntil = null` para que o alarme volte a disparar no novo horário.
3. **Conclusão com Cálculo Automático de Pontualidade (`App.Service.completeEvent`)**:
   - Registra o timestamp exato da conclusão (`completedAt = now.toISOString()`).
   - Calcula automaticamente a diferença em minutos entre o horário efetivo da conclusão e o horário previsto:
     $$\text{diffMinutes} = \frac{\text{actualTime} - \text{scheduledTime}}{60000}$$
   - Formata a diferença via `App.Utils.formatDiffMinutes`:
     - Se $\text{round}(\text{diffMinutes}) > 0$: `"Com atraso de X min"`
     - Se $\text{round}(\text{diffMinutes}) < 0$: `"Com antecedência de X min"`
     - Se $\text{round}(\text{diffMinutes}) == 0$: `"Exatamente no horário"`
   - Permite registrar observações/justificativas de conclusão (`completionNote`), muda `status` para `'concluido'` e encerra qualquer alarme ativo (`alarmState = 'acknowledged'`).
4. **Reabertura com Preservação de Histórico (`App.Service.reopenEvent`)**:
   - Permite retornar um evento concluído para a lista de `Eventos Pendentes`.
   - Caso o horário previsto original já esteja no passado, o modal `#modalReopenEvent` exibe um alerta amarelo (`#boxReopenPastWarning`) e sugere automaticamente a data/hora de `agora + 1 hora` para reprogramação.
   - Antes de limpar `completedAt` e `completedTimeDiffMinutes` no registro ativo, empacota os dados da conclusão anterior (`completedAt`, `diffMinutes`, `completionNote`) e os grava permanentemente em `eventHistory` (`previousValue`), garantindo que nenhuma informação histórica seja perdida.
5. **Exclusão de Evento (`App.Service.deleteEvent`)**:
   - Exclui fisicamente o evento da store `events` e remove em cascata todos os seus registros de auditoria na store `eventHistory`.

### 2.5 Recursos de Produtividade Operacional (Console Global, Inserção Consecutiva, Duplicação, Lote de UOs, Adição Inline)
1. **Seletor Global de Console no Cabeçalho (`#headerActiveConsole`)**:
   - O controlador seleciona seu Console uma única vez no topo da tela. Essa escolha é persistida no IndexedDB (`settings.activeConsoleId`) e aplicada automaticamente ao formulário de novas previsões, ao destaque do Painel Principal e ao filtro automático de Eventos Pendentes (`#checkFilterOnlyActiveConsole`).
2. **Manutenção de Duto e UO (`#checkKeepDutoUO`)**:
   - Checkbox marcado por padrão no formulário de evento que mantém o Duto e a UO selecionados após salvar uma previsão.
3. **Botão "Salvar e + Outra no Duto" (`#btnSubmitAndNew`)**:
   - Salva a previsão atual, permanece na tela de cadastro mantendo Console, Duto, UO, Tipo e TAG selecionados, **avança automaticamente o horário sugerido em +30 minutos**, limpa apenas a descrição, observações e lousa, e posiciona o foco diretamente no campo de descrição (`#inputEventDescription`) para digitação imediata da próxima atividade.
4. **Duplicação Rápida de Eventos (`App.UI.duplicateEvent` / `App.Service.getCloneDataForEvent`)**:
   - Disponível nos cartões e tabelas do Painel, Pendentes e Concluídos (botão `+ Duplicar`).
   - Copia toda a hierarquia (Console, Duto, UO, Tipo, TAG), descrição, notas, prioridade, configurações de alarme e desenho da caneta para um novo formulário de criação, definindo o horário sugerido para **agora + 30 minutos**.
5. **Cadastro de UOs em Lote (`App.Service.saveUOBatch`)**:
   - No formulário de UOs (`#inputUOName`), o controlador pode digitar várias UOs de uma só vez separadas por vírgula, ponto e vírgula ou quebra de linha (ex.: `REFAP, TEDEP, REPLAN, TEBAR`). O sistema processa todas em lote.
6. **Criador Inline de UOs dentro do Formulário de Duto (`#inputInlineNewUO` + `#btnInlineAddUO`)**:
   - Ao cadastrar um novo Duto, se o controlador perceber que falta cadastrar uma ou mais UOs, não precisa sair do formulário do duto: basta digitar o(s) nome(s) no campo inline `+ Digitar nova UO aqui...` e clicar em `+ Criar UO`. O sistema cria as UOs no banco, atualiza todos os dropdowns da aplicação (`refreshAllMasterDataDropdowns`) e **já marca automaticamente os checkboxes das UOs recém-criadas** para aquele duto.

### 2.6 Lousa Digital / Anotação Manuscrita com Caneta Stylus (Tablets e Touch)
- Integrada ao formulário de Nova Previsão (`#boxStylusCanvas` / `#stylusDrawingCanvas`).
- Utiliza a **Pointer Events API** (`pointerdown`, `pointermove`, `pointerup`, `pointercancel`, `pointerleave` com `setPointerCapture`), oferecendo suporte nativo a canetas capacitivas/ativas de tablets (`e.pointerType === 'pen'` com sensibilidade à pressão `e.pressure`), toque com o dedo ou mouse, com bloqueio de rolagem acidental (`touch-action: none`) e **rejeição inteligente de palma (palm rejection)**: quando um traço com caneta stylus está em andamento (`this.stylusActivePointerType === 'pen'`), toques acidentais de mão/dedo (`e.pointerType === 'touch'`) são ignorados, exibindo o modo e a espessura ativa em `#stylusModeIndicator` (`Modo: Caneta (4px)` ou `Modo: Borracha (18px)`).
- Permite escolher a **cor do traço** (`#inputStylusStrokeColor`, padrão `#38bdf8`), a **espessura da ponta** (`#selectStylusStrokeWidth`: Fina 2px, Normal 4px, Grossa 8px), **Desfazer (Undo)** o último traço a partir da pilha de histórico de até 25 snapshots (`#btnUndoStylusCanvas` / `this.stylusHistory`), alternar para o modo **Borracha** (`#btnEraserStylusCanvas`, que usa `globalCompositeOperation = 'destination-out'` com largura 18px), **Limpar** toda a tela com modal de confirmação caso haja desenho (`#btnClearStylusCanvas`) ou alternar **Tela Cheia** (`#btnFullscreenStylusCanvas`, que aplica `.fullscreen-lousa` ao container `#boxStylusCanvas`).
- O desenho é serializado em Base64 (`image/png` via `canvas.toDataURL`) e salvo no atributo `stylusDrawing` do evento.
- Eventos que possuem desenho exibem o selo interativo `✎ Possui Anotação / Esboço` no cartão, na aba `Anotações` do painel Master-Detail (`#pendingDetailPane`) e no Modal de Detalhes (`#detailsModalDrawingBox` / `#detailsStylusContainer` / `#detailsModalDrawingImg`).

### 2.7 Sistema Multicanal de Alarmes e Alertas Operacionais
O sistema dispõe de 6 canais e comportamentos de alerta que podem ser combinados globalmente ou por evento:
1. **Sinal Sonoro Sintetizado Local (`Web Audio API`)**: 4 timbres gerados matematicamente em tempo real sem arquivos externos (`chime`, `beep`, `siren`, `blip`) e controle de volume de `0%` a `100%`.
2. **Janela Modal Flutuante de Alerta (`#modalAlarmTrigger`)**: Popup vermelho pulsante de alto contraste exibido automaticamente sobre qualquer tela quando o alarme dispara.
3. **Destaque Visual do Cartão na Lista**: Borda lateral colorida conforme a faixa de criticidade.
4. **Efeito Visual de Pulsação Luminosa**: Animações CSS `@keyframes pulse-danger` (`.pulsing-card`) e `@keyframes pulse-badge` (`.pulsing-badge`) nos cartões e selos de eventos críticos/atrasados ou com alarme disparado.
5. **Alteração Dinâmica do Título da Aba do Navegador**: Quando há um alarme disparando (`hasActiveFiringAlarm`), o título da aba pisca a cada segundo alternando entre `'⚠️ ALARME OPERACIONAL!'` e `'Caderno de Previsões'`, chamando a atenção mesmo se o controlador estiver em outra aba do navegador.
6. **Notificação Nativa do Sistema Operacional (`Web Notifications API`)**: Dispara notificação nativa do Windows/OS com `requireInteraction: true` contendo a hierarquia (`Console | Duto | UO | TAG`), descrição e horário previsto. Clicar na notificação foca a janela da aplicação (`window.focus()`).

**Mecanismos de Controle do Alarme**:
- **Antecedência Configurável (`leadTime`)**: Pode disparar $N$ minutos antes do horário previsto (padrão 15 min) ou exatamente no horário ($0$ min).
- **Repetição Automática até Reconhecimento**: Se não reconhecido, o alarme volta a tocar e abrir o modal a cada `repeatIntervalMinutes` (padrão 2 min) até o limite de `maxRepeats` (padrão 5 vezes).
- **Reconhecimento Individual ou em Lote (`acknowledgeAlarm`)**: Interrompe o som e as repetições futuras daquele evento (`alarmState = 'acknowledged'`), mantendo o evento pendente até sua conclusão efetiva. Quando há alarmes ativos, o banner persistente `#mobileActiveAlarmsBanner` também oferece o botão `#btnBannerAckAll` para reconhecer todos os alarmes disparados de uma só vez.
- **Adiamento / Snooze (`snoozeAlarm`)**: Silencia temporariamente o alarme por 5, 10, 15, 30 minutos ou valor customizado (1 a 1440 min), agendando novo disparo automático em `alarmSnoozedUntil`.

### 2.8 Classificação Dinâmica por Faixas de Tempo e Cores
- **Separação Estrita de "Atrasado"**: Qualquer evento cujo horário previsto já tenha passado ($\text{diffMs} < 0$) é tratado separadamente das faixas futuras, recebendo automaticamente a classificação **`Atrasado`** (cor `#991b1b`, fundo vermelho escuro `--status-overdue-bg`, ícone `⏱`, prioridade `0`, piscante e sonoro).
- **Faixas de Tempo Futuro Configuráveis (`colorRanges`)**: Para eventos com $\text{diffMs} \ge 0$, o sistema classifica conforme os minutos restantes na tabela de faixas, normalizando a chave CSS via `App.Service.normalizeRangeKey(r.id, r.name)` e atribuindo ícone semântico via `App.Service.getRangeIcon(normKey)`:
  1. **Crítico** (`range_critico` $\rightarrow$ chave CSS `critico`, ícone `⚠`): `0 a 15 min` — Cor `#dc2626` (Vermelho) | Prioridade `1` | Piscar: `Sim` | Som: `Sim`
  2. **Urgente** (`range_urgente` $\rightarrow$ chave CSS `urgente`, ícone `⚡`): `15 a 30 min` — Cor `#ea580c` (Laranja) | Prioridade `2` | Piscar: `Não` | Som: `Não`
  3. **Atenção** (`range_atencao` $\rightarrow$ chave CSS `atencao`, ícone `🔔`): `30 a 45 min` — Cor `#ca8a04` (Amarelo Escuro) | Prioridade `3` | Piscar: `Não` | Som: `Não`
  4. **Monitoramento** (`range_monitor` $\rightarrow$ chave CSS `monitoramento`, ícone `👁`): `45 a 60 min` — Cor `#2563eb` (Azul) | Prioridade `4` | Piscar: `Não` | Som: `Não`
  5. **Normal** (`range_normal` $\rightarrow$ chave CSS `normal`, ícone `●`): `60 a 999999 min` — Cor `#16a34a` (Verde) | Prioridade `5` | Piscar: `Não` | Som: `Não`
- **Validação Matemática de Faixas (`App.Service.validateColorRanges`)**:
  - Deve existir pelo menos 1 faixa cadastrada.
  - Em cada faixa, `minMinutes < maxMinutes`.
  - A primeira faixa ordenada deve iniciar obrigatoriamente em `0 minutos`.
  - **Proibição de Sobreposições e Lacunas**: Para toda faixa $i > 0$, o `minMinutes` da faixa atual deve ser **exatamente igual** ao `maxMinutes` da faixa anterior (`curr.minMinutes === prev.maxMinutes`). Se for menor, acusa erro de sobreposição; se for maior, acusa erro de lacuna.

### 2.9 Trilha de Auditoria e Rastreabilidade Completa
Toda operação gera um registro imutável na store `eventHistory` com `id` (UUID), `eventId`, `action`, `timestamp` (ISO), `description`, `previousValue`, `newValue` e `localUser` (nome do controlador configurado na máquina ou `'Sistema de Alarme'`):
- `criacao`: Criação da previsão operacional.
- `edicao`: Alteração de dados cadastrais, horário, descrição ou alarme.
- `disparo_alarme`: Registro automático do disparo inicial ou de cada repetição, listando quais canais foram acionados (`Som`, `Modal`, `Notificação`).
- `reconhecimento`: Reconhecimento manual pelo controlador.
- `adiamento`: Adiamento (snooze) informando a quantidade de minutos e o novo horário previsto de disparo.
- `conclusao`: Encerramento da atividade com a diferença de tempo calculada e a nota de conclusão.
- `reabertura`: Reabertura de evento concluído com preservação integral dos dados da conclusão anterior em JSON.

### 2.10 Backup Completo (JSON), Importação (Substituição / Mesclagem) e Exportação CSV (Excel)
1. **Exportação de Backup JSON (`App.Backup.exportJSON`)**:
   - Exporta um arquivo `backup_previsoes_dutos_YYYY-MM-DDTHH-MM-SS.json` contendo cabeçalho (`application`, `schemaVersion: 1`, `exportedAt`) e os dados completos de 10 stores (`consoles`, `pipelines`, `operationalUnits`, `pipelineOperationalUnits`, `equipmentTypes`, `equipmentTags`, `events`, `eventHistory`, `colorRanges`, `settings`).
   - Atualiza automaticamente `settings.lastBackupAt`, a pílula de status `#pillBackup` no cabeçalho, o rótulo `#labelLastBackupDate`, o modal `#statusModalLastBackup` e o banner preventivo `#backupOverdueBanner` (que alerta quando nenhum backup local foi realizado ainda ou quando o último backup tem mais de `7` dias — `daysDiff > 7`).
2. **Validação e Importação de Backup JSON (`App.Backup.validateBackupData` / `validateBackupFile` / `importJSON`)**:
   - Verifica sintaxe JSON, compatibilidade de `schemaVersion === 1` e presença das coleções obrigatórias (`consoles`, `pipelines`, `operationalUnits`, `events`).
   - Exibe o modal `#modalImportSummary` com a contagem de registros encontrados e permite escolher entre 2 modos:
     - **Modo Mesclar (`merge` - Padrão)**: Compara os registros pelo `id` (ou `key`). Se o registro não existir localmente, insere; se já existir, atualiza apenas se `newVer >= currentVer`, evitando duplicações e preservando dados locais.
     - **Modo Substituir Tudo (`replace`)**: **Dispara automaticamente o download de um backup JSON preventivo dos dados atuais antes de apagar qualquer coisa**, limpa todas as stores e carrega integralmente o arquivo importado.
3. **Exportação de Relatórios CSV para Microsoft Excel (`App.Backup.exportCSV`)**:
   - Gera arquivos `.csv` codificados em **UTF-8 com BOM (`\uFEFF`)** e delimitados por **ponto e vírgula (`;`)**, com tratamento de escape de aspas e quebras de linha (`App.Utils.escapeCSV`) e datas no padrão brasileiro (`DD/MM/AAAA HH:mm`), garantindo abertura direta no Excel em português sem corrupção de acentos e com separação automática de colunas. Aceita os parâmetros `'pendente'`/`'pending'`, `'concluido'`/`'completed'`, `'todos'`/`'all'` e `'cadastros'`.

### 2.11 Preparação Arquitetural para Sincronização Futura
Todos os registros de entidades operacionais (`consoles`, `pipelines`, `operationalUnits`, `pipelineOperationalUnits`, `equipmentTypes`, `equipmentTags`, `events`) são criados com metadados padronizados para futura replicação/sincronização cliente-servidor:
- `id`: UUID v4 gerado via `crypto.randomUUID()` (ou fallback RFC 4122 em `App.Utils.uuid()`).
- `createdAt`: Timestamp ISO 8601 da criação.
- `updatedAt`: Timestamp ISO 8601 da última modificação.
- `version`: Contador inteiro incremental (`1, 2, 3...`) atualizado a cada `update` ou `toggleActive` para controle de concorrência otimista.
- `active`: Booleano para exclusão lógica (*soft delete*).
- `synchronizationStatus`: Inicializado como `'local-only'`.

---

## 3. Como a Aplicação Funciona Tecnicamente (Arquitetura e Engenharia)

### 3.1 Arquitetura Single-File 100% Offline e Pipeline de Build
A aplicação final é distribuída em um único arquivo autônomo [`index.html`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/index.html) (`10.009` linhas) que contém todo o CSS, HTML, ícones vetoriais (SVG inline) e JavaScript necessários. Não há nenhuma requisição HTTP externa (zero CDNs, zero fontes externas, zero imagens externas).

Para organização da engenharia de código, o projeto é modularizado em 5 módulos Python que são montados pelo script [`build_all.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/build_all.py):
1. [`parts_css.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_css.py) (`CSS_CONTENT` - 1.899 linhas): Variáveis de tema CSS para os 3 temas (`:root`, `body.theme-light` e `body.theme-industrial`), animações `@keyframes`, arquitetura responsiva universal (`body.density-compact` e `body[data-layout-mode="mobile"|"tablet"|"conventional"|"widescreen"|"ultrawide"]`), banners persistentes, bottom navigation bar, master-detail split view, action sheets, lousa stylus com modo tela cheia (`.fullscreen-lousa`) e 10 modais.
2. [`parts_html.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_html.py) (`HTML_CONTENT` - 2.013 linhas): Estrutura semântica do cabeçalho, barra de status, 3 banners persistentes, drawer mobile, barra inferior `#mobileBottomNav`, navegação desktop, 9 seções `.view-section`, botões FAB, 10 modais (`.modal-overlay`) e container de toasts (**372 IDs HTML únicos**).
3. [`parts_js_core.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_core.py) (`JS_CORE` - 665 linhas): Camadas `App.Config`, `App.Utils`, `App.Audio`, `App.Notifications` e `App.DB` (28 métodos).
4. [`parts_js_service.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_service.py) (`JS_SERVICE` - 1.670 linhas): Camadas `App.Service`, `App.AlarmEngine` e `App.Backup` (47 métodos).
5. [`parts_js_ui.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_ui.py) (`JS_UI` - 3.753 linhas): Camada `App.UI` (82 métodos) e listener de inicialização `DOMContentLoaded`.

### 3.2 Arquitetura em Camadas no Namespace `window.App`
Toda a lógica JavaScript é encapsulada no objeto global `window.App`, dividida em 9 módulos bem definidos (**157 métodos no total**):

| Camada / Módulo | Arquivo Fonte | Responsabilidade Técnica |
| :--- | :--- | :--- |
| [`App.Config`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_core.py#L8-L47) | `parts_js_core.py` | Define constantes do banco (`DB_NAME: 'LivroPrevisoesDutosDB'`, `DB_VERSION: 1`), lista inicial de consoles (`INITIAL_CONSOLES`), faixas de cores padrão (`DEFAULT_COLOR_RANGES`) e configurações padrão (`DEFAULT_SETTINGS`, incluindo `theme: 'dark'`, `viewMode: 'cards'`, `responsiveLayoutMode: 'auto'`, `backupReminderDays: 7`, `firstMobileNoticeShown: false`). |
| [`App.Utils`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_core.py#L52-L183) | `parts_js_core.py` | Geração de UUID v4 (`uuid`), normalização de strings (`cleanStr`), sanitização contra XSS (`escapeHTML`), formatação de datas/horas brasileiras (`formatDate`, `formatTime`, `formatDateTime`), cálculo textual de duração e contagem regressiva (`formatDuration`, `formatTimeRemaining`, `formatDiffMinutes`) e escape de valores CSV (`escapeCSV`). |
| [`App.Audio`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_core.py#L188-L333) | `parts_js_core.py` | Gerencia a instância de `AudioContext`, desbloqueio por gesto do usuário (`unlock`), atualização simultânea da pílula `#pillAudio`, do chip `#chipHeaderAudioWarning` e do modal `#statusModalAudio`, e síntese sonora de 4 timbres (`play`). |
| [`App.Notifications`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_core.py#L338-L423) | `parts_js_core.py` | Wrapper para a `Web Notifications API`: verifica suporte (`isSupported`), consulta estado (`getPermissionState`), atualiza `#pillNotif` e `#statusModalNotif`, solicita permissão (`requestPermission`) e envia notificações nativas (`send`). |
| [`App.DB`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_core.py#L428-L663) | `parts_js_core.py` | Camada de persistência assíncrona baseada em `Promises` sobre o `IndexedDB`. Cria as 11 *Object Stores* e seus índices em `onupgradeneeded`, semeia dados iniciais (`initDefaults`), executa operações CRUD (`insert`, `get`, `getAll`, `update`, `delete`, `clear`) e grava erros em `errorLogs` (`logError`). |
| [`App.Service`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_service.py#L6-L1245) | `parts_js_service.py` | Regras de negócio, validações de unicidade, regra de $\ge 2$ UOs por duto, regra de exclusividade global de TAG por UO, verificação de dependências para exclusão, gestão de eventos (criar, editar, concluir, reabrir, duplicar, adiar, reconhecer), validação de faixas de cores, classificação de eventos (`normalizeRangeKey`, `getRangeIcon`, `classifyEvent`), carga de dados de demonstração (`loadDemoData`) e limpeza geral (`clearAllData`). |
| [`App.AlarmEngine`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_service.py#L1250-L1416) | `parts_js_service.py` | Motor de monitoramento em tempo real com loop de 1 segundo (`setInterval`), atualização do relógio oficial (`#liveClock`), atualização dos contadores regressivos visíveis e avaliação/disparo de alarmes (`tick`, `fireAlarm`). |
| [`App.Backup`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_service.py#L1421-L1669) | `parts_js_service.py` | Exportação e validação de backup JSON completo (`validateBackupFile` e `validateBackupData`), importação nos modos `replace` (com backup preventivo automático) e `merge`, e geração de relatórios CSV compatíveis com Excel (`pendente`/`pending`, `concluido`/`completed`, `todos`/`all`, `cadastros`). |
| [`App.UI`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_ui.py#L6-L3737) | `parts_js_ui.py` | Controlador da interface gráfica: gerencia os 3 temas visuais (`applyTheme`, `cycleTheme`), os 7 modos responsivos (`getEffectiveViewportTier`, `applyResponsiveLayoutMode`, `checkViewModeUsabilityWarning`, `handleViewportResize`), cabeçalho e banners persistentes, menu drawer mobile e bottom nav, lousa stylus com undo e tela cheia, comboboxes em cascata, filtros e bottom sheet mobile, painel master-detail com 3 abas (`selectPendingDetailEvent`, `renderPendingDetailPane`), categorias de cadastros (`switchCadastrosCategory`), renderização das 9 telas e controle dos 10 modais (`openAppStatusModal`, `openEventActionSheet`, etc.) e toasts. |

### 3.3 Esquema Completo do Banco de Dados Local IndexedDB (`LivroPrevisoesDutosDB` - 11 Object Stores)
O banco de dados IndexedDB é aberto na versão `1` (`App.Config.DB_VERSION = 1`) e possui **11 Object Stores**:

| # | Nome da Object Store | `keyPath` | Índices Criados (`createIndex`) | Todos os Campos Armazenados no Objeto |
| :-: | :--- | :--- | :--- | :--- |
| **1** | `consoles` | `id` | `name` (unique: false)<br>`active` (unique: false) | `id` (UUID), `name` (String, ex: `'C04'`), `active` (Boolean), `createdAt` (ISO), `updatedAt` (ISO), `version` (Number), `synchronizationStatus` (`'local-only'`) |
| **2** | `pipelines` | `id` | `consoleId` (unique: false)<br>`name` (unique: false)<br>`active` (unique: false) | `id` (UUID), `name` (String, ex: `'OSCAN'`), `consoleId` (UUID FK $\rightarrow$ `consoles.id`), `active` (Boolean), `createdAt` (ISO), `updatedAt` (ISO), `version` (Number), `synchronizationStatus` (`'local-only'`) |
| **3** | `operationalUnits` | `id` | `name` (unique: false)<br>`active` (unique: false) | `id` (UUID), `name` (String, ex: `'REFAP'`), `active` (Boolean), `createdAt` (ISO), `updatedAt` (ISO), `version` (Number), `synchronizationStatus` (`'local-only'`) |
| **4** | `pipelineOperationalUnits` | `id` | `pipelineId` (unique: false)<br>`uoId` (unique: false) | `id` (UUID), `pipelineId` (UUID FK $\rightarrow$ `pipelines.id`), `uoId` (UUID FK $\rightarrow$ `operationalUnits.id`), `createdAt` (ISO), `version` (Number), `synchronizationStatus` (`'local-only'`) |
| **5** | `equipmentTypes` | `id` | `uoId` (unique: false)<br>`name` (unique: false)<br>`active` (unique: false) | `id` (UUID), `name` (String, ex: `'Tanque'`), `uoId` (UUID FK $\rightarrow$ `operationalUnits.id`), `active` (Boolean), `createdAt` (ISO), `updatedAt` (ISO), `version` (Number), `synchronizationStatus` (`'local-only'`) |
| **6** | `equipmentTags` | `id` | `uoId` (unique: false)<br>`equipmentTypeId` (unique: false)<br>`tag` (unique: false)<br>`active` (unique: false) | `id` (UUID), `tag` (String, ex: `'TQ-804'`), `uoId` (UUID FK $\rightarrow$ `operationalUnits.id`), `equipmentTypeId` (UUID FK $\rightarrow$ `equipmentTypes.id`), `active` (Boolean), `createdAt` (ISO), `updatedAt` (ISO), `version` (Number), `synchronizationStatus` (`'local-only'`) |
| **7** | `events` | `id` | `status` (unique: false)<br>`scheduledAt` (unique: false)<br>`consoleId` (unique: false)<br>`pipelineId` (unique: false)<br>`uoId` (unique: false)<br>`active` (unique: false) | `id` (UUID), `consoleId` (UUID), `pipelineId` (UUID), `uoId` (UUID), `equipmentTypeId` (UUID\|null), `tagId` (UUID\|null), `scheduledDate` (`'YYYY-MM-DD'`), `scheduledTime` (`'HH:mm'`), `scheduledAt` (ISO), `description` (String), `notes` (String), `stylusDrawing` (DataURL PNG\|null), `priority` (`'Baixa'`\|`'Normal'`\|`'Alta'`\|`'Crítica'`), `status` (`'pendente'`\|`'concluido'`), `hasAlarm` (Boolean), `useDefaultAlarmSettings` (Boolean), `alarmMinutesBefore` (Number), `alarmAudio` (Boolean), `alarmVisual` (Boolean), `alarmNotification` (Boolean), `alarmRepeat` (Boolean), `alarmRepeatInterval` (Number), `alarmMaxRepeats` (Number), `alarmState` (`'idle'`\|`'triggered'`\|`'snoozed'`\|`'acknowledged'`), `alarmSnoozedUntil` (Timestamp ms\|null), `alarmTriggerCount` (Number), `lastAlarmTriggeredAt` (ISO\|null), `completedAt` (ISO\|null), `completedTimeDiffMinutes` (Number\|null), `completionNote` (String), `active` (Boolean), `createdAt` (ISO), `updatedAt` (ISO), `version` (Number), `synchronizationStatus` (`'local-only'`) |
| **8** | `eventHistory` | `id` | `eventId` (unique: false)<br>`timestamp` (unique: false) | `id` (UUID), `eventId` (UUID FK $\rightarrow$ `events.id`), `action` (`'criacao'`\|`'edicao'`\|`'conclusao'`\|`'reabertura'`\|`'adiamento'`\|`'reconhecimento'`\|`'disparo_alarme'`), `timestamp` (ISO), `description` (String), `previousValue` (String\|null), `newValue` (String\|null), `localUser` (String) |
| **9** | `colorRanges` | `id` | `minMinutes` (unique: false)<br>`priority` (unique: false) | `id` (String/UUID), `name` (String), `color` (Hex String), `minMinutes` (Number), `maxMinutes` (Number), `unit` (`'min'`), `priority` (Number), `blink` (Boolean), `sound` (Boolean), `active` (Boolean) |
| **10** | `settings` | `key` | *(Sem índices secundários)* | `key` (`'app_settings'`), `value` (Objeto contendo: `localUserName`, `soundEnabled`, `soundType`, `soundVolume`, `visualAlertEnabled`, `highlightCardEnabled`, `pulsingEnabled`, `changeTitleEnabled`, `notificationEnabled`, `repeatAlarm`, `repeatIntervalMinutes`, `maxRepeats`, `defaultLeadTimeMinutes`, `theme` (`'dark'`\|`'light'`\|`'industrial'`), `viewMode` (`'cards'`\|`'table'`), `responsiveLayoutMode` (`'auto'`\|`'compact'`\|`'mobile'`\|`'tablet'`\|`'conventional'`\|`'widescreen'`\|`'ultrawide'`), `backupReminderDays` (`7`), `firstMobileNoticeShown` (Boolean), `lastBackupAt`, `activeConsoleId`, `keepDutoUOPrefilled`) |
| **11** | `errorLogs` | `id` | `timestamp` (unique: false) | `id` (UUID), `timestamp` (ISO), `context` (String), `message` (String), `details` (String/Stack) |

### 3.4 Funcionamento do Motor de Monitoramento (`App.AlarmEngine`) e Ciclo de 1 Segundo
Ao iniciar a aplicação (`App.UI.init()`), `App.AlarmEngine.start()` registra um `setInterval(() => this.tick(), 1000)` que executa três tarefas a cada 1 segundo:
1. **Relógio Oficial (`#liveClock`)**: Formata a hora atual do sistema no padrão `DD/MM/AAAA HH:mm:ss` e atualiza o display no cabeçalho.
2. **Contadores Regressivos em Tempo Real (`App.UI.updateLiveTimers()`)**: Percorre todos os elementos DOM `.event-countdown[data-timestamp]` visíveis nos cartões, na tabela ou no painel Master-Detail (`#pendingDetailPane`), além do timer do card Spotlight (`#spotlightTimeLeft`), recalculando a diferença em segundos (`App.Utils.formatTimeRemaining`) para exibir dinamicamente `"Faltam X minutos"` ou `"Atrasado há X segundos"` sem precisar recarregar toda a tabela.
3. **Avaliação de Disparo de Alarmes**:
   - Busca os eventos com `status === 'pendente'` e `hasAlarm === true`.
   - Calcula o instante alvo do alarme: $\text{alarmTargetTime} = \text{scheduledTime} - (\text{leadMins} \times 60000)$.
   - Ignora se estiver em período de adiamento ativo (`nowTime < ev.alarmSnoozedUntil`) ou se já tiver sido reconhecido (`ev.alarmState === 'acknowledged'`).
   - Quando `nowTime >= alarmTargetTime`, verifica três gatilhos:
     - `isFirstTrigger`: `ev.alarmState === 'idle'` ou `!ev.lastAlarmTriggeredAt`
     - `isSnoozeExpired`: `ev.alarmSnoozedUntil && nowTime >= ev.alarmSnoozedUntil`
     - `isRepeatTime`: `repeatEnabled && (repeatsCount < maxRepeats) && (nowTime - lastTriggered >= repeatInterval * 60000)`
   - Se qualquer gatilho for verdadeiro, invoca `this.fireAlarm(ev, settings, colorRanges, isRepeatTime)`, que atualiza o evento no IndexedDB (`alarmState = 'triggered'`, incrementa `alarmTriggerCount`), aciona o som (`App.Audio.play`), abre o modal (`App.UI.showAlarmModal`), envia a notificação do navegador (`App.Notifications.send`), grava na auditoria (`disparo_alarme`), atualiza o título da aba e sincroniza os indicadores de alarme no cabeçalho (`#btnHeaderAlarmBell` / `#headerAlarmBadge`), no banner persistente (`#mobileActiveAlarmsBanner`) e no painel lateral (`#tabletActiveAlarmsPanel`).

### 3.5 Sintetizador Sonoro Local (`App.Audio` - Web Audio API)
Para garantir funcionamento 100% offline sem depender de arquivos `.mp3` ou `.wav` externos, [`App.Audio.play(type, volumePercent)`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_core.py#L250-L332) sintetiza ondas sonoras diretamente no navegador:
- **Teto de Ganho Seguro**: `masterVol = Math.max(0, Math.min(100, volumePercent)) / 100 * 0.3`.
- **4 Timbres Disponíveis**:
  1. **`chime` (Chime Harmônico - Padrão)**: Acorde arpejado de 3 notas senoidais (`sine`) correspondentes a Dó5 (`523.25 Hz`), Mi5 (`659.25 Hz`) e Sol5 (`783.99 Hz`), defasadas em `0.15s` com rampa exponencial suave de `0.45s`.
  2. **`beep` (Beep Duplo Clássico)**: Dois pulsos de onda quadrada (`square`) em Lá5 (`880 Hz`), separados por `0.18s` e duração de `0.14s` cada.
  3. **`siren` (Sirene Operacional de Urgência)**: Oscilador dente-de-serra (`sawtooth`) modulando linearmente a frequência entre `650 Hz` e `950 Hz` em quatro rampas de `0.25s` (duração total `1.1s`).
  4. **`blip` (Blip Suave)**: Pulso único senoidal (`sine`) em Dó6 (`1046.5 Hz`) de `0.16s`.
- **Desbloqueio Automático de Áudio (`AudioContext Autoplay Policy`)**: `App.UI.bindGlobalEvents` registra listeners `{ once: true }` de `click` e `keydown` em `window` (além de clique direto em `#pillAudio` ou `#chipHeaderAudioWarning`) para destravar o `AudioContext` na primeira interação do controlador, ocultando o chip de aviso `#chipHeaderAudioWarning` (`⚠ Áudio não iniciado`) e mudando `#pillAudio` e `#statusModalAudio` de amarelo (`Áudio: Iniciar`) para verde (`Áudio: Ativo`).

### 3.6 Sistema de 3 Temas Visuais, 7 Modos Responsivos e Adaptação Multi-Dispositivo

#### A. Os 3 Temas Visuais Operacionais (`App.UI.applyTheme` / `cycleTheme`)
A aplicação oferece **3 temas visuais completos** projetados especificamente para diferentes condições de iluminação e tipos de monitores em salas de controle e campo, persistidos em `settings.theme` e sincronizados entre o botão de ciclo rápido no cabeçalho (`#btnToggleTheme`), o botão do drawer mobile (`#btnDrawerTheme` / `#labelDrawerTheme`) e o seletor na Aba 6 (`#selectSettingsTheme`):
1. **Tema 1: Controle Escuro (`dark` - Padrão `:root`)**:
   - **Classe no `<body>`**: *(Nenhuma classe extra; utiliza os tokens padrão de `:root`)*.
   - **Paleta e Finalidade**: Fundo azul-noturno profundo (`#0b1120`) e superfície ardósia escuro (`#1e293b`), projetado para salas de controle com iluminação reduzida e operação 24h, minimizando a fadiga ocular durante plantões prolongados.
2. **Tema 2: Claro Operacional / Profissional Claro (`light`)**:
   - **Classe no `<body>`**: `body.theme-light`.
   - **Paleta e Finalidade**: Fundo claro (`#f1f5f9`), superfície branca (`#ffffff`) e texto escuro de alto contraste (`#0f172a`), ideal para ambientes de escritório, salas intensamente iluminadas ou uso diurno em tablets e smartphones.
3. **Tema 3: Industrial Alto Contraste (`industrial`)**:
   - **Classe no `<body>`**: `body.theme-industrial`.
   - **Paleta e Finalidade**: Fundo preto absoluto (`#000000`), superfície grafite escuro (`#0a0a0a`), texto branco puro (`#ffffff`), bordas reforçadas (`#525252`) e destaque primário em amarelo ouro de alta visibilidade (`#eab308` com texto preto `#000000` em `.btn-primary` e `.mobile-fab`). Projetado para painéis industriais de máxima legibilidade, uso em campo sob luz intensa e monitores distantes (video walls).

#### B. Os 7 Modos de Visualização Responsiva (`App.UI.getEffectiveViewportTier` / `applyResponsiveLayoutMode` / `handleViewportResize`)
A arquitetura responsiva universal permite operar tanto em detecção automática quanto forçar manualmente qualquer um dos **7 modos de visualização** através dos seletores sincronizados no cabeçalho (`#selectHeaderViewMode`), no drawer mobile (`#selectDrawerViewMode`) e nas Configurações (`#selectSettingsViewMode`), persistindo a escolha em `settings.responsiveLayoutMode`:

| Valor (`responsiveLayoutMode`) | Rótulo na Interface (`#selectHeaderViewMode` / `#selectSettingsViewMode`) | Atributo / Classe Aplicada ao `<body>` | Faixa de Largura (em `getEffectiveViewportTier`) | Comportamentos Estruturais e Adaptações de UI |
| :--- | :--- | :--- | :--- | :--- |
| **`auto`** | `Automática` / `Automático (Recomendado - Detecta a tela)` | Dinâmico conforme `window.innerWidth` (`handleViewportResize`) | Detecta em tempo real via listener `resize` | Calcula automaticamente o tier efetivo (`mobile`, `tablet`, `conventional`, `widescreen` ou `ultrawide`) conforme a largura da janela. |
| **`compact`** | `Compacta` / `Compacto (Alta Densidade Operacional)` | `body.density-compact` + `body[data-layout-mode="<tier>"]` | Combina alta densidade com o tier da tela atual | Modo de alta densidade operacional: reduz espaçamentos internos (`.card`, `.metric-card`, `.event-card`, `.data-table th/td`) e oculta `.form-help` para exibir mais previsões simultaneamente na tela sem rolagem. |
| **`mobile`** | `Celular` / `Celular (320px a 767px)` | `body[data-layout-mode="mobile"]` | `< 768px` (com ajuste `1fr` em `<= 359px`) | Layout otimizado para operação vertical em smartphones: oculta `.app-nav` desktop e pílulas secundárias do cabeçalho (acessíveis via `#btnHeaderAppStatus` $\rightarrow$ `#modalAppStatus`), exibe `#mobileBottomNav` fixa inferior, reordena o Dashboard (`Spotlight` $\rightarrow$ `Urgentes em Cards` `#dashboardUrgentCards` $\rightarrow$ `Métricas 2x4`), transforma `#filterDrawer` em Bottom Sheet (`.active-sheet`), converte tabelas de Concluídos e Cores em cartões (`#containerCompletedCards`, `#containerColorRangeCards`), exibe `#cadastrosCategoryBar` em lista vertical e abre `#modalAlarmTrigger`/`#modalEventDetails` em tela cheia (`100dvh`) e `#modalSnooze`/`#modalEventActionSheet` como Bottom Sheet. |
| **`tablet`** | `Tablet` / `Tablet (768px a 1199px)` | `body[data-layout-mode="tablet"]` | `768px – 1199px` | Ergonomia dedicada para tablets e telas touch (`min-height: 44px/46px`): divide o topo do Dashboard em `1.75fr 1fr` exibindo o painel lateral `#tabletActiveAlarmsPanel` ao lado do `#spotlightCard`, ativa a visão dividida **Master-Detail** (`1.15fr 1fr`) em Eventos Pendentes com `#pendingDetailPane` (3 abas: `Detalhes`, `Anotações`, `Histórico`), exibe `#cadastrosCategoryBar` para navegação drill-down sem espaço morto e amplia `#stylusDrawingCanvas` (`min-height: 280px`). |
| **`conventional`** | `Monitor Convencional` / `Tela Convencional (1200px a 1599px)` | `body[data-layout-mode="conventional"]` | `1200px – 1599px` | Layout padrão de estação de trabalho desktop: barra horizontal completa de 9 abas (`<nav class="app-nav">`), barra de pílulas de status completa no cabeçalho, Hub Unificado de Cadastros em 3 colunas simultâneas (`switchCadastrosCategory('all')`) e alternância livre entre Cartões e Tabela Compacta. |
| **`widescreen`** | `Widescreen` / `Widescreen (1600px a 2199px)` | `body[data-layout-mode="widescreen"]` | `1600px – 2199px` | Layout expandido para monitores Full HD / Quad HD de sala de controle (`max-width: 2100px`): exibe simultaneamente o `#spotlightCard` e o painel lateral `#tabletActiveAlarmsPanel` (`2fr 1fr`) no Dashboard, mantém os filtros avançados `#filterDrawer` abertos em grid permanente e exibe o Hub de Cadastros em 3 colunas amplas. |
| **`ultrawide`** | `Ultrawide` / `Ultrawide / Videowall (2200px+)` | `body[data-layout-mode="ultrawide"]` | `>= 2200px` | Layout panorâmico para monitores Ultrawide (21:9 / 32:9) e Video Walls de sala de controle (`max-width: 100%`): combina o painel lateral `#tabletActiveAlarmsPanel` no Dashboard (`2fr 1fr`), filtros `#filterDrawer` sempre visíveis e visão dividida **Master-Detail** permanente (`1.6fr 1fr`) em Eventos Pendentes com `#pendingDetailPane` aberto ao lado do grid de cartões. |

- **Proteção contra Modo Manual Incompatível (`App.UI.checkViewModeUsabilityWarning` / `#viewModeWarningBanner`)**: Caso o controlador force manualmente um modo incompatível com a largura física da tela (ex.: modos desktop `conventional`/`widescreen`/`ultrawide` em tela `< 768px`, `ultrawide` em tela `< 1200px`, ou `mobile` em monitor `>= 1600px`), o sistema exibe automaticamente o banner `#viewModeWarningBanner` com a mensagem explicativa em `#bannerViewModeText` e o botão `#btnBannerResetAuto` (`Voltar para Automático`) para restaurar `applyResponsiveLayoutMode('auto', true)` em 1 clique.

### 3.7 Catálogo de Variáveis CSS (Tokens dos 3 Temas: Controle Escuro, Claro Operacional e Industrial Alto Contraste)
Definidas em [`parts_css.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_css.py#L3-L162), as Custom Properties governam a identidade visual nos três temas:

| Variável CSS | Tema 1: Controle Escuro (`:root`) | Tema 2: Claro Operacional (`body.theme-light`) | Tema 3: Industrial Alto Contraste (`body.theme-industrial`) | Finalidade Visual |
| :--- | :--- | :--- | :--- | :--- |
| `--bg-app` | `#0b1120` | `#f1f5f9` | `#000000` | Cor de fundo geral da página e inputs |
| `--bg-surface` | `#1e293b` | `#ffffff` | `#0a0a0a` | Superfície de cartões, cabeçalho, barra de abas e tabelas |
| `--bg-surface-hover` | `#283548` | `#f8fafc` | `#171717` | Estado hover em abas, linhas de tabelas e botões |
| `--bg-surface-active` | `#334155` | `#e2e8f0` | `#262626` | Superfície ativa, cabeçalhos `<th>` e pílulas de status |
| `--bg-elevated` / `--bg-surface-elevated` | `#1e293b` | `#ffffff` | `#0f0f0f` | Fundo de caixas modais (`.modal-box`), drawer e toasts |
| `--border-color` | `#334155` | `#cbd5e1` | `#525252` | Bordas de cartões, tabelas, inputs e divisórias |
| `--border-color-focus` | `#38bdf8` | `#0284c7` | `#facc15` | Contorno de foco de acessibilidade em inputs e botões |
| `--text-main` | `#f8fafc` | `#0f172a` | `#ffffff` | Texto primário de alta legibilidade |
| `--text-secondary` | `#94a3b8` | `#475569` | `#e5e5e5` | Rótulos (`label`), subtítulos e notas secundárias |
| `--text-muted` | `#64748b` | `#94a3b8` | `#a3a3a3` | Textos auxiliares (`.form-help`) e estados vazios |
| `--color-primary` / `--color-primary-hover` | `#0284c7` / `#0369a1` | `#0284c7` / `#0369a1` | `#eab308` / `#ca8a04` | Destaque operacional principal (botões primários e abas ativas) |
| `--color-success` / `--color-success-hover` | `#16a34a` / `#15803d` | *(Herda `:root`)* | `#16a34a` / *(Herda `:root`)* | Verde de conclusão e confirmação |
| `--color-warning` | `#d97706` | *(Herda `:root`)* | `#f59e0b` | Laranja/âmbar de alerta, reconhecimento e inativação |
| `--color-danger` / `--color-danger-hover` | `#dc2626` / `#b91c1c` | *(Herda `:root`)* | `#ef4444` / *(Herda `:root`)* | Vermelho de exclusão, erro e alarme crítico |
| `--color-info` | `#2563eb` | *(Herda `:root`)* | *(Herda `:root`)* | Azul informativo para toasts |
| `--status-overdue-bg` / `border` / `text` | `#450a0a` / `#991b1b` / `#fecaca` | `#fee2e2` / `#b91c1c` / `#991b1b` | `#7f1d1d` / `#ff4d4d` / `#ffffff` | Paleta da condição **Atrasado** |
| `--status-critico-bg` / `border` / `text` | `#7f1d1d` / `#dc2626` / `#fee2e2` | `#fef2f2` / `#dc2626` / `#991b1b` | `#991b1b` / `#ff6666` / `#ffffff` | Paleta da faixa **Crítico** |
| `--status-urgente-bg` / `border` / `text` | `#7c2d12` / `#ea580c` / `#ffedd5` | `#fff7ed` / `#ea580c` / `#c2410c` | `#9a3412` / `#fb923c` / `#ffffff` | Paleta da faixa **Urgente** |
| `--status-atencao-bg` / `border` / `text` | `#713f12` / `#ca8a04` / `#fef08a` | `#fefce8` / `#ca8a04` / `#854d0e` | `#854d0e` / `#facc15` / `#ffffff` | Paleta da faixa **Atenção** |
| `--status-monitor-bg` / `border` / `text` | `#1e3a8a` / `#2563eb` / `#dbeafe` | `#eff6ff` / `#2563eb` / `#1d4ed8` | `#1e40af` / `#60a5fa` / `#ffffff` | Paleta da faixa **Monitoramento** |
| `--status-normal-bg` / `border` / `text` | `#14532d` / `#16a34a` / `#dcfce7` | `#f0fdf4` / `#16a34a` / `#15803d` | `#166534` / `#4ade80` / `#ffffff` | Paleta da faixa **Normal** |
| `--status-concluido-bg` / `border` / `text` | `#064e3b` / `#059669` / `#d1fae5` | `#ecfdf5` / `#059669` / `#065f46` | *(Herda `:root`)* | Paleta do estado **Concluído** |

### 3.8 Catálogo Exaustivo de Todos os Métodos JavaScript por Camada
Abaixo estão listados todos os **157 métodos** implementados nas 8 camadas funcionais JavaScript da aplicação (`parts_js_core.py`: 28; `parts_js_service.py`: 47; `parts_js_ui.py`: 82):

#### A. `App.Utils` — 10 métodos ([`parts_js_core.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_core.py#L52-L183))
- `uuid()`: Gera identificador único universal UUID v4 (`crypto.randomUUID()` ou fallback hexadecimal).
- `cleanStr(str)`: Converte para string, remove espaços nas extremidades (`trim`) e converte para minúsculas (`toLowerCase`).
- `escapeHTML(str)`: Sanitiza `&`, `<`, `>`, `"`, `'` para evitar injeção de HTML/XSS.
- `formatDate(dateStr)`: Formata `'YYYY-MM-DD'` ou ISO para `'DD/MM/AAAA'`.
- `formatTime(timeStr)`: Formata `'HH:mm'` ou objeto `Date`/ISO para `'HH:mm'`.
- `formatDateTime(isoOrDateStr, timeStr)`: Combina data e hora em `'DD/MM/AAAA HH:mm'`.
- `formatDuration(totalSeconds)`: Converte segundos em texto descritivo em português (`"X horas e Y minutos"`, `"X minutos"` ou `"X segundos"`).
- `formatTimeRemaining(targetTimestamp)`: Calcula a diferença entre `targetTimestamp` e `Date.now()`, retornando `{ text, diffSec, isOverdue }` (`"Faltam ..."` ou `"Atrasado há ..."`).
- `formatDiffMinutes(diffMinutes)`: Formata a diferença de conclusão (`"Com atraso de X min"`, `"Com antecedência de X min"` ou `"Exatamente no horário"`).
- `escapeCSV(value)`: Escapa valores contendo `;`, `"` ou quebras de linha para exportação CSV compatível com Excel.

#### B. `App.Audio` — 4 métodos ([`parts_js_core.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_core.py#L188-L333))
- `init()`: Instancia `AudioContext` (`window.AudioContext || window.webkitAudioContext`) e atualiza `#pillAudio`, `#chipHeaderAudioWarning` e `#statusModalAudio`.
- `unlock()`: Executa `ctx.resume()` para desbloquear o áudio após interação do usuário e atualiza os indicadores de status.
- `updateStatusPill()`: Atualiza classe (`ok` vs `warning`), texto (`Áudio: Ativo` vs `Áudio: Iniciar`), visibilidade do chip `#chipHeaderAudioWarning` e texto de `#statusModalAudio`.
- `play(type, volumePercent)`: Sintetiza via osciladores Web Audio API os timbres `'chime'`, `'beep'`, `'siren'` ou `'blip'`.

#### C. `App.Notifications` — 5 métodos ([`parts_js_core.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_core.py#L338-L423))
- `isSupported()`: Verifica se `'Notification' in window`.
- `getPermissionState()`: Retorna `'indisponivel'`, `'concedida'`, `'negada'` ou `'nao_solicitada'`.
- `updateStatusPill()`: Atualiza simultaneamente `#pillNotif` e `#statusModalNotif` conforme o estado da permissão.
- `requestPermission()`: Solicita `Notification.requestPermission()`, atualiza `#pillNotif` e `#statusModalNotif` e retorna booleano.
- `send(title, options)`: Cria `new Notification(title, { requireInteraction: true, ... })` com handler `onclick` que foca a janela (`window.focus()`).

#### D. `App.DB` — 9 métodos ([`parts_js_core.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_core.py#L428-L663))
- `open()`: Abre o banco IndexedDB `LivroPrevisoesDutosDB` (v1) e cria as 11 Object Stores e seus índices em `onupgradeneeded`.
- `initDefaults()`: Semeia os 12 consoles iniciais (`C02`–`C16`), as 5 faixas de cores padrão e o registro `app_settings` (com `C04` como console ativo inicial).
- `insert(storeName, item)`: Executa `store.add(item)` em transação `readwrite`.
- `get(storeName, key)`: Busca um registro pela chave primária (`store.get(key)`).
- `getAll(storeName)`: Retorna todos os registros de uma Object Store (`store.getAll()`).
- `update(storeName, item)`: Executa `store.put(item)` em transação `readwrite`.
- `delete(storeName, key)`: Remove fisicamente um registro pela chave (`store.delete(key)`).
- `clear(storeName)`: Remove todos os registros de uma Object Store (`store.clear()`).
- `logError(error, context)`: Grava um registro de falha técnica na store `errorLogs`.

#### E. `App.Service` — 37 métodos ([`parts_js_service.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_service.py#L6-L1245))
- `getSettings()` / `saveSettings(newSettings)`: Lê e grava o objeto `app_settings` na store `settings`.
- `saveConsole(data)` / `deleteConsole(id)` / `toggleConsoleActive(id)`: CRUD e ativação/inativação de Consoles com validação de unicidade e checagem de dependências (dutos e eventos).
- `savePipeline(data)` / `deletePipeline(id)` / `togglePipelineActive(id)`: CRUD de Dutos com validação de mínimo de 2 UOs, sincronização da tabela associativa `pipelineOperationalUnits` e bloqueio de exclusão se houver eventos.
- `saveUO(data)` / `saveUOBatch(namesString)` / `deleteUO(id)` / `toggleUOActive(id)`: CRUD individual e em lote de UOs (separadas por vírgula, ponto e vírgula ou quebra de linha), reativação automática de UOs inativas no lote e verificação de dependências (dutos, tipos, TAGs e eventos).
- `saveEquipmentType(data)` / `deleteEquipmentType(id)` / `toggleEquipmentTypeActive(id)`: CRUD de Tipos de Equipamento por UO com verificação de dependências (TAGs e eventos).
- `saveEquipmentTag(data)` / `deleteEquipmentTag(id)` / `toggleEquipmentTagActive(id)`: CRUD de TAGs com validação da regra global de exclusividade de TAG por UO em todo o sistema e verificação de dependências (eventos).
- `saveEvent(data)`: Cria ou edita uma previsão operacional, monta `scheduledAt`, reseta o alarme se o horário mudar e grava auditoria (`criacao` ou `edicao`).
- `completeEvent(id, completionNote)`: Conclui um evento, calcula `completedTimeDiffMinutes`, silencia o alarme e grava auditoria (`conclusao`).
- `reopenEvent(id, newDate, newTime)`: Reabre um evento concluído, preserva os dados da conclusão anterior no histórico (`reabertura`) e reprograma o horário se informado.
- `getCloneDataForEvent(id)`: Gera objeto clonado de um evento com horário sugerido para `agora + 30 min`.
- `deleteEvent(id)`: Exclui fisicamente um evento e remove seus registros em `eventHistory`.
- `snoozeAlarm(eventId, minutes)`: Adia um alarme por $N$ minutos (`alarmState = 'snoozed'`, `alarmSnoozedUntil`) e grava auditoria (`adiamento`).
- `acknowledgeAlarm(eventId)`: Reconhece um alarme (`alarmState = 'acknowledged'`) e grava auditoria (`reconhecimento`).
- `logEventHistory(record)`: Insere um registro de rastreabilidade na store `eventHistory`.
- `getColorRanges()` / `validateColorRanges(ranges)` / `saveColorRange(data)` / `deleteColorRange(id)` / `resetColorRanges()`: Gestão completa e validação matemática de contiguidade (sem lacunas e sem sobreposições) das faixas de tempo/cor.
- `normalizeRangeKey(rawId, name)` / `getRangeIcon(normKey)` / `classifyEvent(event, colorRanges)` / `hexToRgb(hex)`: Classifica dinamicamente um evento em `Atrasado` ($\text{diffMs} < 0$) ou na faixa de tempo futuro correspondente, normalizando `key` (`normKey`) e o ícone semântico para coincidir exatamente com as classes CSS `.status-badge.*`.
- `loadDemoData()` / `clearAllData()`: Popula massa de demonstração realista ou limpa todas as coleções reinicializando os padrões.

#### F. `App.AlarmEngine` — 4 métodos ([`parts_js_service.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_service.py#L1250-L1416))
- `start()` / `stop()`: Inicia ou interrompe o timer de 1 segundo (`setInterval`).
- `tick()`: Ciclo de 1 segundo que atualiza `#liveClock`, chama `App.UI.updateLiveTimers()`, avalia todos os eventos pendentes com alarme e alterna `document.title` quando há alarme ativo.
- `fireAlarm(event, settings, colorRanges, isRepeat)`: Executa o disparo do alarme (atualiza estado/contador no banco, toca áudio sintetizado, exibe `#modalAlarmTrigger`, envia Web Notification, grava auditoria `disparo_alarme` e re-renderiza Painel e Pendentes).

#### G. `App.Backup` — 6 métodos ([`parts_js_service.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_service.py#L1421-L1669))
- `exportJSON()`: Exporta as 10 stores de dados em arquivo `.json` e atualiza `settings.lastBackupAt`.
- `validateBackupFile(file)` / `validateBackupData(jsonString)`: Lê o objeto `File` (`file.text()`) e valida sintaxe JSON, versão do esquema (`1`) e coleções obrigatórias.
- `importJSON(backupObject, mode)`: Importa o backup em modo `'merge'` (mesclagem por ID e versão) ou `'replace'` (substituição total precedida de backup automático preventivo).
- `exportCSV(type)` / `downloadBlob(blob, fileName)`: Gera e baixa relatórios CSV UTF-8 com BOM (`'pendente'`/`'pending'`, `'concluido'`/`'completed'`, `'todos'`/`'all'` ou `'cadastros'`).

#### H. `App.UI` — 82 métodos ([`parts_js_ui.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_ui.py#L6-L3737))
- **Inicialização, Motor Responsivo, Temas e Cabeçalho (12)**: `init()`, `getEffectiveViewportTier(mode)`, `applyResponsiveLayoutMode(mode, persist)`, `checkViewModeUsabilityWarning()`, `handleViewportResize()`, `applyTheme(themeName)`, `cycleTheme()`, `updateBackupPill(lastBackupAt)`, `initHeaderConsole()`, `syncActiveConsoleUI()`, `initMobileDrawer()`, `openAppStatusModal()`.
- **Lousa Stylus (4)**: `initStylusPad()`, `clearStylusPad(resetHistory)`, `getStylusData()`, `loadStylusData(dataUrl)`.
- **Sincronização de Combos e Navegação (9)**: `refreshAllMasterDataDropdowns()`, `bindNavEvents()`, `navigateTo(viewId, callback)`, `initNewEventCombos()`, `loadConsoleOptions(...)`, `loadPipelineOptions(...)`, `loadUOOptions(...)`, `loadEquipmentTypeOptions(...)`, `loadEquipmentTagOptions(...)`.
- **Formulário e Operações de Evento (6)**: `bindFormEvents()`, `resetEventForm()`, `editEvent(eventId)`, `duplicateEvent(eventId)`, `acknowledgeAlarm(eventId)`, `deleteEvent(eventId)`.
- **Filtros, Master-Detail, Action Sheet e Renderização de Visões (17)**: `bindFilterEvents()`, `updateViewModeUI()`, `renderDashboard()`, `renderPendingEvents()`, `selectPendingDetailEvent(eventId, tab)`, `renderPendingDetailPane(eventId, tab)`, `openEventActionSheet(eventId)`, `updateLiveTimers()`, `populateFilterDropdowns(consoles, pipelines, uos)`, `renderCompletedEvents()`, `renderConfigAlerts()`, `renderConfigColors()`, `editRange(id)`, `resetRangeForm()`, `deleteRange(id)`, `renderDiagnostic()`, `getDiagnosticReport()`.
- **Cadastros Operacionais (23)**: `renderCadastros()`, `switchCadastrosCategory(category)`, `bindCadastrosForms()`, `renderConsolesTable()`, `renderPipelinesTable()`, `renderUOsTable()`, `renderEquipmentTypesTable()`, `renderEquipmentTagsTable()`, `editConsole(id)`, `toggleConsoleActive(id)`, `deleteConsole(id)`, `editPipeline(id)`, `togglePipelineActive(id)`, `deletePipeline(id)`, `editUO(id)`, `toggleUOActive(id)`, `deleteUO(id)`, `editEquipmentType(id)`, `toggleEquipmentTypeActive(id)`, `deleteEquipmentType(id)`, `editEquipmentTag(id)`, `toggleEquipmentTagActive(id)`, `deleteEquipmentTag(id)`.
- **Modais, Toasts e Eventos Globais (11)**: `bindModalEvents()`, `showAlarmModal(event, isTest)`, `showSnoozeModal(eventId)`, `showCompleteModal(eventId)`, `showReopenModal(eventId)`, `showDetailsModal(eventId)`, `showConfirmModal(title, message, onConfirm)`, `showDependencyModal(title, reasons, onInactivate)`, `showImportSummaryModal(parsedBackup)`, `showToast(message, type)`, `bindGlobalEvents()`.

---

## 4. Mapeamento Exaustivo de Todos os Componentes da Interface Gráfica (372 IDs HTML)

### 4.1 Cabeçalho Global (`<header class="app-header">`), Barra de Status e Banners Persistentes
Localizado no topo fixo da página (`position: sticky; top: 0; z-index: 100`), divide-se em três blocos no `<header>` (`header-left`, `header-status-bar`, `header-actions`) seguidos imediatamente por **3 banners operacionais persistentes** abaixo do cabeçalho:

| ID HTML / Seletor | Tipo de Elemento | Rótulo / Conteúdo Inicial | Função Exata na Aplicação |
| :--- | :--- | :--- | :--- |
| `#btnToggleMobileMenu` | `<button class="btn-hamburger">` | Ícone Hambúrguer (3 linhas) | Visível nos modos compact/mobile/tablet. Abre o menu de navegação retrátil lateral (`#appMobileDrawer`). |
| `.header-brand` | `<div>` | `Caderno de Previsões` / `Dutos • Sala de Controle` | Identidade visual da aplicação com ícone SVG de alarme industrial. |
| `#headerActiveConsole` | `<select class="header-console-select">` | `Console: C04` (populado dinamicamente) | **Seletor Global de Console Operacional Ativo**. Define qual console está ativo em toda a sessão, persistindo em `settings.activeConsoleId` e filtrando automaticamente o Painel, o formulário de Novo Evento e a lista de Eventos Pendentes. |
| `#liveClock` | `<div class="clock-display">` | `--:--:--` $\rightarrow$ `DD/MM/AAAA HH:mm:ss` | Relógio oficial da operação, atualizado a cada 1 segundo pelo `App.AlarmEngine.tick()`. |
| `#pillDB` | `<span class="status-pill ok">` | `• DB: Pronto` | Indicador de status de prontidão do banco de dados local IndexedDB. |
| `#pillAudio` | `<span class="status-pill warning">` | `• Áudio: Iniciar` / `• Áudio: Ativo` | Indicador e botão de ativação da `Web Audio API`. Ao clicar nele, desbloqueia o contexto de áudio, toca um acorde `chime` de confirmação e muda para verde (`ok`). |
| `#pillNotif` | `<span class="status-pill">` | `• Notif: Pendente` / `Solicitar` / `Ativa` / `Negada` / `Indisp.` | Indicador de permissão da `Web Notifications API`. Ao clicar nele, chama `App.Notifications.requestPermission()`. |
| `#btnHeaderTestNotif` | `<button class="status-pill warning">` | `Testar Notificação` | Botão de destaque no cabeçalho que desbloqueia o áudio, toca um `chime`, solicita permissão de notificação (se ainda não concedida) e dispara imediatamente uma notificação nativa de teste do navegador (`"Teste de Alerta Operacional"`). |
| `#pillBackup` | `<span class="status-pill">` | `• Backup: Nunca` / `• Backup: DD/MM/AAAA` | Exibe a data do último backup JSON exportado pelo controlador. |
| `#chipHeaderAudioWarning` | `<span class="status-pill warning">` | `⚠ Áudio não iniciado` | Chip de alerta compacto exibido no cabeçalho quando o `AudioContext` ainda aguarda gesto do controlador. Ao ser clicado, desbloqueia o áudio (`App.Audio.unlock()`), toca um `chime` de confirmação e se auto-oculta (`display: none`). |
| `#selectHeaderViewMode` | `<select class="header-viewmode-select">` | `Visualização: Automática` (7 opções) | Seletor rápido no cabeçalho para alternar entre os **7 modos responsivos** (`auto`, `compact`, `mobile`, `tablet`, `conventional`, `widescreen`, `ultrawide`), sincronizado com `#selectDrawerViewMode` e `#selectSettingsViewMode`. |
| `#btnHeaderAlarmBell` | `<button class="btn-header-bell">` | Ícone SVG Sino + `#headerAlarmBadge` | Botão de sino de alarmes ativos no cabeçalho (pulsa com `.ringing` quando há alarmes disparados não reconhecidos). Clicar nele navega para `#viewPendingEvents` filtrando os alarmes disparados (ou abre diretamente `#modalAlarmTrigger` se houver apenas 1). |
| `#headerAlarmBadge` | `<span class="bell-badge">` | `0` (`display: none` quando `0`) | Badge numérico dentro de `#btnHeaderAlarmBell` que exibe a contagem exata de alarmes disparados pendentes de reconhecimento. |
| `#btnHeaderAppStatus` | `<button class="btn btn-outline btn-icon">` | Ícone SVG `ℹ` | Botão compacto para smartphones/tablets que abre o Modal 10 (`#modalAppStatus` via `App.UI.openAppStatusModal()`) com o resumo completo de saúde do sistema (Áudio, Notificações, IndexedDB e Último Backup). |
| `#btnControllerBadge` | `<button class="btn btn-secondary btn-sm">` | Contém `#headerUserName` | Aciona o handler `promptUserChange` em `bindNavEvents()` para alterar rapidamente o nome do controlador responsável na estação de trabalho atual, salvando em `settings.localUserName`. |
| `#headerUserName` | `<span>` | `Usuário local` | Exibe o nome do controlador ativo dentro do botão `#btnControllerBadge`. |
| `#btnToggleTheme` | `<button class="btn btn-outline btn-icon">` | Contém `#themeIconSun` (SVG Sol) | Alterna ciclicamente (`App.UI.cycleTheme()`) entre os **3 temas visuais** (`Controle Escuro` $\rightarrow$ `Claro Operacional` $\rightarrow$ `Industrial Alto Contraste`), salvando a preferência. |
| `#themeIconSun` | `<svg>` | Ícone de Sol | Ícone vetorial interno do botão de alternância de tema `#btnToggleTheme`. |
| `#btnQuickAddEvent` | `<button class="btn btn-primary btn-sm">` | `+ Nova Previsão` | Limpa o formulário de evento (`resetEventForm()`) e navega imediatamente para a aba `#viewNewEvent`. |
| `#mobileActiveAlarmsBanner` | `<div class="persistent-banner alarm-banner" role="alert">` | Banner vermelho persistente | Exibido automaticamente abaixo do cabeçalho (`.visible`) sempre que há 1 ou mais alarmes disparados (`alarmState === 'triggered'`) aguardando reconhecimento. |
| `#bannerActiveAlarmsText` | `<span>` | `N alarme(s) ativo(s) aguardando reconhecimento` | Texto dinâmico dentro de `#mobileActiveAlarmsBanner` informando a quantidade exata de alarmes disparados. |
| `#btnBannerViewAlarms` | `<button class="btn btn-secondary btn-sm">` | `Ver` | Botão dentro de `#mobileActiveAlarmsBanner` que abre o modal de alarme (quando há 1 alarme ativo) ou navega diretamente para `#viewPendingEvents` filtrando os eventos com alarme (`#filterAlarm = 'sim'`). |
| `#btnBannerAckAll` | `<button class="btn btn-warning btn-sm">` | `Reconhecer` / `Reconhecer Todos` | Botão de ação rápida em `#mobileActiveAlarmsBanner` que reconhece todos os eventos atualmente com `alarmState === 'triggered'` (`App.Service.acknowledgeAlarm`) e atualiza a interface. |
| `#backupOverdueBanner` | `<div class="persistent-banner backup-banner">` | Banner laranja preventivo | Exibido automaticamente (`.visible`) quando nenhum backup local foi realizado ainda ou quando o último backup ocorreu há mais de `7` dias (`daysDiff > (settings.backupReminderDays || 7)`). |
| `#bannerBackupOverdueText` | `<span>` | `Último backup realizado há mais de 7 dias.` | Texto informativo do banner `#backupOverdueBanner` alertando sobre a ausência de backup ou os dias decorridos desde o último backup JSON. |
| `#btnBannerBackupNow` | `<button class="btn btn-warning btn-sm">` | `Realizar backup agora` | Botão de 1 clique dentro de `#backupOverdueBanner` que executa imediatamente `App.Backup.exportJSON()`. |
| `#viewModeWarningBanner` | `<div class="persistent-banner layout-banner">` | Banner amarelo de aviso de layout | Exibido automaticamente (`checkViewModeUsabilityWarning()`) quando o controlador força um modo manual incompatível com a largura física da tela. |
| `#bannerViewModeText` | `<span>` | `O modo de visualização manual escolhido excede a largura ideal desta tela.` | Mensagem dinâmica em `#viewModeWarningBanner` explicando a incompatibilidade entre o modo forçado e a largura da janela. |
| `#btnBannerResetAuto` | `<button class="btn btn-primary btn-sm">` | `Voltar para Automático` | Restaura imediatamente o modo responsivo para `'auto'` (`App.UI.applyResponsiveLayoutMode('auto', true)`). |

---

### 4.2 Menu Retrátil Mobile/Tablet (`#appMobileDrawer`), Barra Inferior (`#mobileBottomNav`) e Botões Flutuantes (FAB)

| ID HTML / Seletor | Tipo de Elemento | Rótulo / Conteúdo | Função Exata na Aplicação |
| :--- | :--- | :--- | :--- |
| `#mobileDrawerOverlay` | `<div class="mobile-drawer-overlay">` | Fundo escurecido (`backdrop-filter: blur(2px)`) | Sobreposição de fundo ao abrir a gaveta mobile (suporta classes `.open` e `.active`). Clicar nele fecha o menu retrátil. |
| `#appMobileDrawer` | `<div class="mobile-drawer">` | Gaveta lateral de `280px` | Container principal do menu lateral retrátil para modos compact, mobile e tablet. |
| `#mobileDrawer` | `<div style="display:none;">` | Elemento auxiliar oculto | Marcador estrutural interno dentro da gaveta mobile. |
| `#btnCloseMobileDrawer` | `<button class="modal-close">` | `×` | Botão superior que fecha o menu retrátil mobile/tablet. |
| `.mobile-nav-link[data-view="..."]` | `9 × <button class="mobile-nav-link drawer-item">` | Links para as 9 visões do sistema | Navega para a respectiva aba (`viewDashboard`, `viewNewEvent`, `viewPendingEvents`, `viewCompletedEvents`, `viewCadastros`, `viewConfigAlerts`, `viewConfigColors`, `viewBackup`, `viewDiagnostic`) e fecha a gaveta. |
| `#badgePendingDrawer` | `<span class="badge-count">` | `0` | Badge contador no item "Painel Principal" do menu mobile, atualizado em tempo real por `renderDashboard()` com o total de eventos pendentes. |
| `#badgePendingNavCountDrawer` | `<span class="badge-count">` | `0` | Badge contador no item "Eventos Pendentes" do menu mobile, atualizado em tempo real por `renderDashboard()`. |
| `#btnDrawerAppStatus` | `<button type="button" class="drawer-item">` | `ℹ Status do Sistema` | Abre o Modal 10 (`#modalAppStatus` via `App.UI.openAppStatusModal()`) a partir do menu lateral mobile e fecha a gaveta. |
| `#btnDrawerTheme` | `<button type="button" class="drawer-item">` | Contém `#labelDrawerTheme` | Alterna ciclicamente entre os 3 temas visuais (`App.UI.cycleTheme()`) diretamente pelo menu mobile. |
| `#labelDrawerTheme` | `<span>` | `🌙 Tema (Escuro)` / `☀ Tema (Claro)` / `⚡ Tema (Industrial)` | Exibe o nome do tema ativo atual dentro de `#btnDrawerTheme`. |
| `#btnDrawerUser` | `<button type="button" class="drawer-item">` | Contém `#labelDrawerUser` | Aciona o handler `promptUserChange` em `bindNavEvents()` para alterar o nome do controlador local. |
| `#labelDrawerUser` | `<span>` | `👤 Usuário: Operador` | Exibe o nome do controlador ativo dentro do item `#btnDrawerUser` no drawer. |
| `#selectDrawerViewMode` | `<select>` | `Automática (Detectar Tela)` (7 opções) | Seletor dentro da gaveta mobile para escolher qualquer um dos 7 modos responsivos, sincronizado com `#selectHeaderViewMode` e `#selectSettingsViewMode`. |
| `#btnDrawerCloseBottom` | `<button type="button" class="drawer-item">` | `✕ Fechar Menu` | Botão de rodapé largo dentro da gaveta mobile para fechar o menu com facilidade em telas grandes ou operação com uma mão. |
| `#mobileBottomNav` | `<nav class="mobile-bottom-nav">` | Barra de navegação fixa inferior | Barra inferior ergonômica exibida no modo `mobile` contendo 5 atalhos principais (`Painel`, `Pendentes`, `Novo`, `Concluídos` e `Mais`). |
| `#badgeBottomNavPending` | `<span class="bottom-nav-badge">` | `0` | Badge numérico no botão "Pendentes" da `#mobileBottomNav`, atualizado por `renderDashboard()` e ocultado automaticamente quando igual a `0`. |
| `#btnBottomNavMore` | `<button type="button" class="bottom-nav-item">` | `⋯ Mais` | Quinto botão da `#mobileBottomNav` que abre a gaveta lateral completa `#appMobileDrawer` para acesso às demais abas (Cadastros, Alertas, Cores, Backup, Diagnóstico). |
| `#btnFabNewEvent` | `<button class="fab-btn">` | Ícone `+` (Canto inferior direito) | Botão de ação flutuante com listener em `initMobileDrawer()` que limpa o formulário (`resetEventForm()`) e abre `#viewNewEvent`. |
| `#fabAddEvent` | `<button class="mobile-fab">` | Ícone `+` | Botão flutuante complementar (estilizado em `parts_css.py` e vinculado em `initMobileDrawer()`) que também limpa o formulário e abre `#viewNewEvent`. |

---

### 4.3 Barra de Navegação Desktop (`<nav class="app-nav">`)
Exibida nos modos desktop (`conventional`, `widescreen`, `ultrawide`), contém 9 botões `.nav-item` com atributo `data-view` e 3 elementos internos com `id`:

| ID HTML / Seletor `data-view` | Tipo de Elemento | Rótulo na Aba | Função Exata na Aplicação |
| :--- | :--- | :--- | :--- |
| `.nav-item[data-view="viewDashboard"]` / `#badgePendingCount` | `<button class="nav-item active">` / `<span class="nav-badge">` | `Painel` + Badge `0` | Ativa a Aba 1 (`#viewDashboard`) e exibe no badge `#badgePendingCount` o total de eventos pendentes. |
| `.nav-item[data-view="viewNewEvent"]` / `#navNewEventLabel` | `<button class="nav-item">` / `<span>` | `Novo Evento` (muda para `Editar Evento` em modo de edição) | Ativa a Aba 2 (`#viewNewEvent`), exibe o rótulo dinâmico `#navNewEventLabel` e carrega os comboboxes do console ativo. |
| `.nav-item[data-view="viewPendingEvents"]` / `#badgePendingNavCount` | `<button class="nav-item">` / `<span class="nav-badge">` | `Eventos Pendentes` + Badge `0` | Ativa a Aba 3 (`#viewPendingEvents`) e exibe no badge `#badgePendingNavCount` o total de eventos pendentes. |
| `.nav-item[data-view="viewCompletedEvents"]` | `<button class="nav-item">` | `Eventos Concluídos` | Ativa a Aba 4 (`#viewCompletedEvents`) com o histórico de previsões encerradas. |
| `.nav-item[data-view="viewCadastros"]` | `<button class="nav-item">` | `Cadastros Operacionais` | Ativa a Aba 5 (`#viewCadastros`) com o Hub Unificado de 3 colunas da estrutura operacional. |
| `.nav-item[data-view="viewConfigAlerts"]` | `<button class="nav-item">` | `Configurações de Alertas` | Ativa a Aba 6 (`#viewConfigAlerts`) para ajuste de sons, volumes, canais, temas e modos responsivos. |
| `.nav-item[data-view="viewConfigColors"]` | `<button class="nav-item">` | `Configurações de Cores` | Ativa a Aba 7 (`#viewConfigColors`) para gestão das faixas de tempo e cores. |
| `.nav-item[data-view="viewBackup"]` | `<button class="nav-item">` | `Backup e Dados` | Ativa a Aba 8 (`#viewBackup`) para exportação/importação JSON, CSV e carga de demonstração. |
| `.nav-item[data-view="viewDiagnostic"]` | `<button class="nav-item">` | `Diagnóstico` | Ativa a Aba 9 (`#viewDiagnostic`) para inspeção técnica das coleções e logs de erros. |

---

### 4.4 Aba 1: Painel Principal (`#viewDashboard`)
Visão executiva e operacional inicial da sala de controle (`<section id="viewDashboard" class="view-section active">`).

#### A. Container da Visão e Cartões de Métricas Clicáveis (`.dashboard-metrics`)
Cada `.metric-card` exibe um indicador global em tempo real e funciona como um atalho de navegação ao ser clicado (`bindNavEvents()`):

| ID HTML / Card (`data-filter`) | Tipo de Elemento | Rótulo e Cor | Ação Exata na Aplicação |
| :--- | :--- | :--- | :--- |
| `#viewDashboard` | `<section class="view-section active">` | Container da Aba 1 (Painel Principal) | Agrupa as métricas operacionais, o grid de destaque (`.dashboard-highlight-grid`) e a seção de atenção imediata (`#cardDashboardUrgent`). |
| `#metricTotalPending` (`data-filter="all"`) | `<div class="metric-value">` | `Total Pendentes` (`#38bdf8`) | Exibe o total de eventos pendentes. Ao clicar no cartão, navega para `#viewPendingEvents` e renderiza a lista de pendentes. |
| `#metricOverdue` (`data-filter="overdue"`) | `<div class="metric-value">` | `Atrasados` (`#f87171`) | Exibe o total de eventos atrasados. Ao clicar no cartão, navega para `#viewPendingEvents` e aplica `#filterStatus = 'Atrasado'`. |
| `#metricNext15` (`data-filter="15min"`) | `<div class="metric-value">` | `Próximos 15 min` (`#ef4444`) | Contabiliza eventos futuros com $0 \le \text{diffMins} \le 15$. Ao clicar, navega para `#viewPendingEvents`. |
| `#metricNext30` (`data-filter="30min"`) | `<div class="metric-value">` | `Próximos 30 min` (`#fb923c`) | Contabiliza eventos futuros com $15 < \text{diffMins} \le 30$. Ao clicar, navega para `#viewPendingEvents`. |
| `#metricNext60` (`data-filter="60min"`) | `<div class="metric-value">` | `Próximos 60 min` (`#60a5fa`) | Contabiliza eventos futuros com $30 < \text{diffMins} \le 60$. Ao clicar, navega para `#viewPendingEvents`. |
| `#metricCompletedToday` (`data-filter="completed"`) | `<div class="metric-value">` | `Concluídos Hoje` (`#4ade80`) | Contabiliza eventos concluídos na data atual (`completedAt.startsWith(todayStr)`). Ao clicar, navega para `#viewCompletedEvents`. |
| `#metricUnacknowledged` (`data-filter="unacknowledged"`) | `<div class="metric-value">` | `Alarmes Pendentes` (`#facc15`) | Contabiliza eventos com alarme disparado não reconhecido (`alarmState === 'triggered'`). Ao clicar, navega para `#viewPendingEvents` definindo `#filterAlarm = 'sim'`. |

#### B. Card de Destaque "Próximo Evento Operacional" (`#spotlightCard`) e Painel de Alarmes para Tablet (`#tabletActiveAlarmsPanel`)
Agrupados no container `.dashboard-highlight-grid`, priorizando exibir o evento mais próximo do **Console Ativo no cabeçalho** (ou o evento global mais próximo caso o console ativo não tenha pendências) ao lado do painel de alarmes ativos nos modos `tablet`, `widescreen` e `ultrawide`:

| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#spotlightCard` | `<div class="spotlight-card">` | Card principal em destaque com borda dupla azul (`#0284c7`) exibindo a próxima previsão operacional. |
| `#spotlightBadgeState` | `<span class="status-badge">` | Badge dinâmico com o nome e cor da faixa atual (`Atrasado`, `Crítico`, `Urgente`, etc.) ou `Sem Pendências`. |
| `#spotlightHierarchy` | `<div class="spotlight-hierarchy">` | Caminho completo `Console • Duto • UO` + badge do `TAG` (se houver). |
| `#spotlightDescription` | `<div class="spotlight-desc">` | Descrição principal da atividade operacional em destaque. |
| `#spotlightNotes` | `<div class="spotlight-notes">` | Observações complementares do evento em destaque. |
| `#spotlightTimeLeft` | `<div class="spotlight-timer">` | Cronômetro regressivo gigante em fonte monoespaçada atualizado a cada 1 segundo (`Faltam X min` ou `Atrasado há X min`). |
| `#spotlightScheduledAt` | `<div>` | Data e hora previstas (`Previsto: DD/MM/AAAA HH:mm`). |
| `#spotlightActions` | `<div class="spotlight-actions">` | Barra de botões de ação rápida gerada dinamicamente para o evento em destaque (`Reconhecer Alarme`, `Concluir`, `Editar`, `+ Duplicar`, `Detalhes`). |
| `#tabletActiveAlarmsPanel` | `<div class="tablet-alarms-panel">` | Painel lateral dedicado (exibido ao lado do `#spotlightCard` nos modos `tablet`, `widescreen` e `ultrawide`) que monitora alarmes disparados e eventos atrasados em tempo real. |
| `#tabletAlarmsCount` | `<span>` | Contador numérico (`0 ativos`) no cabeçalho de `#tabletActiveAlarmsPanel` com a soma de eventos com alarme disparado ou atrasados. |
| `#tabletAlarmsList` | `<div>` | Lista rolável dentro de `#tabletActiveAlarmsPanel` que exibe cada evento crítico/disparado com botões diretos `Reconhecer`, `Adiar (10m)` e `Ver`. |

#### C. Seção "Eventos que Demandam Atenção Imediata" (`#cardDashboardUrgent`)
Lista todos os eventos pendentes que já estão **atrasados** ou previstos para os **próximos 30 minutos** ($\text{diffMins} \le 30$), adaptando-se automaticamente entre tabela (desktop/tablet) e cartões (mobile):

| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#cardDashboardUrgent` | `<div class="card">` | Card container da seção "Eventos que Demandam Atenção Imediata (Atrasados e Próximos 30 min)" com atalho `Ver Todos os Pendentes →`. |
| `#dashboardUrgentCards` | `<div class="dashboard-urgent-cards">` | Container de cartões responsivos exibido no modo `mobile` em substituição à tabela horizontal, com botões `Concluir`, `Reconhecer` (se disparado) e `⋯ Mais` (`App.UI.openEventActionSheet`). |
| `#tableDashboardUrgent` / `#tbodyDashboardUrgent` | `<table>` / `<tbody>` | Tabela com 6 colunas (`Horário`, `Situação`, `Console / Duto`, `UO / Equipamento / TAG`, `Descrição da Atividade`, `Ações` com botões `Concluir`, `Editar` e `+ Duplicar`). |

---

### 4.5 Aba 2: Novo Evento / Cadastrar Previsão (`#viewNewEvent`)
Formulário completo para criação, edição ou duplicação de previsões operacionais (`<section id="viewNewEvent" class="view-section">`).

| ID HTML | Tipo de Elemento | Rótulo / Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#viewNewEvent` | `<section class="view-section">` | Container principal da Aba 2 (Cadastro e Edição de Previsão Operacional). |
| `#formEventTitle` | `<div class="card-title">` | Exibe `Cadastrar Previsão Operacional` (ou `Editar Previsão Operacional` quando em modo de edição). |
| `#labelEventActiveConsole` | `<span class="active-console-tag">` | Exibe em destaque `Console Ativo: C04` sincronizado com o seletor global do cabeçalho. |
| `#labelActiveConsoleBadge` | `<strong style="display:none;">` | Badge auxiliar oculto sincronizado com o nome do console ativo. |
| `#btnCancelEditEvent` | `<button class="btn btn-outline btn-sm">` | Oculto por padrão; aparece durante a edição de um evento para cancelar a edição, limpar o formulário e voltar para `#viewPendingEvents`. |
| `#formEvent` | `<form autocomplete="off">` | Formulário principal de submissão da previsão operacional. |
| `#eventEditId` | `<input type="hidden">` | Guarda o UUID do evento quando está em modo de edição (vazio na criação/duplicação). |
| `#eventConsoleId` | `<input type="hidden">` | Guarda o UUID do Console Operacional ativo herdado do cabeçalho. |
| `#selectEventConsole` | `<input type="hidden">` | Campo oculto auxiliar de compatibilidade para o ID do console. |
| `#selectEventPipeline` | `<select required>` | **Duto (`*`)**: Lista apenas os dutos ativos pertencentes ao console ativo. Ao mudar, carrega as UOs daquele duto e reseta Tipo e TAG. |
| `#selectEventUO` | `<select required disabled>` | **Unidade Operacional - UO (`*`)**: Habilitado após selecionar o Duto; lista apenas as UOs vinculadas ao duto escolhido. Ao mudar, carrega os Tipos de Equipamento daquela UO. |
| `#selectEventEquipmentType` | `<select disabled>` | **Tipo de Equipamento (opcional)**: Habilitado após selecionar a UO; opção padrão `Geral da UO / Não aplicável` ou tipos cadastrados na UO. |
| `#selectEventTag` | `<select disabled>` | **TAG do Equipamento (opcional)**: Habilitado após selecionar um Tipo de Equipamento; lista os TAGs pertencentes àquela UO e Tipo. |
| `#cascadeStatusText` | `<div aria-live="polite">` | Indicador textual em tempo real do encadeamento hierárquico atualizado por `loadPipelineOptions()`, `loadUOOptions()`, `loadEquipmentTypeOptions()` e `loadEquipmentTagOptions()` (ex.: *"✓ 2 UO(s) carregada(s) para o duto selecionado."* $\rightarrow$ *"✓ TAG TQ-804 vinculado à previsão."*). |
| `#inputEventDate` | `<input type="date" required>` | **Data do Evento (`*`)**: Preenchida automaticamente com a data de `agora + 1 hora` ao abrir um novo formulário. |
| `#inputEventTime` | `<input type="time" required>` | **Hora do Evento (`*`)**: Preenchida automaticamente com a hora de `agora + 1 hora` (`HH:mm`). |
| `#selectEventPriority` | `<select>` | **Prioridade**: Opções `Normal` (padrão), `Alta`, `Crítica`, `Baixa`. |
| `#inputEventDescription` | `<input type="text" required>` | **Descrição da Atividade Operacional (`*`)**: Texto principal da manobra ou verificação (ex.: *"Verificar o término do recebimento de MGO"*). |
| `#inputEventNotes` | `<textarea rows="2">` | **Observações e Recomendações Operacionais**: Detalhes adicionais, alinhamentos de válvulas, vazões, telefones. |
| `#btnToggleStylusCanvas` | `<button type="button">` | **Abrir Lousa para Caneta**: Alterna a exibição do container de desenho manual `#boxStylusCanvas` e redimensiona o canvas preservando o conteúdo. |
| `#boxStylusCanvas` | `<div class="stylus-canvas-container">` | Container retrátil da lousa digital para tablets/caneta stylus (suporta modo tela cheia `.fullscreen-lousa`). |
| `#stylusModeIndicator` | `<span>` | Indicador visual do modo e espessura ativos na lousa digital (`Modo: Caneta (4px)` ou `Modo: Borracha (18px)`), exibido quando a lousa está aberta. |
| `#inputStylusStrokeColor` | `<input type="color" value="#38bdf8">` | Seletor de cor do traço da caneta na lousa digital. |
| `#stylusColor` | `<input type="color" style="display:none;">` | Campo auxiliar oculto de cor da caneta. |
| `#selectStylusStrokeWidth` | `<select>` | Seletor de espessura do traço da caneta: `Fina (2px)`, `Normal (4px)`, `Grossa (8px)`. |
| `#stylusWidth` | `<select style="display:none;">` | Seletor auxiliar oculto de espessura. |
| `#btnUndoStylusCanvas` | `<button type="button" class="btn btn-outline btn-sm">` | **↶ Desfazer**: Desfaz o último traço desenhado na lousa digital, restaurando o snapshot anterior da pilha `this.stylusHistory` (até 25 níveis). |
| `#btnEraserStylusCanvas` | `<button type="button">` | **Borracha / Modo Caneta**: Alterna entre modo de desenho (`source-over`) e borracha (`destination-out`, 18px). |
| `#btnClearStylusCanvas` | `<button type="button">` | **Limpar**: Solicita confirmação (se houver traços no canvas) e apaga todo o conteúdo desenhado em `#stylusDrawingCanvas` (`clearStylusPad(true)`). |
| `#btnFullscreenStylusCanvas` | `<button type="button" class="btn btn-outline btn-sm">` | **⛶ Tela Cheia / ✕ Sair Tela Cheia**: Alterna a classe `.fullscreen-lousa` em `#boxStylusCanvas` para expandir a lousa digital em tela cheia. |
| `#stylusDrawingCanvas` | `<canvas width="600" height="220">` | Área de desenho manuscrito interativa (`Pointer Events`) exportada como PNG Base64. |
| `#checkEventAlarmActive` | `<input type="checkbox" checked>` | **Ativar Alarme para esta Previsão**: Habilita ou desabilita o monitoramento de alarme para o evento. |
| `#wrapperUseDefaultAlarm` | `<label class="form-checkbox">` | Container do checkbox `#checkEventUseDefaultAlarm` (ocultado se `#checkEventAlarmActive` for desmarcado). |
| `#checkEventUseDefaultAlarm` | `<input type="checkbox" checked>` | **Usar Configurações Padrão de Alerta**: Quando marcado, usa os parâmetros globais da Aba 6; quando desmarcado, exibe `#boxCustomAlarmSettings`. |
| `#boxCustomAlarmSettings` | `<div class="form-grid">` | Painel de configurações personalizadas de alarme exclusivas para este evento. |
| `#inputEventAlarmLeadTime` | `<input type="number" min="0" max="1440" value="15">` | **Antecedência do Alarme (minutos)** customizada para o evento (`0` dispara exatamente no horário). |
| `#checkEventAlertSound` | `<input type="checkbox" checked>` | Habilita **Sinal Sonoro** específico para este evento. |
| `#checkEventAlertVisual` | `<input type="checkbox" checked>` | Habilita **Alerta Visual na Tela** (Modal) específico para este evento. |
| `#checkEventAlertNotif` | `<input type="checkbox">` | Habilita **Notificação do Navegador** específica para este evento. |
| `#checkEventAlertRepeat` | `<input type="checkbox" checked>` | Habilita **Repetir Alerta até Reconhecimento** específico para este evento. |
| `#inputEventAlertRepeatInterval` | `<input type="number" min="1" max="60" value="2">` | **Intervalo (min)** entre repetições do alarme deste evento. |
| `#inputEventAlertMaxRepeats` | `<input type="number" min="1" max="20" value="5">` | **Máx Repetições** do alarme deste evento. |
| `#checkKeepDutoUO` | `<input type="checkbox" checked>` | **Manter Duto e UO para próximas previsões**: Preserva o Duto e a UO selecionados após salvar. |
| `#btnResetEventForm` | `<button type="button">` | **Limpar**: Reseta todos os campos do formulário e limpa a lousa digital. |
| `#btnSubmitAndNew` | `<button type="button" class="btn btn-success">` | **Salvar e + Outra no Duto**: Salva o evento, mantém Console/Duto/UO/Tipo/TAG, avança a hora prevista em +30 min, limpa a descrição e foca em `#inputEventDescription`. |
| `#btnSubmitEvent` | `<button type="submit" class="btn btn-primary">` | Botão principal de submissão do formulário `#formEvent`, que salva e redireciona para `#viewPendingEvents`. |
| `#btnSubmitEventText` | `<span>` | Rótulo interno de `#btnSubmitEvent`: alterna dinamicamente entre `Salvar Previsão` (criação/duplicação) e `Atualizar Previsão` (edição). |

---

### 4.6 Aba 3: Eventos Pendentes (`#viewPendingEvents`)
Central de acompanhamento operacional das atividades programadas (`<section id="viewPendingEvents" class="view-section">`), com suporte a **Bottom Sheet de Filtros** em smartphones e visão dividida **Master-Detail** em tablets e ultrawide.

| ID HTML | Tipo de Elemento | Rótulo / Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#viewPendingEvents` | `<section class="view-section">` | Container principal da Aba 3 (Eventos Pendentes). |
| `#inputSearchPending` | `<input type="text">` | Pesquisa textual instantânea (`input`) filtrando por descrição, observações, nome do Console, Duto, UO ou código do TAG. |
| `#btnToggleFilters` | `<button class="btn btn-outline btn-sm">` | **Filtros**: Abre ou fecha a gaveta/bottom-sheet de filtros avançados `#filterDrawer`. |
| `#badgeActiveFiltersCount` | `<span class="nav-badge">` | Badge contador dentro de `#btnToggleFilters` atualizado por `renderPendingEvents()` que exibe quantos filtros avançados estão ativos no momento (`display: none` quando `0`). |
| `#checkFilterOnlyActiveConsole` | `<input type="checkbox" checked>` | **Apenas Console Ativo**: Quando marcado (padrão), restringe a listagem apenas às previsões do Console selecionado no cabeçalho (`#headerActiveConsole`). Desmarcar permite ver todos os consoles simultaneamente. |
| `#labelActiveConsoleFilter` | `<strong>` | Exibe o nome do console ativo ao lado de `#checkFilterOnlyActiveConsole` (`C04`), atualizado por `syncActiveConsoleUI()`. |
| `#btnViewCards` | `<button>` | Alterna para a **Visualização em Cartões** (`#containerPendingCards`), salvando em `settings.viewMode = 'cards'`. |
| `#btnViewTable` | `<button>` | Alterna para a **Visualização em Tabela Compacta** (`#containerPendingTable`), salvando em `settings.viewMode = 'table'`. |
| `#selectSortPending` | `<select>` | **Ordenar**: Define o critério de ordenação: `Cronológica (Padrão)` (`cronologica`), `Console` (`console`), `Duto` (`duto`), `UO` (`uo`), `TAG` (`tag`) ou `Prioridade` (`prioridade`: Crítica $\rightarrow$ Alta $\rightarrow$ Normal $\rightarrow$ Baixa). |
| `#btnClearFilters` | `<button>` | **Limpar**: Reseta a busca textual, volta a ordenação para `cronologica`, limpa todos os 8 filtros avançados de `#filterDrawer` e atualiza `#badgeActiveFiltersCount`. |
| `#filterDrawer` | `<div class="toolbar-filters">` | Gaveta retrátil de filtros (que opera como **Bottom Sheet modal deslizante** `.active-sheet` no modo `mobile`) contendo o cabeçalho/rodapé mobile e os 8 filtros abaixo: |
| `#btnCloseFilterSheet` | `<button type="button" class="btn btn-outline btn-sm">` | Botão `✕` no cabeçalho do Bottom Sheet de filtros (`#filterDrawer`) para fechá-lo em telas mobile. |
| `#filterConsole` | `<select>` | Filtra eventos pendentes por um Console específico (`Todos os Consoles`). |
| `#filterPipeline` | `<select>` | Filtra eventos pendentes por um Duto específico (`Todos os Dutos`). |
| `#filterUO` | `<select>` | Filtra eventos pendentes por uma UO específica (`Todas as UOs`). |
| `#filterStatus` | `<select>` | Filtra pela **Situação / Faixa** calculada dinamicamente: `Atrasado`, `Crítico`, `Urgente`, `Atenção`, `Monitoramento`, `Normal`. |
| `#filterAlarm` | `<select>` | Filtra por presença de **Alarme Ativo**: `Todos`, `Com Alarme` (`sim`), `Sem Alarme` (`nao`). |
| `#filterPriority` | `<select>` | Filtra pela **Prioridade**: `Todas`, `Crítica`, `Alta`, `Normal`, `Baixa`. |
| `#filterDateFrom` | `<input type="date">` | **Data De**: Filtra eventos com `scheduledDate >= filterDateFrom`. |
| `#filterDateTo` | `<input type="date">` | **Data Até**: Filtra eventos com `scheduledDate <= filterDateTo`. |
| `#btnSheetClearFilters` | `<button type="button" class="btn btn-secondary btn-sm">` | Botão **Limpar** no rodapé do Bottom Sheet mobile que aciona `#btnClearFilters`. |
| `#btnSheetApplyFilters` | `<button type="button" class="btn btn-primary btn-sm">` | Botão **Aplicar Filtros** no rodapé do Bottom Sheet mobile que aplica os filtros e fecha `#filterDrawer`. |
| `#containerPendingCards` | `<div class="events-container-cards">` | Grid responsivo de cartões `.event-card`. Cada cartão exibe hierarquia, badge de faixa, descrição, notas, botão `✎ Possui Anotação / Esboço`, data/hora, prioridade, contador regressivo ao vivo, botões diretos (`Concluir`, `Editar`, `+ Duplicar`, `Detalhes`, `×`) e o botão mobile `⋯ Mais` (`App.UI.openEventActionSheet`). Nos modos `tablet` e `ultrawide`, clicar em um cartão seleciona-o no painel `#pendingDetailPane`. |
| `#pendingDetailPane` | `<aside class="pending-detail-pane">` | **Painel Lateral Master-Detail (Modos Tablet e Ultrawide)**: Exibido ao lado de `#containerPendingCards` nos modos `tablet` e `ultrawide`, renderizando instantaneamente (`selectPendingDetailEvent(eventId, tab)` / `renderPendingDetailPane(eventId, tab)`) a ficha da previsão selecionada dividida em 3 abas (`Detalhes`, `Anotações`, `Histórico`) e barra de ações (`Concluir`, `Reconhecer`, `Adiar (10m)`, `Editar`, `+ Duplicar`, `Modal Completo`). |
| `#containerPendingTable` | `<div class="table-responsive">` | Container da visualização em tabela compacta (oculto quando em modo `cards`). |
| `#tablePendingEvents` / `#tbodyPendingEvents` | `<table>` / `<tbody>` | Tabela compacta com 8 colunas (`Horário`, `Tempo Restante`, `Situação`, `Console / Duto`, `UO / Equipamento / TAG`, `Descrição`, `Alarme`, `Ações`). |
| `#pendingEmptyMessage` | `<div>` | Mensagem amigável exibida quando não há previsões pendentes para os filtros atuais. |

---

### 4.7 Aba 4: Eventos Concluídos (`#viewCompletedEvents`)
Histórico de atividades encerradas com análise de pontualidade (`<section id="viewCompletedEvents" class="view-section">`).

| ID HTML | Tipo de Elemento | Rótulo / Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#viewCompletedEvents` | `<section class="view-section">` | Container principal da Aba 4 (Eventos Concluídos). |
| `#inputSearchCompleted` | `<input type="text">` | Pesquisa textual instantânea em eventos concluídos (filtra por descrição, notas, nota de conclusão, Console, Duto, UO e TAG). |
| `#btnExportCompletedCSV` | `<button class="btn btn-outline btn-sm">` | **Exportar CSV**: Exporta imediatamente os eventos concluídos em formato CSV compatível com Excel (`App.Backup.exportCSV('completed')`). |
| `#filterCompletedConsole` | `<select>` | Filtra concluídos por Console (`Todos os Consoles`). |
| `#filterCompletedPipeline` | `<select>` | Filtra concluídos por Duto (`Todos os Dutos`). |
| `#filterCompletedUO` | `<select>` | Filtra concluídos por UO (`Todas as UOs`). |
| `#filterCompletedTiming` | `<select>` | Filtra pela **Situação Conclusão**: `Todas`, `Com Antecedência` (`antecedencia`/`antecipado`), `Com Atraso` (`atraso`/`atrasado`) e `Exatamente no Horário` (`noprazo`/`pontual`). |
| `#filterCompletedDateFrom` | `<input type="date">` | **Data Prevista De**: Filtra concluídos com `scheduledDate >= valor`. |
| `#filterCompletedDateTo` | `<input type="date">` | **Data Prevista Até**: Filtra concluídos com `scheduledDate <= valor`. |
| `#containerCompletedCards` | `<div class="completed-cards-container">` | Lista de cartões de eventos concluídos exibida automaticamente no modo `mobile` em substituição à tabela larga, contendo horários previsto/concluído, badge de pontualidade, controlador, resumo de alarme e botões `Reabrir`, `+ Duplicar`, `Detalhes` e `×`. |
| `#tableCompletedWrapper` | `<div class="table-responsive">` | Container responsivo que envolve a tabela `#tableCompletedEvents` nos modos desktop e tablet. |
| `#tableCompletedEvents` / `#tbodyCompletedEvents` | `<table>` / `<tbody>` | Tabela de eventos concluídos ordenada do mais recente para o mais antigo (`completedAt || scheduledAt`), com **9 colunas** sincronizadas entre `<thead>` e `<tbody>`: `Horário Previsto`, `Horário Conclusão`, `Diferença Efetiva`, `Console / Duto`, `UO / Equipamento / TAG`, `Descrição e Observação de Conclusão`, `Controlador` (extraído da trilha de conclusão ou `settings.localUserName`), `Alarmes` (`Disparos: N` ou `Sem alarme`) e `Ações` (`Reabrir`, `+ Duplicar`, `Detalhes`, `×`). |
| `#completedEmptyMessage` | `<div>` | Mensagem exibida quando nenhum evento concluído corresponde aos filtros. |

---

### 4.8 Aba 5: Cadastros Operacionais Unificados (`#viewCadastros`)
Projetada como um **Hub Unificado de 3 Colunas** (`.cadastros-unified-grid.cadastros-hub-grid`) no desktop e com uma **Barra de Categorias Drill-Down** (`#cadastrosCategoryBar`) nos modos `mobile` e `tablet` para gerenciar toda a hierarquia na mesma tela, sem espaço morto (`<section id="viewCadastros" class="view-section">`).

#### Container da Visão e Barra de Categorias Mobile/Tablet (`#cadastrosCategoryBar`)
Exibida nos modos `mobile` e `tablet` (`App.UI.switchCadastrosCategory(category)`), permite alternar entre as 5 entidades cadastrais ou exibir todas (`all`):

| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#viewCadastros` | `<section class="view-section">` | Container principal da Aba 5 (Cadastros Operacionais Unificados). |
| `#cadastrosCategoryBar` | `<div class="cadastros-category-bar">` | Barra de botões de categoria (`.cadastros-category-btn[data-cat="consoles" \| "pipelines" \| "uos" \| "types" \| "tags" \| "all"]`) que filtra qual sub-seção do Hub é exibida em telas mobile e tablet. |
| `#catCountConsoles` | `<span class="cat-count">` | Exibe no botão "Consoles" da `#cadastrosCategoryBar` o total de consoles cadastrados. |
| `#catCountPipelines` | `<span class="cat-count">` | Exibe no botão "Dutos" da `#cadastrosCategoryBar` o total de dutos cadastrados. |
| `#catCountUOs` | `<span class="cat-count">` | Exibe no botão "UOs" da `#cadastrosCategoryBar` o total de Unidades Operacionais cadastradas. |
| `#catCountTypes` | `<span class="cat-count">` | Exibe no botão "Tipos de Equipamento" da `#cadastrosCategoryBar` o total de Tipos de Equipamento cadastrados. |
| `#catCountTags` | `<span class="cat-count">` | Exibe no botão "TAGs" da `#cadastrosCategoryBar` o total de TAGs cadastrados. |

#### Painel 1 (Coluna Esquerda - `#hubCardConsolesPipelines`): `1. Consoles & Dutos`
| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#hubCardConsolesPipelines` | `<div class="cadastro-hub-card" data-cat-group="consoles,pipelines">` | Card container da Coluna 1 agrupando as sub-seções de Consoles (`#subSectionConsoles`) e Dutos (`#subSectionPipelines`). |
| `#subSectionConsoles` | `<div data-cat-item="consoles">` | Container da sub-seção `1.1 Consoles Operacionais`. |
| `#formConsole` | `<form>` | Formulário para criar ou editar um Console Operacional. |
| `#consoleEditId` | `<input type="hidden">` | Guarda o UUID do console em edição. |
| `#inputConsoleName` | `<input type="text" required>` | Nome do Console (ex.: `C04`). |
| `#btnSubmitConsole` | `<button type="submit">` | Salva ou atualiza o Console e sincroniza o cabeçalho global. |
| `#btnCancelConsoleEdit` | `<button type="button">` | Cancela o modo de edição de Console. |
| `#searchConsoles` | `<input type="text">` | Busca textual em tempo real na tabela de consoles. |
| `#filterActiveConsoles` | `<select>` | Filtra a tabela de Consoles por situação: `Todos` (`all`, padrão), `Ativos` (`active`) ou `Inativos` (`inactive`). |
| `#tableConsoles` / `#tbodyConsoles` | `<table>` / `<tbody>` | Lista os consoles mostrando `Console`, quantidade de `Dutos` vinculados, `Situação` (`Ativo`/`Inativo`) e botões `Editar`, `Inativar`/`Ativar` e `×` (Excluir). |
| `#subSectionPipelines` | `<div data-cat-item="pipelines">` | Container da sub-seção `1.2 Dutos Operacionais (Mín. 2 UOs)`. |
| `#formPipeline` | `<form>` | Formulário para criar ou editar um Duto. |
| `#pipelineEditId` | `<input type="hidden">` | Guarda o UUID do duto em edição. |
| `#selectPipelineConsole` | `<select required>` | Seleciona o **Console Responsável (`*`)** pelo duto. |
| `#inputPipelineName` | `<input type="text" required>` | **Nome do Duto (`*`)** (ex.: `OSCAN`, `OSBRA`). |
| `#inputInlineNewUO` | `<input type="text">` | **Atalho Inline**: Permite digitar uma ou várias novas UOs diretamente dentro do cadastro do duto. |
| `#btnInlineAddUO` | `<button type="button">` | **+ Criar UO**: Cria imediatamente a(s) UO(s) digitada(s) em `#inputInlineNewUO`, atualiza todas as listas do sistema e já marca os checkboxes correspondentes em `#boxPipelineUOs`. |
| `#boxPipelineUOs` | `<div class="uo-selection-box">` | Caixa rolável com checkboxes de todas as UOs ativas para seleção múltipla (mínimo obrigatório de 2 UOs por duto). |
| `#inputFilterUOCheckboxes` | *(Seletor JS opcional)* | Listener preventivo em `bindCadastrosForms()` para filtragem textual dos elementos `#boxPipelineUOs label` dentro de `#boxPipelineUOs`. |
| `#btnCancelPipelineEdit` | `<button type="button">` | Cancela o modo de edição do Duto. |
| `#btnSubmitPipeline` | `<button type="submit">` | **Salvar Duto**: Valida ($\ge 2$ UOs) e grava o duto e suas associações M:N em `pipelineOperationalUnits`. |
| `#searchPipelines` | `<input type="text">` | Busca textual em tempo real na tabela de dutos. |
| `#filterActivePipelines` | `<select>` | Filtra a tabela de Dutos por situação: `Todos` (`all`, padrão), `Ativos` (`active`) ou `Inativos` (`inactive`). |
| `#tablePipelines` / `#tbodyPipelines` | `<table>` / `<tbody>` | Lista os dutos mostrando `Duto`, `Console`, nomes das `UOs` vinculadas, `Situação` e botões `Editar`, `Inativar`/`Ativar` e `×` (Excluir). |

#### Painel 2 (Coluna Central - `#hubCardUOsTypes`): `2. Unidades Operacionais (UOs) & Tipos`
| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#hubCardUOsTypes` | `<div class="cadastro-hub-card" data-cat-group="uos,types">` | Card container da Coluna 2 agrupando Unidades Operacionais (`#subSectionUOs`) e Tipos de Equipamento (`#subSectionTypes`). |
| `#subSectionUOs` | `<div data-cat-item="uos">` | Container da sub-seção `2.1 Unidades Operacionais (Suporta Lote)`. |
| `#formUO` | `<form>` | Formulário de cadastro individual ou em lote de Unidades Operacionais. |
| `#uoEditId` | `<input type="hidden">` | Guarda o UUID da UO em edição. |
| `#inputUOName` | `<input type="text" required>` | Permite digitar **uma UO** ou **várias UOs separadas por vírgula** (ex.: `REFAP, TEDEP, REPLAN, TEBAR`). |
| `#btnSubmitUO` | `<button type="submit">` | **Salvar UO**: Executa `saveUO` (se edição) ou `saveUOBatch` (se criação) e chama `refreshAllMasterDataDropdowns()` para atualizar imediatamente os seletores de Duto, Tipo de Equipamento e TAG na mesma tela. |
| `#btnCancelUOEdit` | `<button type="button">` | Cancela a edição da UO. |
| `#searchUOs` | `<input type="text">` | Busca textual em tempo real na tabela de UOs. |
| `#filterActiveUOs` | `<select>` | Filtra a tabela de UOs por situação: `Todos` (`all`, padrão), `Ativos` (`active`) ou `Inativos` (`inactive`). |
| `#tableUOs` / `#tbodyUOs` | `<table>` / `<tbody>` | Lista as UOs mostrando `Nome da UO`, `Dutos` conectados, quantidade de `Tipos`, `Situação` e botões `Editar`, `Inativar`/`Ativar` e `×` (Excluir). |
| `#subSectionTypes` | `<div data-cat-item="types">` | Container da sub-seção `2.2 Tipos de Equipamento por UO`. |
| `#formEquipmentType` | `<form>` | Formulário para criar ou editar um Tipo de Equipamento vinculado a uma UO. |
| `#equipmentTypeEditId` | `<input type="hidden">` | Guarda o UUID do Tipo de Equipamento em edição. |
| `#selectEquipmentTypeUO` | `<select required>` | **UO Vinculada (`*`)**: Seleciona a qual UO este Tipo de Equipamento pertence. |
| `#inputEquipmentTypeName` | `<input type="text" required>` | **Tipo (`*`)**: Nome do tipo (ex.: `Tanque`, `Bomba`, `Esfera`). |
| `#btnCancelEquipmentTypeEdit` | `<button type="button">` | Cancela a edição do Tipo de Equipamento. |
| `#btnSubmitEquipmentType` | `<button type="submit">` | **Salvar Tipo**: Grava o tipo de equipamento na store `equipmentTypes`. |
| `#searchEquipmentTypes` | `<input type="text">` | Busca textual em tempo real na tabela de Tipos de Equipamento. |
| `#filterActiveEquipmentTypes` | `<select>` | Filtra a tabela de Tipos de Equipamento por situação: `Todos` (`all`, padrão), `Ativos` (`active`) ou `Inativos` (`inactive`). |
| `#tableEquipmentTypes` / `#tbodyEquipmentTypes` | `<table>` / `<tbody>` | Lista os tipos mostrando `Tipo`, `UO`, quantidade de `TAGs`, `Situação` e botões `Editar`, `Inativar`/`Ativar` e `×` (Excluir). |

#### Painel 3 (Coluna Direita - `#hubCardTags`): `3. TAGs de Equipamentos`
| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#hubCardTags` | `<div class="cadastro-hub-card" data-cat-group="tags" data-cat-item="tags">` | Card container da Coluna 3 dedicado à gestão de TAGs de Equipamentos. |
| `#formEquipmentTag` | `<form>` | Formulário para criar ou editar um TAG de Equipamento. |
| `#tagEditId` | `<input type="hidden">` | Guarda o UUID do TAG em edição. |
| `#selectTagUO` | `<select required>` | **Unidade Operacional - UO (`*`)**: Ao selecionar a UO, carrega automaticamente os Tipos de Equipamento daquela UO em `#selectTagType`. |
| `#selectTagType` | `<select required disabled>` | **Tipo de Equipamento (`*`)**: Habilitado após escolher a UO. |
| `#inputTagCode` | `<input type="text" required>` | **Código do TAG (`*`)**: Ex.: `TQ-804`, `BB-101A`. Validado pela regra global de exclusividade por UO. |
| `#btnCancelTagEdit` | `<button type="button">` | Cancela a edição do TAG. |
| `#btnSubmitTag` | `<button type="submit">` | **Salvar TAG**: Valida a exclusividade global por UO e grava em `equipmentTags`. |
| `#searchTags` | `<input type="text" data-alias="searchEquipmentTags">` | Busca textual em tempo real na tabela de TAGs pelo código do TAG, nome da UO ou nome do Tipo. |
| `#filterActiveTags` | `<select>` | Filtra a tabela de TAGs por situação: `Todos` (`all`, padrão), `Ativos` (`active`) ou `Inativos` (`inactive`). |
| `#tableEquipmentTags` / `#tbodyEquipmentTags` | `<table>` / `<tbody>` | Lista os TAGs registrados mostrando `TAG`, `UO`, `Tipo`, `Situação` e botões `Editar`, `Inativar`/`Ativar` e `×` (Excluir). |

---

### 4.9 Aba 6: Configurações de Alertas (`#viewConfigAlerts`)
Parametrização global do comportamento sonoro, visual, notificações, tema visual e modo de visualização responsivo (`<section id="viewConfigAlerts" class="view-section">`).
Inclui no topo um banner explicativo (`.notice-banner`) detalhando as **Limitações do Ambiente de Navegador Web** (necessidade de aba aberta, política de autoplay de áudio, permissão explícita de notificações e restrições de foco de janela do SO).

| ID HTML | Tipo de Elemento | Rótulo / Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#viewConfigAlerts` | `<section class="view-section">` | Container principal da Aba 6 (Configurações Globais de Alertas e Preferências Visuais). |
| `#formAlertSettings` | `<form>` | Formulário de configurações globais de alertas e preferências visuais. |
| `#inputSettingsUserName` | `<input type="text">` | **Nome do Controlador neste Computador**: Define a identificação gravada na trilha de auditoria e exibida em `#headerUserName` e `#labelDrawerUser`. |
| `#inputDefaultLeadTime` | `<input type="number" min="0" max="1440" value="15">` | **Antecedência Padrão dos Alarmes (minutos)**: Valor padrão utilizado por todas as previsões que marcam "Usar Configurações Padrão de Alerta". |
| `#selectSettingsViewMode` | `<select>` | **Modo de Visualização (Responsividade Manual ou Automática)**: Seleciona entre os **7 modos responsivos** (`auto`, `compact`, `mobile`, `tablet`, `conventional`, `widescreen`, `ultrawide`), aplicando imediatamente ao `<body>` (`applyResponsiveLayoutMode`) e sincronizando com `#selectHeaderViewMode` e `#selectDrawerViewMode`. |
| `#selectSettingsTheme` | `<select>` | **Tema Visual da Sala de Controle**: Seleciona entre os **3 temas visuais** (`dark`: *Tema 1: Controle Escuro (Padrão)*, `light`: *Tema 2: Claro Operacional (Diurno)*, `industrial`: *Tema 3: Industrial Alto Contraste*), aplicando imediatamente via `applyTheme()`. |
| `#selectSoundType` | `<select>` | **Tipo de Sinal Sonoro**: Escolhe entre os 4 timbres sintetizados: `chime` (*Chime Harmônico*), `beep` (*Beep Duplo*), `siren` (*Sirene Operacional*) e `blip` (*Blip Suave*). |
| `#rangeSoundVolume` | `<input type="range" min="0" max="100" value="80">` | Controle deslizante do volume do alarme sonoro (`0%` a `100%`). |
| `#labelVolumeValue` | `<span>` | Exibe o percentual numérico ao vivo do slider `#rangeSoundVolume` (ex.: `80%`). |
| `#checkSettingSound` | `<input type="checkbox" checked>` | Ativa/desativa globalmente o **Sinal Sonoro Local (Web Audio API)**. |
| `#checkSettingVisualModal` | `<input type="checkbox" checked>` | Ativa/desativa globalmente a **Janela Modal Flutuante de Alerta**. |
| `#checkSettingHighlightCard` | `<input type="checkbox" checked>` | Ativa/desativa o **Destaque Visual do Cartão na Lista**. |
| `#checkSettingPulsing` | `<input type="checkbox" checked>` | Ativa/desativa o **Efeito Visual de Pulsação Luminosa**. |
| `#checkSettingChangeTitle` | `<input type="checkbox" checked>` | Ativa/desativa a **Alteração Dinâmica do Título da Aba** (`⚠️ ALARME OPERACIONAL!`). |
| `#checkSettingNotification` | `<input type="checkbox">` | Ativa/desativa o envio automático de **Notificação do Navegador (Web Notifications)** nos disparos de alarme. |
| `#checkSettingRepeat` | `<input type="checkbox" checked>` | Ativa/desativa a regra global de **Repetir Alarme até Reconhecimento**. |
| `#inputSettingRepeatInterval` | `<input type="number" min="1" max="60" value="2">` | **Intervalo de Repetição (minutos)** padrão global. |
| `#inputSettingMaxRepeats` | `<input type="number" min="1" max="20" value="5">` | **Número Máximo de Repetições** padrão global. |
| `#btnTestSound` | `<button type="button">` | **Testar Som**: Executa imediatamente o timbre selecionado em `#selectSoundType` no volume definido em `#rangeSoundVolume`. |
| `#btnTestVisual` | `<button type="button">` | **Testar Alerta Visual**: Abre o modal `#modalAlarmTrigger` com um evento simulado de demonstração (*"Verificar término do recebimento de Diesel S10 (Evento de Teste)"*). |
| `#btnRequestNotifPermission` | `<button type="button">` | Botão que solicita permissão à API `Notification.requestPermission()`. |
| `#btnRequestNotifText` | `<span>` | Rótulo dinâmico dentro de `#btnRequestNotifPermission` (`Permissão de Notificações` ou `Permissão Concedida`). |
| `#btnTestNotif` | `<button type="button" class="btn btn-warning btn-sm">` | **Testar Notificação do Navegador**: Desbloqueia áudio, toca `chime`, solicita permissão se necessário e envia uma notificação nativa de teste para o sistema operacional. |
| `#btnResetAlertSettings` | `<button type="button">` | **Restaurar Padrões**: Abre confirmação `#modalConfirm` e restaura `App.Config.DEFAULT_SETTINGS` (incluindo tema e modo responsivo). |

---

### 4.10 Aba 7: Configurações de Cores (`#viewConfigColors`)
Gerenciamento das faixas dinâmicas de proximidade temporal e cores (`<section id="viewConfigColors" class="view-section">`).

| ID HTML | Tipo de Elemento | Rótulo / Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#viewConfigColors` | `<section class="view-section">` | Container principal da Aba 7 (Configurações de Faixas de Tempo e Cores). |
| `#btnResetColorRanges` | `<button class="btn btn-outline btn-sm">` | **Restaurar Faixas Padrão**: Abre `#modalConfirm` e restaura as 5 faixas originais de fábrica (`Crítico`, `Urgente`, `Atenção`, `Monitoramento`, `Normal`). |
| `#colorPreviewBar` | `<div class="color-preview-bar">` | Barra horizontal proporcional que renderiza visualmente os blocos `.preview-segment` de cada faixa (de `0` a `60+ min`) com suas respectivas cores. |
| `#colorChainPreview` | `<span>` | Indicador textual encadeado (`0–15 min ➔ 15–30 min ➔ 30–45 min ➔ 45–60 min ➔ 60+ min`) atualizado por `renderConfigColors()` para inspeção imediata da continuidade matemática dos intervalos. |
| `#containerColorRangeCards` | `<div class="color-range-cards">` | Lista de cartões de faixas de cor exibida no modo `mobile` em substituição à tabela, com amostra de cor, limites de tempo, prioridade e botões `Editar` e `×`. |
| `#tableColorRangesWrapper` | `<div class="table-responsive">` | Container responsivo que envolve a tabela `#tableColorRanges` nos modos tablet e desktop. |
| `#tableColorRanges` / `#tbodyColorRanges` | `<table>` / `<tbody>` | Tabela com as faixas cadastradas exibindo: `Nome da Faixa`, `Amostra` (quadrado colorido + código hex), `Limite Inicial (min)`, `Limite Final (min)`, `Piscar / Pulsar`, `Sinal Sonoro`, `Prioridade` e botões `Editar` e `×` (Excluir). |
| `#titleFormRange` | `<h4>` | Título da seção do formulário (`Editar / Nova Faixa de Tempo`). |
| `#formColorRange` | `<form>` | Formulário para adicionar ou editar uma faixa de tempo/cor. |
| `#rangeEditId` | `<input type="hidden">` | Guarda o ID da faixa sendo editada. |
| `#inputRangeName` | `<input type="text" required>` | **Nome da Faixa (`*`)** (ex.: `Crítico`, `Urgente`). |
| `#inputRangeColor` | `<input type="color" value="#dc2626">` | Seletor visual de cor (sincronizado bidirecionalmente com `#inputRangeColorText`). |
| `#inputRangeColorText` | `<input type="text" value="#dc2626" required>` | Campo de texto hexadecimal da cor (sincronizado com `#inputRangeColor`). |
| `#inputRangeMin` | `<input type="number" min="0" max="99999" required>` | **Limite Inicial (minutos) (`*`)**. |
| `#inputRangeMax` | `<input type="number" min="1" max="999999" required>` | **Limite Final (minutos) (`*`)**. |
| `#inputRangePriority` | `<input type="number" min="1" max="10" value="1" required>` | **Prioridade Visual (1 = Mais alta)**. |
| `#checkRangeBlink` | `<input type="checkbox">` | **Piscar / Pulsar Eventos nesta Faixa**. |
| `#checkRangeSound` | `<input type="checkbox">` | **Emitir Alerta Sonoro nesta Faixa**. |
| `#btnCancelRangeEdit` | `<button type="button">` | Cancela a edição da faixa atual e limpa o formulário. |
| `#btnSubmitRange` | `<button type="submit">` | **Salvar Faixa de Cor / Atualizar Faixa**: Executa `App.Service.saveColorRange()`, que valida matematicamente toda a cadeia de faixas contra lacunas ou sobreposições antes de persistir. |

---

### 4.11 Aba 8: Backup e Dados (`#viewBackup`)
Central de preservação de dados, exportação de relatórios e massa de demonstração (`<section id="viewBackup" class="view-section">`). Todos os botões possuem listeners unificados em `App.UI.bindGlobalEvents()`:

| ID HTML | Tipo de Elemento | Rótulo / Conteúdo | Função Exata na Aplicação |
| :--- | :--- | :--- | :--- |
| `#viewBackup` | `<section class="view-section">` | Container da Aba 8 | Agrupa os painéis de Backup Completo (JSON), Importação, Exportação CSV e Massa de Demonstração. |
| `#labelLastBackupDate` | `<span>` | `Último backup: Nunca` / `DD/MM/AAAA HH:mm` | Exibe no cabeçalho do card a data/hora exata do último backup JSON realizado. |
| `#btnExportJSON` | `<button class="btn btn-primary">` | `Baixar Backup Completo (JSON)` | Exporta imediatamente o arquivo JSON completo de backup (`App.Backup.exportJSON()`) e atualiza `#pillBackup`, `#labelLastBackupDate` e `#backupOverdueBanner`. |
| `#inputImportBackupFile` | `<input type="file" accept=".json">` | Seletor de arquivo `.json` | Permite selecionar um arquivo JSON de backup do computador e habilita automaticamente o botão `#btnTriggerImportValidate`. |
| `#btnTriggerImportValidate` | `<button class="btn btn-secondary" disabled>` | `Validar Arquivo` | Valida o arquivo JSON selecionado (`App.Backup.validateBackupFile(file)`) e abre o modal de resumo de importação (`#modalImportSummary`). |
| `#btnExportCSVAllPending` | `<button class="btn btn-outline btn-sm">` | `Eventos Pendentes (CSV)` | Exporta relatório CSV (UTF-8 com BOM) de todas as previsões pendentes (`App.Backup.exportCSV('pending')`). |
| `#btnExportCSVAllCompleted` | `<button class="btn btn-outline btn-sm">` | `Eventos Concluídos (CSV)` | Exporta relatório CSV (UTF-8 com BOM) de todas as previsões concluídas (`App.Backup.exportCSV('completed')`). |
| `#btnExportCSVCadastros` | `<button class="btn btn-outline btn-sm">` | `Estrutura Cadastral (CSV)` | Exporta relatório CSV (UTF-8 com BOM) de todos os Consoles, Dutos, UOs, Tipos e TAGs (`App.Backup.exportCSV('cadastros')`). |
| `#btnLoadDemoData` | `<button class="btn btn-secondary btn-sm">` | `Carregar Dados de Demonstração` | Abre confirmação `#modalConfirm` e popula a base com a massa realista de demonstração (`App.Service.loadDemoData()`: Consoles `C04/C08/C10`, UOs `REFAP/TEDEP/REPLAN/TEBAR`, Dutos `OSCAN/OSBRA/DTCS`, Tipos, TAGs `TQ-804/BB-101A/ES-201/PCV-301` e 6 eventos em todas as faixas de tempo). |
| `#btnWipeAllData` | `<button class="btn btn-danger btn-sm">` | `Apagar Todos os Dados` | Abre o modal de confirmação `#modalConfirm` e, se confirmado, executa `App.Service.clearAllData()`, apagando todas as previsões, cadastros e históricos e restaurando apenas os consoles iniciais (`C02-C16`) e faixas de cores padrão. |

---

### 4.12 Aba 9: Diagnóstico Técnico (`#viewDiagnostic`)
Tela de inspeção de saúde do sistema, estado das APIs do navegador e auditoria técnica das coleções do IndexedDB (`<section id="viewDiagnostic" class="view-section">`).

| ID HTML | Tipo de Elemento | Rótulo / Conteúdo | Função Exata na Aplicação |
| :--- | :--- | :--- | :--- |
| `#viewDiagnostic` | `<section class="view-section">` | Container da Aba 9 | Agrupa os indicadores de saúde técnica, a tabela de coleções do IndexedDB e a tabela de logs de erros. |
| `#btnCopyDiagnostic` | `<button class="btn btn-outline btn-sm">` | `Copiar Diagnóstico` | Gera um relatório JSON completo (`App.UI.getDiagnosticReport()`) contendo versão (`v1.1.0`), timestamp, `navigator.userAgent`, estado do `AudioContext`, permissão de notificações e contagem de cada uma das 11 stores, copiando-o para a área de transferência (`navigator.clipboard.writeText`). |
| `#diagAppVersion` | `<div class="metric-value">` | `v1.1.0` | Exibe a versão atual da aplicação no card visual. |
| `#diagDBStatus` | `<div class="metric-value">` | `Online` $\rightarrow$ `Online (Ativo)` | Exibe o estado de conexão do banco `IndexedDB (Esquema v1)`. |
| `#diagAudioStatus` | `<div class="metric-value">` | `Suspenso` $\rightarrow$ `Aguardando Interação` / `Pronto (Ativo)` | Exibe o estado atual do motor `Web Audio API` (`App.Audio.isUnlocked`). |
| `#diagNotifStatus` | `<div class="metric-value">` | `Pendente` $\rightarrow$ `nao_solicitada` / `concedida` / `negada` | Exibe o estado real da permissão da `Web Notifications API`. |
| `#tbodyDiagCollections` | `<tbody>` | 11 linhas geradas dinamicamente | Lista todas as **11 Object Stores** do IndexedDB (`consoles`, `pipelines`, `operationalUnits`, `pipelineOperationalUnits`, `equipmentTypes`, `equipmentTags`, `events`, `eventHistory`, `colorRanges`, `settings`, `errorLogs`) mostrando nome técnico, finalidade descritiva, **Total de Registros**, **Ativos** (verde) e **Inativos** (cinza). |
| `#btnClearDiagLogs` | `<button class="btn btn-outline btn-sm">` | `Limpar Logs` | Limpa todos os registros da Object Store `errorLogs` (`App.DB.clear('errorLogs')`) e atualiza a tabela. |
| `#tbodyDiagLogs` | `<tbody>` | Até 50 registros mais recentes | Exibe os logs internos de erros capturados (`Data / Hora`, `Contexto`, `Mensagem`, `Detalhes Técnicos / Stack`). |

---

### 4.13 Mapeamento de Todos os 10 Modais do Sistema e Container de Toasts
Existem **10 janelas modais `.modal-overlay`** completas no HTML (`parts_html.py`), todas detalhadas nas tabelas abaixo. Todos os modais podem ser fechados pressionando a tecla `Escape`, clicando fora da caixa sobre o `.modal-overlay` ou clicando no botão `×`.

#### Modal 1: Disparo de Alerta Operacional (`#modalAlarmTrigger`)
Exibido automaticamente quando o `App.AlarmEngine` dispara um alarme ou ao clicar em "Testar Alerta Visual":

| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#modalAlarmTrigger` | `<div class="modal-overlay" role="dialog" aria-modal="true">` | Overlay do modal de disparo de alarme operacional (abre em tela cheia `100dvh` no modo `mobile`). |
| `#modalAlarmTitle` | `<h3>` | Título com ícone de raio `ALERTA DE PREVISÃO OPERACIONAL!`. |
| `#btnCloseAlarmModal` | `<button class="modal-close">` | Botão `×` para fechar o modal. |
| `#alarmModalHierarchy` | `<div>` | Exibe `CONSOLE | DUTO | UO | TAG`. |
| `#alarmModalDescription` | `<div>` | Descrição em destaque da atividade operacional. |
| `#alarmModalNotes` | `<div>` | Observações do evento. |
| `#alarmModalScheduledTime` | `<div>` | Data e hora previstas (`DD/MM/AAAA HH:mm`). |
| `#alarmModalCountdown` | `<div>` | Tempo restante ou tempo de atraso em vermelho (`#ef4444`). |
| `#btnAlarmAcknowledge` | `<button class="btn btn-warning">` | **Reconhecer Alarme**: Chama `App.Service.acknowledgeAlarm()`, interrompendo som e repetições futuras. |
| `#btnAlarmSnoozePrompt` | `<button class="btn btn-secondary">` | **Adiar...**: Abre o Modal 2 (`#modalSnooze`) para escolher o tempo de adiamento. |
| `#btnAlarmCompleteDirect` | `<button class="btn btn-success">` | **Concluir Evento**: Fecha o modal de alarme e abre imediatamente o Modal 3 (`#modalCompleteEvent`). |
| `#btnAlarmOpenDetails` | `<button class="btn btn-outline">` | **Abrir Detalhes**: Fecha o modal de alarme e abre o Modal 5 (`#modalEventDetails`). |

#### Modal 2: Adiar Alarme / Snooze (`#modalSnooze`)
Permite postergar temporariamente um alarme disparado:

| ID HTML / Seletor | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#modalSnooze` | `<div class="modal-overlay" role="dialog" aria-modal="true">` | Overlay do modal de adiamento (opera como *Bottom Sheet* no modo `mobile`). |
| `#btnCloseSnoozeModal` | `<button class="modal-close">` | Botão `×` para fechar. |
| `.btn-quick-snooze[data-min="5" \| "10" \| "15" \| "30"]` | `4 × <button class="btn-quick-snooze">` | Botões de atalho rápido (`5 min`, `10 min`, `15 min`, `30 min`) que preenchem automaticamente `#inputSnoozeMinutes`. |
| `#inputSnoozeMinutes` | `<input type="number" min="1" max="1440" value="5">` | Campo numérico para digitar qualquer quantidade de minutos de adiamento. |
| `#btnCancelSnooze` | `<button class="btn btn-secondary">` | Botão `Cancelar`. |
| `#btnConfirmSnooze` | `<button class="btn btn-primary">` | **Confirmar Adiamento**: Chama `App.Service.snoozeAlarm(eventId, mins)`, grava na trilha de auditoria e reagenda o disparo para `Date.now() + mins * 60000`. |

#### Modal 3: Concluir Evento (`#modalCompleteEvent`)
Exibido ao clicar em "Concluir" em qualquer evento pendente:

| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#modalCompleteEvent` | `<div class="modal-overlay" role="dialog" aria-modal="true">` | Overlay do modal de conclusão de previsão operacional. |
| `#btnCloseCompleteModal` | `<button class="modal-close">` | Botão `×` para fechar. |
| `#completeModalEventDesc` | `<div>` | Descrição da atividade que está sendo concluída. |
| `#completeModalHierarchy` | `<div>` | Caminho `Console • Duto • UO • TAG`. |
| `#completeModalScheduledTime` | `<div>` | Horário previsto original (`DD/MM/AAAA HH:mm`). |
| `#completeModalActualTime` | `<div>` | Horário efetivo exato da conclusão (`DD/MM/AAAA HH:mm` em verde `#4ade80`). |
| `#completeModalTimeDiff` | `<div>` | Diferença calculada automaticamente (`Exatamente no horário`, `Com antecedência de X min` ou `Com atraso de X min`). |
| `#inputCompleteNotes` | `<textarea rows="3">` | Campo para **Observações da Conclusão (Opcional)**. |
| `#btnCancelCompleteModal` | `<button class="btn btn-secondary">` | Botão `Cancelar`. |
| `#btnConfirmCompleteModal` | `<button class="btn btn-success">` | **Confirmar Conclusão**: Executa `App.Service.completeEvent()`, move para concluídos e grava auditoria. |

#### Modal 4: Reabrir Evento (`#modalReopenEvent`)
Exibido ao clicar em "Reabrir" em um evento da aba de Concluídos:

| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#modalReopenEvent` | `<div class="modal-overlay" role="dialog" aria-modal="true">` | Overlay do modal de reabertura de evento concluído. |
| `#btnCloseReopenModal` | `<button class="modal-close">` | Botão `×` para fechar. |
| `#boxReopenPastWarning` | `<div class="notice-banner warning">` | Banner amarelo de aviso exibido automaticamente quando o horário previsto original do evento já expirou no passado. |
| `#inputReopenDate` | `<input type="date">` | Define a **Nova Data Prevista** (sugere `agora + 1h` se o horário original já passou). |
| `#inputReopenTime` | `<input type="time">` | Define a **Nova Hora Prevista**. |
| `#btnCancelReopenModal` | `<button class="btn btn-secondary">` | Botão `Cancelar`. |
| `#btnConfirmReopenModal` | `<button class="btn btn-warning">` | **Confirmar Reabertura**: Executa `App.Service.reopenEvent()`, preservando os dados da conclusão anterior na auditoria e devolvendo o evento para Pendentes. |

#### Modal 5: Detalhes do Evento e Histórico de Auditoria (`#modalEventDetails`)
Exibe a ficha completa do evento, o desenho da caneta stylus (se houver) e a linha do tempo de auditoria:

| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#modalEventDetails` | `<div class="modal-overlay" role="dialog" aria-modal="true">` | Overlay do modal de detalhes completos e trilha de auditoria (abre em tela cheia `100dvh` no modo `mobile`). |
| `#btnCloseDetailsModal` | `<button class="modal-close">` | Botão `×` no cabeçalho. |
| `#detailsModalPath` | `<div>` | Exibe `Console / Duto / UO`. |
| `#detailsModalEquipment` | `<div>` | Exibe `Tipo (TAG)` ou `Geral`. |
| `#detailsModalSchedule` | `<div>` | Horário previsto (`DD/MM/AAAA HH:mm`). |
| `#detailsModalStatus` | `<div>` | Situação atual (`Pendente` ou `Concluído`). |
| `#detailsModalDescription` | `<div>` | Descrição completa da atividade. |
| `#detailsModalNotesBox` / `#detailsModalNotes` | `<div class="span-full">` / `<div>` | Container e texto das observações cadastradas no evento. |
| `#detailsModalDrawingBox` / `#detailsModalDrawingImg` / `#detailsStylusContainer` | `<div class="span-full">` / `<img>` / `<div>` | Containers e elemento `<img>` nativos sincronizados por `showDetailsModal()` para exibir a imagem PNG Base64 (`event.stylusDrawing`) da anotação manuscrita/esboço feito na lousa digital (ocultados automaticamente quando o evento não possui desenho). |
| `#detailsTimeline` | `<div class="timeline">` | Linha do tempo vertical que lista cronologicamente todos os registros de `eventHistory` daquele evento (data/hora, nome do controlador responsável, tipo da ação em caixa alta e descrição detalhada). |
| `#btnCloseDetailsModalBtn` | `<button class="btn btn-secondary">` | Botão `Fechar` no rodapé. |

#### Modal 6: Confirmação Genérica Acessível (`#modalConfirm`)
Substitui o `window.confirm()` nativo por um diálogo modal estilizado:

| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#modalConfirm` | `<div class="modal-overlay" role="dialog" aria-modal="true">` | Overlay do diálogo modal de confirmação genérica. |
| `#modalConfirmTitle` | `<h3>` | Título dinâmico da confirmação. |
| `#btnCloseConfirmModal` | `<button class="modal-close">` | Botão `×` para fechar. |
| `#modalConfirmMessage` | `<p>` | Texto descritivo da ação a ser confirmada. |
| `#btnCancelConfirm` | `<button class="btn btn-secondary">` | Botão `Cancelar`. |
| `#btnAcceptConfirm` | `<button class="btn btn-danger">` | Botão vermelho `Confirmar` que dispara o callback `onConfirm`. |

#### Modal 7: Dependência Operacional / Bloqueio de Exclusão (`#modalDependency`)
Aberto automaticamente quando o controlador tenta excluir fisicamente um Console, Duto, UO, Tipo ou TAG que possui registros dependentes:

| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#modalDependency` | `<div class="modal-overlay" role="dialog" aria-modal="true">` | Overlay do modal de bloqueio de exclusão por dependências. |
| `#modalDependencyTitle` | `<span>` | Título dinâmico (ex.: `Console com Dependências`, `UO com Dependências`). |
| `#btnCloseDependencyModal` | `<button class="modal-close">` | Botão `×` para fechar. |
| `#modalDependencyDesc` | `<p>` | Texto explicativo do bloqueio de exclusão física. |
| `#modalDependencyList` | `<ul>` | Lista preenchida dinamicamente com a contagem exata de vínculos (ex.: `2 duto(s) associado(s)`, `5 evento(s) no histórico`). |
| `#btnCloseDependencyModalBtn` | `<button class="btn btn-secondary">` | Botão `Entendido` para fechar sem alterar. |
| `#btnDependencyInactivate` | `<button class="btn btn-warning">` | Botão amarelo **Inativar Registro** que converte a tentativa de exclusão física em exclusão lógica (`toggle*Active`), preservando o histórico. |

#### Modal 8: Resumo da Importação de Backup (`#modalImportSummary`)
Exibido após validar um arquivo JSON de backup:

| ID HTML / Seletor | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#modalImportSummary` | `<div class="modal-overlay" role="dialog" aria-modal="true">` | Overlay do modal de validação e resumo de importação de backup JSON. |
| `#btnCloseImportSummaryModal` | `<button class="modal-close">` | Botão `×` para fechar. |
| `#importSummaryCounts` | `<div>` | Painel que resume a `Versão do Esquema`, `Data da Exportação` e as quantidades encontradas no arquivo (`Consoles`, `Dutos`, `UOs`, `Tipos`, `TAGs`, `Eventos`). |
| `input[name="importMode"][value="merge" \| "replace"]` | `2 × <input type="radio">` | Opções **Mesclar Dados** (`merge`, selecionado por padrão) e **Substituir Tudo** (`replace`, que gera backup automático antes de substituir). |
| `#btnCancelImportSummary` | `<button class="btn btn-secondary">` | Botão `Cancelar`. |
| `#btnConfirmImportSummary` | `<button class="btn btn-primary">` | **Executar Importação**: Executa `App.Backup.importJSON(parsedBackup, mode)`. |

#### Modal 9: Menu Rápido de Ações do Evento - Action Sheet Mobile (`#modalEventActionSheet`)
Exibido ao tocar no botão `⋯ Mais` de qualquer cartão de evento (`App.UI.openEventActionSheet(eventId)`):

| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#modalEventActionSheet` | `<div class="modal-overlay" role="dialog" aria-modal="true">` | Overlay modal estilo *Bottom Sheet* (`.modal-box` alinhado na base em modo `mobile`). |
| `#actionSheetEventTitle` | `<h3>` | Exibe a descrição da atividade operacional selecionada. |
| `#btnCloseActionSheet` | `<button class="modal-close">` | Botão `×` no cabeçalho para fechar o Action Sheet. |
| `#actionSheetEventSubtitle` | `<div>` | Exibe a hierarquia e o horário previsto (`Console • Duto • UO | DD/MM/AAAA HH:mm`). |
| `#actionSheetButtonsContainer` | `<div class="action-sheet-list">` | Container populado dinamicamente com botões largos de toque (`.action-sheet-btn`) para todas as operações aplicáveis ao evento: `✓ Concluir Evento`, `Reconhecer Alarme` e `Adiar Alarme (Snooze)` (se disparado), `✎ Editar Previsão`, `+ Duplicar Evento (+30 min)`, `🔍 Ver Detalhes e Histórico` e `✕ Excluir Evento`. |

#### Modal 10: Status Operacional do Sistema (`#modalAppStatus`)
Exibido ao clicar no botão `ℹ` do cabeçalho (`#btnHeaderAppStatus`) ou no item `Status do Sistema` do drawer mobile (`#btnDrawerAppStatus`) via `App.UI.openAppStatusModal()`:

| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#modalAppStatus` | `<div class="modal-overlay" role="dialog" aria-modal="true">` | Overlay modal com o resumo executivo dos subsistemas críticos do navegador. |
| `#btnCloseAppStatusModal` | `<button class="modal-close">` | Botão `×` no cabeçalho. |
| `#statusModalAudio` | `<div>` | Exibe o estado em tempo real da `Web Audio API` (`Ativo (Pronto)` em verde ou `Aguardando interação (Clique em Testar)` em amarelo). |
| `#btnStatusModalTestAudio` | `<button type="button" class="btn btn-outline btn-sm">` | Botão `Ativar / Testar Som` que desbloqueia o `AudioContext`, toca um `chime` e atualiza o status no próprio modal. |
| `#statusModalNotif` | `<div>` | Exibe o estado da `Web Notifications API` (`Ativa (Concedida)`, `Negada no navegador`, `Indisponível neste navegador` ou `Pendente (Clique para solicitar)`). |
| `#btnStatusModalTestNotif` | `<button type="button" class="btn btn-warning btn-sm">` | Botão `Solicitar / Testar` que pede permissão de notificação ao navegador e dispara uma notificação nativa de teste imediata. |
| `#statusModalDB` | `<div>` | Exibe o estado do banco de dados local (`Pronto (Offline Ativo)`). |
| `#statusModalLastBackup` | `<div>` | Exibe a data e hora do último backup JSON realizado (`DD/MM/AAAA HH:mm` ou `Nunca realizado`). |
| `#btnCloseAppStatusFooter` | `<button type="button" class="btn btn-secondary">` | Botão `Fechar` no rodapé do modal. |

#### Container Global de Notificações Toast (`#toastContainer`)
| ID HTML | Tipo de Elemento | Função Exata na Aplicação |
| :--- | :--- | :--- |
| `#toastContainer` | `<div class="toast-container" aria-live="polite">` | Posicionado no canto inferior direito (`z-index: 2000`), exibe avisos flutuantes temporários (4,5 segundos) criados por `App.UI.showToast(message, type)` nas variantes `toast-success` (verde), `toast-danger` (vermelho), `toast-warning` (amarelo) e `toast-info` (azul). |

---

## 5. Registro de Auditoria Técnica e Unificação de Bindings (`v1.1.0`)

Na auditoria técnica inicial da aplicação, haviam sido identificadas **9 divergências de binding e sincronização** entre a marcação HTML/CSS e os controladores JavaScript. Na versão **`v1.1.0`**, **todas as 9 divergências foram 100% corrigidas, unificadas e verificadas** nos módulos [`parts_css.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_css.py), [`parts_html.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_html.py), [`parts_js_core.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_core.py), [`parts_js_service.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_service.py) e [`parts_js_ui.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_ui.py):

1. **[RESOLVIDO] Unificação Total dos IDs da Aba 8 (`#viewBackup`) e Validação de Arquivo (`validateBackupFile`)**:
   - Em [`parts_js_ui.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_ui.py#L1218-L1308), `bindGlobalEvents()` agora vincula diretamente todos os IDs presentes em `parts_html.py` (com fallback seguro): `#btnExportJSON`, `#inputImportBackupFile`, `#btnTriggerImportValidate`, `#btnExportCSVAllPending`, `#btnExportCSVAllCompleted`, `#btnExportCSVCadastros` e `#btnLoadDemoData` (conectado a `App.Service.loadDemoData()` com modal de confirmação `#modalConfirm`).
   - Além disso, [`App.Backup.validateBackupFile(file)`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_service.py#L1486-L1498) foi implementado em `parts_js_service.py` encapsulando a leitura `file.text()` e delegando para `validateBackupData(text)`.
2. **[RESOLVIDO] Parâmetros de Exportação CSV em `#btnExportCompletedCSV` e `App.Backup.exportCSV(type)`**:
   - Em [`parts_js_ui.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_ui.py#L1281-L1285), `#btnExportCompletedCSV` passa a chamar `App.Backup.exportCSV('completed')`, e [`App.Backup.exportCSV(type)`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_service.py#L1563-L1651) foi normalizado para aceitar tanto `'pending'`/`'pendente'` quanto `'completed'`/`'concluido'`, `'all'` e `'cadastros'`.
3. **[RESOLVIDO] Alinhamento dos Valores do Filtro `#filterCompletedTiming` (Aba 4)**:
   - Em [`parts_js_ui.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_ui.py#L2136-L2144), `renderCompletedEvents()` agora aceita ambos os conjuntos de valores semânticos: `(fTiming === 'antecipado' || fTiming === 'antecedencia')`, `(fTiming === 'pontual' || fTiming === 'noprazo')` e `(fTiming === 'atrasado' || fTiming === 'atraso')`, funcionando em total harmonia com os `<option>` de `parts_html.py`.
4. **[RESOLVIDO] Unificação das Classes do Drawer Mobile (`#appMobileDrawer`), Token CSS `--bg-surface-elevated` e Botões FAB**:
   - Em [`parts_css.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_css.py#L51-L403), a variável `--bg-surface-elevated` foi definida nos temas, as regras CSS estilizaram conjuntamente `.mobile-drawer-overlay.active, .mobile-drawer-overlay.open` e `.mobile-drawer.active, .mobile-drawer.open`, e o seletor `.fab-btn, .mobile-fab` foi unificado.
   - Em [`parts_js_ui.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_ui.py#L368-L443), `initMobileDrawer()` alterna ambas as classes (`.open` e `.active`) ao abrir/fechar a gaveta e vincula o listener de criação rápida tanto em `#fabAddEvent` quanto em `#btnFabNewEvent`.
5. **[RESOLVIDO] Inclusão dos 5 Seletores `#filterActive*` no HTML da Aba 5 (`#viewCadastros`)**:
   - Em [`parts_html.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_html.py#L844-L1150), foram adicionados os 5 seletores de filtro de situação (`#filterActiveConsoles`, `#filterActivePipelines`, `#filterActiveUOs`, `#filterActiveEquipmentTypes` e `#filterActiveTags`) com as opções `Ativos` (`active`), `Inativos` (`inactive`) e `Todos` (`all`), permitindo consultar e reativar registros inativos diretamente nas tabelas de Cadastros.
6. **[RESOLVIDO] Alinhamento Exato das 9 Colunas de `#tableCompletedEvents` (Aba 4)**:
   - Em [`parts_js_ui.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_ui.py#L2096-L2200), `renderCompletedEvents()` extrai o controlador responsável pela conclusão a partir de `eventHistory` (`completedByMap`) e renderiza exatamente as **9 células `<td>`** correspondentes às 9 colunas do `<thead>` (`Horário Previsto`, `Horário Conclusão`, `Diferença Efetiva`, `Console / Duto`, `UO / Equipamento / TAG`, `Descrição e Observação de Conclusão`, `Controlador`, `Alarmes` e `Ações`), além de popular simultaneamente os cartões mobile em `#containerCompletedCards`.
7. **[RESOLVIDO] Sincronização Nativa de `#detailsModalDrawingBox` e `#detailsModalDrawingImg` no Modal 5 (`#modalEventDetails`)**:
   - Em [`parts_js_ui.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_ui.py#L3433-L3448), `showDetailsModal()` utiliza diretamente os elementos `#detailsModalDrawingBox` e `#detailsModalDrawingImg` declarados em `parts_html.py`, atribuindo `drawingImg.src = ev.stylusDrawing` e exibindo/ocultando `drawingBox` conforme a existência de desenho no evento.
8. **[RESOLVIDO] Normalização de `classification.key` (`cssKey`) para as Classes CSS `.status-badge.*`**:
   - Em [`parts_js_service.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_service.py#L971-L1009), `App.Service.classifyEvent()` normaliza `matchedRange.id` removendo o prefixo `'range_'` e mapeando `'monitor'` $\rightarrow$ `'monitoramento'`, retornando `key: cssKey` (`'critico'`, `'urgente'`, `'atencao'`, `'monitoramento'`, `'normal'`) e preservando `rangeId: matchedRange.id`, garantindo correspondência 1:1 com as regras `.status-badge.*` de `parts_css.py`.
9. **[RESOLVIDO] Sincronização dos Badges do Drawer Mobile, Bottom Nav e `#labelActiveConsoleFilter`**:
   - `renderDashboard()` ([`parts_js_ui.py`](file:///c:/Users/tdyb/OneDrive%20-%20TRANSPETRO/%C3%81rea%20de%20Trabalho/Livro%20de%20Previs%C3%B5es/parts_js_ui.py#L1456-L1486)) agora atualiza simultaneamente todos os contadores de pendências e alarmes (`#badgePendingCount`, `#badgePendingNavCount`, `#badgePendingDrawer`, `#badgePendingNavCountDrawer`, `#badgeBottomNavPending`, `#headerAlarmBadge`, `#mobileActiveAlarmsBanner` e `#backupOverdueBanner`), e `#labelActiveConsoleFilter` foi incluído em `parts_html.py` (linha 580) e sincronizado em `syncActiveConsoleUI()`.

