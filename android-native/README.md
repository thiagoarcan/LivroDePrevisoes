# Livro de Previsões — Android nativo

Aplicativo **nativo em Kotlin**, organizado em quatro módulos, sem WebView e sem servidor. A interface usa Views Android; o aplicativo funciona offline.

| Módulo | Responsabilidade |
|---|---|
| `domain` | Regras de cadastros, previsões, histórico, alertas, validação e intercâmbio JSON/CSV |
| `data` | Snapshot privado com gravação atômica e logs técnicos separados |
| `alerts` | Monitoramento em primeiro plano, áudio PCM, diálogo e notificações Android |
| `app` | Interface nativa, formulários, desenho, navegação, arquivos e diagnóstico |

## Usar e migrar

1. Instale o APK de **teste local**, autorizando a instalação da fonte usada apenas se confiar no arquivo.
2. Cadastre consoles, UOs, dutos com ao menos duas UOs e, opcionalmente, equipamentos/TAGs.
3. Configure o nome do operador em **Alertas**; crie previsões e acompanhe **Painel**, **Pendentes** e **Concluídos**.
4. Para trazer dados do navegador, abra a aplicação original e exporte um backup JSON. No Android, entre em **Backup → Importar e mesclar** ou **Substituir todos os dados**. Não existe transferência automática do IndexedDB do navegador.
5. Antes de substituir, limpar ou carregar demonstração, escolha onde salvar o backup preventivo. Cancelar ou falhar na gravação impede a alteração destrutiva.

O JSON preserva `schemaVersion: 1`, as dez coleções de dados, IDs, versões, históricos, configurações e desenhos. Logs de diagnóstico são locais e não integram o backup portátil, como na aplicação original. CSV tem BOM UTF-8, separador ponto-e-vírgula e proteção contra fórmulas; é uma exportação para consulta, não para restauração.

Os instantes `scheduledAt` importados são preservados mesmo quando o aparelho está em outro fuso. Detalhes mostram o instante e a data/hora registrada; edição de notas sem mudar data/hora não desloca o evento. Uma alteração explícita de agendamento usa o fuso atual do aparelho.

As listas exibem até 100 previsões por página. Busca, filtros, totais e exportações continuam considerando a base completa; use Anterior/Próxima para percorrer os demais resultados.

## Alertas: limite importante

O monitoramento funciona **somente com o aplicativo aberto e ativo**. Ao sair, bloquear a tela ou suspender a atividade, o motor e o áudio são pausados; ao retornar, os vencimentos são reavaliados. Este é o contrato já declarado pela aplicação web original, não uma garantia de alarmes em segundo plano.

Notificações dependem da autorização do Android e das configurações do canal. O aplicativo registra os canais efetivamente acionados/aceitos pela plataforma; uma chamada aceita não comprova que uma pessoa viu ou ouviu o alerta. Volume do aparelho, modo silencioso e políticas do sistema continuam relevantes. Não há reconhecimento ou conclusão automática de atividades. O aplicativo não substitui procedimentos de segurança operacional.

Configurações exclusivas da interface web, como título da aba e modos de monitor desktop, são preservadas no intercâmbio, mas não simuladas como funcionalidades Android. A interface nativa se adapta à largura disponível. Marcações de faixa usadas apenas pelo navegador são identificadas como compatibilidade, sem afirmar que alteram os disparos nativos.

## Dados e segurança

- Sem permissão de Internet, analytics ou conta remota.
- Arquivos escolhidos via seletor do Android, sem acesso amplo ao armazenamento.
- Snapshot e rascunhos ficam no diretório privado do aplicativo; não são dados reais incluídos no projeto.
- Corrupção da base gera tela de erro, nunca reinicialização silenciosa.
- Desinstalar/limpar os dados do app pode remover a base local. Exporte backups antes.
- UTF-8 inválido e sequências Unicode sem par são recusados, sem substituir caracteres ou alterar os dados atuais. A recuperação de arquivo corrompido copia os bytes originais.
- Importação tem limite de 32 MiB. PNGs têm limites de tamanho/dimensões para reduzir risco de memória; arquivos inválidos são rejeitados antes de modificar a base.

## Compilar e testar

Veja [tools/README.md](tools/README.md) para o caminho Android Studio/Gradle e o build Kotlin reproduzível com dependências oficiais pinadas. O caminho alternativo produz APK real, com Kotlin, recursos Android e DEX; não é um HTML renomeado.

```bash
cd android-native
python3 tools/bootstrap-tools.py
bash tools/test.sh
bash tools/build-apk.sh
```

Requisitos do build alternativo: Linux x86-64, Java 21+, `keytool`, Python 3, Bash e `flock`. O APK requer Android 8/API 26 ou superior e tem target API 36. A configuração Gradle usa Kotlin 1.9.24, Java bytecode 17 e permite JDK 17+.

### Assinatura e atualização

O APK entregue usa uma chave de **teste**, privada e fora do repositório. Ela não é chave de produção e não está no ZIP. Preserve a chave separadamente se precisar gerar atualizações que instalem sobre a mesma aplicação. Builds assinados com outra chave podem exigir desinstalação; faça backup antes. Não há publicação na Play Store, release pública, merge em `master` ou certificado de produção.

### Evidências

A [verificação técnica](VERIFICATION.md) e o relatório entregue identificam fonte, hashes, testes executados e limitações. Testes de regra JVM, testes de Views via Robolectric, compilação/assinatura do APK e testes em aparelho são evidências diferentes: uma não é apresentada como substituta de outra. Não usar este build de teste em operação crítica sem homologação no aparelho e processo reais.
