# Correção integral — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Corrigir os 40 grupos da auditoria e a composição responsiva com evidência de testes no navegador local.
**Architecture:** Preservar namespace App e geradores Python. Corrigir persistência/serviços, depois interface, depois composição CSS/HTML, integrando testes reais em perfis isolados.
**Tech Stack:** Python 3.12, JavaScript nativo, IndexedDB, HTML/CSS e Playwright Microsoft Edge.
**Spec:** docs/superpowers/specs/2026-10-25-correcao-integral-design.md e auditoria_interface/dados/achados_consolidados.json.

## Global Constraints
- Manter index.html único, offline e sem recursos remotos.
- Preservar banco do usuário e compatibilidade com dados e backups válidos anteriores.
- Não editar DOCX/PDFs nem substituir a auditoria anterior; registrar resultados posteriores em revisao_interface_2026_10_25.
- Não esticar objetos nem deixar regiões operacionais vazias quando existir contexto útil; rolagem interna em listas/tabelas, nunca overflow global.
- Não alegar cobertura física móvel a partir de viewport emulado.
- Pasta sem Git: cópias dos originais e diffs substituem worktree/commits. Não inicializar repositório ou sobrescrever dados pessoais.

## Review Focus
- Backup malformado ou conflito deve manter base atual íntegra.
- Alarmes simultâneos, múltiplas abas e operações concorrentes não devem ressuscitar eventos concluídos.
- Mudanças de console/layout/zoom preservam edição, filtros e desenhos.
- Dados longos, 500 eventos e nomes importados não devem quebrar leitura nem executar código.
- Teclado e diálogos empilhados não podem disparar uma ação cancelada nem alcançar o fundo oculto.

### Task 1: Persistência, integridade, alarmes e backup
**Files:** parts_js_core.py, parts_js_service.py; testes específicos em tests/test_core_browser.py.
**Interfaces:** Preservar métodos existentes. Produzir App.DB.atomic(stores, callback), leitura de snapshot, validação completa de backup, transações de operações relacionadas e motor serializado. Nomes adicionais devem ser documentados para UI.
- [x] Criar regressões que falham para GUI-08/09/17/18/19/20, falha de transação, validações cadastrais e ações concorrentes.
- [x] Executar RED no navegador real e registrar causas.
- [x] Corrigir formatação, CSV, validações, transações, merge, motor/concorrência e exposição de erros.
- [x] Executar GREEN e gerar relatório de interfaces e diff.
- [x] Revisão independente de especificação e qualidade.

### Task 2: Comportamentos e acessibilidade da interface
**Files:** parts_js_ui.py e testes UI. Alterações HTML mínimas coordenadas no relatório para Task3.
**Interfaces:** Consumir serviços corrigidos; preservar App.UI métodos públicos; documentar classes/IDs necessários ao layout.
- [x] Regressões RED: cancelamento, demonstração, desenho, detalhe, contadores, filtros, métricas, estados, foco, canvas e controles.
- [x] Corrigir GUI-03/04/05/06/07/10/11/12/13/14/15/16/21/22/25/27/28/29/34/35/36/37/40.
- [x] Criar atualização temporal incremental, gerenciamento central de modais, estados e canvas proporcional.
- [x] Testar fluxos e revisar diff antes do layout.

### Task 3: Composição responsiva integral e HTML semântico
**Files:** parts_css.py, parts_html.py; gerador adicional de UI de painéis se necessário via novo módulo incorporado no build.
**Interfaces:** Respeitar classes e métodos da Task2. Coordenar painéis por ID sem duplicar controles.
- [x] RED para overflow, sidebar, navegação inferior, botões/nomes, campos e detalhes em 19 larguras.
- [x] Implementar shell proporcional: celular, tablet retrato/paisagem, convencional, wide e ultra; cards de largura legível e contexto útil ocupando regiões adicionais.
- [x] Corrigir semântica, fontes, alvos, temas, grupos expansíveis, layout cadastro/configurações/diagnóstico e safe-area/teclado.
- [x] GREEN para todas visões/modais/modos/temas; capturar interfaces finais e revisar.

### Task 4: Integração, regressão completa e revisão final
**Files:** build_all.py, tests, documentos de validação em revisao_interface_2026_10_25.
- [x] Regerar index.html e executar verificadores estruturais e suíte comportamental inteira.
- [x] Cobrir casos adicionais descobertos, sempre RED→GREEN para defeitos novos.
- [x] Revisar todas as 40 resoluções e requisitos documentais reproduzíveis; registrar casos físicos pendentes.
- [x] Solicitar revisão fresca do conjunto e resolver achados importantes.
- [x] Entregar index.html atualizado, relatório de testes, matriz de resolução e capturas; confirmar integridade dos arquivos de referência.
