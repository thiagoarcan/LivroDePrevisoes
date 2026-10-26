# Caderno de Previsões Operacionais em Dutos

Aplicação local para registrar e acompanhar previsões operacionais em salas de controle de dutos. Contexto inferido diretamente do código; não houve entrevista, conforme a solicitação explícita de execução autônoma da remodelação.

O operador seleciona um console, programa atividades por duto/UO/equipamento, acompanha prazos, reconhece ou adia alarmes e registra conclusões. O sistema mantém histórico, permite reabrir e duplicar previsões, desenhar anotações, administrar cadastros, configurar faixas de tempo e alertas, exportar/importar dados e consultar diagnósticos.

Nove áreas: painel, nova previsão, pendentes, concluídos, cadastros, alertas, cores, backup e diagnóstico. IndexedDB é a persistência; o artefato distribuído é index.html autossuficiente, gerado pelos módulos parts_*.py e build_all.py.

Restrições: preservar cálculos, horários, modelos, armazenamento, eventos, IDs e comandos; não exigir rede, serviços comerciais, fontes externas ou dependências novas. Os dados de demonstração utilizados nos testes ficam em contextos de navegador temporários.

Direção da remodelação autorizada em 26/10/2026: modo Operate, console sóbrio em grafite e verde mineral; temas claro e industrial preservados. Hierarquia entre navegação, superfície de trabalho e contexto. Tipografia nativa local para legibilidade e operação offline. Foco em prazos e ações, sem ilustrações ou conteúdo inventado. Primeiro viewport: seleção de console, indicadores compactos e próximo evento. Celular mantém navegação inferior, formulário em coluna e menus; tablet possui composição intermediária; monitores amplos apresentam painéis simultâneos.
