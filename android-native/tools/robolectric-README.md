# Standalone, pinned Robolectric JVM runner

This optional toolchain runs **Robolectric 4.16.1**, not a plain `android-all` JVM
stub and not an emulator. It supports native Android Activity/View tests on the
existing Java 21 runtime, without Gradle, an installed Android SDK, or SDK
license acceptance. It is complementary to, and does not replace, device testing.

## Bootstrap and verify

From `android-native`:

```sh
# Existing toolchain: supplies ECJ and the original Android 16 / API 36 jar.
python3 tools/bootstrap-tools.py

# Separate official Robolectric runtime; ~198 MB including native runtime assets.
python3 tools/robolectric-bootstrap.py
python3 tools/robolectric-bootstrap.py --verify-only
python3 tools/robolectric-test-bootstrap.py
./tools/robolectric-smoke.sh
```

The separate `robolectric-artifacts.lock.json` pins 36 runtime artifacts and 47
POM files by SHA-256 and byte length. Downloads use HTTPS URLs from Maven Central
(`repo.maven.apache.org`) and Google Maven (`dl.google.com`) only. This is an
observed-content hash lock, not a claim of independent signature verification.
The runtime closure follows the official Robolectric 4.16.1 POM with Maven
nearest-first version mediation, compile/runtime scopes, optional filtering,
and declared dependency exclusions. Parent POMs and imported dependency
management POMs are retained for provenance. The lock is the reproducible input;
bootstrap does not dynamically resolve versions or consult Maven metadata.

The two AndroidX AARs are `androidx.test:monitor:1.8.0` and
`androidx.test.espresso:espresso-idling-resource:3.7.0`. Their original AAR hashes
and extracted `classes.jar` hashes are pinned separately. All artifacts and
extracted classes stay in `build/robolectric` (override with `ROBOLECTRIC_CACHE`).
An invalid cached file is rejected by `--verify-only`; ordinary bootstrap
re-downloads or re-extracts it and verifies before replacement.

The original, separately pinned framework is
`android-all-16-robolectric-13921718.jar`, normally in `build/toolchain` (override
with `TOOLCHAIN_CACHE`). `robolectric-run.sh` verifies that original framework
against the duplicate hash in the Robolectric lock before use. It does not use
the Kotlin-metadata-filtered `android-framework-compile.jar` at runtime. The
runner is offline and instruments the original jar itself; no preinstrumented
framework or hidden Java network download is required.

## Compile a native UI test

A Java test can be compiled with the existing ECJ compiler:

```sh
RCP=$(python3 tools/robolectric-bootstrap.py --verify-only --classpath)
java -jar build/toolchain/ecj-3.39.0.jar -8 -proc:none \
  -classpath "build/main:build/r-classes:build/toolchain/android-all-16-robolectric-13921718.jar:$RCP" \
  -d build/ui-tests path/to/MyActivityTest.java
./tools/robolectric-run.sh \
  "build/main:build/r-classes:build/ui-tests:build/toolchain/kotlin-stdlib-1.9.24.jar" \
  com.example.MyActivityTest
```

The Java test uses ECJ Java 8 source/bytecode mode to avoid JPMS split-package
conflicts between Android `java.lang` helpers and the Java module system when
Kotlin classes are on the classpath. Production Kotlin remains JVM 17 and the
runner executes on Java 21. This does not downgrade the application.

Use the actual main/R/test output paths from the build being tested. Include
other application dependencies in the first argument as needed. For Kotlin
compilation, the existing `compile_kotlin` helper can use the filtered framework
compile view plus `$RCP`; runtime must still use the original framework.

For a resource-independent/programmatic UI test, use:

```java
@RunWith(RobolectricTestRunner.class)
@Config(manifest = Config.NONE, sdk = 36)
@GraphicsMode(GraphicsMode.Mode.LEGACY)
public class MyActivityTest { /* real ActivityController assertions */ }
```

`Config.NONE` deliberately does not load an app manifest or compiled app
resources. Tests that depend on app XML resources need their own correct
Robolectric resource/manifest configuration; the simple smoke fixture does not
claim to verify that path. `GraphicsMode.LEGACY` avoids the native renderer and
is appropriate for view-state and click assertions, not screenshot fidelity.

The exact underlying launch is:

```sh
java -Drobolectric.offline=true \
  -Drobolectric.usePreinstrumentedJars=false \
  -Drobolectric.dependency.dir="$PWD/build/toolchain" \
  -cp "<main:test:R:application-dependencies>:build/toolchain/android-all-16-robolectric-13921718.jar:$RCP" \
  org.junit.runner.JUnitCore <test-classes>
```

## Verified behavior

`robolectric-smoke/RobolectricSmokeTest.java` is a test fixture only. It uses the
actual `RobolectricTestRunner` to start a framework `Activity`, attach a real
`TextView`, find it by ID, assert its text, dispatch `performClick()`, assert the
changed text, check API 36, and close the activity controller. The smoke script
compiles that fixture fresh before running JUnit. It neither changes production
app/domain code nor alters the normal build/test scripts.


## Actual MainActivity tests (no signing)

```sh
./tools/robolectric-native-tests.sh
```

This script compiles the current `domain`, `data`, `alerts`, and `app` Kotlin
sources plus generated R classes into the isolated
`build/robolectric/native-ui` directory. It compiles and runs every JUnit fixture under
`robolectric-native-tests/` against that fresh output.
It does not create an APK or access a signing key. Tests use `.create().start()`
without `.resume()`; ordinary UI tests do not start the foreground monitor.
The dedicated asynchronous alarm tests explicitly start the real controller
with sound disabled globally and per event, and assert no AudioTrack is created.
Synthetic fixture data remains inside Robolectric's isolated application files.
Provider failure/success tests use Robolectric's ContentResolver stream registry
and real application callbacks; they do not substitute the app's data service.

The predictive-back fixture also sets the real ApplicationInfo predictive-back
opt-in to mirror the application's manifest, then inspects its actual platform
proxy registration before window attachment and invokes that registered
callback. It does not assert that a physical system gesture was simulated.

The fixture explicitly sets `ApplicationInfo.targetSdkVersion = 36` before
constructing an Activity, in addition to `@Config(sdk = 36)`. Because
`Config.NONE` is deliberate, these tests do **not** prove packaged manifest,
permission declaration, resource configuration, or installed-APK behavior. Those
remain separate APK/static checks and device/emulator acceptance work. They do
exercise the current production Activity, Android views and callbacks, actual
file-backed domain service, settings, drafts and SAF handling on the official
Robolectric Android 36 sandbox.

## Licensing and packaging boundary

Robolectric is MIT-licensed; its published POMs record the project and license
URLs. The dependency closure contains components under their own licenses;
those original JAR/AAR license notices are retained unchanged, and all upstream
POMs needed for the resolved graph are pinned alongside them for provenance.
Do not treat the whole dependency closure as MIT. The caches are JVM test-only.
No Robolectric runner, AndroidX test library, native test runtime, `android-all`,
ECJ, POM, or test fixture is an application APK input, and the normal APK build
script is not modified by this optional runner.


The extended native fixtures cover strict JSON on Android's own `org.json`,
file-preserving corrupt-load behavior, and the real asynchronous alarm worker.
Race tests execute exactly the scheduling pulse, wait for the actual persisted
claim without draining main-thread delivery, perform pause/completion, then
drain the main looper until the real worker finishes. The polling bound is a
failure deadline, not an arbitrary sleep used as evidence of completion. A
separate two-event case verifies visual-dialog queuing, delivery-audit channel
union, and that presenting a queued visual does not repost its notification.

Additional regression fixtures verify recovery export preserves malformed UTF-8
bytes exactly (the recovery path must never decode/re-encode the original), and
exercise 500 cached events through 100-card native pages with a counting
SnapshotStore behind the real LivroService. The bulk test traverses all five
pages, proves all 500 records are accessible exactly once, checks top/bottom
previous/next controls, and limits live status watchers to 100. It checks two
store loads for the first pending-list render, zero extra loads during paging,
per-card hierarchy/name lookup and full-dataset search, and identity reuse of
the actual row/name caches. Search finds off-page records, changed filters reset
the page, a vanished last page clamps after mutation, and detail-return plus
file-backed Activity recreation preserve the current page/query. These are bounded read/cache
assertions, not a claim that disk-read counts alone measure JSON-copying or UI
performance; render duration is printed only as informational evidence.

Twenty actual search/filter edits verify retained clock watchers match the
visible card count and that navigation releases old watchers. The live-label
check uses a schema-valid minute-aligned deadline and waits for the actual
clock boundary before invoking the production tick runnable. It verifies the
same status TextView changes to overdue without replacing the page or editing
fields. This check can take up to roughly a minute; it does not use an arbitrary
sleep as proof that an update occurred and does not start audio.

The Unicode boundary regression separately rejects escaped or in-memory lone
UTF-16 surrogates in JSON strings and keys before Android can silently replace
them during UTF-8 persistence. It verifies valid paired emoji survive actual
Android JSONObject serialization and file save/load, while invalid stored
escape sequences remain byte-for-byte untouched for raw recovery.


The staged-replacement regression validates an incoming document through the
real SAF callback, then corrupts only the staged UTF-8 bytes before confirming
and successfully closing the preventive backup. Replacement must strictly
re-decode that staged file and reject it without changing the live database or
repairing the staged bytes. This is separate from raw recovery export and from
initial import validation.


A registered-platform-callback regression covers Back from both pending and
completed event details: it must return to the originating paged list and keep
its page, query and advanced-filter values. The separate Back regression still
covers dirty-draft cancellation/confirmation and finishing at the dashboard.
