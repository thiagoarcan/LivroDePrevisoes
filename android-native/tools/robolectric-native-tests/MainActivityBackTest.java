package br.com.livrodeprevisoes.app;

import android.app.AlertDialog;
import android.os.Looper;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.TextView;
import android.window.OnBackInvokedCallback;
import android.util.Pair;
import java.util.List;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.Robolectric;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.Shadows;
import org.robolectric.android.controller.ActivityController;
import org.robolectric.annotation.Config;
import org.robolectric.annotation.GraphicsMode;
import org.robolectric.shadows.ShadowAlertDialog;
import org.robolectric.shadows.ShadowWindowOnBackInvokedDispatcher;
import org.robolectric.util.ReflectionHelpers;
import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
@Config(manifest = Config.NONE, sdk = 36)
@GraphicsMode(GraphicsMode.Mode.LEGACY)
public class MainActivityBackTest {
    @Test public void predictiveBackRegistersPlatformCallbackAndProtectsDraftThenFinishesAtRoot() {
        RuntimeEnvironment.getApplication().getApplicationInfo().targetSdkVersion = 36;
        // Config.NONE omits the APK manifest; reproduce its explicit predictive-back opt-in.
        ReflectionHelpers.callInstanceMethod(RuntimeEnvironment.getApplication().getApplicationInfo(), "setEnableOnBackInvokedCallback", ReflectionHelpers.ClassParameter.from(boolean.class, true));
        ReflectionHelpers.callStaticMethod(ShadowWindowOnBackInvokedDispatcher.class, "setEnablePredictiveBack", ReflectionHelpers.ClassParameter.from(boolean.class, true));
        try (ActivityController<MainActivity> controller = Robolectric.buildActivity(MainActivity.class).create().start()) {
            MainActivity activity = controller.get();
            assertTrue(activity.getInitialized());
            AlertDialog onboarding = ShadowAlertDialog.getLatestAlertDialog();
            if (onboarding != null) onboarding.dismiss();
            // Before resume/window attachment, Android36 retains registrations in its real proxy.
            List<Pair<OnBackInvokedCallback, Integer>> callbacks = ReflectionHelpers.getField(activity.getOnBackInvokedDispatcher(), "mCallbacks");
            assertFalse("Target36 must register an actual platform back callback; legacy onBackPressed is not enough", callbacks.isEmpty());
            OnBackInvokedCallback callback = callbacks.get(callbacks.size() - 1).first;
            activity.navigate("alerts", null);
            callback.onBackInvoked();
            assertEquals("dashboard", activity.getScreen());
            assertFalse(activity.isFinishing());
            activity.navigate("new", null);
            EditText description = findInput(activity, activity.findViewById(android.R.id.content), "Descrição da atividade *");
            assertNotNull(description);
            description.setText("Rascunho não deve desaparecer pelo gesto Voltar");
            callback.onBackInvoked();
            assertEquals("new", activity.getScreen());
            AlertDialog discard = ShadowAlertDialog.getLatestAlertDialog();
            assertTrue(discard.isShowing());
            discard.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();
            Shadows.shadowOf(Looper.getMainLooper()).idle();
            assertEquals("new", activity.getScreen());
            assertFalse(activity.isFinishing());
            callback.onBackInvoked();
            ShadowAlertDialog.getLatestAlertDialog().getButton(AlertDialog.BUTTON_POSITIVE).performClick();
            Shadows.shadowOf(Looper.getMainLooper()).idle();
            assertEquals("dashboard", activity.getScreen());
            callback.onBackInvoked();
            assertTrue(activity.isFinishing());
        }
    }
    private static EditText findInput(MainActivity activity, View view, String label) {
        if (view instanceof TextView && label.equals(((TextView) view).getText().toString()) && view.getLabelFor() != View.NO_ID) {
            View candidate = activity.findViewById(view.getLabelFor());
            if (candidate instanceof EditText) return (EditText) candidate;
        }
        if (view instanceof ViewGroup) {
            ViewGroup group = (ViewGroup) view;
            for (int i = 0; i < group.getChildCount(); i++) {
                EditText found = findInput(activity, group.getChildAt(i), label);
                if (found != null) return found;
            }
        }
        return null;
    }
}
