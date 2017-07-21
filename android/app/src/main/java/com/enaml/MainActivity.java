package com.enaml;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.graphics.Color;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.util.Log;

import com.frmdstryr.enamlnative.demo.BuildConfig;
import com.frmdstryr.enamlnative.demo.R;
import com.joanzapata.iconify.Iconify;
import com.joanzapata.iconify.fonts.EntypoModule;
import com.joanzapata.iconify.fonts.FontAwesomeModule;
import com.joanzapata.iconify.fonts.IoniconsModule;
import com.joanzapata.iconify.fonts.MaterialCommunityModule;
import com.joanzapata.iconify.fonts.MaterialModule;
import com.joanzapata.iconify.fonts.MeteoconsModule;
import com.joanzapata.iconify.fonts.SimpleLineIconsModule;
import com.joanzapata.iconify.fonts.TypiconsModule;
import com.joanzapata.iconify.fonts.WeathericonsModule;
import com.jventura.pybridge.AssetExtractor;
import com.jventura.pybridge.PyBridge;

import java.io.PrintWriter;
import java.io.StringWriter;


public class MainActivity extends AppCompatActivity {

    public static final String TAG = "MainActivity";

    // Reference to the activity so it can be accessed from the python interpreter
    public static MainActivity mActivity = null;

    // Assets version
    final int mAssetsVersion = BuildConfig.VERSION_CODE;
    final boolean mAssetsAlwaysOverwrite = BuildConfig.DEBUG; // Set only on debug builds

    // Save layout elements to display a fade in animation
    // When the view is loaded from python
    FrameLayout mContentView;
    View mPythonView;
    View mLoadingView;
    Bridge mBridge;
    boolean mLoadingDone = false;
    int mShortAnimationDuration = 300;

    AppEventListener mAppEventListener;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d(TAG,"onCreate");

        // Save reference so python can access it
        mActivity = this;
        mBridge = new Bridge(this);

        // Show loading screen
        setContentView(R.layout.activity_main);

        initIcons();

        // Save views for animation when loading is complete
        mContentView = (FrameLayout) findViewById(R.id.contentView);
        mLoadingView = findViewById(R.id.loadingView);

        // Extract and start python in the background
        (new PythonTask()).execute("python");
    }

    /**
     * AsyncTask that:
     *  1. Extracts the python assets folder
     *  2. Initializes the python interpreter
     *  3. Calls the app start function of the bootstrap
     */
    private class PythonTask extends AsyncTask<String,String,String>{

        protected String doInBackground(String... dirs) {
            // Extract python files from assets
            String path = dirs[0];
            AssetExtractor assetExtractor = new AssetExtractor(mActivity);

            // If assets version changed, remove the old, and copy the new ones
            if (mAssetsAlwaysOverwrite || assetExtractor.getAssetsVersion() != mAssetsVersion) {
                publishProgress("Preparing... Please wait.");
                assetExtractor.removeAssets(path);
                assetExtractor.copyAssets(path);
                assetExtractor.setAssetsVersion(mAssetsVersion);

                // On first load change message
                publishProgress("Loading... Please wait.\n(may take a few seconds)");
            } else {
                // Start the Python interpreter
                publishProgress("Loading... Please wait.");
            }



            // Get the extracted assets directory
            String pythonPath = assetExtractor.getAssetsDataDir() + path;
            String nativePath = getApplicationInfo().nativeLibraryDir;
            // Initialize python
            // Note: This must be NOT done in the UI thread!
            PyBridge.start(pythonPath, nativePath);
            Log.i(TAG, "Python main() finished!");
            // Done
            PyBridge.stop();

            return pythonPath;
        }

        /**
         * When the python has finished the loading in the background
         * Call start to display the view.
         * @param result
         */
        protected void onPostExecute(String pythonPath) {
            Log.i(TAG, "Python thread complete!");
        }

        /**
         * Set the progress text to make loading not seem as slow.
         * @param status
         */
        protected void onProgressUpdate(String... status) {
            TextView textView = (TextView) findViewById(R.id.textView);
            textView.setText(status[0]);
        }
    }

    /**
     * Init for icons
     */
    public void initIcons() {
        Iconify
                .with(new FontAwesomeModule())
                .with(new EntypoModule())
                .with(new TypiconsModule())
                .with(new MaterialModule())
                .with(new MaterialCommunityModule())
                .with(new MeteoconsModule())
                .with(new WeathericonsModule())
                .with(new SimpleLineIconsModule())
                .with(new IoniconsModule());

    }


    /**
     * Set error message text in loading view.
     * @param message: Message to display
     */
    public void showErrorMessage(String message) {
        if (!BuildConfig.DEBUG) {
            // Crash on release
            throw new RuntimeException(message);
        }
        Log.e(TAG,message);

        // Move to top of screen
        TextView textView = (TextView) findViewById(R.id.textView);
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
        if (BuildConfig.DEBUG) {
            // do something for a debug build
            StringWriter sw = new StringWriter();
            e.printStackTrace(new PrintWriter(sw));
            showErrorMessage(sw.toString());
        } else {
            // Crash on release
            throw new RuntimeException(e);
        }
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
            //animateView(mLoadingView,mContentView);
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

        // Swap the views back
        animateView(mLoadingView, mPythonView);
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


    /**
     * Pass data to bridge for processing. Called by Python via the JNI
     * @param data
     */
    public void processEvents(byte[] data) {
        mBridge.processEvents(data);
    }

    /**
     * Interface for python to listen to events occuring in native widgets. All
     * events will be batched and called in onEvents.
     */
    public interface AppEventListener {
        /**
         * All widgets created that have listeners will batch their events and dispatch
         * them to the python interpreter here.
         * @param event
         */
        void onEvents(byte[] data);

        /**
         * Called when the Activity is resumed from pause
         */
        void onResume();

        /**
         * Called when the Activity is paused
         */
        void onPause();

        /**
         * Called when the Activity is stopped. Do any cleanup
         * and handling shutdown here.
         */
        void onStop();


        void onDestroy();
    }


    /**
     * Set the app event listener to use. Meant to be used from python
     * so it can receive events from java.
     * @param listener
     */
    public void setAppEventListener(AppEventListener listener) {
        mAppEventListener = listener;
    }

    public AppEventListener getAppEventListener() { return mAppEventListener; }

    @Override
    protected void onResume() {
        super.onResume();
        if (mAppEventListener!=null) {
            mAppEventListener.onResume();
        }
    }


    @Override
    protected void onPause() {
        super.onPause();
        if (mAppEventListener!=null) {
            mAppEventListener.onPause();
        }
    }

    @Override
    protected void onStop() {
        super.onStop();
        if (mAppEventListener!=null) {
            mAppEventListener.onStop();
        }


    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        // Wait for python to properly exit
        if (mAppEventListener!=null) {
            mAppEventListener.onDestroy();
        }

    }
}
