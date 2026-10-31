# Matriz de aceitação Android nativo

**Estado:** roteiro preparado; não representa execução em dispositivo/emulador. Registrar aparelho, API, versão do APK, data, resultado e evidência em cada linha ao executar. Usar exclusivamente dados sintéticos.

## Ambiente e apresentação
- Instalar APK em Android 8/API26 e versão atual; iniciar sem rede. Confirmar ausência de WebView, solicitações de Internet e armazenamento amplo.
- Primeiro uso: aviso explícito de alertas apenas com app aberto/ativo; dispensar e verificar que não se repete.
- Abrir todas as nove áreas pelo menu e pela navegação. Conferir grafite, claro e industrial, TalkBack, fonte 200%, toque mínimo 48 dp, contraste, teclado, barras/insets do sistema.
- Telefone em retrato/paisagem e tablet: rolar conteúdo, alcançar salvar/cancelar, manter desenho e textos ao girar. Alterar tema e confirmar persistência após reiniciar.

## Cadastros e previsões
- Criar console, duas UOs, duto com ambas, tipo dentro da UO e TAG dentro de tipo/UO. Testar lote de UOs, nomes vazios, duplicados e acentos.
- Editar cada categoria; inativar/reativar; tentar excluir pai com dependência. Confirmar erro claro e nenhuma alteração parcial.
- Criar previsão com seletores em cascata, data/hora, prioridade, notas e alarme personalizado. Tentar combinação inválida, data impossível e descrição vazia.
- Selecionar data/hora pelo diálogo nativo; criar evento no passado e cruzando meia-noite. Conferir fuso do aparelho e data original de backup importado.
- Desenhar, desfazer, limpar, desfazer limpeza, salvar e reabrir. Editar somente notas de desenho importado e confirmar que o data URL permanece idêntico no JSON exportado.
- Rotacionar durante formulário e diálogo; sair com alterações deve pedir confirmação. Reiniciar Activity pelo sistema com rascunho e conferir restauração (não usar força-parada como garantia de salvamento).

## Operação e alertas
- Painel: contagens por console e próximo evento; comparar filtros e ordenação com dados de teste. Prazos de 1 segundo a menos devem aparecer atrasados.
- Pendentes/concluídos: busca com/sem acento, filtros de hierarquia, prioridade, datas, alarme e prazo; limpar filtros. Com 500 registros, percorrer cinco páginas de até 100 cartões, conferir contagem total/intervalo e buscar registro fora da página atual. Mudanças de filtro reiniciam a primeira página; alterações de dados ajustam a última página sem perder resultados. Voltar dos detalhes pelo botão explícito, pelo botão do sistema e pelo gesto preditivo deve preservar a lista, página, busca e filtros; recriar Activity também deve preservar a página. Completar, ver diferença real-prevista e histórico, reabrir com horário e duplicar.
- Excluir previsão: confirmar inativação e preservação do histórico no backup.
- Salvar nome do operador e confirmar autoria nas ações. Som com volume 0/80/100 e quatro timbres; teste visual; permissão de notificação negada/concedida.
- Alarme em primeiro plano: um disparo inicial, intervalos e máximo de repetições, reconhecer, adiar, concluir, vários simultâneos. Conferir histórico de canais realmente entregues.
- Colocar app em segundo plano/bloquear tela: monitoramento deve pausar, sem promessa de alarme. Retomar e reavaliar vencidos; nenhum reconhecimento/conclusão automático.

## Backup e recuperação
- Exportar JSON via SAF para provedor local, importar por mescla e por substituição. Exportar quatro modalidades CSV; verificar BOM UTF-8, ponto e vírgula, aspas, quebras e neutralização de fórmulas.
- Cancelar importação e exportação: dados idênticos antes/depois. Substituir/demo/limpar só após documento preventivo fechado com sucesso.
- Simular provedor SAF que falha ao abrir, escrever, flush ou close: não executar ação destrutiva; explicar eventual arquivo incompleto. Recriar Activity enquanto SAF está aberto e completar/cancelar.
- JSON inválido/truncado, coleção ausente, relações inexistentes, conflito de versão, PNG inválido, imagem excessiva e arquivo >32 MiB: mensagem e armazenamento intacto. Corromper o UTF-8 do arquivo de importação já preparado antes de finalizar o backup preventivo: rejeitar a substituição e manter o snapshot atual intacto.
- Corromper snapshot privado no ambiente de teste: mostrar erro sem reinicializar; exportar cópia original. Disco cheio: erro original legível mesmo se gravar diagnóstico também falhar.

## Cores e diagnóstico
- Faixas válidas contíguas desde zero; rejeitar lacuna, sobreposição, vazio e cor inválida. Adicionar/remover em rascunho e salvar conjunto atômico.
- Diagnóstico: versão, API, fuso, contagens, permissão e logs; copiar relatório e limpar apenas logs. Confirmar que relatórios não incluem descrições das previsões.

## Evidência automática desta versão (não substitui execução manual)

- 101 testes JVM aprovados no conjunto completo.
- 27 testes com framework Android real via Robolectric aprovados, incluindo navegação, cinco páginas com todos os 500 registros, limite de 100 cartões, busca global, preservação de página/filtros no Voltar preditivo, rotação/recriação, SAF cancelado/com falhas, recuperação byte a byte, importação preparada com UTF-8 corrompido, relógio e alertas assíncronos.
- Logs de referência: `build/delivery-evidence/ui-final-jvm-live.log` e `build/robolectric/native-27-final-verification.log`.
- Aparelho físico, renderização visual, áudio percebido, TalkBack, provedores SAF reais e comportamento de fabricantes continuam exigindo a matriz manual acima.
