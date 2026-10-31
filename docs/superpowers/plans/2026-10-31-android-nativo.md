# Android Nativo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement task-by-task. Checklist steps track evidence.

**Goal:** Complete the existing native Kotlin Android branch with the nine existing functional areas and compatible data migration.
**Architecture:** Native Android Views with domain, data, alerts, app modules. Atomic private JSON snapshot persistence preserves browser backup semantics; no WebView.
**Tech Stack:** Kotlin 1.9.24, Android public APIs 26–36, org.json, JVM JUnit, pinned official compiler/packager dependencies.
**Spec:** docs/superpowers/specs/2026-10-31-android-nativo-design.md

## Global Constraints
- Native Kotlin, separate modules; preserve existing web source and generator outputs.
- Use existing android-nativo-kotlin branch; authorized branch pushes only, no merge/release.
- Preserve schemaVersion 1, data identifiers/history and transactional import.
- No real personal data in tests, repository or artifacts. No signing key in source ZIP.
- Foreground alarms only, explicitly disclosed; no background guarantee.
- Tests must run against real implementations; device verification reported separately.

## Review Focus
- Malformed/orphan/duplicate imports preserve every existing collection and metadata.
- Canceled/failed preventive file saves never proceed with replace/demo/clear.
- Reopened/rescheduled/snoozed events obey repeat counts, zero lead/volume and no duplicate claims.
- Inactive referenced master records remain editable in original links but reject new invalid links.
- Rotation/background/Back and large import files do not silently discard committed data or claim false notifications.

### Task 1: Reproducible Kotlin build/test
Files: android-native/tools/*, Gradle configuration, manifests/resources.
- [x] Bootstrap trusted pinned Kotlin/compiler/test dependencies; record provenance/licenses.
- [x] Run existing 2 JUnit tests; build a throwaway Kotlin probe to validate DEX/signature tooling.
- [x] Expose tools/test.sh and tools/build-apk.sh; verify signature/tamper/ZIP checks.

### Task 2: Domain and compatible transactions
Files: domain/src/main/kotlin/.../LivroService.kt, BackupCodec.kt; domain/src/test/kotlin/.../*.kt.
Interfaces: spec's SnapshotStore/LivroService/BackupCodec/MergeResult.
- [x] Write tests first for CRUD relationships, dates/audit, alarms, strict import/merge/replace/CSV.
- [x] Observe RED, implement candidates validated before one save, observe GREEN.
- [x] Preserve existing tests, legacy backup fixtures, zero values and no hidden resets.

### Task 3: Native storage, alert integration and nine-area interface
Files: data/*, alerts/*, app/*.
Interfaces: consume domain contract exactly; no direct mutation outside service.
- [x] Write failing storage/save-failure and UI-state contract tests.
- [x] Implement atomic storage, foreground engine, permission-aware notifications, sound lifecycle.
- [x] Implement nine areas, hierarchy forms, drawing, filters, history, settings/themes/colors, SAF import/export and diagnostics.
- [x] Ensure destructive flows await confirmed preventive export and cancellation is safe.

### Task 4: End-to-end validation and delivery
Files: tests/verification reports, android-native/README.md, artifact packaging scripts.
- [x] Run full JVM suite and APK build/signature validation; inspect APK native classes/resources. Re-run after final review fixes before delivery.
- [x] Attempt real device/emulator verification only through available authorized tools; label unavailable testing accurately. No device/emulator available; API 26/36 Robolectric evidence is separate.
- [x] Obtain independent whole-branch review, fix significant issues with RED→GREEN. Core review and fresh focused final review found no remaining delivery blocker; device acceptance remains separate.
- [ ] Verify remote branch has not advanced, push authorized branch commits without force, verify remote head.
- [ ] Save test APK and source ZIP plus evidence in Library; exclude private keys/build caches/data.

## Delivery record
The final verification report records the exact test counts, artifact hashes and published source revision. External branch publication and Library upload receipts are verified after the source commit; they cannot be inferred from this checklist.
