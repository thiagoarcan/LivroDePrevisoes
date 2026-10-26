# Validação da correção integral

Os testes usam perfis temporários. Não reutilizam o perfil do usuário nem sua base IndexedDB. O HTML temporário permite verificar alterações sem publicar uma versão intermediária em index.html.

## Comandos finais

Executar na raiz do projeto, com Python e Playwright já disponíveis nesta máquina:

`python tests/validate_delivery.py` executa a sequência completa abaixo, interrompe na primeira falha e registra comandos, logs e hashes em `resultados/validacao_integracao.json`. Os verificadores antigos que não retornam exit code de falha também são conferidos pela saída textual.

```powershell
$env:PYTHONIOENCODING='utf-8'
python build_all.py
python tests/verify_distributed_artifact.py
python tests/verify_reference_integrity.py
python tests/run_suite.py --distributed
$env:PREVISOES_TEST_DISTRIBUTED='1'
python tests/test_layout_browser.py --screenshots
python tests/test_firefox_native.py
python verify_app.py
python verify_adjustments.py
python verify_mobile_tablet_adaptation.py
```

`--distributed` usa o index.html gerado, copiado para origem temporária. O núcleo também possui testes HTTP locais para transações e concorrência. O runner registra hashes de todos os fontes antes/depois para invalidar execuções em que o produto tenha mudado.

## Cobertura executável

- Formatação local, datas impossíveis, referências, atores e histórico.
- Transações, abort/rollback, importação inválida e backup preventivo.
- Mesclagem, conflitos, duplicidades, campos obrigatórios e conteúdo inseguro.
- Alarmes, repetição, reconhecimento, adiamento, zeros, duas abas e fallback.
- Criação, edição, conclusão, reabertura, duplicação e cadastro hierárquico pelos formulários.
- Downloads JSON/CSV, importação por arquivo, preferências e funcionamento offline.
- Modalidade de listas, paginação, contadores, filtros, estados de diálogos e foco.
- Desenho por mouse, proporção, rotação simulada, fullscreen, undo/borracha e preservação.
- Eventos sintéticos de caneta: pressão altera a área real do traço; toque de palma não interrompe caneta ativa; cancelamento libera o ponteiro. Não substituem hardware físico.
- Texto, nomes acessíveis, teclado, contraste dos componentes amostrados e movimento reduzido.
- Nove visões, sete modos, três temas, dez modais e 19 larguras (320–3440 px).
- Microsoft Edge automatizado e Firefox instalado em modo headless com perfil isolado.

As contagens e os resultados finais ficam em resultados. Os logs RED preservam as reproduções dos defeitos; não representam falhas da entrega final.

## Limites

Uma suíte finita não prova ausência de todos os defeitos nem 100% das combinações possíveis de dados. A meta de 100% refere-se aos cenários catalogados e executáveis nesta máquina, com zero falhas finais. Não se declara cobertura de aparelho físico, palma/caneta real, teclado virtual do sistema móvel, luminosidade externa, som audível, notificações do sistema, tela bloqueada ou suspensão por teste de viewport. Os ramos de capacidade/negação são exercitados sem alterar configurações do sistema.
