#!/usr/bin/env bash
# Compile current production Kotlin/resources for real Activity JVM tests; no signing.
set -euo pipefail
source "$(dirname "$0")/common.sh"
source "$TOOLS/resources.sh"
verify_tools
python3 "$TOOLS/robolectric-bootstrap.py" --verify-only
WORK="${ROBOLECTRIC_CACHE:-$PROJECT/build/robolectric}/native-ui"
mkdir -p "$WORK"
exec 9>"$WORK/.lock"
flock 9
mkdir -p "$WORK/main" "$WORK/test"
find "$WORK/main" "$WORK/test" -type f -delete
prepare_resources "$WORK"
mapfile -d '' SOURCES < <(find "$PROJECT"/{domain,data,alerts,app}/src/main/kotlin -name '*.kt' -print0 | sort -z)
compile_kotlin -classpath "$STDLIB:$ANNOTATIONS:$ANDROID:$WORK/r-classes" \
  -module-name livro_robolectric_main -d "$WORK/main" "${SOURCES[@]}"
RCP="$(python3 "$TOOLS/robolectric-bootstrap.py" --verify-only --classpath)"
mapfile -d '' TEST_SOURCES < <(find "$TOOLS/robolectric-native-tests" -name '*.java' -print0 | sort -z)
# Java 8 source mode avoids JPMS split-package errors from Android's java.lang helpers.
# The application remains Kotlin/JVM 17; execution uses Java 21.
java -jar "$CACHE/ecj-3.39.0.jar" -8 -proc:none -warn:none \
  -classpath "$WORK/main:$WORK/r-classes:$STDLIB:$ANDROID:$RCP" \
  -d "$WORK/test" "${TEST_SOURCES[@]}"
if (( $# > 0 )); then
  TESTS=("$@")
else
  mapfile -t TESTS < <(find "$WORK/test" -name '*Test.class' ! -name '*\$*' | sort | sed "s|^$WORK/test/||;s|/|.|g;s|\.class$||")
fi
"$TOOLS/robolectric-run.sh" "$WORK/main:$WORK/test:$WORK/r-classes:$STDLIB" "${TESTS[@]}"
