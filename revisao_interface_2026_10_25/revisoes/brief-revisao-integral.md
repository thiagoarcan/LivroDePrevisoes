# Revisão independente da entrega integral

Escopo autorizado: corrigir todos os 40 grupos da auditoria, incluindo layout que aproveite o viewport sem esticar objetos, e executar os testes reproduzíveis nos navegadores desta máquina. Não há Git; o snapshot `../originais` e os diffs nesta pasta substituem commits. Não editar o produto nesta revisão.

Leia o plano `docs/superpowers/plans/2026-10-25-correcao-integral.md`, a especificação correspondente, `auditoria_interface/dados/achados_consolidados.json`, os reports/reviews das três tarefas e a proposta `revisao_interface_2026_10_25/task-3-layout-proposta.md`. Consulte também a matriz completa de 321 requisitos em `auditoria_interface/dados/matriz_requisitos_docx.json` e os 22 elementos de `matriz_visual.json`: os 40 achados são agrupamentos e não substituem requisitos que poderiam ter sido omitidos. As evidências/linhas da matriz são históricas; não as trate como diagnóstico da revisão atual. Confirme a implementação real, não apenas os relatórios.

O alvo de distribuição é `index.html`, gerado por `build_all.py` dos cinco blocos Python; `JS_UI` inclui o módulo adicional de apresentação. Preserve dados e perfil reais. Testes em contextos/origens temporárias apenas. Os comandos e limites físicos estão em `revisao_interface_2026_10_25/TESTES.md`.

Avalie especialmente:

- Integridade de importação, conflitos/rollback e compatibilidade com backups válidos anteriores.
- Alarmes e concorrência: conclusão não pode ser sobrescrita por tick; diálogo com await não pode agir sobre outro evento; zero é valor válido. O lease localStorage é advisory; claims IndexedDB transacionais são a proteção operacional.
- Modal/drawer/teclado/foco, cancelamento de callbacks, proteção de gravação, identificação do controlador e textos destrutivos.
- Composição visual das nove telas em celular/tablet/convencional/wide/ultra; examine capturas e os três PDFs de referência renderizados. Ausência de overflow global sozinha não prova layout bom; confira leitura, regiões úteis, dimensões, estados vazios, controles e formulários.
- Confira explicitamente DOCX P0313/P0315 e a proposta de navegação compacta no tablet em paisagem. O report Task3 menciona drawer em tablet; determine se a implementação atende a composição exigida ou se restou um desvio sem decisão documentada. Não presumir conformidade apenas por haver botão de menu. Confira também a distribuição editor/lousa em paisagem contra a proposta.
- Consistência dos três temas, semântica e alvos de toque; canvas proporcional e rascunhos preservados em resize/modo.
- Evidência final: suíte comportamental e matrizes devem testar a mesma revisão congelada e o HTML distribuído. Não confundir geometria Firefox com toda a suíte funcional nem emulação com hardware físico.
- Rastreabilidade dos 40 achados e honestidade das limitações. Não aceitar afirmação de 100% de code coverage ou prova universal de ausência de defeitos.

Minor conhecido registrado nas tarefas 1/2: coexistência de definições legadas e overrides no gerador facilita comparação mas aumenta manutenção. Reavalie se gera defeito real; não transforme preferência de refatoração em bloqueio sem evidência.

Registre achados com severidade Critical/Important/Minor, arquivo/linha, reprodução/evidência e recomendação concreta. Para aprovado, diga explicitamente que não há Critical/Important aberto. Salve revisão em `revisao_interface_2026_10_25/revisoes/revisao-integral.md`. Se encontrar defeito, reproduza e indique teste que o cubra; não corrija o produto como revisor.
