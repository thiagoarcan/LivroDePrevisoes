# Re-revisão independente — Task 3, rodada 1

Data: 25/10/2026. **Veredito: APROVADO no escopo desta rodada. 10/10 achados ADDRESSED; 0 NOT ADDRESSED. Abertos: Critical 0, Important 0, Minor 0. Nenhum novo Critical/Important identificado no delta.**

## Escopo

Revisados os achados I1–I6 e M1–M3 do parecer anterior, mais X1 comunicado pela coordenação. Comparação de `revisoes/task3-fix1.diff` com `task3_r1_base`, leitura direta das fontes CSS/HTML/Presentation e dos testes. Os três Minor foram incluídos conforme determinação do usuário registrada pela coordenação. Não foi reaberta a implementação de UI/core/service, nem a correção paralela do controlador na lista. Nenhum arquivo de produto foi alterado.

## Veredito por achado

| ID | Resultado | Verificação da correção |
| --- | --- | --- |
| I1 | **ADDRESSED** | `parts_css.py:9` resolve os aliases de superfície no `body`, junto aos tokens dos temas. Modais claros têm fundo claro e texto legível. Testes verificam contraste efetivo de título, corpo, fechar e ações em confirmação/conclusão nos três temas; capturas clara e industrial conferidas visualmente. |
| I2 | **ADDRESSED** | `parts_html.py:644` agrupa contexto; regras CSS posicionam foco, urgentes e panorama na mesma região inicial em widescreen. Métricas continuam visíveis; ultrawide mantém quatro regiões simultâneas. Testes cobrem 1920, 2200, 2559, 2560 e 3440, além da precedência das métricas em tablet/conventional. Capturas 1920 e 3440 conferidas. |
| I3 | **ADDRESSED** | Aviso de alertas ocupa uma faixa compacta, formulário começa à esquerda e prévia fica ao lado nas larguras amplas. O aviso deixou de esticar verticalmente a coluna principal. Regressão em 1920/3440 e captura 3440 conferidas. |
| I4 | **ADDRESSED** | `parts_js_presentation.py:180` usa o estado atual da categoria e `inputTagCode`; `:190` consulta a junção `pipelineOperationalUnits` nos dois sentidos. Testes conferem nomes reais, vínculos múltiplos, indicação de registro inativo, prévia de TAG em edição e preservação integral do snapshot. |
| I5 | **ADDRESSED** | As tabelas recebem larguras mínimas de coluna adequadas, preservam palavras e usam rolagem interna. Regiões têm nome, foco por teclado, indicação de rolagem e resposta às setas. Testes cobrem diagnóstico em 320/390/768/1024/1440 e TAG em 390. Reprodução independente adicional em 390 confirmou tabela de 740 px dentro de região de 338 px, linhas de dados de 43–62 px e zero `pageerror`. Capturas de cores e diagnóstico em 1440 e diagnóstico móvel conferidas. |
| I6 | **ADDRESSED** | Removida a grade inline que impedia o empilhamento do backup no celular. Seções usam a largura disponível; `backupSelectedFileName` apresenta o nome integral com quebra segura. Testes verificam empilhamento em 320/390/600, seleção real de arquivo, ausência de overflow e ação de validação habilitada. Captura de 320 conferida. |
| M1 | **ADDRESSED** | `parts_css.py:36` amplia o seletor de console para 180 px. Regressão considera largura do texto, padding e seta nas quatro larguras de desktop, com relógio real. Console completo visível nas capturas conferidas. |
| M2 | **ADDRESSED** | A sentença do aviso de dependências é um único parágrafo, preservando o destaque inline. O nome da ação não fica mais comprimido como item flex independente. Regressão de dimensões e captura móvel clara conferidas. |
| M3 | **ADDRESSED** | `parts_html.py:1524` usa `details/summary` para os filtros avançados; `parts_js_presentation.py:155` resume escopo e quantidade. Começa recolhido no celular e aberto em desktop, preservando valores e evitando troca enquanto o foco está dentro do grupo. Testes verificam abrir/fechar, selecionar, resumo e redimensionamento. A captura móvel mostra o primeiro concluído na tela inicial. |
| X1 | **ADDRESSED** | `parts_js_presentation.py:76` trata `null`, vazio e espaços como “Não informado”, e normaliza o nome válido com `trim()`. O teste de edição ampliado verifica o campo Controlador no detalhe para os quatro casos; o nome do criador não é usado como substituto. |

## Evidência independente e limites

Executado novamente `python revisao_interface_2026_10_25/run_task3_fix1.py`: **18 testes, 0 falhas, 0 erros**, em 21,594 s. Lidos os testes de qualidade (10), revisão (6) e edição (2), incluindo as asserções que sustentam os itens acima. Resultado em `resultados/task3-fix1-focused.log` e `.json`.

Executado também `python revisao_interface_2026_10_25/revisoes/task3-fix1-review-probe.py`, com Edge headless, HTML/IndexedDB temporários e demonstração isolada. Medidas em [task3-fix1-review-probe.json](task3-fix1-review-probe.json) e captura própria em [task3-fix1-review-diagnostic-390.png](task3-fix1-review-diagnostic-390.png). Não foi acessado perfil ou banco real.

Capturas do implementador inspecionadas diretamente: dashboard 1920/3440, alertas 3440, confirmação clara, dependências claras, conclusão industrial, filtros recolhidos, backup 320, cadastros 390, diagnóstico 390/1440 e cores 1440. As capturas móveis iniciais não mostram todas as tabelas abaixo da dobra; por isso o diagnóstico recebeu a reprodução adicional com rolagem até a tabela.

Os resultados completos **120/120**, matriz **1651/1651 stable** e inventário de **104 capturas** são evidências informadas pelo implementador e conferidas pela coordenação; não foram reexecutados integralmente por este revisor. A aprovação é das fontes e do delta solicitado; a integração e a validação do HTML distribuído permanecem com a coordenação.

SHA256 dos três arquivos conferidos após a execução, iguais a `resultados/task3-fix1-source-hashes.json`:

- `parts_css.py`: `81a9b5f437dddf4f0ba1ede38576ba48c4322dc7d35691e0fa88e5931c373e9c`
- `parts_html.py`: `55871f17e5ffbb33e4060de7ef146852d9aad985a0f0dfd8230de5fe7e45fe9e`
- `parts_js_presentation.py`: `23877feadb1e3ace5c1955a70ddae0337e391570dc102087f7cf1edf02b7b5bc`

## Qualidade e achados abertos

O delta mantém a apresentação dependente do contrato da UI e do snapshot, sem introduzir gravações, polling paralelo ou novo fluxo de negócio. Conteúdo variável continua sendo inserido por texto; vínculos são derivados da junção real. O disclosure nativo e as regiões de rolagem preservam operação por teclado. Não foi identificado novo Critical/Important no patch, nem pendência entre os dez achados desta rodada. Nenhuma observação Minor adicional foi encaminhada ao ledger da revisão geral.
