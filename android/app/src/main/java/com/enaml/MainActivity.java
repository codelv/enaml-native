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

import com.frmdstryr.enamlnative.demo.R;
import com.jventura.pybridge.AssetExtractor;
import com.jventura.pybridge.PyBridge;

import java.io.PrintWriter;
import java.io.StringWriter;


public class MainActivity extends AppCompatActivity {

    public static final String TAG = "MainActivity";

    // Reference to the activity so it can be accessed from the python interpreter
    public static MainActivity mActivity = null;

    // Assets version
    final int mAssetsVersion = 2;
    final boolean mAssetsAlwaysOverwrite = true; // Set only on debug builds

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
                publishProgress("Unpacking... Please wait.");
                assetExtractor.removeAssets(path);
                assetExtractor.copyAssets(path);
                assetExtractor.setAssetsVersion(mAssetsVersion);
            }

            // Start the Python interpreter
            publishProgress("Initializing... Please wait.");

            // Get the extracted assets directory
            String pythonPath = assetExtractor.getAssetsDataDir() + path;

            // Initialize python
            // Note: This must be NOT done in the UI thread!
            PyBridge.start(pythonPath);
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
     * Set error message text in loading view.
     * @param message: Message to display
     */
    public void showErrorMessage(String message) {
        if (message!=null) {
            TextView textView = (TextView) findViewById(R.id.textView);
            textView.setTop(0);
            ViewGroup.MarginLayoutParams params = (ViewGroup.MarginLayoutParams) textView.getLayoutParams();
            params.setMargins(10,10, 10, 10);
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
    }

    /**
     * Set error message text in loading view from an exception
     * @param e: Exception to display.
     */
    public void showErrorMessage(Exception e) {
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
        mPythonView = view;
        mContentView.addView(view);
        animateView(view, mLoadingView);
        mLoadingDone = true;
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
     * Pass data to bridge for processing.
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
