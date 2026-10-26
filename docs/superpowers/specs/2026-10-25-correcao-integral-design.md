# Correção integral da aplicação

## Autorização e referência
O usuário autorizou todas as correções da auditoria, inclusive layout e testes completos possíveis no navegador desta máquina. A especificação é o DOCX de adaptação, os três Designer*.pdf e os 40 grupos em auditoria_interface/dados/achados_consolidados.json. Não é necessário escolher novamente entre caminhos já avaliados: executar as correções mantendo o aplicativo offline existente.

## Decisões de implementação
- Manter geração Python → index.html único, offline, sem dependências remotas e com o mesmo IndexedDB. Preservar dados existentes e históricos. Operações destrutivas apenas em perfis temporários nos testes.
- Usar o viewport inteiro com navegação lateral em desktop, cabeçalho compacto e barra inferior no celular. Distribuir painéis complementares em telas amplas; limitar linhas/campos e não expandir alturas por mero preenchimento. Sem rolagem horizontal da página inteira; tabelas e painéis podem ter rolagem interna.
- Tornar os estados de interface coerentes com o modelo: um ID/timestamp para cada contador, transições temporais contínuas, nomes/IDs/classes únicos e foco acessível.
- Substituições de backup são atômicas e precedidas de validação completa. Mesclagem não regride dados e apresenta conflitos. Texto importado não executa HTML. Formulários validam relações, datas e números. Zero é valor válido onde anunciado.
- Validar todos os critérios da auditoria reproduzíveis no Edge/Chromium local, incluindo fluxos reais, layouts, temas, teclado, downloads, importação, falhas e concorrência. Registrar testes e capturas posteriores, separando testes físicos indisponíveis.

## Aceitação
Todos os 40 achados possuem resolução ou decisão explicitamente ligada ao requisito (ambiguidade documental não cria obrigação simultânea). Nove visões, dez modais, sete modos e três temas funcionam; 19 larguras de 320 a 3440 px sem overflow global. Nenhum P0/P1 conhecido permanece aberto. Cenários de aparelho físico não são declarados testados por emulação.
