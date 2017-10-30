package com.codelv.enamlnative;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.graphics.Color;
import android.os.Build;
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

    final HashMap<String, Long> mProfilers = new HashMap<>();


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
    }

    @Override
    protected void onPause() {
        super.onPause();
        // Initialize the packages
        for (EnamlPackage pkg: getPackages()) {
            pkg.onStop();
        }

    }

    @Override
    protected void onStop() {
        super.onStop();
        // Initialize the packages
        for (EnamlPackage pkg: getPackages()) {
            pkg.onStop();
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        // Initialize the packages
        for (EnamlPackage pkg: getPackages()) {
            pkg.onDestroy();
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


}
