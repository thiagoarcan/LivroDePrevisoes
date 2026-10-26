# Correção integral — aplicação 1.2.0

25/10/2026 — Horário de Brasília

A aplicação foi corrigida mantendo o arquivo HTML único, o funcionamento offline e a base IndexedDB. Os testes utilizaram origens/perfis temporários; os dados do usuário e os documentos de referência foram preservados.

A composição usa navegação lateral em monitores, rail compacto no tablet em paisagem e topo móvel com relógio e aviso condicional de áudio. Editor e lousa ficam paralelos quando há largura útil. Campos e textos mantêm largura de leitura; a área adicional apresenta listas, detalhe selecionado e contexto real, sem dados inventados para preencher a tela.

Os defeitos de integridade, alarmes, importação, cancelamento, identidade de diálogos, foco, filtros, resize, cache e desenho foram tratados e cobertos por regressões. Os registros abaixo identificam a resolução dos 40 grupos da auditoria.

100% dos cenários catalogados e executados nesta máquina; não é 100% de code coverage ou prova de ausência de todos os defeitos.

Core e UI passaram por revisão independente e correções escopadas. O fallback de lease apenas reduz concorrência quando navigator.locks não está disponível; a exclusão de claims de alarmes e a preservação de conclusões são garantidas pelas transações IndexedDB.

Estados sem registros mostram orientações e resumos compactos. Não se esticam cartões ou se inventam séries para preencher uma tela sem dados. Modos manuais respeitam a preferência; o automático distribui o contexto segundo a largura útil.

A revisão integral confrontou os 321 requisitos documentais e os 22 elementos visuais; os registros seguintes resolvem os 40 agrupamentos da auditoria. Isso não significa que existam 321 novos testes individuais. A coexistência de métodos legados e overrides permanece como dívida de manutenção aceita, sem defeito operacional novo identificado; sua consolidação exige tarefa isolada com as regressões preservadas.

| Bateria | Resultado | Evidência |
| --- | --- | --- |
| Comportamento no Edge | 131/131 | resultados/suite_final.json |
| Geometria, temas e modais no Edge | 1651/1651 | resultados/layout_completo.json |
| Compatibilidade e layout no Firefox instalado | 1229/1229 | resultados/firefox_resultado.json |

## Resolução dos achados

- **GUI-01 — corrigido:** Automático publica o tier efetivo em todas as larguras e recalcula a composição após resize; Compacto ajusta densidade sobre o tier automático. Evidência: test_layout_browser.py: auto-tier e navegação; test_ui_controller_browser.py: resize e modalidades; test_final_findings_browser.py; test_final_actions_browser.py; revisoes/revisao-integral-fix-review.md
- **GUI-02 — corrigido:** Cabeçalho e shell redistribuem controles conforme a área útil; tabelas têm rolagem local. A página não usa overflow oculto para mascarar controles fora da tela. Evidência: layout_completo.json; firefox_resultado.json; capturas final_*; test_final_findings_browser.py; test_final_actions_browser.py; revisoes/revisao-integral-fix-review.md
- **GUI-03 — corrigido:** Navegação inferior usa as classes do HTML, quatro destinos, rótulos e estado ativo; o fluxo de toque cria e conclui uma previsão. Evidência: test_workflows_browser.py: test_touch_mobile_creates_and_completes_from_cards; matriz mobile-navigation
- **GUI-04 — corrigido:** Faixa de alarmes acompanha a altura medida do cabeçalho. Reconhecer todos remove o disparo e preserva eventos pendentes. Evidência: test_layout_browser.py: alarm-banner-visible e banner-ack-all-does-not-complete-events
- **GUI-05 — corrigido:** Filtros móveis abrem como sheet gerenciado por foco/inert/stack, com contagem dos filtros e fechamento explícito. Evidência: test_ui_browser.py: test_filters_are_bottom_sheet_on_mobile; modais e teclado
- **GUI-06 — corrigido:** Spotlight mantém identidade e timestamp próprios, independentes dos filtros de Pendentes. Evidência: test_ui_browser.py: test_spotlight_keeps_own_countdown_after_filtered_list
- **GUI-07 — corrigido:** Contador do modal atualiza o timestamp do próprio alarme com precisão de segundos. Evidência: test_ui_browser.py: test_alarm_modal_countdown_moves e test_alarm_countdown_shows_second_precision
- **GUI-08 — corrigido:** Atualização temporal invalida criticidade, métricas e inclusão urgente ao cruzar limites; ticks ociosos evitam leitura/renderização completos e escritas desnecessárias. Evidência: test_temporal_classification_updates_without_action; test_idle_timers_do_not_read_or_render_pages; test_idle_tick_and_unchanged_atomic_issue_zero_native_writes
- **GUI-09 — corrigido:** Zero é preservado em antecedência, volume e repetição; volume zero ou inválido não cria osciladores. Evidência: test_settings_keep_zero_values; test_zero_default_lead_does_not_fire_fifteen_minutes_early; test_no_audio_nodes_for_zero_or_invalid_volume
- **GUI-10 — corrigido:** Cancelamento descarta callbacks; confirmação captura a identidade antes de operações assíncronas e protege ações em andamento. Evidência: test_cancelled_confirmation_never_executes; test_cancelled_dependency_never_executes; test_complete_identity_survives_interleaved_alarm
- **GUI-11 — corrigido:** Detalhes controlam o ancestral visível do desenho e limpam imagem residual ao alternar eventos. Evidência: test_ui_browser.py: test_details_shows_saved_drawing
- **GUI-12 — corrigido:** Detalhe inicial usa chaves normalizadas; seleção e modalidade são preservadas durante resize. Evidência: test_tablet_detail_initial_content_and_alarm_value; test_pending_modality_and_page_survive_resize_and_manual_tiers
- **GUI-13 — corrigido:** Resumo usa antecedência efetiva das configurações padrão ou específicas, inclusive zero. Evidência: test_tablet_detail_initial_content_and_alarm_value; test_zero_settings_and_event_alarm_reopen_without_defaults
- **GUI-14 — corrigido:** Painel lateral e contagem usam alarmes ativos disparados da mesma origem de dados. Evidência: test_ui_browser.py: test_alarm_counts_agree; capturas do painel e alarmes ativos
- **GUI-15 — corrigido:** Cartões concluídos recolhem/expandem com aria-expanded e preservam expansão ao trocar modalidade. Evidência: test_completed_cards_really_expand; test_completed_modality_changes_preserve_page_filter_selection_and_expansion
- **GUI-16 — corrigido:** Demonstração restaura a massa completa anunciada; substituição é explícita e protegida por backup preventivo. Evidência: test_demo_button_actually_loads_demo; test_demo_clear_and_backup_roundtrip
- **GUI-17 — corrigido:** Backup passa por validação estrita de esquema, campos, referências e imagem antes da prévia; texto importado não vira código executável. Evidência: test_backup_rejects_unsafe_metadata_and_missing_collections; test_backup_rejects_invalid_types_png_and_impossible_iso
- **GUI-18 — corrigido:** Substituição exige backup preventivo e aplica coleções em transação atômica; falha preserva a base anterior. Evidência: test_replace_requires_preventive_backup_without_metadata_side_effects; test_backup_replace_rolls_back_aborted_write; test_invalid_import_preserves_base
- **GUI-19 — corrigido:** Mesclagem não regride versão/timestamp; conflitos estruturados são apresentados sem falso sucesso e sem sobrescrever silenciosamente registros. Evidência: test_merge_does_not_regress_equal_version_older_timestamp; test_declined_import_reports_conflict_without_success
- **GUI-20 — corrigido:** CSV trata datas/horas locais e ISO, inclui BOM/separador e protege texto livre contra fórmulas; registros inativos são tratados explicitamente. Evidência: test_local_date_and_csv_formula; test_csv_download_bom_formula_and_inactive_filter; downloads de CSV
- **GUI-21 — corrigido:** Gerenciador central move/contém/devolve foco, torna o fundo inerte e limita Escape ao diálogo superior. Evidência: test_modal_moves_and_traps_focus_and_restores; test_alarm_snooze_escape_only_closes_top; leitura por leitor de tela não certificada
- **GUI-22 — corrigido:** Gaveta fechada fica inerte e fora da sequência de Tab; aberta controla foco e estado anunciado. Evidência: test_closed_drawer_not_in_tab_sequence; test_drawer_opens_and_closes_by_keyboard
- **GUI-23 — corrigido:** Campos têm rótulos associados; diálogos e controles de ícone recebem nomes acessíveis; IDs são únicos. Evidência: test_all_dialogs_and_controls_have_accessible_names; test_no_duplicate_ids_after_repeated_navigation; inspeção semântica
- **GUI-24 — corrigido:** Tipografia e alvos de campos/ações foram ajustados à orientação ergonômica; labels de checkbox participam da área acionável. Evidência: test_mobile_fields_and_main_actions_have_touch_size; capturas e revisão visual
- **GUI-25 — corrigido:** Descrição é textarea inicialmente vazia; formulário usa grupos operacionais, observações expansíveis e dois comandos explícitos de salvamento; Enter não submete acidentalmente. Evidência: test_description_is_multiline; test_description_enter_does_not_submit; test_new_event_has_operational_fieldsets; jornada edição; test_final_findings_browser.py; test_final_actions_browser.py; revisoes/revisao-integral-fix-review.md
- **GUI-26 — corrigido:** Layout usa safe-area e altura dinâmica; detecção de teclado considera foco editável e escala para não confundir pinch com teclado. Rotação emulada preserva valores. Evidência: test_pinch_zoom_does_not_claim_keyboard_and_editable_shrink_does; test_browser_rotation_keeps_form_and_drawing; teclado móvel físico pendente
- **GUI-27 — corrigido:** Lousa separa coordenadas lógicas 1200×440 da apresentação proporcional, preserva desenho e oferece fullscreen, undo, borracha e limpeza confirmada. Evidência: test_browser_rotation_keeps_form_and_drawing; test_canvas_undo_eraser_and_confirmed_clear; test_fullscreen_drawing_escape_returns_to_form; caneta física pendente; test_final_findings_browser.py; test_final_actions_browser.py; revisoes/revisao-integral-fix-review.md
- **GUI-28 — corrigido:** Categoria cadastral, seleção e rascunhos permanecem ao alternar modos e redimensionar a tela. Evidência: test_category_survives_layout_change; jornadas e revisão visual de cadastros
- **GUI-29 — corrigido:** Métricas usam botões nativos e abrem listas com o mesmo recorte temporal, incluindo dia local dos concluídos e limpeza do escopo. Evidência: test_metrics_apply_correct_time_filter; test_completed_metric_uses_local_day_and_can_be_cleared; test_metric_cards_support_keyboard
- **GUI-30 — corrigido:** Cadastros apresentam categoria, lista, editor e vínculos conforme o espaço, preservando formulários e regras de dependência. Evidência: test_master_forms_create_hierarchy_and_dependency_dialog; capturas final_*_viewCadastros.png
- **GUI-31 — corrigido:** Shell convencional usa navegação lateral persistente e área principal coordenada. Evidência: matriz desktop-sidebar; capturas final_1440_*
- **GUI-32 — corrigido:** Wide/ultra distribuem listas, foco, detalhe e contexto real. Formulários e cartões mantêm largura de leitura; estados vazios são compactos e honestos. Evidência: matriz whole-viewport-used/no-stretched-spotlight; capturas final_1920_* e final_3440_*; revisão visual
- **GUI-33 — corrigido:** Tokens dos três temas cobrem componentes, contadores, badges e navegação; cores de criticidade não são a única indicação e o texto usa tokens legíveis. Evidência: test_rendered_text_contrast_key_components; matriz de temas; capturas final_tema_*; luminosidade física pendente; test_final_findings_browser.py; test_final_actions_browser.py; revisoes/revisao-integral-fix-review.md
- **GUI-34 — corrigido:** Configurações usam grupos expansíveis e previews explícitos; preferências de destaque/pulsação são respeitadas junto com movimento reduzido. Evidência: test_display_preferences_actually_disable_pulsing; matriz reduced-motion; capturas de alertas/cores
- **GUI-35 — corrigido:** Alterações de cadastro publicam snapshot após commit e repovoam filtros, preservando seleção válida sem itens antigos. Evidência: test_new_master_data_appears_in_filters; test_five_catalog_toggles_publish_committed_snapshot; test_delayed_catalog_confirmation_publishes_only_after_commit
- **GUI-36 — corrigido:** Diagnóstico usa versão central, erros persistidos e lembrete configurável; avisos explicam armazenamento local e limitações de execução de alarmes no navegador. Evidência: test_async_visual_error_is_logged_without_loop; test_modes_and_themes_persist_after_reload; diagnóstico e textos revisados; test_final_findings_browser.py; test_final_actions_browser.py; revisoes/revisao-integral-fix-review.md
- **GUI-37 — corrigido:** Folha de ações identifica o evento; conclusões/histórico registram o responsável real ou declaram sua ausência. Evidência: test_action_sheet_has_context; test_zero_repeat_and_real_actor; jornadas de conclusão/edição; test_final_findings_browser.py; test_final_actions_browser.py; revisoes/revisao-integral-fix-review.md
- **GUI-38 — decisao_documentada:** Critério documental usa o conteúdo das três pranchas PDF distintas e breakpoints 768/1200/1920/2560 como decisão de composição. Diferenças de sufixos PNG e números ilustrativos são documentadas. Evidência: task-3-layout-proposta.md; auditoria_interface/dados/analise_referencias.md; integridade_referencias.json
- **GUI-39 — corrigido:** Listas renderizam apenas a modalidade necessária, com lotes de 50 e navegação pelo conjunto filtrado; resize preserva página e seleção. Evidência: test_pagination_keeps_all_data_but_one_modality_and_fifty_nodes; test_dashboard_urgent_list_is_bounded; tablet físico não usado como benchmark
- **GUI-40 — corrigido:** Diálogos seguem política explícita de cancelamento/fechamento e ficam protegidos durante gravação; ações destrutivas são separadas e adiamento tem limites validados. Evidência: test_async_confirmation_is_single_and_cannot_escape; test_snooze_out_of_bounds; testes de cancelamento, dependências e backup; test_final_findings_browser.py; test_final_actions_browser.py; revisoes/revisao-integral-fix-review.md

## Não verificado em aparelho físico

- Teclado virtual real, áreas seguras do sistema e rotação em Android/iOS físicos; viewport e visualViewport emulados não substituem aparelho.
- Caneta, pressão, rejeição da palma e nitidez física da lousa; mouse e eventos sintéticos de caneta/pressão/palma foram exercitados.
- Som audível nos alto-falantes e notificação exibida pelo sistema operacional; APIs, volume zero e ramos de permissão foram exercitados.
- Entrega de alarmes com tela bloqueada, suspensão ou navegador fechado; o produto informa essas limitações.
- Leitura por leitor de tela e luminosidade externa; nomes/foco/teclado e contraste amostrado foram verificados, sem certificação formal WCAG.
- Desempenho em tablet físico; paginação e volume de nós foram testados nesta máquina.

## Decisões adotadas e custos caso estejam erradas

- Preservar o banco e usar transações IndexedDB como proteção operacional dos disparos e conclusões, sem migração destrutiva. Custo se incorreta: Um erro no protocolo transacional poderia duplicar alarmes ou sobrescrever uma conclusão; regressões de concorrência e rollback exercitam esses casos.
- Concluir a revisão do núcleo antes de corrigir a UI/layout, mantendo identificadas as falhas esperadas e restaurando a demonstração original completa. Custo se incorreta: A execução em etapas poderia atrasar a detecção de incompatibilidades entre camadas; a suíte integrada e a revisão final verificam a composição.
- Tratar o lease localStorage como mecanismo auxiliar quando navigator.locks não existe, sem prometer exclusividade dos callbacks nesse fallback. Custo se incorreta: Callbacks podem concorrer nesse ambiente; a segurança de cada disparo depende dos claims transacionais, testados também sem navigator.locks.
- Corrigir a detecção de teclado para considerar foco editável e escala, evitando classificar pinch zoom como teclado aberto antes do novo CSS consumir esse estado. Custo se incorreta: Uma heurística incorreta pode ocultar navegação ou não reconhecer um teclado real; testes sintéticos cobrem a lógica, mas aparelhos físicos ainda precisam de ensaio.
- Incluir os três achados visuais classificados como Minor na correção: console completo, recomendação de dependência legível e filtros de concluídos recolhíveis. Custo se incorreta: Há uma pequena ampliação da alteração de apresentação; testes precisam confirmar preservação dos IDs, valores, foco e regras operacionais.

## Execução e rastreabilidade

Consulte TESTES.md, os JSON/CSV de resultados, as revisões e os hashes de fontes. Os logs RED são históricos de reprodução, não falhas da versão final.