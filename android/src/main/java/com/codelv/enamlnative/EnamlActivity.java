package com.codelv.enamlnative;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.graphics.Color;
import android.os.Build;
import android.content.Intent;
import android.os.Handler;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.util.Log;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class EnamlActivity extends AppCompatActivity {

    public static final String TAG = "EnamlActivity";


    // Reference to the activity so it can be accessed from the python interpreter
    public static EnamlActivity mActivity = null;

    // Save layout elements to display a fade in animation
    // When the view is loaded from python
    FrameLayout mContentView;
    View mPythonView;
    View mLoadingView;
    Bridge mBridge;
    boolean mLoadingDone = false;
    int mShortAnimationDuration = 300;
    final List<EnamlPackage> mEnamlPackages = new ArrayList<EnamlPackage>();
    PermissionResultListener mPermissionResultListener;
    final List<ActivityResultListener> mActivityResultListeners = new ArrayList<ActivityResultListener>();
    final List<ActivityLifecycleListener> mActivityLifecycleListeners = new ArrayList<ActivityLifecycleListener>();
    final List<BackPressedListener> mBackPressedListeners = new ArrayList<BackPressedListener>();

    final HashMap<String, Long> mProfilers = new HashMap<>();
    final Handler mHandler = new Handler();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Save reference so python can access it
        mActivity = this;

        // Initialize the packages
        EnamlApplication app = (EnamlApplication) getApplication();
        mEnamlPackages.addAll(app.getPackages());

        // Create
        for (EnamlPackage pkg: getPackages()) {
            Log.d(TAG, "Creating "+pkg);
            pkg.onCreate(this);
        }


        prepareLoadingScreen();

        // Now initialize everything
        for (EnamlPackage pkg: getPackages()) {
            pkg.onStart();
        }

        // Now notify any listeners
        for (ActivityLifecycleListener listener:mActivityLifecycleListeners) {
            listener.onActivityLifecycleChanged("created");
        }

    }

    public List<EnamlPackage> getPackages() {
        return mEnamlPackages;
    }

    /**
     * Show the loading screen. Can be overridden if necessary.
     */
    protected void prepareLoadingScreen() {
        // Show loading screen
        setContentView(R.layout.activity_main);

        // Save views for animation when loading is complete
        mContentView = (FrameLayout) findViewById(R.id.contentView);
        mLoadingView = findViewById(R.id.loadingView);
    }

    /**
     * Set the bridge implementation
     * @param bridge
     */
    public void setBridge(Bridge bridge) {
        mBridge = bridge;
    }


    /**
     * Should debug messages be used.
     * @return
     */
    public boolean showDebugMessages() {
        return ((EnamlApplication)getApplication()).showDebugMessages();
    }

    /**
     * Set error message text in loading view.
     * @param message: Message to display
     */
    public void showErrorMessage(String message) {
        if (!showDebugMessages()) {
            // Crash on release
            throw new RuntimeException(message);
        }
        Log.e(TAG,message);

        // Push to end of handler stack as this can occur during the view change animation
        mHandler.post(()->{
            // Move to top of screen
            TextView textView = (TextView) findViewById(R.id.textView);
            textView.setHorizontallyScrolling(true);
            ((ViewGroup.MarginLayoutParams) textView.getLayoutParams()).setMargins(10, 10, 10, 10);
            textView.setTextAlignment(View.TEXT_ALIGNMENT_TEXT_START);
            textView.setTextColor(Color.RED);
            textView.setText(message);

            // Hide progress bar
            View progressBar = findViewById(R.id.progressBar);
            progressBar.setVisibility(View.INVISIBLE);

            // If error occured after view was loaded, animate the error back in
            if (mLoadingDone) {
                // Swap the views back
                animateView(mLoadingView, mPythonView);
            }
        });
    }

    /**
     * Set error message text in loading view from an exception
     * @param e: Exception to display.
     */
    public void showErrorMessage(Exception e) {
        // do something for a debug build
        StringWriter sw = new StringWriter();
        e.printStackTrace(new PrintWriter(sw));
        showErrorMessage(sw.toString());
    }


    /**
     * Set the content view and fade out the loading view
     * @param view
     */
    public void setView(View view) {
        Log.i(TAG, "View loaded!");
        // Support reloading the view
        if (mPythonView!=null) {
            mContentView.removeView(mPythonView);
            mContentView.forceLayout();
            mLoadingView.setVisibility(View.VISIBLE);
        }
        mPythonView = view;
        mContentView.addView(view);
        animateView(view, mLoadingView);
        mLoadingDone = true;
    }

    /**
     * Show the loading screen again with the given message
     */
    public void showLoading(String message) {
        // Set the message
        TextView textView = (TextView) findViewById(R.id.textView);
        float dp = getResources().getDisplayMetrics().density;
        ((ViewGroup.MarginLayoutParams) textView.getLayoutParams()).setMargins(10, Math.round(200*dp), 10, 10);
        textView.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
        textView.setTextColor(Color.GRAY);
        textView.setText(message);

        // Show progress bar
        View progressBar = findViewById(R.id.progressBar);
        progressBar.setVisibility(View.VISIBLE);
        if (mPythonView!=null && mLoadingView!=mPythonView) {
            // Swap the views back
            animateView(mLoadingView, mPythonView);
        }
    }

    protected void animateView(View in, View out) {
        // Set the content view to 0% opacity but visible, so that it is visible
        // (but fully transparent) during the animation.
        in.setAlpha(0f);
        in.setVisibility(View.VISIBLE);

        // Animate the content view to 100% opacity, and clear any animation
        // listener set on the view.
        in.animate()
            .alpha(1f)
            .setDuration(mShortAnimationDuration)
            .setListener(null);

        // Animate the loading view to 0% opacity. After the animation ends,
        // set its visibility to GONE as an optimization step (it won't
        // participate in layout passes, etc.)
        out.animate()
            .alpha(0f)
            .setDuration(mShortAnimationDuration)
            .setListener(new AnimatorListenerAdapter() {
                @Override
                public void onAnimationEnd(Animator animation) {
                    out.setVisibility(View.GONE);
                }
            });
    }


    /**
     * Get bridge controller
     * @return
     */
    public Bridge getBridge() {
        return mBridge;
    }

    @Override
    protected void onResume() {
        super.onResume();
        // Initialize the packages
        for (EnamlPackage pkg: getPackages()) {
            pkg.onResume();
        }

        // Now notify any listeners
        for (ActivityLifecycleListener listener:mActivityLifecycleListeners) {
            listener.onActivityLifecycleChanged("resumed");
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        // Initialize the packages
        for (EnamlPackage pkg: getPackages()) {
            pkg.onStop();
        }

        // Now notify any listeners
        for (ActivityLifecycleListener listener:mActivityLifecycleListeners) {
            listener.onActivityLifecycleChanged("paused");
        }

    }

    /**
     * Dispatch the back pressed event to all listeners. If any of them
     * return true then skip the default handler.
     */
    @Override
    public void onBackPressed(){
        boolean handled = false;
        for (BackPressedListener listener: mBackPressedListeners) {
            handled = handled || listener.onBackPressed();
        }
        if (!handled) {
            super.onBackPressed();
        }
    }

    @Override
    protected void onStop() {
        super.onStop();
        // Initialize the packages
        for (EnamlPackage pkg: getPackages()) {
            pkg.onStop();
        }

        // Now notify any listeners
        for (ActivityLifecycleListener listener:mActivityLifecycleListeners) {
            listener.onActivityLifecycleChanged("stopped");
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        // Initialize the packages
        for (EnamlPackage pkg: getPackages()) {
            pkg.onDestroy();
        }

        // Now notify any listeners
        for (ActivityLifecycleListener listener:mActivityLifecycleListeners) {
            listener.onActivityLifecycleChanged("destroyed");
        }

    }

    /**
     * Set the app permission listener to use. Meant to be used from python
     * so it can receive events from java.
     * @param listener
     */
    public void setPermissionResultListener(PermissionResultListener listener) {
        mPermissionResultListener = listener;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        if (mPermissionResultListener !=null) {
            mPermissionResultListener.onRequestPermissionsResult(requestCode, permissions, grantResults);
        }
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }

    public interface PermissionResultListener{

        /**
         * Receive permission request results
         * @param code
         * @param permissions
         * @param results
         */
        void onRequestPermissionsResult(int code, String[] permissions, int[] results);
    }

    /**
     * Add an app activity result listener to use. Meant to be used from python
     * so it can receive events from java.
     * @param listener
     */
    public void addActivityResultListener(ActivityResultListener listener) {
        mActivityResultListeners.add(listener);
    }

    public void removeActivityResultListener(ActivityResultListener listener) {
        mActivityResultListeners.remove(listener);
    }

    /**
     * Let Packages and python handle activity results and break execution
     * if needed.
     * @param requestCode
     * @param resultCode
     * @param data
     */
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        boolean handled = false;
        for (ActivityResultListener listener: mActivityResultListeners) {
            if (listener.onActivityResult(requestCode, resultCode, data)) {
                handled = true; // But still execute the rest
            }
        }
        if (!handled) {
            super.onActivityResult(requestCode, resultCode, data);
        }
    }

    public interface ActivityResultListener{

        /**
         * Receive activity request results from Intents
         * @param requestCode
         * @param resultCode
         * @param data
         */
        boolean onActivityResult(int requestCode, int resultCode, Intent data);
    }

    /**
     * Add an app activity lifecycle listener to use. Meant to be used from python
     * so it can receive events from java when the app state changes.
     * @param listener
     */
    public void addActivityLifecycleListener(ActivityLifecycleListener listener) {
        mActivityLifecycleListeners.add(listener);
    }

    public void removeActivityLifecycleListener(ActivityLifecycleListener listener) {
        mActivityLifecycleListeners.remove(listener);
    }

    public interface ActivityLifecycleListener{

        /**
         * Receive activity lifecycle changes
         * @param state
         */
        void onActivityLifecycleChanged(String state);
    }


    /**
     * Add a back press listener to use. Meant to be used from python
     * so it can receive events from java when the back button is pressed.
     * @param listener
     */
    public void addBackPressedListener(BackPressedListener listener) {
        mBackPressedListeners.add(listener);
    }

    public void removeBackPressedListener(BackPressedListener listener) {
        mBackPressedListeners.remove(listener);
    }

    public interface BackPressedListener {
        /**
         * Called when the back button is pressed. All listeners will be called. If
         * one of them return true the default handler will NOT be invoked.
         *
         * Handlers must be fast or they will block the UI.
         */
        boolean onBackPressed();
    }

    /**
     * Return build info. Called from python at startup to get info like screen density
     * and API version.
     * @return
     */
    public HashMap<String,Object> getBuildInfo() {
        HashMap<String, Object> result = new HashMap<String, Object>() {{
            put("BOARD",Build.BOARD);
            put("BOOTLOADER", Build.BOOTLOADER);
            put("BRAND", Build.BRAND);
            put("DISPLAY", Build.DISPLAY);
            put("DEVICE", Build.DEVICE);
            put("FINGERPRINT", Build.FINGERPRINT);
            put("HARDWARE", Build.HARDWARE);
            put("HOST", Build.HOST);
            put("ID", Build.ID);
            put("MANUFACTURER", Build.MANUFACTURER);
            put("MODEL", Build.MODEL);
            put("TIME", Build.TIME);
            put("TAGS", Build.TAGS);
            put("PRODUCT", Build.PRODUCT);
            put("SERIAL", Build.SERIAL);
            put("USER", Build.USER);
            put("SDK_INT",Build.VERSION.SDK_INT);
            put("BASE_OS", Build.VERSION.BASE_OS);
            put("RELEASE", Build.VERSION.RELEASE);
            put("CODENAME", Build.VERSION.CODENAME);
            put("DISPLAY_DENSITY", getResources().getDisplayMetrics().density);
            put("DISPLAY_WIDTH", getResources().getDisplayMetrics().widthPixels);
            put("DISPLAY_HEIGHT", getResources().getDisplayMetrics().heightPixels);
        }};
        return result;
    }

    /**
     * Utility for measuring how long tasks take.
     */
    public void startTrace(String tag) {
        Log.i(TAG, "[Trace][" + tag + "] Started ");
        mProfilers.put(tag, System.currentTimeMillis());
    }

    public void stopTrace(String tag) {
        Log.i(TAG, "[Trace][" + tag + "] Ended " + (System.currentTimeMillis() - mProfilers.get(tag)) + " (ms)");
    }


    /**
     * Reset stats on the bridge
     */
    public void resetBridgeStats() {
       mBridge.resetStats();
    }

    /**
     * Reset cached objects on the bridge
     */
    public void resetBridgeCache() {
        mBridge.clearCache();
    }

}
