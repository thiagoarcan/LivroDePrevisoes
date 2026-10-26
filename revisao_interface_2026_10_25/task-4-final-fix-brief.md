# Task 4 — correção única dos achados da revisão integral

Leia primeiro `revisoes/revisao-integral.md`: a lista completa e verbatim é I1–I4 e M1. Corrija o conjunto nesta única rodada, conforme `subagent-driven-development/references/final-review.md`. M2 é dívida de manutenção expressamente aceita pelo revisor; não refatore core/service/overrides nesta entrega.

O usuário autorizou todas as correções e os documentos/composição já aprovados são os requisitos. Não solicitar nova aprovação de layout. Esta rodada concretiza a navegação tablet paisagem, horário/aviso de áudio visíveis, composição editor+lousa lateral e simplificação de ações móveis que faltaram. Preserve o restante aprovado, os dados e referências reais. Sem Git; base imutável em `revisoes/final_fix_base`.

## Escopo

Pode alterar `parts_css.py`, `parts_html.py`, `parts_js_presentation.py` e a marcação/handlers mínimos em `parts_js_ui.py` necessários para política de ações/versionamento/apresentação. Preserve APIs/UI central, identidade antes de await, foco/inert/busy, controle de importação, desenhos e snapshot readonly. Não alterar persistência, transações, motor ou serviços. Se achar imprescindível mudar algo além desse escopo, reporte evidência antes de agir. Não editar index/build nesta rodada; a raiz regerará e validará o distribuído após congelamento.

## Regressões confirmadas

`tests/test_final_findings_browser.py`: sete casos **RED 7 falhas, zero erros** na cópia do HTML distribuído revisado; log `resultados/integral_final_wave_red.log`.

- Rail tablet efetivamente visível/contido em1024×768/1199×800, operável por teclado e toque, com seleção preservada durante retrato/retorno.
- Lousa paralela à atividade nesses tamanhos, com largura de edição legível, aspecto1200×440 e preservação do bitmap, rascunho e foco após rotação. O formulário continua único; fullscreen permanece no gerenciador oficial.
- Relógio real e aviso condicional de áudio visíveis/contidos em320/390/600/768/820/1024/1199. Áudio pronto retira o aviso. O probe antigo `verify_task3_header.py` também deve ser corrigido para medir o relógio real, sem alegar geometria somente por textContent. Não criar polling paralelo ou outro motor para o relógio; se precisar decompor texto, use o tick/evento oficial incremental.
- Cartão móvel só exibe ações prioritárias e Mais; Editar/Duplicar/Detalhes/Excluir continuam no sheet nomeado. Excluir deve ficar em seção destrutiva separada e confirmação/cancelamento atuais preservados. Reconhecer/Adiar/Concluir permanecem diretamente alcançáveis quando apropriados. Harmonizar spotlight; desktop continua com ações apropriadas.
- Drawer, diagnóstico renderizado e diagnóstico copiado usam `App.Config.APP_VERSION`; retirar placeholder obsoleto. O relatório esclareceu que Status não é um segundo bug de versão. Não trocar um literal antigo por outro que volte a ficar desatualizado.
- X2 confirmado posteriormente pela raiz, no mesmo caminho de metadados do drawer: após configurar `localUserName=Controladora Maria` e recarregar, cabeçalho usa o nome salvo mas `labelDrawerUser` continua “Operador”. `reloadPreferences` e alteração do nome já sincronizam a gaveta; a inicialização omite a publicação. O sétimo teste reproduz isso no distribuído. Corrigir a sincronização inicial, sem nova persistência; GUI-37 exige identificação coerente.

Os testes da raiz não devem ser enfraquecidos; reporte com evidência se encontrar uma expectativa incorreta. Acrescente cobertura dirigida de alarme disparado/ações e geometria útil de lista/detalhe tablet se necessário. Use dados temporários; não tocar o banco/perfil do usuário, clipboard real ou notificações do sistema.

## Verificação e contrato

Execute cobertura direcionada RED→GREEN, suíte integrada inteira (esperada127 antes de novos testes seus), matriz completa19larguras×7modos×9visões/temas/modais com capturas e compilação. Testes de fontes usam o helper sem `PREVISOES_TEST_DISTRIBUTED=1`; após corrigir fontes a raiz vai reconstruir index e executar novamente o pipeline completo nos dois navegadores.

Após os últimos ajustes, congele produto. Append relatório em `task-4-final-fix-report.md` com arquivos, cada achado, comandos e saídas, limites, capturas, hashes e diff contra `final_fix_base`. Retorne contrato curto. Não spawn. A raiz enviará exatamente uma re-revisão escopada dessa rodada ao revisor integral.
