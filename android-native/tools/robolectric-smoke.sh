#!/usr/bin/env bash
# A real framework Activity/View lifecycle regression for the standalone runner.
set -euo pipefail
TOOLS="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$(cd "$TOOLS/.." && pwd)"
TOOLCHAIN="${TOOLCHAIN_CACHE:-$PROJECT/build/toolchain}"
WORK="${ROBOLECTRIC_CACHE:-$PROJECT/build/robolectric}/smoke-classes"
python3 "$TOOLS/robolectric-bootstrap.py" --verify-only
RCP="$(python3 "$TOOLS/robolectric-bootstrap.py" --verify-only --classpath)"
mkdir -p "$WORK"
exec 9>"$WORK/.lock"
flock 9
java -jar "$TOOLCHAIN/ecj-3.39.0.jar" -17 -proc:none \
  -classpath "$TOOLCHAIN/android-all-16-robolectric-13921718.jar:$RCP" \
  -d "$WORK" "$TOOLS/robolectric-smoke/RobolectricSmokeTest.java"
"$TOOLS/robolectric-run.sh" "$WORK" RobolectricSmokeTest
