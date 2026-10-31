import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.Robolectric;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.annotation.Config;
import org.robolectric.annotation.GraphicsMode;
import org.robolectric.android.controller.ActivityController;
import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
@Config(manifest = Config.NONE, sdk = 36)
@GraphicsMode(GraphicsMode.Mode.LEGACY)
public class RobolectricSmokeTest {
    public static class FixtureActivity extends Activity {
        @Override public void onCreate(Bundle state) {
            super.onCreate(state);
            TextView view = new TextView(this);
            view.setId(1234);
            view.setText("Livro JVM native UI");
            view.setOnClickListener(v -> view.setText("Clicked in real Activity"));
            setContentView(view);
        }
    }
    @Test public void nativeActivityLifecycleAndTextViewClickWork() {
        try (ActivityController<FixtureActivity> controller = Robolectric.buildActivity(FixtureActivity.class).setup()) {
            FixtureActivity activity = controller.get();
            TextView view = activity.findViewById(1234);
            assertNotNull(view);
            assertEquals("Livro JVM native UI", view.getText().toString());
            assertTrue(view.performClick());
            assertEquals("Clicked in real Activity", view.getText().toString());
            assertEquals(36, android.os.Build.VERSION.SDK_INT);
        }
    }
}
