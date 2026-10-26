# Integração contínua

O workflow `Quality` executa em pushes, pull requests e acionamento manual.

- **Build and distributed artifact** (Ubuntu, Python 3.12): testes do executor; verifica o HTML versionado; executa `build_all.py`; exige `git diff --exit-code -- index.html`; verifica novamente os nove critérios de integridade.
- **Edge behaviors and quick layout** (Windows 2022): `tests/run_suite.py --distributed` e `tests/test_layout_browser.py --quick`.
- **Full layout (msedge/firefox)** (Windows 2022): matrizes completas em jobs independentes. Edge inclui capturas; Firefox usa um executável instalado explicitamente pelo Playwright. Ambos usam os critérios originais, sem aumentar tolerâncias.

Todos os jobs de navegador dependem do build. Não há `continue-on-error`. Falhas, erros, skips e descoberta vazia da suite comportamental impedem aprovação. A matriz extensa roda também em PRs, pois é parte dos critérios de aceitação.

`requirements-ci.txt` fixa as dependências diretas. O Edge instalado pelo Playwright é o canal estável; sua versão pode evoluir. A versão do Firefox é vinculada à versão fixada do Playwright.

`PREVISOES_TEST_OUTPUT=ci-results` separa as novas evidências das históricas. Artefatos por job/run/tentativa são retidos por 14 dias, inclusive em falhas. Os relatórios incluem hashes e verificação de estabilidade das fontes. `PREVISOES_TEST_DISTRIBUTED=1` seleciona o HTML entregue, inclusive nos testes core. Contextos, perfis e arquivos de teste continuam temporários, sem perfil persistente de usuário.

Para executar localmente, instalar `requirements-ci.txt` e `python -m playwright install msedge firefox`. Definir `PREVISOES_TEST_OUTPUT` e `PREVISOES_TEST_DISTRIBUTED` como acima. Para o harness nativo Firefox, `PREVISOES_FIREFOX_BINARY` pode apontar ao executável retornado por `p.firefox.executable_path` dentro de `sync_playwright()`; sem a variável, permanece o caminho padrão do Windows.

Os números 131, 1.651 e 1.229 do relatório de 25/10/2026 são evidência histórica local. Somente uma execução identificada na aba Actions comprova CI. Cada execução atual informa suas próprias contagens.

Para impedir merges com falhas, os checks deste workflow devem ser exigidos por uma regra de proteção do branch master. Criar o workflow por si só não ativa essa regra.
