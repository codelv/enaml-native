package com.enaml;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.util.Log;

import com.jventura.pyapp.R;
import com.jventura.pybridge.AssetExtractor;
import com.jventura.pybridge.PyBridge;

import org.msgpack.core.MessageBufferPacker;
import org.msgpack.core.MessagePack;
import org.msgpack.core.MessageUnpacker;
import org.msgpack.value.Value;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.ArrayList;


public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";


    // Reference to the activity so it can be accessed from the python interpreter
    public static MainActivity mActivity = null;

    // Class name to pass to python for loading
    private final String mActivityId = "com.enaml.MainActivity";

    // Assets version
    public final int mAssetsVersion = 1;
    public final boolean mAssetsAlwaysOverwrite = true; // Set only on debug builds

    // Save layout elements to display a fade in animation
    // When the view is loaded from python
    private FrameLayout mContentView;
    private View mLoadingView;
    private Bridge mBridge;
    private int mShortAnimationDuration = 300;

    // Handler to hook python into the Android application event loop
    private final Handler mCallbackHandler = new Handler();

    private AppEventListener mAppEventListener;
    private ArrayList<MessageBufferPacker> mEventList = new ArrayList<MessageBufferPacker>();
    private int mEventCount = 0;
    private int mEventDelay = 3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

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

            return pythonPath;
        }

        /**
         * When the python has finished the loading in the background
         * Call start to display the view.
         * @param result
         */
        protected void onPostExecute(String pythonPath) {
            /*
            try {

                JSONObject json = new JSONObject();
                json.put("method", "version");
                result = PyBridge.call(json);
                TextView textView = (TextView) findViewById(R.id.textView);
                textView.setText(result.getString("result"));

                // Load the View
                JSONObject json = new JSONObject();
                JSONObject params = new JSONObject();
                json.put("method", "load");
                params.put("activity", mActivityId);
                json.putOpt("params", params);
                result = PyBridge.call(json);

                // Start python
                if (result!=null && !result.has("error")) {
                    json = new JSONObject();
                    json.put("method", "start");
                    result = PyBridge.call(json);
                }

                // Check and display any errors
                if (result!=null && result.has("error")) {
                    JSONObject error = result.getJSONObject("error");
                    if (error!=null) {
                        showErrorMessage(error.getString("message"));
                    }
                }
            } catch (JSONException e) {
                showErrorMessage(e);
            }
            */

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
    protected void showErrorMessage(String message) {
        if (message!=null) {
            TextView textView = (TextView) findViewById(R.id.textView);
            textView.setTop(0);
            textView.setTextAlignment(View.TEXT_ALIGNMENT_TEXT_START);
            textView.setTextColor(Color.RED);
            textView.setText(message);

            // Hide progress bar
            View progressBar = findViewById(R.id.progressBar);
            progressBar.setVisibility(View.INVISIBLE);
        }
    }

    /**
     * Set error message text in loading view from an exception
     * @param e: Exception to display.
     */
    protected void showErrorMessage(Exception e) {
        StringWriter sw = new StringWriter();
        e.printStackTrace(new PrintWriter(sw));
        showErrorMessage(sw.toString());
    }


    /**
     * Set the content view and fade out the loading view
     * @param view
     */
    public void setView(View view) {
        Log.i(TAG,"View loaded!");
        mContentView.addView(view);

        // Set the content view to 0% opacity but visible, so that it is visible
        // (but fully transparent) during the animation.
        view.setAlpha(0f);
        view.setVisibility(View.VISIBLE);

        // Animate the content view to 100% opacity, and clear any animation
        // listener set on the view.
        view.animate()
            .alpha(1f)
            .setDuration(mShortAnimationDuration)
            .setListener(null);

        // Animate the loading view to 0% opacity. After the animation ends,
        // set its visibility to GONE as an optimization step (it won't
        // participate in layout passes, etc.)
        mLoadingView.animate()
            .alpha(0f)
            .setDuration(mShortAnimationDuration)
            .setListener(new AnimatorListenerAdapter() {
                @Override
                public void onAnimationEnd(Animator animation) {
                    mLoadingView.setVisibility(View.GONE);
                }
            });

    }


    /**
     * Interface for python to pass it's calls in a structured manner
     * for Java to actually call.  For instance
     *
     *
     * In python, using jnius
     *
     * class TextView(JavaProxyClass):
     *      __javaclass__ = `android.widgets.TextView`
     *
     * #: etc.. for other widgets
     *
     * v = LinearLayout()
     *
     * tv = TextView()
     * tv.setText("text")
     *
     * v.addView(tv)
     *
     * maps to:
     * [
     *  #: Argument of context is implied
     *  ("createView", ("android.widgets.LinearLayout",0x01)),
     *  ("createView", ("android.widgets.TextView",0x02)),
     *  ("updateView", (0x02,"setText","text")),
     *  ("updateView", (0x01,"addView",{"ref":0x01})
     * ]
     *
     * @warning This is called from the Python thread, NOT the UI thread!
     *
     * @param view
     */
    public void processEvents(byte[] data) {
        long startTime = System.nanoTime();
        Log.i(TAG,"Start processing... ");
        MessageUnpacker unpacker = MessagePack.newDefaultUnpacker(data);
        try {
            int eventCount = unpacker.unpackArrayHeader();
            for (int i=0; i<eventCount; i++) {
                int eventTuple = unpacker.unpackArrayHeader(); // Unpack event tuple
                String eventType = unpacker.unpackString(); // first value
                int paramCount = unpacker.unpackArrayHeader();

                if (eventType.equals("createObject")) {
                    int objId = unpacker.unpackInt();
                    String objClass = unpacker.unpackString();
                    int argCount = unpacker.unpackArrayHeader();
                    Value[] args = new Value[argCount];
                    for (int j=0; j<argCount; j++) {
                        Value v = unpacker.unpackValue();
                        args[j] = v;
                    }
                    runOnUiThread(()->{mBridge.createObject(objId, objClass, args);});
                } else if (eventType.equals("updateObject")) {
                    int objId = unpacker.unpackInt();
                    String objMethod = unpacker.unpackString();
                    int argCount = unpacker.unpackArrayHeader();
                    Value[] args = new Value[argCount];
                    for (int j=0; j<argCount; j++) {
                        Value v = unpacker.unpackValue();
                        args[j] = v;
                    }
                    runOnUiThread(()->{mBridge.updateObject(objId, objMethod, args);});
                } else if (eventType.equals("updateObjectField")) {
                    int objId = unpacker.unpackInt();
                    String objField = unpacker.unpackString();
                    int argCount = unpacker.unpackArrayHeader();
                    Value[] args = new Value[argCount];
                    for (int j=0; j<argCount; j++) {
                        Value v = unpacker.unpackValue();
                        args[j] = v;
                    }
                    runOnUiThread(()->{mBridge.updateObjectField(objId, objField, args);});
                } else if (eventType.equals("deleteObject")) {
                    int objId = unpacker.unpackInt();
                    runOnUiThread(()->{mBridge.deleteObject(objId);});
                } else if (eventType.equals("showView")) {
                    runOnUiThread(()->{setView(mBridge.getRootView());});
                } else if (eventType.equals("displayError")) {
                    String errorMessage = unpacker.unpackString();
                    runOnUiThread(()->{showErrorMessage(errorMessage);});
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        long duration = (System.nanoTime()-startTime) / 1000000;
        Log.i(TAG,"Done processing! ("+duration+" ms)");
    }

    /**
     * Post an event to the app listener
     */
    public void sendEvent(MessageBufferPacker event) {
        mEventCount += 1;
        mEventList.add(event);
        (new Handler()).postDelayed(()->{
            sendEvents();
        },mEventDelay);
    }

    /**
     * When events stop coming in, send to python.
     * TODO: Should it have a time limit?
     */
    public void sendEvents() {
        mEventCount -= 1;
        if (mAppEventListener!=null && mEventCount==0) {
            MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
            try {
                packer.packArrayHeader(mEventList.size());
                for (MessageBufferPacker event: mEventList) {
                    packer.addPayload(event.toByteArray());
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            mAppEventListener.onEvents(packer.toByteArray());
            mEventList.clear();
        }
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

    }


    /**
     * Set the app event listener to use. Meant to be used from python
     * so it can receive events from java.
     * @param listener
     */
    public void setAppEventListener(AppEventListener listener) {
        mAppEventListener = listener;
    }

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
        PyBridge.stop();
    }
}
