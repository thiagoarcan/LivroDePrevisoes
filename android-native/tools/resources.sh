#!/usr/bin/env bash
# Sourced after common.sh. Compiles the app's native resources and its generated R.
prepare_resources() {
  local work="$1"
  local main="$PROJECT/app/src/main"
  mkdir -p "$work/gen" "$work/r-classes"
  find "$work/gen" "$work/r-classes" -type f -delete
  python3 - "$main/AndroidManifest.xml" "$work/AndroidManifest.xml" <<'PY'
import sys
import xml.etree.ElementTree as ET
ET.register_namespace('android', 'http://schemas.android.com/apk/res/android')
tree = ET.parse(sys.argv[1])
root = tree.getroot()
if root.get('package') not in (None, 'br.com.livrodeprevisoes'):
    raise ValueError('Unexpected Android application package')
root.set('package', 'br.com.livrodeprevisoes')
tree.write(sys.argv[2], encoding='utf-8', xml_declaration=True)
PY
  local link_args=()
  if [[ -d "$main/res" ]] && find "$main/res" -type f | grep -q .; then
    "$CACHE/aapt2" compile --dir "$main/res" -o "$work/compiled-resources.zip"
    link_args+=("$work/compiled-resources.zip")
  fi
  if [[ -d "$main/assets" ]]; then link_args+=(-A "$main/assets"); fi
  "$CACHE/aapt2" link -I "$ANDROID" --manifest "$work/AndroidManifest.xml" \
    --min-sdk-version 26 --target-sdk-version 36 --version-code 1 --version-name 1.0.0 \
    --java "$work/gen" -o "$work/resources.apk" "${link_args[@]}"
  mapfile -d '' r_sources < <(find "$work/gen" -name '*.java' -print0 | sort -z)
  if (( ${#r_sources[@]} > 0 )); then
    java -jar "$CACHE/ecj-3.39.0.jar" -17 -proc:none -warn:none \
      -classpath "$ANDROID" -d "$work/r-classes" "${r_sources[@]}"
  fi
}
