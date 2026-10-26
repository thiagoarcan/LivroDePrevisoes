# Task 4 — rodada final única de correções

25/10/2026. Implementação dos achados I1–I4 e M1 de `revisoes/revisao-integral.md`, mais X2 confirmado pela raiz no mesmo caminho de metadados do drawer. Base imutável: `revisoes/final_fix_base`. Este relatório documenta a implementação e sua verificação; a re-revisão independente e a integração do HTML distribuído permanecem com a raiz.

## Correções

| Achado | Resultado concreto |
| --- | --- |
| I1 — rail tablet paisagem | O tier tablet usa rail de 80 px a partir de 1000 px em paisagem. Os nove destinos mantêm os mesmos botões/handlers, nomes acessíveis, estado atual e títulos de apoio. O drawer continua disponível; em retrato/estreito permanece a navegação por drawer. Lista/detalhe ficam simultâneos: em 1024 px medem aproximadamente 489/407 px; em 1199 px, 584/487 px. Teclado, toque e rotação preservando seleção foram exercitados. |
| I2 — relógio e aviso de áudio | Cabeçalho móvel/tablet exibe o relógio oficial real e o aviso condicional existente, com comando de 44 px. Os indicadores técnicos continuam no Status. Nenhum relógio, timer, polling ou motor paralelo foi introduzido. O `ResizeObserver` oficial continua atualizando a altura real usada pelo banner de alarmes. Em 320 px, relógio e aviso cabem na mesma linha; cabeçalho medido em 161,17 px com aviso, contra 187,06 px antes do ajuste final de gap. |
| I2 — contraste associado | A cobertura dirigida confirmou que o texto amarelo inline de áudio indisponível no Status tinha contraste 1,48:1 no tema claro. CSS específico usa o token de texto do tema, preservando o texto de estado e o comando existente. Medidas finais do aviso: dark 9,68:1, light 6,74:1, industrial 9,68:1; do texto de áudio no Status: 16,84:1, 13,28:1 e 21:1. Os estados pronto/indisponível passam nos três temas. |
| I3 — editor/lousa paralelos | No mesmo limiar tablet paisagem, Atividade e Lousa ocupam colunas paralelas de um único formulário. Os grupos têm altura natural. Toolbar compactada ocultando somente labels de controles de compatibilidade já ocultos e um label duplicado sem associação; Cor e Espessura mantêm labels `for` associados, e Borracha mantém nome textual. Canvas conserva bitmap lógico 1200×440 e proporção visual. Rascunho, foco, bitmap e seleção sobrevivem à rotação. Fullscreen continua no controlador oficial. |
| I4 — política de ações móveis | Cartão e spotlight mostram ações operacionais prioritárias e Mais. Editar, Duplicar, Detalhes e Excluir ficam no sheet nomeado no mobile; desktop conserva as ações diretas. Exclusão fica em seção separada e nomeada “Ação destrutiva”, usando a confirmação atual. Reconhecer, Adiar e Concluir permanecem diretamente disponíveis quando o alarme está disparado; Adiar foi harmonizado também no spotlight. |
| M1 — versão central | Drawer recebe `App.Config.APP_VERSION` na inicialização da apresentação. Removido literal v1.1.0 do drawer e placeholder antigo do diagnóstico. Drawer, diagnóstico renderizado e JSON copiado usam a mesma fonte central; clipboard foi substituído somente no contexto de teste. |
| X2 — usuário no drawer após reload | A inicialização oficial da UI publica `settings.localUserName` também em `labelDrawerUser`, com o mesmo fallback do cabeçalho. Regressão salva “Controladora Maria” na base temporária, recarrega e confere o drawer. Nenhuma persistência nova foi criada. |

M2 permanece **dívida de manutenção aceita**, conforme a triagem do revisor integral: consolidar futuramente os overrides legados de core/service numa tarefa isolada. Não foi feita refatoração dessas camadas.

## Verificação RED → GREEN

O runner usa HTML temporário montado das fontes e IndexedDB isolado, sem perfil/dados reais do usuário. `--baseline` injeta somente os quatro módulos da base imutável em memória, sem reverter o workspace. Os sete testes da raiz foram preservados; a única adaptação foi aguardar o sheet ativo depois de tocar Mais, respeitando o timeout de 5 s e os mesmos asserts. Probe demonstrou que `is_visible()` imediato ocorria antes dos awaits de leitura já existentes; a raiz concordou com essa sincronização.

Quatro testes complementares em `tests/test_final_actions_browser.py` cobrem largura útil/seleção em lista+detalhe tablet, ações diretas de alarme disparado, rotas secundárias e identidade pelo sheet, separação destrutiva e contraste de áudio nos três temas. Após o ajuste final de gap, esse último teste também verifica o alinhamento de relógio/aviso na mesma linha em 320 px.

| Comando | Resultado |
| --- | --- |
| `python revisao_interface_2026_10_25/run_task4_fix.py --baseline` | **11 falhas / 11 testes**, zero erros/skips, 10,414 s. |
| `python revisao_interface_2026_10_25/run_task4_fix.py --all` | **131/131**, zero falhas/erros/skips, 102,092 s. |
| `python revisao_interface_2026_10_25/run_task4_fix.py` após ajuste final | **11/11**, zero falhas/erros/skips, 12,153 s. |
| `python tests/test_layout_browser.py --screenshots` | **1651/1651**, zero falhas, `sources_stable:true`; saída e hashes finais preservados em `resultados/task4-layout-completo.json`. |
| `python revisao_interface_2026_10_25/capture_task4_fix.py` | **32 capturas** específicas, zero page errors, medidas em `resultados/task4-captures.json`. |
| `python revisao_interface_2026_10_25/verify_task3_header.py` | **GREEN 320/768/1200/3440**. Probe corrigido para medir efetivamente retângulo positivo e contenção do relógio no cabeçalho/viewport, além do texto real, console e sino. |
| `python -m compileall -q parts_css.py parts_html.py parts_js_presentation.py parts_js_ui.py` | Sucesso. |
| `python revisao_interface_2026_10_25/make_task4_diffs.py` | Diffs e hashes finais gerados. |

**Sequência precisa:** os 131 testes passaram antes da última alteração de CSS, que reduziu somente o gap horizontal do grupo relógio/aviso de 9,6 para 5,6 px. Depois dessa alteração foram repetidos os 11 dirigidos, a matriz inteira com capturas, o probe de cabeçalho, compilação e hashes. A raiz autorizou evitar outra repetição redundante da suíte funcional nesta etapa e executará os 131 casos no HTML distribuído reconstruído, juntamente do pipeline dos dois engines. Este relatório não apresenta os 131 anteriores como execução sobre o último hash de CSS.

## Evidências e delta

- Logs/JSON: `resultados/task4-baseline.*`, `task4-focused.*`, `task4-suite.*`, `task4-layout-completo.json`.
- Capturas específicas: `task4-header-<largura>-audio-{waiting,ready}.png` para 320/390/600/768/820/1024/1199; `task4-pending-*`, `task4-editor-start-*` e `task4-editor-drawing-*` em 768/1024/1199; `task4-audio-header-*` e `task4-audio-status-*` nos três temas; cartões, sheet e metadados em mobile. Todas estão em `resultados/` e listadas no manifest `task4-captures.json`.
- A matriz completa usa as 70 capturas `final_*`. O probe de cabeçalho mantém quatro `final_header_real_*`. As 32 capturas específicas, as 70 da matriz e as quatro do probe somam 106 capturas da verificação desta rodada.
- Diffs contra `final_fix_base`: `resultados/task4-parts_css.py.diff`, `task4-parts_html.py.diff`, `task4-parts_js_presentation.py.diff`, `task4-parts_js_ui.py.diff`.
- Hashes: `resultados/task4-source-hashes.json`. O gerador auxiliar de HTML foi atualizado para preservar o metadado central caso seja reutilizado; não integra o runtime/build.

## Contratos preservados e entrega

Somente CSS, HTML, Presentation e alterações mínimas de marcação/metadados na UI foram modificados no produto. O delta UI limita-se a classes de política de ações, ação Adiar do spotlight, wrapper semântico da exclusão e publicação inicial do usuário no drawer. Não modifica await/identidade, stack de modais, foco/inert/busy, confirmação, importação, cache ou handlers de persistência. Core, serviço, motor, build e `index.html` foram preservados. Snapshot segue somente leitura; não há reconstrução do formulário ou canvas no resize. Não foi usado overflow global oculto para esconder falhas.

As fontes são entregues congeladas para a única re-revisão escopada, sem falha conhecida aberta nas verificações desta rodada. Hashes foram recalculados contra o disco e coincidem com o registro final; core, serviço, build e index foram comparados byte a byte com a base e permanecem iguais. Integração/build e testes finais no distribuído, inclusive Firefox nativo, pertencem à raiz. Emulação de toque e pointer não certifica aparelho físico, caneta/palma real, teclado virtual externo, som audível, notificações externas, suspensão ou permissões do sistema. As medidas de contraste cobrem os estados amostrados e não constituem certificação universal WCAG.
