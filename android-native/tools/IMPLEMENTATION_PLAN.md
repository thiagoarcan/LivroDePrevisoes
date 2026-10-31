# Native Kotlin toolchain implementation plan

> For agentic workers: use executing-plans task-by-task.

**Goal:** Build and verify a native Kotlin APK and domain/backup JVM tests with pinned official artifacts.
**Architecture:** Standard multi-module Gradle Android project plus independently reproducible Kotlin CLI/AAPT2/D8 fallback. Build-time framework and JVM JSON are excluded from the APK. Test signing identity remains outside the repository.
**Tech stack:** Kotlin 1.9.24, Java bytecode 17, Android API 26–36, JUnit 4.13.2, Python 3, Bash.
**Spec:** Parent handoff: native modules domain, data, alerts, app; package br.com.livrodeprevisoes; no WebView replacement; no release signing.

## Constraints and review focus
- Pin SHA-256, source URL, file size, and upstream SHA-1 where available; preserve licensing.
- Do not read, reuse, or copy any other project's signing key.
- JVM tests must use real org.json, not Android stubs.
- APK must omit Android framework, JUnit, compiler, and JVM-only JSON.
- Test key must not be tracked, bundled, or mistaken for a release key.

## Tasks
- [x] Bootstrap compiler + testing dependencies, verify compiler starts, make tools/test.sh available.
- [x] Add package integrity tests and see an expected failure; implement deterministic packager and verifier.
- [x] Add separate-module compilation and verified APK signing/build scripts.
- [x] Add normal Gradle configs/wrapper and usage/license/limitations documentation.
- [x] Run current complete test suite, build final app, verify v2/v3 signatures, manifests and byte-identical rebuild.
