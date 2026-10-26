# Re-review Task 2 — fix round 2

**I3 / GUI-37: ADDRESSED.** Veredito de especificação da correção: **APROVADO**. Qualidade do patch: **APPROVE**. Nenhuma nova quebra Critical/Important ou Minor identificada nas duas expressões alteradas.

Escopo: `revisoes/task2-fix2.diff` contra `task2_r2_base`, seção final de `task-2-report.md`, regressão `tests/test_edit_journey_browser.py` e evidências `task2-fix2-tests.log/.json`. Não reabri Task 3, não alterei produto e não repeti a suíte.

As duas modalidades agora usam o mesmo critério: `completedBy` deve ser uma string com conteúdo após trim; caso contrário, a autoria exibida é **Não informado**. Conferido em `parts_js_ui.py:2633` para cards e `parts_js_ui.py:2676` para tabela. Foram removidos tanto o fallback a `createdBy` quanto a atribuição inferida a Usuário local. Um nome de executor preenchido continua sendo mostrado sem alteração; campo ausente/undefined também cai no fallback pela verificação de tipo. As expressões apenas produzem texto e não escrevem o evento ou seu histórico.

A regressão executa null, string vazia, espaços e executor real nas duas modalidades. Para cada caso, exige o texto esperado e proíbe o nome da pessoa que apenas criou. O caso de propriedade ausente não aparece como iteração independente do teste entregue; seu tratamento está coberto diretamente pela condição de tipo da expressão revisada. Isso não deixa lacuna funcional no achado.

O diff contém somente as duas substituições declaradas. O verificador de escopo também compara a fonte inteira à base após essas duas substituições, preservando a concatenação da Task 3. Nenhuma mudança em CSS/HTML/Presentation integra esta decisão.

Evidência entregue conferida: **44/44 testes passam, zero falhas, zero erros e zero skips**, em 37,175 s, sendo edição 2, UI 24 e controlador 18. O teste de edição mantém o mesmo registro e histórico; o teste de autoria cobre as duas apresentações. A aprovação é restrita a I3 e ao patch desta rodada, sem ampliar a conclusão para a integração visual em revisão separada.
