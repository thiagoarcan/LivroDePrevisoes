# Task 3 — Layout integral, semântica e apresentação coordenada

Leia primeiro este brief, depois task-2-report.md (contrato final da UI), task-3-layout-proposta.md (composição aprovada pelo coordenador) e spec docs/superpowers/specs/2026-10-25-correcao-integral-design.md.

## Escopo
Implementar parts_css.py e parts_html.py. Pode criar parts_js_presentation.py para App.Presentation e incorporar sua string ao final de JS_UI em parts_js_ui.py (somente import/concatenação Python; não reimplementar métodos Task2). JS_UI exportado deve conter a apresentação para que os cinco blocos de build_all e testes existentes continuem suficientes. HTMLfinal permaneceúnico e offline. Semeditarcore/service/index. Não spawn.

## Objetivo visual inegociável
Usar a área útil da tela para contexto verdadeiro, listas e detalhes coordenados, sem alargar desnecessariamente campos, textos e cartões e sem grandes regiões mortas quando existem dados úteis. Não resolve apenas removermax-width nem esconderoverflowdo body. Ver proposta9visões×5tiers; use prioridadeoperacionalDOCX e Designer.pdf/Designer(1).pdf/Designer(2).pdf. Capturasrenderizadas em auditoria_interface/referencias. Nãoinvente dados,gráficos ou conteúdo repetido para preencher monitor.

## Contrato final de UI
Task2 expõe app-ui-update {reason,view,eventId?} e App.UI.getPresentationState() → {snapshot,settings,ranges,view,activeConsoleId,pending,completed,selectedEventId,spotlightEventId,category,tier,metricFilter,filters,classifyEvent}. App.UI.formatCountdown(timestamp) dá {text,isOverdue} comsegundos. App.UI.init chama App.Presentation.init se definido, antes do motor. Apresentação escutaevento+input/change,sem polling paralelo e semmonkeypatch dezmétodos.
Auto:data-layout-mode mobile<768,tablet<1200,conventional<1920,widescreen<2560,ultrawide>=2560. Compacto classe density-compact sobre tierauto; layout-narrow quando viewportfísico<768protegequalquermodoforçado. --app-header-height é medida porResizeObserver doUI. Modais gerenciadosporopenModal/closeModal,foco/inert/stack;adaptação usa attrs e classes existentes.
ClassespreferidasHTMLbottom-nav-item/bottom-nav-fab/bottom-nav-badge,cadastros-category-btn,completed-card-details. NovosUI IDs pendingPagination/completedPagination nav.events-pagination,btnClearCompletedScope;classe.detail-navigation; body.disable-pulsing/disable-highlight/keyboard-open/layout-narrow. inputBackupReminderDaysnumber1–3650jáinjetado seausente,adicionarfonteHTMLsemduplicar. Canvasbuffer1200×440,UIwidth100%heightautoaspectRatio;nãoforçarminheightqueestique. Modal fullscreenboxStylusCanvas é gerenciadopelamesmastack.

Contexto do dashboard deve usar snapshot.events (ativos/pendentes e console relevante), não state.pending de uma listagem filtrada anterior. state.pending/completed representam os filtros de suas respectivas visões. Tratar snapshot como readonly; usar cópias para sort. Seleção adicional de dashboard pode pertencer a App.Presentation sem alterar spotlightEventId/timestamp. Não derivar o próximo evento de uma lista de outro contexto.

## Trabalho por componente
- Shell: app-nav lateralreal no desktop,rail/drawer tablet,cabeçalho móvelcompacto(~2linhas),console/sino/menu sempreacessíveis,barra inferior4destinos estilizados. Não duplicar IDs para header/nav. Sidebar desktop208–240px,max300. mainwidth100%max-widthnone,min-width0. Backup/layoutwarningssecundários não ocupam váriasbarrasfixas. Alarmbannersempreabaixoheaderreal,sem top52fixo.
- Dashboard:declararregiões e distribuirSpotlight,alarmes,listaurgente/detalhe e panorama realporfaixa/duto/console; wide3regiões,ultra4quandoháconteúdo. Setemétricascompactas,contador28–36pxnormal,descriçãomax65–80ch,Spotlight<=1100pxem3440. Semcardalto sóparaencher. Alarme/estado/tempojuntos,Reconhecerprincipalquando triggered eaçõessecundárias nomenuemcelular.
- Nova previsão:textarea descrição;fieldsetslocalização/programação/atividade/alarme/lousa;keepDutoUOeaçõesclaras;footersticky semobstruircampo;gruposcustomalarme/observaçõesexpansíveis. Emwide/ultra usarpreviewnão salvo e eventosrelacionadosduto/UO,semcampo1800pxouformestreitocentralcom2kmargem.
- Pendentes:tabela ecardsemwrappermestrecomum dentrogridlista/detalhe; detalheaparecequandoespaçopermite;filtrosem sheet mobile; contexto/relacionados/históricoselecionadonasáreasadicionais. Toolbarsemmin-widthrígido. Paginaçãoacessível.
- Concluídos:cardscompactosexpansíveisnomobile,novecolunasemwrapperinternododesktop;resumo/período/detalhe/históricoreais emtelasgrandes. Açõesdestrutivasseparadas.
- Cadastros:categoria→lista→formnomobile;duasregiõesnotablet;categoria/lista/editor/vínculosemwides. Pode moverformstableIDs paragroupsnovospreservandolistenerseformIDs. Nãoapenasocultarumhubdejanelagrande. Novo/editar/voltarlistaclaros.
- Alertas:gruposdetails/summary commesmoform;testesompertotimbre/volume,notificaçãopertopermissão;previewdeediçãoestatusreais;camposalinhadossemmin280queestoure320.
- Cores:lista/cadeia,editor epreviewdaedição;préviaéexemplo,nãodadosfictícios;nome/faixa/textoalémcor;evitarpainelaltovazio.
- Backup:export/import/CSV/statuslocal emregiõesúteis;demonstração/limpezaseparadas;prévia segurausaresultadooficial;mostrardownload/integridadeclaramente.Semarquivo,darsóorientaçãocurta.
- Diagnóstico:status/coleções/logsemregiões;lógicasmóveislistadasemcards/tabelaresponsiva;copiarfunciona;metadadosreais,semfalsozerodeerro.

## Semântica e estética
Fonteprincipal16px,auxiliar14px,camposmin48pxmobile/tablet,botõesprincipais48px,ícones44×44,labelsdecheckboxacionáveis;densidadecompactanãodestróioperação. Estilosdecomponentescentralizados;limparinlinefont/widthqueimpedeCSS,manterinlinevisibilityJSatécoordenar. Todosinputs/select/textarea têmnomerealassociado;10dialogsaria-labelledby;fecharsimbólico temaria-label;SVGdecorativoaria-hidden;metricasnativasbutton;navpáginacomaria-currentorpatterncompletotabs. Não usarlabelgenérico paraenganarteste.
Temasescuro/claro/industrial consistentes;primaryindustrialamarelo/preto,escuro/claroazuladequado;tokensdelegibilidadeparaSpotlight/timers/badges/navegação. Eliminarcoresfixasclarasemfundoclaroe#991b1btextosobreescuro. Textocustomfaixanãopodeficarilegível;usarfaixacomoborda/marcadoreretextotokenlegível. Movimento reduzido epreferências disablepulsing/highlight respeitadas. Safeareas ealtura100dvhcomfallback,modalbodyrolável efooter/headeracessíveisaté844×390;nenhumconteúdoforatela no320.

## Testes e entrega
TDDREDlayout járegistrado102verificações(64falhas) e5a11y(4falhas). UI24tem22pass+2HTMLesperadas;workflows10GREEN,controller9emfinalizaçãoTask2. Rodar tests/test_layout_browser.py --quick;depoisfull --screenshots. Matrizfull19larguras×7modos×9visões +auto/nav/3temas/10modaisem5tamanhos. RootcomplementaráFirefoxnativoheadless;script tests/test_firefox_native.py --quick jáexercitaGecko153semwebdriver eperfisreais.
Rodar tambémUI/a11y/workflows para não quebrarcontratos. Testesharnessbrowser_support criaHTMLtemporáriousandoos5blocos;novomódulodeveestarincluídoemJS_UI. NãoaumentartimeoutsnemrebaixaraceitesparaforçarGREEN. SeaparecerbugJSdaTask2notificarcoordenadorcomteste,semcorrigirforaescoposemcoordenação.
Salvar report task-3-report.md,contratos/painéis/testes/capturas e diffsourcescontraoriginais. Produtoemroot,nãooutrascópias. Evidências novas emrevisao_interface_2026_10_25/resultados;preservarauditoriaanterior. Não tocarbasedousuário.
