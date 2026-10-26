# Auditoria estática contra o DOCX

Foram lidos 478 parágrafos extraídos e a tabela de breakpoints. A matriz registra 321 itens: parcial: 194, aderente: 101, nao_aderente: 23, nao_verificado: 3.

A unidade principal é parágrafo normativo ou item de lista. Obrigações compostas conservam o texto integral e recebem parcial se qualquer parte diverge. Exemplos não são cobrados como campos adicionais. Recomendações abertas são marcadas em natureza e não constituem falhas mandatórias. Os itens de síntese da seção 25 repetem requisitos anteriores e não devem ser somados como obrigações únicas. O arquivo cobertura_paragrafos_docx.json rastreia os parágrafos contextuais excluídos da contagem. Aderente significa código compatível encontrado; não certifica resultado em dispositivo real.

## Divergências por tela

- Geral: Automático não ativa CSS mobile/tablet; largura útil não considera altura, painéis ou densidade; conventional não cria navegação lateral. Referências de breakpoint do próprio DOCX divergem entre tabela inicial e seção 1.4.
- Cabeçalho/navegação: barra inferior apenas no modo manual; pílulas não reaparecem condicionalmente quando falham; tablet não tem sidebar persistente compacta.
- Painel: métrica 15/30/60 não aplica intervalo; unacknowledged filtra qualquer hasAlarm; Spotlight continua com muitas ações. Timer pode ser do primeiro evento global, em vez do evento do console ativo. Classificações não são recalculadas pelo updateLiveTimers.
- Pendentes: bottom sheet não recebe active-sheet; preferência table permanece no celular; ordem das informações diverge e ações secundárias continuam expostas. Badge ignora Apenas Console Ativo.
- Nova previsão: descrição input de linha única; grade não separa regiões localização/programação; barra sticky não trata teclado virtual; encadeamento inclui anúncios aria-live nos campos dependentes.
- Lousa: tela cheia opcional por segundo comando, sem bloqueio explícito de scroll do body; ferramentas não fixas; proporção e rotação precisam ensaio físico. Suporte pen, undo e confirmação estão implementados.
- Alarmes: ações explícitas e fechamento não reconhece; aviso inicial ausente e status omite limites de segundo plano/tela bloqueada/permissão. Todos modais fecham ao clicar no overlay.
- Concluídos: nove colunas corrigidas; expansão usa nomes de classe divergentes e detalhes não recolhem corretamente.
- Cadastros: filtros ativos/inativos corrigidos; tablet não organiza duas regiões; inclusão/edição permanecem no hub.
- Alertas: seções não expansíveis. highlightCardEnabled/pulsingEnabled persistem mas não governam renderização.
- Cores: validação identifica nomes de faixas; cadeia exibida não antecipa edição pendente; editor permanece na própria visão.
- Backup: download/CSV possuem handlers e normalização de concluido; replace anuncia backup preventivo, porém não tem confirmação reforçada. Cancelar importação/confirmar não remove callbacks antigos.
- Diagnóstico: stores permanecem tabela, sem lista expansível; cópia implementada.
- Detalhes: lousa é exibida no filho de um ancestral display:none, continuando invisível. Sem foco restaurado e sem gestão do teclado virtual.

## As 12 correções da seção 24

- DOCX-P0470 — **aderente**: Drawer e overlay adicionam/removem open e active conjuntamente; CSS aceita ambas. Evidência: parts_js_ui.py:340, parts_css.py:414, parts_css.py:433.
- DOCX-P0471 — **aderente**: FABs ocultos; barra inferior com Novo. Evidência: parts_css.py:538, parts_css.py:1608, parts_html.py:1626.
- DOCX-P0472 — **aderente**: Usos atuais empregam bg-elevated; variável legada permanece definida nos três temas como valor equivalente. Correção funcional atende ao requisito; manter compatibilidade não é falha. Evidência: parts_css.py:13, parts_css.py:1733.
- DOCX-P0473 — **aderente**: Todos badges drawer/mobile são atualizados no renderDashboard. Evidência: parts_js_ui.py:1675.
- DOCX-P0474 — **aderente**: Botões backup/CSV vinculados por listeners e aliases; validar downloads no navegador-alvo. Evidência: parts_js_ui.py:1288, parts_js_ui.py:1331.
- DOCX-P0475 — **aderente**: Chamada continua concluido, mas serviço normaliza para completed. Correção funcional equivalente, não literal. Evidência: parts_js_ui.py:1332, parts_js_service.py:1567.
- DOCX-P0476 — **aderente**: Handlers aceitam antecedencia, atraso e noprazo usados no HTML. Tolerância <=1min para rótulo Exato no Horário deve ser esclarecida. Evidência: parts_html.py:833, parts_js_ui.py:2318.
- DOCX-P0477 — **aderente**: Cinco filtros ativos/inativos presentes. Evidência: parts_html.py:951, parts_html.py:1016, parts_html.py:1062, parts_html.py:1108, parts_html.py:1171.
- DOCX-P0478 — **aderente**: CSS aceita chaves range_* e nomes normalizados. Equivalência funcional; não exige remover ids persistidos. Evidência: parts_css.py:670, parts_css.py:676, parts_css.py:682, parts_css.py:688.
- DOCX-P0479 — **nao_aderente**: Pai detailsModalDrawingBox está display:none. JS seleciona filho detailsStylusContainer e mostra somente filho; anotação continua invisível. Evidência: parts_html.py:1843, parts_html.py:1845, parts_js_ui.py:3542, parts_js_ui.py:3564.
- DOCX-P0480 — **aderente**: Nove cabeçalhos correspondem a nove td renderizadas. Evidência: parts_html.py:856, parts_js_ui.py:2400.
- DOCX-P0481 — **aderente**: Elemento labelActiveConsoleFilter criado e atualizado. Evidência: parts_html.py:654, parts_js_ui.py:326.

## Limites e validação necessária

Sem execução de navegador ou alteração da aplicação nesta tarefa. Confirmar em navegador: teclado virtual, foco/leitor de tela, downloads, rotação e proporção do canvas, persistência de filtros/seleção/scroll e funcionamento offline real. Linhas referem-se aos fontes Python contendo HTML/CSS/JS, não ao index.html gerado. A leitura do DOCX preservou fontes originais; nenhum comportamento foi inferido apenas por comentário Fix.


## Revisão final integrada

A consolidação posterior limitou afirmações sobre teclado virtual não testado, reconheceu busca por input e botões Limpar/Aplicar existentes, tratou alternativas de navegação/tabela como não cumulativas e incorporou os testes de downloads no Edge. A matriz JSON e o relatório consolidado contêm os estados finais; os testes físicos permanecem pendentes.
