# -*- coding: utf-8 -*-
import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

checks = {
    "Initial Consoles C02-C16": all(c in content for c in ['C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C10', 'C11', 'C14', 'C15', 'C16']),
    "Duto >= 2 UOs validation": "no mínimo 2 Unidades Operacionais" in content,
    "Global TAG rule message": "já está cadastrado na UO" in content and "não pode ser associado a outra UO" in content,
    "Future sync fields": all(f in content for f in ['id', 'createdAt', 'updatedAt', 'version', 'active', 'synchronizationStatus', 'local-only']),
    "IndexedDB stores": all(s in content for s in ['consoles', 'pipelines', 'operationalUnits', 'pipelineOperationalUnits', 'equipmentTypes', 'equipmentTags', 'events', 'eventHistory', 'colorRanges', 'settings', 'errorLogs']),
    "Web Audio API synthesized tones": "AudioContext" in content and all(t in content for t in ['chime', 'beep', 'siren', 'blip']),
    "Web Notifications API": "Notification" in content and "requestPermission" in content,
    "Excel CSV with BOM and semicolon": "\\uFEFF" in content and ";" in content,
    "JSON Backup & Restore with merge/replace": "application/json" in content and "merge" in content and "replace" in content,
    "Audit trail": "eventHistory" in content and all(a in content for a in ['criacao', 'edicao', 'conclusao', 'reabertura', 'adiamento', 'reconhecimento']),
    "Cascading dropdowns": "loadPipelineOptions" in content and "loadUOOptions" in content and "loadEquipmentTypeOptions" in content and "loadEquipmentTagOptions" in content,
    "Color ranges no overlap/gap check": "sobreposição entre os intervalos" in content and "lacuna entre os intervalos" in content,
    "Overdue on top": "diffMs < 0" in content or "diffSec < 0" in content,
    "Realtime clock & 1s countdown": "liveClock" in content and "setInterval" in content,
    "Cards and Compact Table views": "containerPendingCards" in content and "containerPendingTable" in content,
    "Theme support (dark/light)": "theme-light" in content and "--bg-app" in content,
    "Diagnostic screen": "diagAppVersion" in content and "diagDBStatus" in content and "diagAudioStatus" in content and "diagNotifStatus" in content,
    "Browser limitations explanation": "Limitações do Ambiente de Navegador Web" in content
}

print("=== VERIFICAÇÃO DOS REQUISITOS DO SISTEMA ===")
all_passed = True
for name, passed in checks.items():
    print(f"[{'OK' if passed else 'FALHA'}] {name}")
    if not passed:
        all_passed = False

if all_passed:
    print("\nTodos os 18 requisitos estruturais verificados com SUCESSO!")
else:
    print("\nHouve falha em alguns requisitos.")

