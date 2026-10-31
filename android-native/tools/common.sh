#!/usr/bin/env bash
# Shared CLI compiler environment. Source only from scripts using set -euo pipefail.
TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="$(cd "$TOOLS/.." && pwd)"
CACHE="${TOOLCHAIN_CACHE:-$PROJECT/build/toolchain}"
ANDROID="$CACHE/android-framework-compile.jar"
STDLIB="$CACHE/kotlin-stdlib-1.9.24.jar"
ANNOTATIONS="$CACHE/annotations-13.0.jar"
JSON="$CACHE/json-20240303.jar"
JUNIT="$CACHE/junit-4.13.2.jar"
HAMCREST="$CACHE/hamcrest-core-1.3.jar"
COMPILER="$CACHE/kotlin-compiler-embeddable-1.9.24.jar:$STDLIB:$CACHE/kotlin-script-runtime-1.9.24.jar:$CACHE/kotlin-reflect-1.6.10.jar:$CACHE/kotlin-daemon-embeddable-1.9.24.jar:$CACHE/trove4j-1.0.20200330.jar:$ANNOTATIONS"
compile_kotlin() {
  java -cp "$COMPILER" org.jetbrains.kotlin.cli.jvm.K2JVMCompiler \
    -no-stdlib -no-reflect -jvm-target 17 -language-version 1.9 -api-version 1.9 "$@"
}
verify_tools() { python3 "$TOOLS/bootstrap-tools.py" --verify-only --cache "$CACHE"; }
