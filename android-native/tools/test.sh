#!/usr/bin/env bash
# Real JUnit JVM tests: Android framework only on compile classpath, never runtime.
set -euo pipefail
source "$(dirname "$0")/common.sh"
verify_tools
WORK="${TEST_WORK_DIR:-$PROJECT/build/manual-tests}"
mkdir -p "$WORK"
exec 9>"$WORK/.lock"
flock 9
mkdir -p "$WORK/main" "$WORK/test"
find "$WORK/main" "$WORK/test" -type f -delete
MAIN_SOURCES=()
TEST_SOURCES=()
RESOURCE_CLASSPATH=""
for module in ${TEST_MODULES:-domain data alerts app}; do
  for kind in main test; do
    if [[ -d "$PROJECT/$module/src/$kind/resources" ]]; then RESOURCE_CLASSPATH+=":$PROJECT/$module/src/$kind/resources"; fi
  done
  if [[ -d "$PROJECT/$module/src/main/kotlin" ]]; then
    while IFS= read -r -d '' file; do MAIN_SOURCES+=("$file"); done < <(find "$PROJECT/$module/src/main/kotlin" -name '*.kt' -print0 | sort -z)
  fi
  if [[ -d "$PROJECT/$module/src/test/kotlin" ]]; then
    while IFS= read -r -d '' file; do TEST_SOURCES+=("$file"); done < <(find "$PROJECT/$module/src/test/kotlin" -name '*.kt' -print0 | sort -z)
  fi
done
(( ${#MAIN_SOURCES[@]} > 0 && ${#TEST_SOURCES[@]} > 0 )) || { echo 'No main/test Kotlin sources found' >&2; exit 1; }
R_CLASSPATH=""
if [[ " ${TEST_MODULES:-domain data alerts app} " == *" app "* ]] && [[ -f "$PROJECT/app/src/main/AndroidManifest.xml" ]]; then
  source "$TOOLS/resources.sh"
  prepare_resources "$WORK"
  R_CLASSPATH=":$WORK/r-classes"
fi
# Put real JSON first so JVM tests compile against its actual implementation.
compile_kotlin -classpath "$STDLIB:$ANNOTATIONS:$JSON:$ANDROID$R_CLASSPATH" -module-name livro_test_main -d "$WORK/main" "${MAIN_SOURCES[@]}"
compile_kotlin -classpath "$WORK/main:$STDLIB:$ANNOTATIONS:$JSON:$ANDROID$R_CLASSPATH:$JUNIT:$HAMCREST" \
  -Xfriend-paths="$WORK/main" -module-name livro_tests -d "$WORK/test" "${TEST_SOURCES[@]}"
if (( $# > 0 )); then
  TESTS=("$@")
else
  mapfile -t TESTS < <(find "$WORK/test" -name '*Test.class' ! -name '*\$*' | sort | sed "s|^$WORK/test/||;s|/|.|g;s|\.class$||")
fi
(( ${#TESTS[@]} > 0 )) || { echo 'No JUnit *Test classes found' >&2; exit 1; }
java -cp "$WORK/main:$WORK/test:$STDLIB:$JSON:$JUNIT:$HAMCREST$RESOURCE_CLASSPATH" org.junit.runner.JUnitCore "${TESTS[@]}"
