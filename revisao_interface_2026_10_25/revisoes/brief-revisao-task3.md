# Revisão Task 3 — composição e semântica

Faça revisão independente somente leitura do produto implementado em `parts_css.py`, `parts_html.py`, `parts_js_presentation.py` e da concatenação Python no final de `parts_js_ui.py`. Compare com `revisao_interface_2026_10_25/task-3-brief.md`, `task-3-layout-proposta.md`, contrato `task-2-report.md` e a Task 3 do plano. Diff contra originais em `revisoes/task-3.diff`; o módulo novo não tinha original. Sem Git.

Examine as capturas atuais `revisao_interface_2026_10_25/resultados/final_*.png` e as três pranchas PDF renderizadas em `auditoria_interface/referencias/*pagina_01.png`. Os PDFs são distintos; imagens PNG do diretório raiz não correspondem todas aos sufixos dos PDFs. Confira a aplicação em contexto temporário caso necessário. Não use perfil/base reais.

O usuário exige toda a largura útil com regiões reais, sem campos/cartões esticados nem grandes áreas mortas havendo contexto útil. Julgue as nove telas nos cinco tiers, menus, header, sidebar, navegação inferior, master/detail, formulários e modais. Não aceite apenas overflow=0 como prova de boa composição, e não exija dados fictícios ou gráficos decorativos em estados vazios.

Verifique semântica e nomes reais, textarea inicialmente vazia, grupos lógicos/disclosures, ações de gravação, lousa proporcional/fullscreen, contraste nos três temas, paleta customizada, alvos de toque, sticky/safearea/zoom e navegação com teclado. As chamadas devem continuar usando a UI aprovada e o snapshot readonly; não pode haver polling paralelo nem render completo a cada segundo. O panorama do dashboard não pode herdar filtro antigo da lista.

A suíte comportamental de fontes passou 100/100 antes dos últimos ajustes de geometria. Evidências definitivas serão indicadas pelo coordenador ao despachar. Não interprete falhas antigas RED como falhas atuais. Regressões novas devem ser reproduzidas; timeouts de harness exigem distinguir seletor/fixture/contensão de defeito real.

Relate spec compliance e code quality, com achados Critical/Important/Minor, arquivo/linha, reprodução e recomendação. Salve `revisao_interface_2026_10_25/revisoes/task-3-review.md`. Não corrija produto. Diga explicitamente se há Critical/Important aberto; status aprovado exige nenhum. Não abra escopo cosmético fora da proposta sem ligação com os requisitos.
