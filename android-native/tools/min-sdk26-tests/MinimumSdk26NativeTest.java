package br.com.livrodeprevisoes.app;

import android.os.Build;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.Robolectric;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.android.controller.ActivityController;
import org.robolectric.annotation.Config;
import org.robolectric.annotation.GraphicsMode;
import static org.junit.Assert.*;

/** Minimum-SDK boundary probe, not a physical-device or packaged-resource test. */
@RunWith(RobolectricTestRunner.class)
@Config(manifest = Config.NONE, sdk = 26)
@GraphicsMode(GraphicsMode.Mode.LEGACY)
public class MinimumSdk26NativeTest {
    @Test public void android8LaunchDataAndEveryNativeScreenUseAvailablePublicApis() {
        RuntimeEnvironment.getApplication().getApplicationInfo().targetSdkVersion = 36;
        try (ActivityController<MainActivity> controller = Robolectric.buildActivity(MainActivity.class).create().start()) {
            MainActivity activity = controller.get();
            assertEquals(26, Build.VERSION.SDK_INT);
            assertTrue("Application failed to initialize on minimum SDK", activity.getInitialized());
            activity.getService().loadDemoData(true);
            assertFalse("Real file-backed demo must load", activity.getService().rows("events").isEmpty());
            for (String screen : new String[]{"dashboard", "pending", "completed", "registry", "alerts", "colors", "backup", "diagnostics", "new"}) {
                activity.navigate(screen, null);
                assertEquals("Failed to enter native screen on Android 8", screen, activity.getScreen());
                assertNotNull(activity.findViewById(android.R.id.content));
            }
            activity.onBackPressed();
            assertEquals("Legacy Back must remain functional below API 33", "dashboard", activity.getScreen());
        }
    }
}
