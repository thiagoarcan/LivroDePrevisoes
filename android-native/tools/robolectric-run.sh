#!/usr/bin/env bash
# Real Robolectric JUnit runner; does not install or invoke the Android SDK.
set -euo pipefail
TOOLS="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$(cd "$TOOLS/.." && pwd)"
FRAMEWORK_DIR="${TOOLCHAIN_CACHE:-$PROJECT/build/toolchain}"
if (( $# < 2 )); then
  echo "Usage: $0 <compiled-classpath> <JUnitTestClass> [...]" >&2
  echo 'compiled-classpath should include main/test/R classes and Kotlin stdlib if needed.' >&2
  exit 2
fi
COMPILED_CLASSPATH="$1"
shift
RCP="$(python3 "$TOOLS/robolectric-bootstrap.py" --verify-only --classpath)"
FRAMEWORK="$(python3 - "$TOOLS/robolectric-artifacts.lock.json" "$FRAMEWORK_DIR" <<'PY'
import hashlib, json, pathlib, sys
entry = json.loads(pathlib.Path(sys.argv[1]).read_text())['framework']
path = pathlib.Path(sys.argv[2]).resolve() / entry['file']
if not path.is_file():
    raise SystemExit(f'Missing original Android framework: {path}; run tools/bootstrap-tools.py')
with path.open('rb') as stream:
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
        digest.update(chunk)
if path.stat().st_size != entry['size'] or digest.hexdigest() != entry['sha256']:
    raise SystemExit(f'Unverified original Android framework: {path}')
print(path)
PY
)"
exec java \
  -Drobolectric.offline=true \
  -Drobolectric.usePreinstrumentedJars=false \
  -Drobolectric.dependency.dir="$(dirname "$FRAMEWORK")" \
  -cp "$COMPILED_CLASSPATH:$FRAMEWORK:$RCP" \
  org.junit.runner.JUnitCore "$@"
