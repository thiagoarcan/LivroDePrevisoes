# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

checks = {
    # 1. Console no cabeçalho
    "1.1 Header Console Dropdown": 'id="headerActiveConsole"' in content,
    "1.2 Event form displays Active Console badge": 'id="labelEventActiveConsole"' in content,
    "1.3 Hidden Console Input for event submission": 'id="eventConsoleId"' in content,
    "1.4 Filter only active console toggle": 'id="checkFilterOnlyActiveConsole"' in content,

    # 2. Várias ocorrências no mesmo duto
    "2.1 Button Salvar e Inserir Outra neste Duto": 'id="btnSubmitAndNew"' in content,
    "2.2 Checkbox Manter Duto e UO": 'id="checkKeepDutoUO"' in content,
    "2.3 Action Duplicar Evento": 'duplicateEvent' in content and '+ Duplicar' in content,
    "2.4 getCloneDataForEvent in service": 'getCloneDataForEvent' in content,

    # 3. Inserção de duas ou mais UOs (Lote e Inline)
    "3.1 Batch UO service saveUOBatch": 'saveUOBatch' in content,
    "3.2 Batch input hint for UOs (REFAP, TEDEP)": 'REFAP, TEDEP' in content,
    "3.3 Quick inline UO addition in Duto form": 'id="btnInlineAddUO"' in content and 'id="inputInlineNewUO"' in content,

    # 4. Sincronização de UOs no Tipo de Equipamento
    "4.1 Centralized master data synchronization": 'refreshAllMasterDataDropdowns' in content,
    "4.2 Equipment Type UO select updated": 'selectEquipmentTypeUO' in content,

    # 5. Cadastros em aba única sem abas separadas / espaço morto
    "5.1 Unified Cadastros Hub Grid": 'cadastros-hub-grid' in content,
    "5.2 All 5 cadastros tables present simultaneously": all(t in content for t in ['tableConsoles', 'tablePipelines', 'tableUOs', 'tableEquipmentTypes', 'tableEquipmentTags']),

    # 6. Botão de Testar Notificação do Navegador
    "6.1 Prominent Header notification test button": 'id="btnHeaderTestNotif"' in content,
    "6.2 Settings notification test button": 'id="btnTestNotif"' in content,

    # 7. Adaptações para Tablet e Celulares (Touch, Retrátil, Caneta)
    "7.1 Mobile collapsible drawer menu": 'id="appMobileDrawer"' in content and 'id="btnToggleMobileMenu"' in content,
    "7.2 Mobile Drawer overlay": 'id="mobileDrawerOverlay"' in content,
    "7.3 Mobile Floating Action Button (FAB)": 'id="fabAddEvent"' in content,
    "7.4 Stylus / Caneta Canvas Pad": 'id="stylusDrawingCanvas"' in content,
    "7.5 Stylus Canvas controls (Clear, Eraser, Stroke, Color)": all(c in content for c in ['btnClearStylusCanvas', 'btnEraserStylusCanvas', 'inputStylusStrokeColor', 'selectStylusStrokeWidth']),
    "7.6 Pointer events for touch/pen drawing": 'pointerdown' in content and 'pointermove' in content and 'pointerup' in content,
    "7.7 Stylus drawing saved in event": 'stylusDrawing' in content
}

print("=== VERIFICAÇÃO DOS 6 AJUSTES SOLICITADOS ===")
all_passed = True
for name, passed in checks.items():
    status = "OK" if passed else "FALHA"
    print(f"[{status}] {name}")
    if not passed:
        all_passed = False

if all_passed:
    print("\nTODOS OS REQUISITOS E AJUSTES FORAM VERIFICADOS COM 100% DE SUCESSO!")
else:
    print("\nHouve falha em alguns dos itens acima.")

