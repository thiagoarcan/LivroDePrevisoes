# Livro de Previsões — Android nativo modular

## Autoridade e intenção
O usuário pediu Android **nativo em Kotlin**, módulos separados, aplicativo completo, execução contínua e trabalho direto no GitHub. Essas instruções posteriores substituem a proposta de wrapper, que não será implementada. Adotamos a branch existente `android-nativo-kotlin`, base `e0b70d7794c2a643f5479c92b456e81ea2964cd4`. Não publicar release, mesclar ou operar dados reais.

## Abordagens
A interface web embutida reduziria retrabalho, mas contradiz a escolha explícita. A abordagem adotada é Kotlin com Views Android reais e módulos `domain`, `data`, `alerts`, `app`. Não há WebView. A interface operacional grafite/verde, português, temas claro/industrial e legibilidade touch orientam a adaptação sem copiar geometria desktop.

## Escopo funcional
1. Painel por console, próximos eventos, contagens e ações.
2. Criar/editar/duplicar previsões: hierarquia completa, data/hora local, prioridade, notas, desenho PNG e alertas específicos/padrão.
3. Pendentes: busca/filtros, ordenação temporal, detalhes, histórico, reconhecer/adiar/concluir/excluir logicamente.
4. Concluídos: busca, detalhes/histórico, diferença prevista/real, reabrir e duplicar.
5. Cadastros: consoles, dutos, UOs, relações, tipos de equipamento e TAGs; validar dependências, unicidade e inativação.
6. Alertas: sons, modal, notificação nativa autorizada, antecedência, repetição limitada, reconhecimento, adiamento e auditoria.
7. Cores/temas: faixas contíguas, sem sobreposição, cores válidas, configurações persistidas.
8. Backup: JSON schemaVersion 1 compatível com as 10 coleções de dados do navegador, merge/replace transacional; CSV UTF-8 BOM e ponto-e-vírgula. Logs técnicos são locais, separados das 10 coleções do backup. Substituição/demo/limpeza exigem backup preventivo concluído.
9. Diagnóstico: versão, coleções/contagens, estado de alertas, logs e copiar relatório.

## Dados e segurança
Persistência nativa privada via gravação atômica de snapshot JSON; nunca apagar/reinicializar silenciosamente dados inválidos. Cada operação monta candidato, valida e grava uma vez. Manter nomes de campos, IDs, versões, datas ISO, histórico e compatibilidade de backup do site. Migração é exportar do navegador e importar no Android, não acesso automático ao banco do navegador. SAF para abrir/criar documentos, sem permissão de armazenamento amplo. Sem rede, analytics, autenticação remota ou serviços pagos. Não permitir execução de conteúdo importado; textos são renderizados em Views. Dados do usuário e chaves não entram no Git/source ZIP.

## Alertas e ciclo de vida
Preservar contrato existente: monitoramento enquanto aplicativo aberto/ativo. A aplicação web já declara que não toca fechada. Retomar reavalia vencimentos; parar atividade pausa motor e áudio. Não inventar garantia de segundo plano, exatidão sob Doze ou automação operacional. Mostrar limitação em Alertas e onboarding; notificação requer permissão e canal. Uma eventual fase de alarmes com app fechado exige desenho próprio. Nenhuma ação de reconhecer/concluir pode ocorrer sem comando do operador.

## Arquitetura e contratos
`domain`: modelos existentes + `SnapshotStore { load(): JSONObject?; save(snapshot: JSONObject) }`, `LivroService`, `BackupCodec`, regras puras. JSON é formato de intercâmbio preservado, não interface web.
`data`: `FileSnapshotStore` privado atômico, diagnóstico de falha sem reset.
`alerts`: integração Android para som/notificação e ciclo foreground, sem alterar regras do domínio.
`app`: Activity e componentes nativos organizados por área; seletores, dialogs, listagens, formulários, canvas de desenho, SAF. Conteúdo de UI em português. Back/rotação/estado de formulário respeitados.

Interface de serviço: `snapshot(): JSONObject`, `rows(name): List<JSONObject>`, `settings(): JSONObject`, `saveRecord(store,row): JSONObject`, `setRecordActive(store,id,active)`, `saveEvent(input): JSONObject`, `completeEvent(id,note)`, `reopenEvent(id,date,time)`, `duplicateDraft(id): JSONObject`, `snoozeAlarm(id,minutes)`, `acknowledgeAlarm(id)`, `deleteEvent(id)`, `saveSettings(value)`, `saveColorRanges(rows)`, `dueAlarms(): List<JSONObject>`, `fireAlarm(id,channels): JSONObject?`, `restore(backup,mode,preventiveBackupConfirmed=false): MergeResult`, `loadDemoData(preventiveBackupConfirmed=false)`, `clearAllData(preventiveBackupConfirmed=false)`.
`BackupCodec.validate(snapshot): JSONObject`, `merge(existing,incoming): MergeResult`; `MergeResult(snapshot, inserted, updated, skipped, conflicts: List<String>, applied:Boolean)`. Source helpers generate snapshots with `application`, `schemaVersion`, `exportedAt`, `data`.

## Verificação e limites
Testes JVM reais de regras, persistência, datas, backup inválido/atômico/conflitos, CSV, alarmes e estados. Testes Android/instalação se ambiente acessível; caso contrário declarar ausência, nunca substituir evidência de dispositivo por compilação. Validar APK assinatura, manifest, DEX, CRC e integridade. Build Kotlin reproduzível com dependências oficiais pinadas; chave local exclusiva, não incluída no código. Android 8/API26 mínimo, API36 target como escolha de implementação; sem promessa de Play production. Fonte web e geradores permanecem intactos. Revisão independente antes da entrega. APK de teste, fonte completa, instruções e relatório com limitações explícitas.
