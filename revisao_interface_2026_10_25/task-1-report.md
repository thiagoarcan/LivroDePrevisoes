# Task 1 — persistência, integridade, motor e backup

Status: DONE_WITH_CONCERNS. Implementação do núcleo e fix round 1 concluídos; 33 testes do núcleo passam no Edge. Integração visual permanece sob Tasks 2/3, com falhas históricas discriminadas abaixo. Fonte única de versão: `App.Config.APP_VERSION = '1.2.0'`. DB_NAME e DB_VERSION preservados; nenhuma base/perfil real foi apagado ou utilizado nos testes.

## Arquivos e revisão

Alterados apenas `parts_js_core.py`, `parts_js_service.py`, `tests/test_core_browser.py`, este relatório e evidências próprias em `resultados/`. Nenhuma edição em index.html, UI, HTML, CSS ou build_all.py. Sem Git neste workspace: `resultados/task1.diff` contém o diff contra os originais. Self-review conferiu relações, abort/commit, preservação de histórico, comparação de merge e chamadas assíncronas. Ajustes transacionais ficam em blocos finais identificados nos geradores, substituindo os métodos públicos legados; as funções não substituídas continuam disponíveis.

## Resultado funcional

Datas Date/ISO e datas/horas simples são formatadas no fuso local; criação e reabertura conferem os componentes do calendário, rejeitando normalização de 31/02. formatDateTime também interpreta data simples como meia-noite local. CSV conserva BOM UTF-8/separador ponto e vírgula, neutraliza prefixos de fórmulas em strings e exclui eventos tombstone em todas as modalidades filtradas.

Escritas CRUD resolvem apenas em transaction.oncomplete e rejeitam abort. Serviços de eventos com auditoria, cadastro de duto com vínculos, alterações cadastrais, configurações, faixas e importação usam transações únicas. Referências são validadas por existência e compatibilidade; novos vínculos não aceitam inativos, edição pode preservar o vínculo inativo original. Duas UOs distintas são obrigatórias. Alterações de console/duto/UO/tipo/TAG que quebrariam eventos ou outros cadastros são rejeitadas com rollback. Unicidade cadastral é case insensitive, incluindo TAG global. Configurações, enumerações existentes, cores, textos, links, números e datas têm validação de tipo/faixa.

Eventos registram createdBy/completedBy a partir do nome configurado, preservam versão e updatedAt nas transições, validam snooze 1–1440 e zeram contador/último disparo na reabertura/reprogramação. Exclusão de evento é tombstone `active:false`, alarmState acknowledged, com registro `exclusao`; histórico anterior permanece. Limpeza completa explícita é operação diferente, descrita abaixo.

Backup valida previamente envelope, exportedAt ISO, todas as dez coleções obrigatórias, linhas, IDs únicos, chaves settings, referências, relação entre entidades, datas/horários, estados, números e faixas. Coleção desconhecida é rejeitada. IDs inseguros e desenho que não seja data:image/png;base64 com assinatura PNG são rejeitados. O desenho tem limite de três milhões de caracteres. Os metadados opcionais ausentes em faixas/settings legados continuam aceitos; backup legado válido foi importado em teste. Nenhuma coleção obrigatória ausente é interpretada como apagar dados.

Motor serializa ticks na aba; solicita lock exclusivo navigator.locks e possui fallback de lease localStorage de 15 segundos, renovado a cada 5 segundos. Cada disparo relê e avalia o evento dentro da mesma transação que altera estado e acrescenta histórico. Estado concluído/reconhecido por operação concorrente não é sobrescrito. Há nova leitura antes dos canais visuais/externos. Callbacks visuais são aguardados e erros vão para errorLogs sem repetição infinita do mesmo disparo. O título permanece sinalizando ALARME enquanto existir evento ativo triggered. Histórico enumera canais que estavam disponíveis e cuja chamada terminou com sucesso; áudio requer AudioContext running e desbloqueado, notificação requer permissão e objeto criado. Volume/antecedência/repetições zero são respeitados.

`maxRepeats` significa repetições ADICIONAIS ao disparo inicial; zero permite apenas o inicial. Snooze expirado autoriza novo disparo manualmente adiado independentemente desse limite.

## Contrato para Task 2 / UI

- `App.DB.DATA_STORES`: consoles, pipelines, operationalUnits, pipelineOperationalUnits, equipmentTypes, equipmentTags, events, eventHistory, colorRanges, settings. ErrorLogs é diagnóstico local e não compõe o formato de backup legado.
- `await App.DB.snapshot(stores = App.DB.DATA_STORES)` retorna `{nomeColecao: [registros]}` de uma única transação readonly, resolvida em oncomplete.
- `await App.DB.atomic(stores, (draft, transaction) => resultado)` lê arrays de todas as coleções selecionadas dentro de transação readwrite; callback altera `draft[colecao]`, e apenas os arrays alterados são regravados em conjunto. Arrays JSON inalterados não geram escritas. Callback DEVE ser síncrono; Promise/throw/request error/abort rejeitam com rollback. A Promise externa só resolve após commit. Não fazer await externo dentro do callback. As coleções devem ser não vazias, existentes e sem nomes repetidos, como exigido pela própria API IndexedDB.
- `App.Validation.validateData(data)` valida o dataset inteiro e retorna o mesmo objeto ou lança Error. `settings`, `ranges`, `integer`, `isISO` também ficam públicos para feedback antecipado; serviços continuam sendo a autoridade final.
- `App.Backup.validateBackupData(stringOuObjeto)` retorna cópia validada do envelope ou lança Error. `validateBackupFile(fileOuString)` mantém a API existente e chama a validação completa. A UI deve validar ANTES de construir resumo/usar exportedAt. Não confiar em um objeto fornecido diretamente a showImportSummaryModal.
- `await App.Backup.createSnapshot()` retorna `{application,schemaVersion:1,exportedAt,data}` consistente, sem download. `exportJSON()` baixa esse snapshot e devolve o envelope; atualiza lastBackupAt após o download.
- `await App.Backup.importJSON(envelope, 'merge'|'replace')` sempre revalida. Retorno: `{mode, inserted, updated, skipped, conflicts:[{store,id,reason}], applied}`. Replace é uma transação única. Merge compara version e updatedAt/createdAt/timestamp: qualquer retrocesso é contado como skipped; revisão igual com conteúdo diferente gera conflito; duplicidade de negócio entre IDs diferentes gera conflito. Qualquer conflito deixa TODO o candidato sem aplicação (`applied:false`, inserted/updated zerados). O banco existente permanece intacto; UI deve mostrar conflitos/skipped e só anunciar sucesso aplicado se `applied:true`. Dados inválidos lançam Error sem escrita.
- `App.AlarmEngine.onTick = async state => {...}` é callback opcional aguardado. Também dispara `window` CustomEvent `alarm-engine-tick`, detail `{now,triggeredIds,channels:{audio,visual,notification}}`. Permite atualizar contadores/canais/estado sem renderizar páginas inteiras por segundo. Os pilares de áudio/notificação e timers existentes já são atualizados no tick.
- `App.AlarmEngine.channels(event,settings)` fornece disponibilidade efetiva; `due(event,settings,now?)` permite leitura da elegibilidade. fireAlarm ignora snapshot desatualizado e relê a linha transacionalmente.
- `App.Service.clearAllData()` é limpeza EXPLÍCITA, transacional de todas as dez coleções mais errorLogs: apaga inclusive histórico e configurações, recria consoles, faixas padrão e settings com C04 selecionado. UI deve tratar como destrutiva e oferecer backup conforme fluxo autorizado.
- `App.Service.loadDemoData()` é transacional, exige catálogo operacional vazio (sem UOs/dutos/eventos), preserva os seis exemplos originais, quatro UOs REFAP/TEDEP/REPLAN/TEBAR, dutos OSCAN/OSBRA/DTCS, quatro tipos/TAGs e seis vínculos. Inclui previsão PIG e evento concluído. Base ocupada causa Error claro, sem misturar demonstração com dados reais. UI decide backup/limpeza explícita antes de chamar. Não repetir silenciosamente.

## Testes e evidências

Todos com Python Playwright, `chromium.launch(channel='msedge', headless=True)`, novo browser context temporário, servidor/origem temporários e timezone America/Sao_Paulo. HTML temporário combina os cinco blocos atuais; nunca chama build_all global. Banco IndexedDB é real. Abort é injetado no sucesso de requests reais; apenas falhas visuais são simuladas quando necessário. Nenhum perfil persistente real é usado.

- RED inicial: `task1-red.txt`: 15 testes, 13 falhas, 1 erro de produção (formatDate recebendo Date fazia split), 1 teste de abort inicialmente falso positivo por exceção do próprio harness. O harness foi corrigido. `task1-commit-baseline-red.txt` reconfirma contra originais que abort após request successful retornava `[false,null]`, ou seja, Promise resolvia apesar de rollback. A falha esperada agora é demonstrada sem o erro de harness.
- RED ampliado: `task1-expanded-red.txt` e `task1-final-red.txt`; este último 29 testes, falhas de CSV com inativos/texto e coleção inválidos, além de whitelist industrial. As falhas foram corrigidas. Um erro intermitente inicial de setup vinha de começar fixtures antes de initDefaults terminar; o harness agora aguarda o log de inicialização completa.
- RED áudio zero: `task1-audio-zero-red.txt` confirmou 7 osciladores reais criados pelos quatro timbres com volume zero; guard antes de unlock/criação e canal indisponível com volume zero corrigem o problema.
- RED focados: `task1-calendar-red.txt` prova deslocamento de data simples para dia anterior; `task1-demo-red.txt` prova a regressão temporária de simplificar a massa original (restaurada); `task1-types-red.txt` prova aceitação indevida de números persistidos como string, corrigida para impedir versão concatenada.
- GREEN final: `task1-green.txt`: **30 testes, 0 falhas, 0 erros, 22.303 s**. Cobrem datas, CSV/BOM/fórmulas/tombstones, referências e inativos, zero, atores, snooze, reabertura, abort do CRUD e de import com rollback, backup malicioso/incompleto/duplicado/órfão, snapshot legado, merge antigo e duplicidade de negócio, dois ticks e duas abas, conclusão concorrente, falha visual com log e massa demo completa. WebAudio real confirmou os quatro timbres com volume 0/NaN sem criar osciladores.
- `python -m compileall -q parts_js_core.py parts_js_service.py tests/test_core_browser.py`: sucesso.
- Suíte geral solicitada pelo TDD foi executada antes da conclusão visual: `task1-suite-integrada.txt`: 60 testes, 21 falhas e 4 erros. Os erros de fixture ligados à massa demonstrativa simplificada foram corrigidos restaurando os exemplos. Registro não é apresentado como GREEN geral.
- Após restauração: `task1-workflows.txt`: **8 workflows, 7 passam, 1 falha**: `test_browser_rotation_keeps_form_and_drawing` (aspect ratio bitmap 2.727 vs CSS 6.018), atribuído a Tasks 2/3. Jornada criar→concluir→reabrir→duplicar, inserção consecutiva, busca PIG, downloads, modos/temas, offline e reconhecimento/snooze passam.

Falhas UI da suíte geral, pendentes das Tasks 2/3: test_action_sheet_has_context, test_alarm_counts_agree, test_alarm_modal_countdown_moves, test_all_dialogs_and_controls_have_accessible_names, test_cancel_import_discards_old_file, test_cancelled_confirmation_never_executes, test_cancelled_dependency_never_executes, test_category_survives_layout_change, test_closed_drawer_not_in_tab_sequence, test_demo_button_actually_loads_demo, test_description_is_multiline, test_details_shows_saved_drawing, test_drawer_opens_and_closes_by_keyboard, test_filters_are_bottom_sheet_on_mobile, test_metrics_apply_correct_time_filter, test_modal_moves_and_traps_focus_and_restores, test_new_master_data_appears_in_filters, test_settings_keep_zero_values, test_tablet_detail_initial_content_and_alarm_value. Erros gerais registrados: test_completed_cards_really_expand, test_temporal_classification_updates_without_action, test_create_complete_reopen_duplicate_journey e test_save_and_another_preserves_location; os dois últimos já passam no rerun workflows após restauro. Falha geral test_search_filter_sort_and_clear também já passa após restauro. Os testes UI restantes precisam rerun após Task 2; não foram ocultados ou ajustados para aceitar demo reduzida.

## Limites e decisões

A primitive atomic regrava arrays das coleções selecionadas; prioriza consistência para o aplicativo offline e pode ser custosa com bases muito grandes. Validação estrita não corrige silenciosamente bases legadas que já contenham órfãos/incompatibilidades produzidas por bugs antigos; preserva os dados e acusa a inconsistência. Merge conservador não mescla campos de duas revisões; relata conflitos para intervenção do usuário. errorLogs não entra no backup v1 por compatibilidade do formato legado. A normalização optional de metadados segue o que o exportador antigo realmente produzia.

Teste de duas abas usa navigator.locks disponível no Edge. Fallback lease está implementado e a checagem transacional final impede duplicidade de claims mesmo se houver disputa do lease; o ramo com navigator.locks desabilitado não foi exercitado separadamente nesta suíte. Som físico, permissão de notificação concedida pelo sistema, tela bloqueada e aparelho físico não são declarados testados. A emissão externa de áudio/notificação não pode ser parte de uma transação IndexedDB; a decisão e o registro inicial são atômicos, canais concluídos são anotados depois e há nova checagem antes de cada canal.


## Revisão Task 1 — Fix round 1/5

Os três achados Important de `revisoes/task-1-review.md` foram reproduzidos pelos novos testes antes da mudança e corrigidos. A revisão de código foi tratada com o workflow receiving-code-review; cada alegação foi conferida no código e em IndexedDB real. Escopo preservado: apenas os dois geradores do núcleo/serviço e seu teste; nenhuma edição em UI, CSS, HTML ou index.html.

Patch desta rodada exclusivamente contra o snapshot anterior ao fix: `revisoes/task1-fix1.diff`, base `revisoes/task1_r1_base/{parts_js_core.py,parts_js_service.py,test_core_browser.py}`. Não confundir com o diff inicial contra originais. Self-review desta rodada conferiu que não há mudanças fora dos três achados e da explicitação do contrato do lease.

### 1. Backup preventivo antes da substituição

`importJSON(...,'replace')` primeiro valida o arquivo inteiro, depois aguarda `exportJSON({preventive:true})` e somente então abre a transação de substituição. Falha de export ou de download rejeita o replace; nenhuma coleção, registro de settings, lastBackupAt, version ou updatedAt é alterado. O teste compara as onze coleções, incluindo errorLogs, antes/depois das duas falhas.

API adicional: `exportJSON(options={})` aceita `{preventive:true}`. Nesse modo apenas lê snapshot consistente e aguarda downloadBlob; não salva settings/lastBackupAt nem chama callbacks visuais. Exportação normal sem argumentos conserva seu comportamento. downloadBlob pode retornar Promise; exportJSON agora a aguarda. O teste positivo também confirma que o snapshot preventivo contém o evento original e que o original ainda existe quando downloadBlob termina, antes de a substituição removê-lo. O navegador não expõe ao JavaScript comum a confirmação da gravação final do arquivo pelo sistema operacional; a garantia observável é falha síncrona/assíncrona reportada pelo contrato de export/download, sem antecipar a substituição.

### 2. Esquema explícito e campos funcionais obrigatórios

A validação agora exige presença própria dos campos por coleção; undefined e null não substituem um campo funcional obrigatório. Exceções nullable são explícitas: equipamento/TAG opcional, adiamento, último disparo e dados de conclusão do evento; previousValue/newValue do histórico.

- Consoles e UOs exigem id, name, active, createdAt, updatedAt, version, synchronizationStatus; dutos também consoleId e tipos também uoId.
- TAGs exigem id/tag/uoId/equipmentTypeId e os metadados operacionais de catálogo.
- Vínculos exigem id/pipelineId/uoId/createdAt/version/synchronizationStatus; updatedAt/active nunca foram exigidos porque o produtor legado não os escrevia.
- Eventos exigem referências (incluindo chaves opcionais nullable), descrição/notes/prioridade/status, data/hora/timestamp, hasAlarm, useDefaultAlarmSettings, antecedentes/canais/repetições/intervalo/limite, alarmState, alarmSnoozedUntil, alarmTriggerCount, lastAlarmTriggeredAt, dados de conclusão e metadados active/createdAt/updatedAt/version/synchronizationStatus.
- Histórico exige id/eventId/action/timestamp/description/previousValue/newValue/localUser.
- Faixas exigem id/name/color/minMinutes/maxMinutes/priority/blink/sound/active.
- Settings exige key/value; value exige os controles funcionais de alarme e identidade: localUserName, soundEnabled, soundType, soundVolume, visualAlertEnabled, notificationEnabled, repeatAlarm, repeatIntervalMinutes, maxRepeats e defaultLeadTimeMinutes. Preferências visuais posteriores continuam podendo usar defaults.

Compatibilidade legítima distinta: createdBy/completedBy/stylusDrawing em eventos, unit em faixas e metadados createdAt/updatedAt/version/synchronizationStatus em faixas/settings continuam opcionais. O teste remove os campos obrigatórios individualmente de todas as dez coleções e exige rejeição; depois omite hasAlarm/alarmTriggerCount e confirma importação rejeitada com base intacta. Também remove os metadados legados opcionais e confirma arquivo aceito.

### 3. Tick ocioso sem escritas no IndexedDB

`tick()` usa um snapshot consistente de events/settings para pré-filtrar due; somente candidatos chegam a fireAlarm. O claim mantém a releitura e a checagem due dentro da transação final, que continuam protegendo conclusão/reconhecimento/claim concorrentes.

`App.DB.atomic` agora compara a representação JSON inicial/final de cada array e só clear/add nas coleções alteradas. Callback no-op ou claim invalidado por concorrência não regravam os arrays. O contrato de callback síncrono/commit/rollback permanece; a primitive opera sobre os registros JSON do aplicativo.

O novo teste desabilita alarmes na massa de seis eventos, instrumenta os métodos nativos reais add/put/clear/delete e executa tick, atomic no-op e fireAlarm de concluído. Antes: 128 chamadas de escrita nesse conjunto; depois: **zero**. Leituras e checagem de elegibilidade permanecem, sem regravar settings ou auditoria ociosamente.

### Decisão fundamentada sobre lease

Foi mantida a alternativa advisory explicitamente permitida no pedido desta rodada. navigator.locks fornece exclusividade real de callbacks quando disponível. O fallback localStorage apenas reduz concorrência; não é mutex, não tem garantia de fencing e não promete exclusividade de callbacks ou de entregas de eventos diferentes. O comentário do código e este contrato substituem qualquer interpretação anterior de exclusividade do fallback.

A autoridade para exclusão de CLAIMS do mesmo ciclo é a transação IndexedDB em events/eventHistory/settings: cada aba relê o evento e reavalia due após adquirir a transação readwrite; somente a primeira elegível grava incremento e auditoria. A segunda encontra o novo estado/instante/contador e não grava. Conclusão/reconhecimento usam stores em comum e não são sobrescritos por snapshots antigos. A decisão evita introduzir locks runtime com expiração em errorLogs, misturar diagnóstico com coordenação ou prometer exclusividade externa que um lease expirável não asseguraria. O teste de compatibilidade existente exercita duas abas com navigator.locks desabilitado; ele prova o cenário de claims, não todos os interleavings de callbacks.

### Comandos e resultados desta rodada

RED focado (com Python Playwright/Edge/IndexedDB reais e HTML temporário):

`python -X utf8 -m unittest discover -s tests -p test_core_browser.py -k preventive -k functional_fields -k zero_native_writes -v`

Resultado: **3 testes, 3 falhas esperadas**, 22.101 s. Evidência: `resultados/task1-fix1-red.txt`. Os testes falhavam por backup preventivo não chamado, campos omitidos aceitos e escritas nativas ociosas; não houve erro de harness.

GREEN completo do núcleo:

`python -X utf8 -m unittest discover -s tests -p test_core_browser.py -v`

Resultado: **33 testes, zero falhas, zero erros**, 85.700 s. Evidência: `resultados/task1-fix1-green.txt`. São os 30 anteriores mais os três novos, preservando regressões de abort/rollback/merge/datas/zero/histórico/duas abas/demonstração. `python -m compileall -q parts_js_core.py parts_js_service.py tests/test_core_browser.py` também terminou com sucesso.

A suíte integrada de UI/layout e as limitações físicas continuam sob coordenação das Tasks 2/3; as falhas históricas acima são evidências da fase anterior, não um novo resultado global após este fix. Status desta entrega: **DONE_WITH_CONCERNS**, somente pelo contrato advisory do fallback e pelas integrações externas ainda sob revisão. Os três Important foram corrigidos e estão GREEN.

Verificação adicional após fix1: `python -X utf8 -m unittest discover -s tests -p test_compatibility_browser.py -v` — **3 testes GREEN, 9.911 s**, incluindo duas abas sem navigator.locks. Log: `resultados/task1-fix1-compatibility.txt`. Isso atualiza a evidência de fallback da rodada anterior e não altera sua classificação advisory.
