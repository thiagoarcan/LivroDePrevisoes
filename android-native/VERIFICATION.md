# Verificação da versão Android nativa - 31/10/2026

**Entrega para homologação, não certificação de produção.** Kotlin nativo, quatro módulos e nove áreas funcionais. Sem WebView. Código web e geradores existentes preservados.

## Resultado verificável

| Evidência | Resultado | Alcance |
|---|---:|---|
| JVM, quatro módulos | 101 testes aprovados | Regras, armazenamento, backup, alarmes e estado da interface |
| Gradle, domain/data | 68 testes aprovados | Sobrepõem a suíte JVM; não somar como testes únicos |
| Robolectric API 36 | 27 testes aprovados | Activity, Views, callbacks, SAF simulado e trabalhador real de alertas |
| Robolectric API 26 | 1 smoke aprovado | Inicialização, demonstração persistida, nove telas e Back legado |
| Ferramentas | 5 + 3 testes aprovados | Integridade do pacote e bootstrap das dependências |
| Aplicação web preservada | 18 verificações estruturais | Cinco blocos gerados idênticos; JavaScript aprovado em `node --check` |
| APK | Dois builds byte a byte idênticos | Assinaturas v2/v3, CRC, DEX, alinhamento e licenças verificados; DEX adulterado rejeitado |

Os testes nativos usam o framework Android real do Robolectric com `Config.NONE` e gráficos legados. Não são instalação em aparelho, teste do manifesto/tema empacotado em execução ou validação visual. Manifesto, permissões e recursos são verificados separadamente na compilação/inspeção do APK. O smoke API 26 não comprova áudio físico.

## Regressões relevantes

- Referências originais inativas e PNG original preservados na edição.
- JSON completo e estrito; UTF-8 inválido e Unicode sem par recusados sem normalização ou gravação parcial. Emoji válido preservado.
- Cancelamento/falha de escrita, flush ou fechamento do backup preventivo bloqueia substituição, demonstração e limpeza.
- Recuperação exporta bytes originais; arquivo temporário de restauração é novamente validado antes da alteração.
- Pausa antes da entrega não perde um alarme sem repetição; conclusão antes do callback impede aviso obsoleto; notificações antigas são removidas e visuais simultâneos ficam na fila.
- 500 registros acessíveis em cinco páginas de até 100 cartões, com busca em toda a base, limites de página, restauração de estado e retorno por Back.
- Duas leituras iniciais do snapshot; nenhuma leitura adicional para paginação, busca e 500 consultas de hierarquia no teste. Watchers antigos são removidos; passagem real de prazo atualiza o mesmo campo sem reconstruir o formulário.

A revisão independente não encontrou bloqueadores restantes no escopo inspecionado. A correção final do Back foi novamente compilada e testada pelo revisor. Contagens de verificações independentes e das suítes principais se sobrepõem.

## Identificação do APK

- Arquivo de entrega: `LivroDePrevisoes-Android-teste.apk`
- Pacote: `br.com.livrodeprevisoes`; versão `1.0.0`, código `1`
- Android mínimo: 8 / API 26; target API 36
- Tamanho: 2,310,602 bytes
- Única permissão declarada: `POST_NOTIFICATIONS`; sem Internet ou armazenamento amplo
- SHA-256: `e61fa13e2e9160c1dcb0cd09eae2ad73c8f31d0ed4ca1a4088e4f4eb6c127f18`
- SHA-256 do certificado de teste: `379bf134d02d690d96b1650aea49ffb179d2e9b45ac628d1d25a6eea61160649`
- Fingerprint dos 22 arquivos principais: `eda83410aa9ac771398f023f6246941f55df75b2ff205140145f7151d4f911da`

A chave privada não integra o Git, o ZIP ou o APK. Builds futuros com outra chave podem exigir desinstalação; exporte os dados antes. Não houve merge em `master`, release pública, Play Store ou assinatura de produção.

## Limites que permanecem

**Alertas somente com o aplicativo aberto e ativo**, conforme o contrato da aplicação web original. Não há garantia com tela bloqueada, processo encerrado ou app em segundo plano. A aceitação de um canal pelo Android não prova que alguém viu/ouviu o aviso.

Migração do navegador é manual por JSON schemaVersion 1. Preferências exclusivamente visuais do navegador permanecem no backup, mas não são apresentadas como comportamento Android. Importação limitada a 32 MiB; bases grandes precisam de homologação no aparelho real.

Não executados: instalação em aparelho/emulador, áudio e notificações no hardware, provedores SAF reais, TalkBack/fonte grande/renderização física, build APK/lint pelo SDK oficial, AAB/Play. O E2E completo do navegador não executou por indisponibilidade de configuração de browser/sandbox; as verificações estruturais não o substituem.

Use [a matriz manual](app/qa/ANDROID_MANUAL_MATRIX.md) antes de uso operacional. Instruções em [README](README.md) e [tools/README](tools/README.md). O ZIP contém o projeto Android completo e evidências; o relatório entregue identifica o commit remoto publicado e os hashes finais.
