#!/usr/bin/env bash
# Exercise compiler, native resources, DEX, signing, deterministic rebuild and tamper rejection.
set -euo pipefail
source "$(dirname "$0")/common.sh"
verify_tools
python3 -m unittest discover -s "$TOOLS" -p 'test_*.py' -v
WORK="$PROJECT/build/toolchain-selftest"
FIXTURE="$WORK/project"
mkdir -p "$FIXTURE/tools" "$FIXTURE/app/src/main/res/values"
for source in "$TOOLS"/*.sh "$TOOLS"/*.py "$TOOLS/ApkSignTool.java" "$TOOLS/artifacts.lock.json"; do cp "$source" "$FIXTURE/tools/"; done
for module in domain data alerts app; do mkdir -p "$FIXTURE/$module/src/main/kotlin/sample/$module"; done
cat > "$FIXTURE/domain/src/main/kotlin/sample/domain/Label.kt" <<'KOTLIN'
package sample.domain
class Label { fun value(): String = "Livro Kotlin nativo" }
KOTLIN
cat > "$FIXTURE/data/src/main/kotlin/sample/data/Store.kt" <<'KOTLIN'
package sample.data
import sample.domain.Label
class Store { fun title() = Label().value() }
KOTLIN
cat > "$FIXTURE/alerts/src/main/kotlin/sample/alerts/Message.kt" <<'KOTLIN'
package sample.alerts
import sample.data.Store
class Message { fun text() = Store().title() }
KOTLIN
cat > "$FIXTURE/app/src/main/kotlin/sample/app/MainActivity.kt" <<'KOTLIN'
package sample.app
import android.app.Activity
import android.os.Bundle
import android.widget.TextView
import br.com.livrodeprevisoes.R
import sample.alerts.Message
class MainActivity : Activity() {
    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        setContentView(TextView(this).apply { text = Message().text() + getString(R.string.probe) })
    }
}
KOTLIN
cat > "$FIXTURE/app/src/main/AndroidManifest.xml" <<'XML'
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
  <application android:theme="@android:style/Theme.Material.Light.NoActionBar" android:label="Livro build probe">
    <activity android:name="sample.app.MainActivity" android:exported="true">
      <intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter>
    </activity>
  </application>
</manifest>
XML
printf '%s\n' '<resources><string name="probe"> nativo</string></resources>' > "$FIXTURE/app/src/main/res/values/strings.xml"
export TOOLCHAIN_CACHE="$CACHE"
export LOCAL_TEST_KEYSTORE="${LOCAL_TEST_KEYSTORE:-$(dirname "$(dirname "$PROJECT")")/livro_android_private/livro-test.p12}"
bash "$FIXTURE/tools/build-apk.sh" "$WORK/first.apk"
bash "$FIXTURE/tools/build-apk.sh" "$WORK/second.apk"
cmp "$WORK/first.apk" "$WORK/second.apk"
python3 - "$WORK/first.apk" "$WORK/tampered.apk" <<'PY'
from pathlib import Path
import struct, sys, zipfile
original, target = map(Path, sys.argv[1:])
data = bytearray(original.read_bytes())
with zipfile.ZipFile(original) as package:
    entry = package.getinfo('classes.dex')
    name_len, extra_len = struct.unpack_from('<HH', data, entry.header_offset + 26)
    offset = entry.header_offset + 30 + name_len + extra_len
    data[offset + 100] ^= 1
target.write_bytes(data)
PY
if java -cp "$FIXTURE/build/manual-apk/helper-classes:$CACHE/apksig-9.5.0.jar" ApkSignTool verify "$WORK/tampered.apk" > "$WORK/tamper.log" 2>&1; then
  echo 'ERROR: signature verifier accepted modified DEX' >&2; exit 1
fi
grep -q 'APK signature invalid' "$WORK/tamper.log"
echo 'PASS: native Kotlin modules + resources + DEX + APK v2/v3, byte-identical rebuild, and tamper rejection.'
