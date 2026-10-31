# Native bounded event lists — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement task-by-task; use TDD before production changes.

**Goal:** Bound pending/completed native event lists to 100 rendered cards while retaining all matching data and operational actions.

**Architecture:** Filter and sort the complete render-scoped snapshot first, then calculate clamped page bounds and render one slice. Keep page index in Activity state; no storage, backup, domain, network, or dependency change. Existing list controls remain mounted during filtering and mutation refreshes.

**Tech Stack:** Kotlin 1.9.24, native Android Views, JVM JUnit, Robolectric API36.

**Spec:** `docs/superpowers/specs/2026-10-31-android-nativo-design.md`; parent approved the pagination proposal on 2026-10-31 at 14:23:41 UTC.

## Global Constraints
- At most 100 event cards and clock watchers per list page.
- Portuguese range text `Exibindo 1–100 de 500`; native `Anterior` / `Próxima` controls at top and bottom, disabled at bounds.
- All search/filter criteria operate over all events, before slicing; no record is discarded.
- Search/filter edits reset to first page. Mutations preserve the current page where valid, otherwise clamp.
- Details/back and Activity recreation retain page index. Explicit pagination scrolls to result start; mutations do not replace search/filter controls.
- No dependency additions, persistence/schema changes, or other UI rewrites. Commits and publication remain parent-owned.

## Review Focus
1. Exact multiples, partial last pages and empty sets must not omit or duplicate rows.
2. Searching for a row not on the visible page must still return it.
3. Removing the final result on the final page must clamp to a remaining page.
4. Returning from details/recreating Activity must retain the page without initial Spinner callbacks resetting it.
5. Paging/filtering must release obsolete watchers, preserve controls, and cause no extra store reads.

## Task 1 — Pure bounded range
Files: `app/.../UiState.kt`, `app/src/test/.../UiStateTest.kt`.
- [x] Add literal tests for totals 0, 1, 100, 101, 500; negative/oversized page; shrinking total; all 500 indices reachable once.
- [x] Observe RED against unbounded behavior.
- [x] Implement `PageBounds(page:Int,start:Int,endExclusive:Int,total:Int)` and `pageBounds(total:Int,requestedPage:Int,size:Int=100)` with validated arguments and clamped indices.
- [x] Run pure tests GREEN.

## Task 2 — Native list integration
Files: `MainActivity.kt`, `EventScreens.kt`, `tools/robolectric-native-tests/NativeRenderCacheTest.java` (toolchain worker owns runtime tests).
- [x] Runtime cap regression observed RED: expected 100 card watchers, actual 500.
- [x] Extend runtime assertions: all 500 reachable; off-page full search; zero additional store loads; mutation clamp; page retention; field identity.
- [x] Add `listPage` Activity state and Bundle persistence. Reset only on actual navigation/filter changes, not unchanged initial Spinner selections.
- [x] Apply bounds after complete filtering/sorting in `fill`; show total/range and top/bottom pagers; explicitly scroll on pager clicks only.
- [x] Maintain subtree watcher cleanup and mutation-refresh clamping.
- [x] Run all JVM and runtime suites, then notify parent/toolchain source freeze for rebuild.

## Adjacent recovery boundary approved during execution
On 2026-10-31 at 14:27 UTC, parent requested staged replacement imports reuse `readBounded` on an input stream before `BackupCodec.parse`, rather than permissive `File.readText`. The runtime regression must corrupt staged UTF-8, finish the preventive export, then verify replacement fails and live data remains unchanged. This is a one-line `BackupScreens.kt` boundary correction, not a new workflow.

## Verification outcome
- Pure pagination: 3 observed assertion failures (unbounded 500 vs expected 100, partial-page and clamp failures), then GREEN.
- Complete JVM suite: 101 tests passed, exit 0; tool output observed 2026-10-31 14:31:38 UTC. Transparent post-run capture: `android-native/build/delivery-evidence/ui-final-101-post-run-capture.log`.
- Actual Android framework via Robolectric: 26 tests passed, 76.719 seconds. Live tee: `android-native/build/robolectric/native-26-paged-verification.log`. Includes all 500 unique rows reachable, 100 maximum watchers, no extra page/search store reads, filter resets, 500→250 mutation clamp, detail return and Activity recreation page/query persistence, live deadline/field identity, staged UTF-8 rejection after preventive export, and existing native workflows.
- Initial pagination/staged-import source freeze: 2026-10-31 14:30:10 UTC, superseded by the narrow navigation review correction below. APK rebuilding/publication remains parent-owned; no device-rendering claim is made.

## Final navigation consistency review
At 2026-10-31 14:32:59 UTC, the parent approved one narrow review correction: system/predictive Back from pending/completed details must return to the originating list without resetting page, query or filters, matching the explicit list-return action. Dirty-draft confirmation and root finishing remain unchanged. A native registered-callback regression is required RED→GREEN before the `MainActivity.handleBack` branch changes.

The actual registered API36 callback reproduced the review defect (expected pending list, actual dashboard). The narrow branch was corrected at 2026-10-31 14:36:33 UTC. The registered-callback regression passed for both pending and completed lists, preserving page 2, query and date filter; existing dirty-draft and root Back behavior also passed. Complete JVM verification uses live tee `android-native/build/delivery-evidence/ui-final-jvm-live.log`.

## Final frozen handoff
- Final complete JVM suite: **101 passed**, exit 0, 0.968 seconds; live log `android-native/build/delivery-evidence/ui-final-jvm-live.log`.
- Final combined native framework suite: **27 passed**, runner exit 0, 58.15 seconds; live log `android-native/build/robolectric/native-27-final-verification.log`. Includes pagination, same-list predictive Back, full search, page clamping/restoration, cached reads, live clock, raw-byte recovery and staged UTF-8 protection.
- Independent review closed with no remaining findings in scope.
- Production Kotlin source has not changed since **2026-10-31 14:36:33 UTC**. Documentation completed after reading the final aggregate output on 2026-10-31 at 14:44:55 UTC. No further source or documentation edits are planned after handoff; parent owns commit, APK packaging and publication.
