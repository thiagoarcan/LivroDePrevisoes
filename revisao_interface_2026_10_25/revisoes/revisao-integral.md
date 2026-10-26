# Revisão independente da entrega integral

25/10/2026. **Veredito: REQUEST CHANGES / NÃO APROVADO para encerramento integral. Abertos: Critical 0, Important 4, Minor 2 (um conhecido).** Os resultados executados são válidos para seus cenários; não sustentam ainda o encerramento de todos os requisitos de composição. Manter `whole_review:false`.

## Escopo e método

Leitura do brief, plano, especificação, proposta de composição Task 3, 321 itens da matriz DOCX, 22 itens da matriz visual, agrupamentos da auditoria, decisões técnicas/de entrega, pareceres e relatórios das tarefas. Inspeção direta dos fontes de persistência/transações, validação/importação/merge, claims do motor, controlador de modais, composição HTML/CSS e Presentation, usando `whole-delivery.diff` como índice das mudanças contra os snapshots. A revisão não considera as antigas linhas/status das matrizes como diagnóstico atual.

Conferidas visualmente as três pranchas PDF renderizadas em `auditoria_interface/referencias`; capturas finais das nove telas, incluindo Pendentes e Nova previsão 1024, Dashboard 3440, Cadastros 1920, Cores 1440, Alertas/Backup/Diagnóstico/Concluídos 390 e temas claro/industrial 1024. Os PDFs sustentam a distinção entre navegação tablet lateral e drawer móvel; números ilustrativos e gráficos não foram elevados a requisitos operacionais novos.

Executado probe próprio dirigido com Edge headless, contexto e arquivo temporários, **cópia do `index.html` distribuído**, em 390×844, 768×1024, 1024×768, 1199×800 e 1440×900. Script: `revisao-integral-probe.py`; medidas: `revisao-integral-probe.json`; capturas: `integral-header-*.png`, `integral-tablet-form.png`, `integral-mobile-actions.png`. Zero `pageerror`, hashes do produto preservados. Nenhum dado/perfil real foi usado e nenhum produto foi editado. A suíte de 120 casos não foi repetida.

## Important

### I1 — Tablet em paisagem continua sem navegação lateral compacta

**Fonte:** `parts_css.py:347`, `:349`, `:371`. **Requisitos:** DOCX P0313/P0315, P0304, visual V10, proposta Task 3 §2 e §3.

**Reprodução:** abrir a cópia distribuída em modo Automático a 1024×768 ou 1199×800, com drawer fechado. O tier é `tablet`, mas `.app-nav` tem `display:none`, largura e altura zero. O drawer mede 340 px e permanece em x=-357, inteiramente fora do viewport. Não existe outro rail lateral visível. A regra é incondicional para todo tier tablet; não considera a largura útil suficiente em paisagem. O relatório Task 3 descreve drawer em tablet, mas nenhuma decisão técnica substitui explicitamente o requisito de paisagem.

**Impacto:** toda troca entre destinos continua exigindo abrir e fechar o drawer, apesar do espaço para o rail compacto previsto. A presença do botão hambúrguer e de lista/detalhe não atende à composição de navegação exigida. P0317 permite drawer em retrato; essa permissão não substitui P0313 em paisagem.

**Recomendação:** implementar navegação lateral compacta/recolhível quando a área útil comportar o rail e os painéis, preservando drawer no retrato/estreito. A proposta prevê aproximadamente 72 px em paisagem; o limiar deve preservar largura legível de lista/detalhe. Não basta alterar somente o texto do relatório.

**Regressão necessária:** assert de rail realmente visível, retângulo dentro do viewport, destinos acessíveis por teclado/toque e layout simultâneo em 1024×768 e 1199×800, com transição de/para 768×1024 sem perda de seleção. `tests/test_layout_browser.py:30`–36 verifica navegação somente abaixo de 768 e a partir de 1200; hoje não detecta esse desvio tablet.

### I2 — Cabeçalho móvel/tablet esconde relógio e aviso de áudio indisponível

**Fonte:** `parts_css.py:351`, `:370`, `:391`; contêiner em `parts_html.py:48`; atualização em `parts_js_core.py:237`. **Requisitos:** DOCX P0054, P0073/P0074, P0321/P0322 e visual V01; proposta §3/§7.

**Reprodução:** modo Automático a 390, 768, 1024 ou 1199 px. O `liveClock` contém a hora real, porém não tem retângulos renderizados; `.header-status-bar` está `display:none`. Ao simular a capacidade de áudio ainda não desbloqueada (`App.Audio.isUnlocked=false; App.Audio.updateStatusPill()`), `chipHeaderAudioWarning` passa corretamente a `display:inline-flex`, mas continua com retângulo 0×0 devido ao ancestral oculto. Em 1440 ambos aparecem. As capturas finais também mostram a ausência de relógio no celular/tablet.

**Impacto:** o horário operacional desaparece e uma condição que exige interação para áudio fica escondida justamente nos layouts móveis. O botão genérico Status permite consulta manual, mas P0073 exige expor no cabeçalho a condição que requer ação. Não se trata de alegação sobre som físico: a condição lógica e sua ocultação são reproduzíveis no DOM.

**Recomendação:** separar relógio compacto e aviso condicional dos indicadores técnicos recolhidos; organizar os dois em linhas que caibam sem prejudicar console/sino. Mostrar o aviso somente quando necessário e retirá-lo quando o áudio estiver pronto.

**Regressão necessária:** verificar visibilidade efetiva, dimensões positivas e contenção do relógio e do aviso no viewport, com áudio pronto e indisponível, nas larguras móveis/tablet. `verify_task3_header.py:14` apenas verifica que o texto do relógio deixou de ser placeholder; sua mensagem final afirma geometria do relógio sem medir sua caixa. Corrigir também essa asserção/evidência.

### I3 — Nova previsão tablet não entrega editor e lousa/contexto paralelos em paisagem

**Fonte:** `parts_css.py:108`–110, `:321`–329, `:352`–369; `parts_html.py:960`. **Requisitos:** proposta Task 3 §4.2 (paisagem: editor à esquerda, lousa/contexto à direita), DOCX P0304/P0349/P0356 e composição tablet autorizada.

**Reprodução:** em 1024×768 Automático, abrir Nova previsão e clicar em Abrir Lousa para Caneta. Localização e Programação compartilham uma linha; Atividade e Lousa seguem ocupando toda a largura. Lousa começa em y≈857, canvas em y≈1180, prévia não salva em y≈1922. O formulário tem 955 px de largura útil de grupos e a prévia ocupa 992 px abaixo. Nenhuma regra tablet posiciona lousa/contexto ao lado do editor; as regras paralelas existem apenas para wide/ultra.

**Impacto:** o uso simultâneo de preenchimento e anotação/contexto planejado para tablet paisagem continua exigindo percorrer uma página longa. Duas colunas de campos de Localização/Programação não são a composição editor/lousa acordada. O canvas mantém proporção correta (aproximadamente 895×328); não há aqui achado de perda/deformação do desenho.

**Recomendação:** criar a composição tablet paisagem por largura útil, com região editável legível e lousa/contexto lateral, preservando o único formulário e a dimensão lógica do desenho. Usar empilhamento quando não houver largura suficiente, sem duplicar campos ou reconstruir rascunhos no resize. Conciliar a dimensão da lousa com fullscreen e mínimos de toque.

**Regressão necessária:** medir posição e sobreposição vertical das regiões editor/lousa/contexto em 1024×768/1199×800; verificar rascunho, bitmap, foco e seleção antes/depois de resize e abertura da lousa. A matriz atual de ausência de overflow não verifica essa composição.

### I4 — Ações secundárias/destrutivas continuam no grupo frequente do cartão móvel

**Fonte:** `parts_js_ui.py:2308`–2313; equivalente de ações redundantes do spotlight em `:2024`–2030. **Requisitos:** DOCX P0173/P0414, visual V06 e encerramento proposto GUI-40.

**Reprodução:** Pendentes, Automático, 390×844, massa isolada. O primeiro cartão renderiza seis botões visíveis: Concluir, Editar, + Duplicar, Detalhes, × Excluir e Mais. Os quatro primeiros ficam na primeira linha; Excluir e Mais juntos na segunda. Não existe separação contextual da ação destrutiva; Mais já oferece o destino apropriado para as ações menos frequentes. O HTML gerado confirma o handler direto `App.UI.deleteEvent` no mesmo `.event-card-actions`.

**Impacto:** permanece a densidade e a proximidade de exclusão com ações de rotina apontadas pela auditoria. A resolução GUI-40 declara que as ações destrutivas são separadas, mas isso não vale para esse caminho principal. A confirmação de exclusão protege a gravação: **não** foi observado apagamento sem confirmação nem se está alegando isso.

**Recomendação:** no móvel, manter as ações operacionais prioritárias e Mais no cartão; concentrar Duplicar/Detalhes/Excluir no menu contextual, com exclusão em seção destrutiva separada e confirmação atual preservada. Harmonizar o spotlight com a mesma política de ações secundárias.

**Regressão necessária:** assert de ausência de Excluir/Duplicar/Detalhes no grupo frequente móvel e de acesso às mesmas ações pelo sheet nomeado; confirmar que cancelar não executa exclusão e que a identidade correta é mantida. Manter as ações essenciais de alarme diretamente disponíveis.

## Minor e triagem

### M1 — Versão da interface ainda divergente

`parts_html.py:269` contém `v1.1.0` no drawer; configuração em `parts_js_core.py:9` e diagnóstico mostram 1.2.0. O probe captura o texto antigo do drawer. O literal de diagnóstico em `parts_html.py:2988` também começa em v1.1.0, mas é atualizado corretamente pela UI ao abrir Diagnóstico: não é uma segunda ocorrência incorreta visível após renderizar. Isso impede afirmar centralização integral da versão em GUI-36, embora não altere o funcionamento operacional.

**Triagem concreta:** preencher a versão do drawer pela mesma fonte `App.Config.APP_VERSION` e retirar o placeholder obsoleto do diagnóstico (ou injetar a mesma constante no build). Verificar drawer, Diagnóstico e diagnóstico copiado. Corrigir na entrega, ajuste pequeno sem necessidade de refatoração ampla.

### M2 — Overrides legados coexistem com implementações efetivas (conhecido)

`parts_js_core.py:670` e `parts_js_service.py:1672`/`:1885` acrescentam definições finais aos objetos já declarados. Revalidei a ordem de composição: as versões transacionais e do motor são incorporadas antes da inicialização da UI; não identifiquei um defeito operacional novo decorrente da coexistência. A manutenção exige conhecer qual método vence no final do bloco.

**Triagem concreta:** aceitar como dívida de manutenção nesta entrega, registrar no ledger final e consolidar cada método em uma única definição numa futura tarefa isolada, mantendo as regressões de rollback, concorrência e compatibilidade. Não bloqueia sozinho e não justifica refatoração agora.

## Evidência validada e aspectos preservados

Os JSON finais registram **120/120** casos comportamentais Edge, **1651/1651** verificações da matriz Edge e **1229/1229** verificações Firefox nativo: **3000**, zero falhas, erros/skips informados pela suíte, nove etapas do pipeline aprovadas. Conferi igualdade dos hashes entre suíte, matrizes e pipeline e recalculados contra o produto no disco. `index.html` SHA256: `fed01e3dd5d7ab61a6a2cf12cad974b7d2670c55ef326c112add9ff8c4d04768`. Artefato 9/9 e integridade 22/22 conferidos. Esses resultados são evidência do implementador conferida, não uma reexecução integral pelo revisor.

O checker compara os cinco blocos exatos, incluindo Presentation concatenado à UI, com o HTML único e ausência de recursos remotos incorporados. A suíte usa o distribuído nas jornadas e matrizes; os testes específicos do núcleo compõem os mesmos blocos numa origem HTTP temporária para concorrência. A igualdade dos blocos/hashes dá rastreabilidade, sem transformar esses testes HTTP numa execução literal do arquivo distribuído.

Na inspeção do núcleo, o commit resolve em `transaction.oncomplete`, as importações inválidas são validadas antes da mutação, a substituição exige exportação preventiva, conflitos deixam o conjunto inalterado e o claim do alarme relê o estado dentro da transação. Conclusões não são regravadas a partir do snapshot antigo. Zero usa operadores/validação apropriados. O lease localStorage continua explicitamente advisory, com autoridade transacional no IndexedDB; não foi promovido a mutex nem a garantia universal.

O controlador mantém ações de confirmação únicas, invalidação por geração de pedido assíncrono, proteção busy e pilha de foco/inert; a autoria de conclusão usa o executor real ou declara ausência. Presentation deriva contexto do snapshot oficial e usa inserção textual para dados variáveis; não introduz motor ou escrita paralelos. Os patches das rodadas aprovadas permanecem nos fontes atuais. Não foi encontrado novo Critical em persistência/importação/concorrência nessa revisão.

A apresentação convencional/wide/ultra agrega contexto real sem exigir gráficos fictícios; campos e tabelas possuem regiões de leitura/rolagem. As correções anteriores de modal claro, contraste amostrado, vínculos cadastrais, tabelas, filtros de concluídos e nome de arquivo móvel permanecem visíveis nas capturas/fontes. Nenhum overflow global apareceu no probe. Esses pontos positivos não substituem os quatro requisitos abertos acima.

O gerador de relatório usa gates e hashes e recusa finalizar enquanto `whole_review` estiver falso. Sua distinção entre cenários catalogados e code coverage é adequada. Antes de liberar o gate, ajustar fontes/testes, repetir as verificações afetadas e atualizar as resoluções GUI-01/02/25/27/36/40 conforme aplicável, sem declarar que todos os 321 itens foram testados individualmente. A revisão confrontou a matriz documental; não produziu 321 novos testes nem certificação integral de acessibilidade.

## Limites

Não certifica aparelho físico, caneta/palma real, teclado virtual do sistema, som audível, notificações externas, tela bloqueada, suspensão ou luminosidade. Firefox final é compatibilidade/geometria com seus casos próprios, não repetição automática de toda a suíte comportamental Edge. A execução finita não prova ausência universal de defeitos. Após correções, re-revisar especificamente I1–I4/M1 e os deltas; M2 pode permanecer como dívida explicitamente aceita.
