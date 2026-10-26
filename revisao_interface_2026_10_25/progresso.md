# SDD ledger — plan: docs/superpowers/plans/2026-10-25-correcao-integral.md

Autorização: pedido explícito de todas as correções e testes, com documentos e auditoria já definidos.
Ambiente: pasta sem Git; originais preservados em originais. Worktree/commits inaplicáveis. Revisões usam diff contra snapshots.
Pré-voo: Task1 produz serviços preservando assinaturas para Task2. Task2 publica contrato de IDs/classes para Task3. Task3 mantém todos controles funcionais e reporta novas interfaces para integração. Sem edição concorrente de arquivos de produto.

| Tarefas | Interface/escopo comparado | Resultado |
| --- | --- | --- |
| 1 consigo | core/service e testes específicos; mesmo DB e formatos válidos antigos | Coerente; transações devem preservar históricos |
| 2 consigo | JS UI e regressões; marcação semântica delegada à Task3 | Coerente; publicar contrato IDs/classes |
| 3 consigo | CSS/HTML e composição, sem duplicar controles | Coerente; módulos adicionais apenas se necessários |
| 4 consigo | Build, matriz e revisão final | Coerente; não sobrescrever auditoria histórica |
| 1 → 2 | Assinaturas de serviços, importJSON e onTick | Preservar assinaturas; documentar retornos adicionais no relatório Task1 |
| 2 → 3 | Classes/IDs dos modais, navegação, filtros, detalhes e formulários | HTML pode mover elementos preservando ID e listeners; sem edição simultânea |
| 1/2/3 → 4 | Cinco geradores e APIs para suíte integrada | Testar HTML temporário durante implementação; regerar index no final |

Task 1: em andamento — testes RED e implementação por agente, revisão independente na conclusão.
Regressão layout original: 102 verificações rápidas, 64 reprovações (log layout_red.log), cobrindo 4 larguras e nove visões.
Regressão UI original inicial: 23 testes; harness corrigido para seletor de métrica, evento visível e range input. Reexecução de RED usa snapshot original via PREVISOES_TEST_BASELINE para evitar mistura com core em edição.
Task 1: implementação inicial30/30GREEN; revisãoindependente solicitou3correções:backup preventivo replace, campos obrigatórios no backup e zeroescritasemtickocioso. Fixround1/5 emandamento; base emrevisoes/task1_r1_base.
Ruling: exclusão transacional de claims é obrigação operacional; lease precisa garantia condizente com descrição, sem migração destrutiva. Interleaving do lease não demonstrou duplicação de evento com claim atômico. Fallback no navegador sem navigator.locks passou3/3compatibility; manter ensaio na suíte final.
Ruling: UI/HTML/CSS só começam após revisão do núcleo; testes gerais antes disso têm falhas esperadas discriminadas. Não alterar expectativas para aceitar regressões da massa demo; massa original foi restaurada antes doGREEN.
Task 1: fix round1/5 —3Important ADDRESSED,0abertos; revisãoescopada aprovada (revisoes/task-1-fix1-review.md).33core+3compatGREEN. Backup preventivo restaura proteção; backup exige camposfuncionais; tickocioso0escritas. Task1complete.
Task1minor(deferred): móduloslegados e overridesativos coexistem; mudança funcional isolada facilita comparação,consolidação futura exige revisão própria. Não é defeito operacional conhecido.
Task1Ruling: fallbacklocalStorage é advisory; exclusão de claims e preservação de conclusão são transacionais no IndexedDB. navigator.locks fornece exclusividade de callbacks quando disponível. Não prometer mutex no fallback.
Task 2: em andamento — consumo dos contratos finaisTask1,23regressõesUI e10workflows+5acessibilidade.
Task2 inicial:84testes=79pass+5HTML/CSSprevistos;revisãoencontrouC1eventoerradoemcorridamodal, I1resizelistaconcluídos eI2cache/hookscadastro. Fixround1/5despachado; baserevisoes/task2_r1_base.
Ruling Task2M1: falsosinalkeyboard-openemzooméload-bearingparaCSSdaTask3. Corrigirantesdoconsumidorocultar navegação, emvezdedeferiruma regressão previsível. Probecaptura escala2semcampoemfoco;nãofoialeghadonavegaçãoperdidaantesCSS.
Task 2: fix round1/5 — C1/I1/I2/M1 ADDRESSED; revisãoescopada APROVADA (revisoes/task-2-fix1-review.md). Suite94=89pass+5HTML/CSSprevistos,0errors;controller18/18,workflows11/11. Task2complete,semCritical/Importantaberto.
Task 3: em andamento — layoutintegralHTML/CSS/App.Presentation conformebrief/proposta;preservarcontratoUI.

Task3 intermediário: discovery100/100GREEN pelo implementador (100 inclui4Presentation,1jornadaeditar e1toque novos). Matriz completa ainda em correção; não é gatefinal. Raiz adicionou testes/verify_reference_integrity.py (22/22GREEN contra hashes históricos), verify_distributed_artifact.py (RED esperado: indexaindaoriginal), hashes+sources_stable nasmatrizes, briefrevisãoTask3/integral e resolucoes_propostas.json semgatefinal. Observaçõesvisuais eminvestigação: alarmeultrawide/footerecaptura, toolbarfullscreen, stickyMobile, avisosdadolocal. Task3fontesexclusivasdoimplementador.

Task2 reaberta fixround2/5: raizreproduziu I3(GUI37) controlador concluído ausente usa createdBy indevidamente emtabela/cards; legado/importação completedBy:null mostra criador comoexecutor. RED emresultados/ator_conclusao_red.log, teste test_missing_completion_actor_is_not_replaced_with_creator. Base snapshotrevisoes/task2_r2_base. CorreçãoescopadaUIPart,semconflitocomrevisãoTask3(CSS/HTML/Presentation/concat) emandamento.

Task2 fixround2/5: I3 ADDRESSED, revisaoescopadaAPROVADA(revisoes/task-2-fix2-review.md),44/44GREEN,zeroquebranovapatch. FonteUIsó2expressões;GUI37nãoinfereexecutorapartirdocriador. Task2completeoutravez.

Task3revisãoinicial: REPROVADA,6Important+3Minor,0Critical. Importants:aliasmodaisclaro1.036contraste;gridwideáreamorta;Alertasavisoesticado;M:Nvínculofalso;tablesletraporletra;Backupmobileduascolunas. REDraizquality10/10falhas0erro. X1rootconfirmed:PresentationcompletedBybrancogeralacuna, ator_presentation_red.log.
Ruling Task3M1/M2/M3: usuárioautorizaTODAScorreções epropostaprevêconsolelegível, avisolegivelefiltrosConcluídosrecolhíveis; trataros3Minorcomocorreçõesmandatóriasescopadas namesmarodada, nãodeferir. Custoseerrado:pequenaalteraçãoapresentacionaladicional;IDs/estado/regrasdevempermanecer. Task3fixround1/5iniciada,base task3_r1_base.

Task3 fixround1/5:10/10ADDRESSED(I1-I6,M1-M3,X1),0Critical/Important/Minoraberto;APROVADO emrevisoes/task-3-fix1-review.md. Rerunindependente18/18. Fontescongeladas;Task3complete. Task4integraçãoiniciada via tests/validate_delivery.py(build+artefato+refs+3legados+120suite+1651layout+Firefoxnative).

Task4integração120+1651+1229=3000GREEN,0falhas/erros/skips,mesmosource_hashes,distributedtrue,stabletrue. tests/validate_delivery.py9etapasPASS(build,artifact9/9,refs22/22,3legados,Edge120suite,Edge1651layout,Firefox1229). IndexSHA256fed01e3dd5d7ab61a6a2cf12cad974b7d2670c55ef326c112add9ff8c4d04768. Packagewhole-delivery.diff13181linhas;wholeReviewfrescoaindapendente. Gatedreportnãofoigerado;decisoes_entrega.jsonwhole_reviewFALSE.

WholeReviewREQUESTCHANGES:0Critical,4Important(I1railtablet,I2clock/audioocultos,I3editorlousapaisagem,I4açoesmóveis),M1versãodrawerparacorrigir,M2overridesdívidaconhecidaACEITA(nãobloqueia). Reportrevisao-integral.md confrontou321DOCX+22visuais. RootRED6/6fail0error test_final_findings_browser.py noHTMLdistribuído;baseline final_fix_base. UMAfinalfixwave despachada todalistacompleta;gatewhole_reviewFALSE e structuralfalse+6resoluçõespendentesatéregressãofinal. NãoháaprovaçãofinalnemRELATORIO_FINALainda.

FinalfixwaveX2rootconfirmed(GUI37,mesmometaDrawerM1):labelDrawerUsermantémOperadorapósreloadmesmocomlocalUserNameControladoraMaria. Headercorreto;reloadPreferences/edituserjáatualiza, initomitia. Test_final_findings_browseragora7RED/7fail0errorsnoindexbase,reportintegral_final_wave_red.log. Trabalhadoravisadoparacorrigirnamesmawave;suíteesperada127. Semnovatarefa/persistência/refactor.

ENTREGA CONCLUÍDA: finalfixwave6/6ADDRESSED,0Critical/Importantnovos,revisoes/revisao-integral-fix-review.md;M2dívidamanutençãoaceita. Revisorindependente11/11distribuído+foco/geom ehashstable. Pipelinefinal9/9PASS131+1651+1229=3011/3011,zeroerro/falha/skip,samesourcehashindexf6ae6e81325747394ff2b06147fbc79ed5426989cf74b02818d5f030edd9c12b. GatesallTRUE;40resoluções(39corrigido+GUI38decisaodocumentada),RELATORIO_FINAL.html/.md eCSV+resumo_final.jsongerados. Gallery102capturas(70matrix+32Task4)comlinksvalidos;verify_final_report.pyPASS6checks(incluib uscaGUI10+restauração40+imagemcarrega+zeroPageError). PlanoTask4todochecked. SemGit:nenhummerge/push/menu/remoçãoworkspaceaplicável;produto/artefatospreservados. Nenhumaediçãoprodutoapósúltimopipeline. Limitesfísicosnofinalreport;5decisões/custosdecisoes_tecnicas.jsonincluídas. Finaluserdeveserauto-contidocomlinksapp/report econtagens,escopofinito,nãoprometer100%codecoverage.
