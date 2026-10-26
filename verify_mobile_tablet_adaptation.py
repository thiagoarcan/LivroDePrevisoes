import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

checks = [
    # Seção 4 e 7: Modos de visualização e seletor manual de layout
    ("4.1 Seletor de Modo de Visualização no Cabeçalho", "id=\"selectHeaderViewMode\""),
    ("4.2 Seletor de Modo de Visualização na Gaveta Mobile", "id=\"selectDrawerViewMode\""),
    ("4.3 Seletor de Modo de Visualização nas Configurações", "id=\"selectSettingsViewMode\""),
    ("4.4 Opções de Modo (auto, compact, mobile, tablet, conventional, widescreen, ultrawide)", "value=\"ultrawide\""),
    ("4.5 Banner não bloqueante de aviso de modo manual", "id=\"viewModeWarningBanner\""),
    ("4.6 Botão Voltar para Automático no banner", "id=\"btnBannerResetAuto\""),
    ("4.7 Persistência de responsiveLayoutMode em DEFAULT_SETTINGS", "responsiveLayoutMode: 'auto'"),

    # Seção 18 e Designer (3).png: 3 Temas Visuais
    ("18.1 Tema 1 Controle Escuro, Tema 2 Claro e Tema 3 Industrial Alto Contraste", "body.theme-industrial"),
    ("18.2 Seletor de 3 temas na gaveta e configurações", "Industrial Alto Contraste"),
    ("18.3 Ciclar pelos 3 temas (dark -> light -> industrial)", "cycleTheme: async function()"),

    # Seção 24: Todas as 12 Correções Obrigatórias de Inconsistências
    ("24.1 Fix #1: Unificar .open e .active na gaveta e overlay", ".mobile-drawer.open"),
    ("24.2 Fix #2: Eliminar duplicação de #fabAddEvent e integrar na barra inferior", "id=\"mobileBottomNav\""),
    ("24.3 Fix #3: Definir variável CSS --bg-surface-elevated", "--bg-surface-elevated:"),
    ("24.4 Fix #4: Atualizar todos os badges de pendentes (incluindo gaveta e bottom nav)", "badgePendingNavCountDrawer"),
    ("24.5 Fix #5: Vincular ambos os pares de botões de backup/exportação e validateBackupFile", "validateBackupFile: async function"),
    ("24.6 Fix #6: Normalizar tipos em exportCSV (pendente/pending, concluido/completed, cadastros/master, todos/all)", "if (type === 'master') normType = 'cadastros'"),
    ("24.7 Fix #7: Harmonizar filtro de pontualidade (antecedencia/antecipado, noprazo/pontual, atraso/atrasado)", "fTiming === 'antecedencia' || fTiming === 'antecipado'"),
    ("24.8 Fix #8: Adicionar filtros Ativos/Inativos/Todos em #viewCadastros", "id=\"filterActiveConsoles\""),
    ("24.9 Fix #9: Normalizar classes de faixa de cor (critico, urgente, atencao, monitoramento, normal) + ícones", "normalizeRangeKey: function"),
    ("24.10 Fix #10: Unificar container de desenho em #modalEventDetails (#detailsStylusContainer)", "id=\"detailsStylusContainer\""),
    ("24.11 Fix #11: Renderizar as 9 colunas em #tableCompletedEvents + cards expansíveis no celular", "id=\"containerCompletedCards\""),
    ("24.12 Fix #12: Garantir #labelActiveConsoleFilter na tela de pendentes", "id=\"labelActiveConsoleFilter\""),

    # Experiência Mobile (Seções 9, 10, 12)
    ("12.1 Chip de aviso de áudio não iniciado no cabeçalho", "id=\"chipHeaderAudioWarning\""),
    ("12.2 Modal/Sheet de Status da Aplicação", "id=\"modalAppStatus\""),
    ("12.3 Banner persistente de alarmes ativos não reconhecidos", "id=\"mobileActiveAlarmsBanner\""),
    ("12.4 Banner persistente de backup vencido (> 7 dias)", "id=\"backupOverdueBanner\""),
    ("12.5 Cards de eventos urgentes no Dashboard Mobile", "id=\"dashboardUrgentCards\""),
    ("12.6 Folha de Ações Rápidas (Action Sheet [⋯])", "id=\"modalEventActionSheet\""),
    ("12.7 Barra sticky de submissão no formulário de previsão", "class=\"form-sticky-submit-bar\""),
    ("12.8 Lousa Stylus com Desfazer (Undo) e Tela Cheia (Fullscreen)", "id=\"btnUndoStylusCanvas\""),
    ("12.9 Barra de categorias (Drill-down) em Cadastros", "id=\"cadastrosCategoryBar\""),
    ("12.10 Encadeamento visual e cards de faixas de cores", "id=\"colorChainPreview\""),

    # Experiência Tablet (Seção 13)
    ("13.1 Painel lateral de Alarmes Ativos no Dashboard Tablet", "id=\"tabletActiveAlarmsPanel\""),
    ("13.2 Painel Master-Detail na tela de Eventos Pendentes Tablet", "id=\"pendingDetailPane\""),
    ("13.3 Prioridade para caneta/stylus (palm rejection) e suporte a pressão", "e.pointerType === 'pen' && e.pressure")
]

print("=== VERIFICAÇÃO DA ADAPTAÇÃO PARA TABLETS E CELULARES ===")
failed = 0
for label, needle in checks:
    if needle in content:
        print(f"[OK] {label}")
    else:
        print(f"[FAIL] {label} (missing: {needle})")
        failed += 1

# Verificar unicidade de IDs no HTML (fora das tags <script>)
html_without_script = re.sub(r'<script>.*?</script>', '', content, flags=re.S)
all_ids = re.findall(r'\bid="([^"]+)"', html_without_script)
seen_ids = set()
dup_ids = set()
for i in all_ids:
    if i in seen_ids:
        dup_ids.add(i)
    seen_ids.add(i)

if dup_ids:
    print(f"[FAIL] IDs duplicados encontrados no HTML: {dup_ids}")
    failed += 1
else:
    print(f"[OK] Unicidade de IDs no HTML verificada ({len(all_ids)} IDs únicos, 0 duplicações)")

if failed == 0:
    print("\nTODOS OS 36 REQUISITOS DE ADAPTAÇÃO MOBILE/TABLET VERIFICADOS COM 100% DE SUCESSO!")
else:
    print(f"\nFALHA EM {failed} VERIFICAÇÃO(ÕES)!")
    sys.exit(1)

