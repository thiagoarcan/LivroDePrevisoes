# Native Kotlin Android build and test tools

This project has **four real Kotlin modules** (`domain`, `data`, `alerts`, `app`)
and native Android views. The fallback uses the official Kotlin JVM compiler,
AAPT2, D8 and AOSP apksig; it does not convert the web application, substitute
Java for Kotlin, or bundle a WebView.

## Standard Android Studio / Gradle route

Open `android-native` with Android Studio. Install JDK 17 or 21 and the Android SDK
platform 36 through the normal SDK manager and accept any licences yourself.
Then run from `android-native`:

```sh
./gradlew :domain:test :data:test :alerts:testDebugUnitTest :app:testDebugUnitTest :app:assembleDebug
```

Gradle **8.13** and Android Gradle Plugin **8.13.0** support API 36. Kotlin is
**1.9.24**, Java/Kotlin bytecode targets **17**, minimum Android API **26** and
target API **36**. The Gradle distribution checksum is enforced in
`gradle/wrapper/gradle-wrapper.properties`; the official wrapper JAR was checked
against the Gradle-published SHA-256. Wrapper script/JAR provenance:
`https://github.com/gradle/gradle/tree/v8.13.0`.

```sh
sha256sum -c tools/GRADLE_WRAPPER_SHA256SUMS
```

A full SDK/Gradle build is a separate verification path from the fallback.
Do not describe a successful manual APK build as an Android Gradle Plugin,
Android lint, emulator, device, or Play release test.

## Reproducible SDK-independent fallback

Requirements: Linux x86-64/glibc, Java runtime 21+ and `keytool`, Bash,
`flock`, and Python 3. It was verified with OpenJDK 21.0.12.1.
No SDK installation or SDK licence acceptance is performed.

```sh
cd android-native
python3 tools/bootstrap-tools.py
bash tools/test.sh
bash tools/build-apk.sh
```

Output: `build/livro-de-previsoes-local-test.apk`. Optional first build argument
selects another output APK. `TOOLCHAIN_CACHE=/absolute/path` overrides the
ignored `build/toolchain` cache. Artifact provenance, sizes and pinned hashes
are in `artifacts.lock.json`; initial Maven downloads also checked repository
SHA-1 files. Cached artifacts are verified before every test/build.

```sh
(cd build/toolchain && sha256sum -c ../../tools/SHA256SUMS)
bash tools/selftest.sh
```

`selftest.sh` creates an isolated **test fixture**, not the delivered app. It
compiles four Kotlin modules, native `Activity`/`TextView` and a generated `R`
class; builds twice; checks byte equality, Android package/API levels, v2/v3
signatures, ZIP CRCs, DEX hashes, alignment, Kotlin licensing, and dependency
boundaries; then proves a modified DEX is rejected by signature verification.
Its log/output can be kept under ignored `build/`.

### Tests and concurrent work

`test.sh` compiles `src/main/kotlin` and `src/test/kotlin` in all four modules,
then runs JUnit classes named `*Test`. Main/test resources are included on the
runtime classpath. AAPT2 generates app `R` if needed. Tests
use the real Maven `org.json` implementation. The Android framework is on the
**compile classpath only**; unit tests must not instantiate Android classes.
Android-view tests need a real runner such as Robolectric, not the framework
jar by itself.

```sh
TEST_MODULES='domain data' TEST_WORK_DIR=/tmp/livro-data-tests bash tools/test.sh
TEST_MODULES=domain bash tools/test.sh br.com.livrodeprevisoes.domain.PrevisaoTest
python3 -m unittest discover -s tools -p 'test_*.py' -v
```

Each work directory is locked to avoid concurrent compiler output races; cache
bootstrap is also locked. The normal default test output is
`build/manual-tests`, and APK intermediates are `build/manual-apk`.

### Signing: private test key, not a release key

The default key is **outside the repository**, in the sibling directory
`livro_android_private/livro-test.p12`. For this workspace its complete path is
`/workspace/shared/livro_android_private/livro-test.p12`. Explicitly select it
or another private development key:

```sh
LOCAL_TEST_KEYSTORE=/private/path/livro-test.p12 bash tools/build-apk.sh
```

The first build creates an RSA 2048-bit test key with restrictive permissions,
using the standard development password `android` and alias
`androiddebugkey`. The script refuses a key path inside the repository.
**Do not publish this key or use this signing identity for production.**
Preserve it privately if subsequent local APKs must update the same install;
a different key requires uninstalling the old app first (which can erase data).
Identical source, tools, runtime and signing key produce identical APK bytes.

### Platform/compiler separation

Robolectric's Apache-licensed Android 16/API 36 framework source build is used
for compilation/resource linking, never bundled in the APK. Its original JAR
contains unrelated Kotlin 2.x runtime and module metadata; bootstrap derives
`android-framework-compile.jar` by removing `kotlin/`, `kotlinx/`, and
`*.kotlin_module` entries without changing Android classes or resources.
This prevents foreign Kotlin metadata conflicting with Kotlin 1.9.24.
The original JAR stays byte-identical to its pinned upstream artifact.

The fallback compiles each app module separately, enforcing Kotlin module
visibility. Only module class JARs, generated `R`, and Kotlin stdlib are D8
program inputs. JVM JSON, Android framework, compiler, annotations, JUnit and
Robolectric are **not** APK inputs. The verifier additionally reads DEX class
**definitions** to reject accidental framework/JSON/test/compiler inclusion.
The app uses platform `org.json` on Android.

Limitations: no official SDK hidden-API checking or lint, no native libraries,
no AndroidX dependency graph, no manifest/resource merging across libraries,
no R8 shrinking, AAB/Play signing, or device/runtime guarantees. App manifest
and resources are owned by `app/src/main`; source manifest omits `package`
for modern AGP and the fallback injects it only into a derived copy.
Use only public Android APIs and validate installed behavior separately.

## Dependencies / licences

Downloaded files are caches, not committed binaries (except the official
small Gradle wrapper JAR). Complete original POMs are hash-pinned and retained.
Extracted notices are under `build/toolchain/licenses`; original JARs also
retain their embedded notices.

| Artifact | Version | Licence | Packaged in app? |
|---|---|---|---|
| Kotlin compiler, daemon, script runtime | 1.9.24 | Apache-2.0 | No |
| Kotlin reflect (compiler dependency) | 1.6.10 | Apache-2.0 | No |
| Kotlin stdlib | 1.9.24 | Apache-2.0 | Yes; LICENSE and NOTICE included in both build routes |
| JetBrains annotations | 13.0 | Apache-2.0 | No |
| IntelliJ trove4j | 1.0.20200330 | LGPL-2.1 | No; compiler-only |
| Eclipse ECJ | 3.39.0 | EPL-2.0 | No |
| Android framework | 16-robolectric-13921718 | Apache-2.0 | No |
| AAPT2 Linux | 9.5.0-16666295 | Apache-2.0 and bundled notices | No |
| D8/R8 | 9.5.28 | BSD-3-Clause and bundled notices | No |
| AOSP apksig | 9.5.0 | Apache-2.0 | No |
| JSON-java | 20240303 | Public domain, per POM | No; JVM tests/compile-only |
| JUnit | 4.13.2 | EPL-1.0 | No |
| Hamcrest core | 1.3 | BSD | No |
| Gradle wrapper | 8.13 | Apache-2.0 | No |

Artifacts originate from Maven Central, Google Maven, and versioned JetBrains
Kotlin licence files. No other application's signing key is used.

## Optional native-view runtime checks

After the normal toolchain bootstrap, the separate pinned Robolectric runner
can test the production Activity and Views on a JVM (not an emulator/device):

```sh
python3 tools/robolectric-bootstrap.py
bash tools/robolectric-native-tests.sh
bash tools/min-sdk26-tests.sh
```

The first native suite uses Android API 36. The optional minimum-SDK probe
uses the original Maven Android 8/API 26 framework, separately pinned in
`min-sdk26-artifacts.lock.json` (approximately 101 MB, Apache-2.0 per its
preserved upstream POM). It recompiles current
production Kotlin, launches the real Activity without resuming/audio, loads
file-backed demo data, visits all nine screens and checks legacy Back.
These additional frameworks and runner dependencies are never APK inputs.
They use `Config.NONE` and legacy graphics: packaged resources/manifest,
screenshots, physical audio and installed-device behavior remain separate
acceptance work. See [robolectric-README.md](robolectric-README.md).

The tracked `tools/apk-assets/licenses` copies match the pinned Kotlin licence
files and are included by the standard Gradle app asset source set; the manual
packager embeds the same verified notices from its toolchain cache.
