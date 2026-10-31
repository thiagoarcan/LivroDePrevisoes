#!/usr/bin/env bash
# Native Kotlin Android APK. Compiler/module outputs are not a WebView wrapper.
set -euo pipefail
source "$(dirname "$0")/common.sh"
source "$TOOLS/resources.sh"
verify_tools
OUT="${1:-$PROJECT/build/livro-de-previsoes-local-test.apk}"
WORK="$PROJECT/build/manual-apk"
mkdir -p "$WORK"
exec 9>"$WORK/.lock"
flock 9
KEY="${LOCAL_TEST_KEYSTORE:-$(dirname "$(dirname "$PROJECT")")/livro_android_private/livro-test.p12}"
JAVA_RUNTIME="${JAVA_HOME:-$(dirname "$(dirname "$(readlink -f "$(command -v java)")")")}"
# Never write a signing key inside the source checkout, even if explicitly passed.
python3 - "$PROJECT/.." "$KEY" <<'PY'
from pathlib import Path
import sys
repository, key = map(lambda value: Path(value).resolve(), sys.argv[1:])
if key.is_relative_to(repository):
    raise ValueError('LOCAL_TEST_KEYSTORE must be outside the source repository')
PY
mkdir -p "$WORK/classes" "$WORK/dex" "$WORK/helper-classes" "$(dirname "$OUT")"
find "$WORK/classes" "$WORK/dex" "$WORK/helper-classes" -type f -delete
prepare_resources "$WORK"
CLASSPATH="$STDLIB:$ANNOTATIONS:$ANDROID:$WORK/r-classes"
JARS=()
for module in domain data alerts app; do
  mapfile -d '' sources < <(find "$PROJECT/$module/src/main/kotlin" -name '*.kt' -print0 | sort -z)
  (( ${#sources[@]} > 0 )) || { echo "No Kotlin sources found for module $module" >&2; exit 1; }
  mkdir -p "$WORK/classes/$module"
  echo "Compiling native Kotlin module :$module (${#sources[@]} source files)"
  compile_kotlin -classpath "$CLASSPATH" -module-name "livro_$module" -d "$WORK/classes/$module" "${sources[@]}"
  python3 "$TOOLS/jar-classes.py" "$WORK/classes/$module" "$WORK/$module.jar"
  JARS+=("$WORK/$module.jar")
  CLASSPATH="$CLASSPATH:$WORK/$module.jar"
done
python3 "$TOOLS/jar-classes.py" "$WORK/r-classes" "$WORK/resources.jar"
# ONLY application modules, generated R, and the pinned Kotlin runtime are inputs.
# Framework, compiler, annotations, JVM JSON, and test libraries are never packaged.
java -cp "$CACHE/r8-9.5.28.jar" com.android.tools.r8.D8 --release \
  --min-api 26 --lib "$ANDROID" --lib "$JAVA_RUNTIME" --output "$WORK/dex" \
  "${JARS[@]}" "$WORK/resources.jar" "$STDLIB"
python3 "$TOOLS/pack-apk.py" "$WORK/resources.apk" "$WORK/dex" "$WORK/unsigned.apk" "$CACHE/licenses"
if [[ ! -f "$KEY" ]]; then
  (umask 077; mkdir -p "$(dirname "$KEY")"; keytool -genkeypair -keystore "$KEY" -storetype PKCS12 \
    -storepass android -keypass android -alias androiddebugkey -keyalg RSA -keysize 2048 \
    -validity 10000 -dname 'CN=Livro local test only,OU=Development,O=Livro de Previsoes,C=BR' -noprompt)
fi
java -jar "$CACHE/ecj-3.39.0.jar" -17 -proc:none -warn:none \
  -classpath "$CACHE/apksig-9.5.0.jar" -d "$WORK/helper-classes" "$TOOLS/ApkSignTool.java"
java -cp "$WORK/helper-classes:$CACHE/apksig-9.5.0.jar" ApkSignTool sign "$WORK/unsigned.apk" "$OUT" "$KEY"
python3 "$TOOLS/verify-apk-zip.py" "$OUT"
"$CACHE/aapt2" dump badging "$OUT" > "$WORK/badging.txt"
grep -q "package: name='br.com.livrodeprevisoes'" "$WORK/badging.txt"
grep -Eq "^(minSdkVersion|sdkVersion):'26'" "$WORK/badging.txt"
grep -q "targetSdkVersion:'36'" "$WORK/badging.txt"
sha256sum "$OUT"
echo "Built native Kotlin locally test-signed APK: $OUT"
