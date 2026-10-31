#!/usr/bin/env bash
# Optional minimum-API test: real Robolectric Android 8 framework, never packaged.
set -euo pipefail
source "$(dirname "$0")/common.sh"
source "$TOOLS/resources.sh"
verify_tools
python3 "$TOOLS/robolectric-bootstrap.py" --verify-only
WORK="$PROJECT/build/robolectric-min26"
mkdir -p "$WORK/main" "$WORK/test"
exec 9>"$WORK/.lock"
flock 9
python3 - "$TOOLS/min-sdk26-artifacts.lock.json" "$WORK" <<'PY'
from pathlib import Path
import hashlib, json, sys, urllib.request
lock, cache = Path(sys.argv[1]), Path(sys.argv[2])
for artifact in json.loads(lock.read_text())['artifacts']:
    name = artifact['file']
    if Path(name).name != name:
        raise ValueError('Invalid minimum-SDK artifact name')
    target = cache / name
    def valid(path):
        return path.is_file() and path.stat().st_size == artifact['size'] and hashlib.sha256(path.read_bytes()).hexdigest() == artifact['sha256']
    if not valid(target):
        if not artifact['url'].startswith('https://repo.maven.apache.org/maven2/org/robolectric/android-all/8.0.0_r4-robolectric-r1/'):
            raise ValueError('Unexpected minimum-SDK framework origin')
        partial = target.with_suffix(target.suffix + '.partial')
        urllib.request.urlretrieve(artifact['url'], partial)
        if not valid(partial):
            partial.unlink(missing_ok=True)
            raise ValueError('Minimum-SDK framework checksum mismatch')
        partial.replace(target)
    print('Verified minimum-SDK framework:', name)
PY
find "$WORK/main" "$WORK/test" -type f -delete
prepare_resources "$WORK"
mapfile -d '' SOURCES < <(find "$PROJECT"/{domain,data,alerts,app}/src/main/kotlin -name '*.kt' -print0 | sort -z)
compile_kotlin -classpath "$STDLIB:$ANNOTATIONS:$ANDROID:$WORK/r-classes" \
  -module-name livro_min_sdk_main -d "$WORK/main" "${SOURCES[@]}"
RCP="$(python3 "$TOOLS/robolectric-bootstrap.py" --verify-only --classpath)"
java -jar "$CACHE/ecj-3.39.0.jar" -8 -proc:none -warn:none \
  -classpath "$WORK/main:$WORK/r-classes:$STDLIB:$ANDROID:$RCP" \
  -d "$WORK/test" "$TOOLS/min-sdk26-tests/MinimumSdk26NativeTest.java"
java -Drobolectric.offline=true -Drobolectric.usePreinstrumentedJars=false \
  -Drobolectric.dependency.dir="$WORK" \
  -cp "$WORK/main:$WORK/test:$WORK/r-classes:$STDLIB:$CACHE/android-all-16-robolectric-13921718.jar:$RCP" \
  org.junit.runner.JUnitCore br.com.livrodeprevisoes.app.MinimumSdk26NativeTest
