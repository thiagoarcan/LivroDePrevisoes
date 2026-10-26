# Re-revisão independente — rodada final

25/10/2026. **Veredito: APROVADO. I1–I4, M1 e X2: 6/6 ADDRESSED. Não há Critical/Important aberto. Nenhum novo Critical/Important ou Minor identificado no delta.** M2 permanece a dívida de manutenção previamente aceita, sem bloqueio.

## Escopo

Revisão restrita a `final-fix-wave.diff` contra `final_fix_base`, `task-4-final-fix-report.md`, os 11 testes dirigidos e as evidências da rodada. Foram conferidos fontes atuais, alterações CSS/HTML/Presentation/UI e a preservação dos contratos do controlador. Não foi repetida a revisão integral, nem alterado o produto, nem usado o perfil/banco real.

## Veredito dos seis itens

| ID | Veredito | Evidência conferida |
| --- | --- | --- |
| I1 — rail tablet paisagem | **ADDRESSED** | `parts_css.py:386` introduz rail de 80 px no tier tablet com largura útil ≥1000 px e paisagem. Os botões originais e seus nomes acessíveis são preservados; Presentation acrescenta títulos de apoio. Probe próprio no distribuído mediu rail x=0, largura=80 e alturas 636,6/668,6 px em 1024×768/1199×800. Lista/detalhe ficam simultâneos, com aproximadamente 489/407 e 584/487 px, dentro do viewport. Os testes exercitam Enter, toque, seleção e retorno de retrato. O drawer continua sendo a alternativa estreita; deixou de substituir indevidamente o rail da paisagem. |
| I2 — relógio e áudio | **ADDRESSED** | `parts_css.py:357`–361 e `:421` mantêm o grupo relevante visível no tablet/móvel. Em 320 px, medição independente: cabeçalho 161,17 px; relógio 140,41×20,30 px; aviso 149,75×44 px; ambos contidos e alinhados na mesma linha. O aviso some quando o áudio fica pronto e o relógio permanece. A matriz dirigida passa em sete larguras de 320 a 1199. `verify_task3_header.py` agora mede caixa positiva/contida do relógio, corrigindo o falso alcance da asserção anterior. |
| I3 — editor/lousa tablet | **ADDRESSED** | `parts_css.py:395`–398 posiciona Atividade e Lousa em colunas paralelas do mesmo formulário, com altura natural. Testes próprios executados verificam disposição lateral, largura legível e aspecto 1200/440 em 1024/1199, fazem traço real de mouse e comprovam preservação de bitmap, texto e foco após retrato/paisagem. A captura tablet de desenho confirma as duas regiões operáveis; fullscreen e ferramentas permanecem disponíveis. As regras de toolbar removem labels redundantes/de controles já ocultos; Cor/Espessura mantêm associação e Borracha continua nomeada. |
| I4 — ações móveis | **ADDRESSED** | `parts_js_ui.py:2028`–2030 e `:2310`–2313 marcam secundárias, e CSS `:424` as retira do grupo móvel. Concluir/Mais permanecem; Reconhecer/Adiar ficam diretamente acessíveis quando disparado, também no spotlight. Sheet mantém Editar/Duplicar/Detalhes/Excluir; exclusão ocupa seção nomeada e separada (`parts_js_ui.py:2508`). Testes verificam identidade das rotas, ausência de gravação ao duplicar rascunho, cancelamento seguro de exclusão e reconhecimento sem conclusão. Probe adicional confirma retorno do foco ao Mais original após Escape do sheet e após cancelar exclusão. |
| M1 — versão | **ADDRESSED** | `parts_html.py:269` usa `data-app-version`, preenchido por `App.Config.APP_VERSION` em `parts_js_presentation.py:9`; placeholder antigo do diagnóstico foi retirado. O teste no distribuído abre drawer, diagnóstico e copia JSON, confirmando a mesma versão central e ausência de v1.1.0 no drawer. |
| X2 — usuário após reload | **ADDRESSED** | `parts_js_ui.py:300` publica o nome configurado no drawer durante a inicialização oficial, com o fallback já utilizado no cabeçalho. A regressão salva “Controladora Maria” na base temporária, recarrega e verifica o nome. Não há nova escrita, timer ou fonte de dados. |

O ajuste associado de I2 em `parts_css.py:149` substitui a cor inline ilegível do texto de áudio no Status pelo token do tema. Foram lidas as medidas da rodada e executadas novamente as asserções ≥4,5:1 nos estados pronto/indisponível dos três temas, além do aviso no cabeçalho. O texto de estado permanece explícito; o ajuste não altera áudio/core.

## Execução independente

Comando: `python -X utf8 revisao_interface_2026_10_25/revisoes/final-fix-review-probe.py`.

**11/11 testes dirigidos aprovados, zero falhas, erros e skips**, usando cópia do HTML distribuído em contexto temporário. O mesmo script realizou medidas adicionais de geometria e as duas verificações de restauração de foco. Zero `pageerror`; fontes estáveis. Log: `final-fix-review-tests.log`; resultado/medidas/hashes: `final-fix-review-probe.json`; captura própria: `fix-review-header-320.png`.

Foram inspecionadas a captura própria de 320 px e as capturas da rodada `task4-header-320-audio-waiting.png`, `task4-pending-1024.png` e `task4-editor-drawing-1024.png`, além das asserções dos demais estados. O cabeçalho com aviso tem três faixas funcionais e altura natural; relógio e áudio cabem na mesma linha final. O aviso de primeiro uso mostrado no probe é conteúdo separado, sem sobreposição do cabeçalho.

## Integração final conferida

Após a execução dirigida, os JSON finais já estavam completos. Foram lidos e confrontados com os hashes atuais no disco:

- Suíte comportamental: **131/131**, zero falhas/erros/skips, `distributed_html:true`, `sources_stable:true`.
- Matriz Edge: **1651/1651**, completa, distribuída e estável.
- Firefox nativo: **1229/1229**, matriz completa, distribuída e estável.
- Total catalogado final: **3011 verificações aprovadas**.
- Pipeline: nove etapas PASS; artefato **9/9**; integridade das referências **22/22**.

Suíte, matrizes e integração têm o mesmo conjunto de hashes, recalculados contra os fontes atuais. SHA256 do `index.html`: `f6ae6e81325747394ff2b06147fbc79ed5426989cf74b02818d5f030edd9c12b`. O núcleo/serviço mantêm os hashes da revisão anterior. A suíte integrada final foi executada pela raiz; este revisor reexecutou somente os 11 dirigidos e probes descritos acima. Os 131 anteriores ao último gap CSS não foram confundidos com o resultado final sobre este hash.

## Qualidade e limite do parecer

O delta permanece localizado: composição CSS, duas saídas de metadados, política visual de ações e seção destrutiva. Não altera persistência, importação, validação, motor, callback transacional, geração de pedidos de modais, proteção busy ou gerenciamento central de foco. Não há reconstrução do formulário/canvas no resize nem conteúdo fictício.

**M2 continua aceito:** as definições legadas e overrides de core/service devem ser consolidados futuramente numa tarefa isolada com suas regressões; não houve defeito novo demonstrado por essa coexistência. Abertos após a rodada: Critical 0, Important 0, Minor 1 aceito (M2).

A aprovação fecha os achados da revisão integral e permite liberar o gate de revisão, mantendo os demais gates de geração. Não representa certificação de aparelho físico, caneta/palma real, teclado virtual, som audível, notificações externas, suspensão ou acessibilidade universal. Os limites de evidência e de cobertura do relatório continuam válidos.
