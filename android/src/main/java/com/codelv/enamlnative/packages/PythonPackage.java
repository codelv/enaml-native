package com.codelv.enamlnative.packages;

import android.content.pm.PackageManager;
import android.os.AsyncTask;
import android.util.Log;

import com.codelv.enamlnative.AssetExtractor;
import com.codelv.enamlnative.BuildConfig;
import com.codelv.enamlnative.EnamlActivity;
import com.codelv.enamlnative.EnamlPackage;
import com.codelv.enamlnative.python.PythonInterpreter;
import com.codelv.enamlnative.python.RemotePythonInterpreter;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;


/**
 * Created by jrm on 10/15/17.
 */

public class PythonPackage implements EnamlPackage {
    public static final String TAG = "PythonPackage";
    // Assets version
    //final int mAssetsVersion = BuildConfig.VERSION_CODE;
    //final boolean mAssetsAlwaysOverwrite = BuildConfig.DEBUG; // Set only on debug builds

    EnamlActivity mActivity;
    PythonTask mPython;
    boolean mDestroyRequested = false;
    PythonInterpreter mPythonInterpreter;

    public void onCreate(EnamlActivity activity) {
        mActivity = activity;
        if (BuildConfig.DEV_REMOTE_DEBUG) {
            mPythonInterpreter = RemotePythonInterpreter.instance();
        } else {
            mPythonInterpreter = PythonInterpreter.instance();
        }

        if (mPythonInterpreter.isInitialized()) {
            // Do nothing
        } else {
            mPython = new PythonTask();
            new Thread(mPython).start();
        }
    }

    @Override
    public void onStart() {

    }

    @Override
    public void onResume() {

    }

    @Override
    public void onPause() {

    }

    @Override
    public void onStop() {

    }

    @Override
    public void onDestroy() {
        mDestroyRequested = true;
        if (mPythonInterpreter != null) {
            mPythonInterpreter.stop();
        }
    }

    /**
     * AsyncTask that:
     *  1. Extracts the python assets folder
     *  2. Initializes the python interpreter
     *  3. Calls the app start function of the bootstrap
     */
    private class PythonTask implements Runnable {//extends AsyncTask<String,String,String> {

        public void run() {
            //protected String doInBackground(String... dirs) {
            // Extract python files from assets
            String path = "python";
            // Get the extracted assets directory
            String assetsPath = mActivity.getApplicationInfo().dataDir + "/assets/"+ path;
            String cachePath = mActivity.getCacheDir().getPath();
            String nativePath = mActivity.getApplicationInfo().nativeLibraryDir;

            AssetExtractor assetExtractor = new AssetExtractor(mActivity);

            // Get install time
            long installTime = 0;
            try {
                installTime = mActivity.getPackageManager().getPackageInfo(
                        mActivity.getPackageName(),0
                ).lastUpdateTime;
            } catch (PackageManager.NameNotFoundException e) {
                e.printStackTrace();
            }

            File pyc = new File(assetsPath + "/main.pyc");
            File py = new File(assetsPath + "/main.py");

            // If assets version changed, remove the old, and copy the new ones
            if (assetExtractor.getAssetsVersion() != installTime || !(pyc.exists()||py.exists())) {

                //publishProgress("Updating... Please wait.");
                assetExtractor.removeAssets(path);
                assetExtractor.copyAssets(path);
                assetExtractor.setAssetsVersion(installTime);

                // On first load change message
                //publishProgress("Loading... Please wait.");
            } else {
                // Start the Python interpreter
                //publishProgress("Loading... Please wait.");
            }

            // Initialize python
            // Note: This must be NOT done in the UI thread!
            int result = mPythonInterpreter.start(assetsPath, cachePath, nativePath);
            Log.i(TAG, "Python main() finished with code: "+result);
            mPythonInterpreter.stop();

            //return assetsPath;
            onPostExecute(assetsPath);
        }

        /**
         * When the python has finished the loading in the background
         * Call start to display the view.
         * @param result
         */
        protected void onPostExecute(String pythonPath) {
            Log.i(TAG, "Python thread complete!");
            if (!mDestroyRequested && mActivity.showDebugMessages()) {
                mActivity.showErrorMessage(
                        "Unexpected python interpreter exit\n" +
                                "Check the logcat output for errors!\n" +
                                "This may indicate a build issue leading to missing or \n" +
                                "inaccessible python or shared libraries.\n" +
                                "Log output:\n\n"+ getErrorMessage()
                );
            }
        }

        /**
         * Read the logcat output and display the error
         * @thanks to https://stackoverflow.com/questions/27957300/read-logcat-programmatically-for-an-application
         * @return
         */
        protected String getErrorMessage() {
            StringBuilder builder = new StringBuilder();
            String processId = Integer.toString(android.os.Process.myPid());
            try {
                String[] command = new String[] { "logcat", "-d", "-v", "brief" };

                Process process = Runtime.getRuntime().exec(command);

                BufferedReader bufferedReader = new BufferedReader(
                        new InputStreamReader(process.getInputStream()));

                String line;
                while ((line = bufferedReader.readLine()) != null) {
                    if (line.contains(processId)) {
                        builder.append(line+"\n");
                    }
                }
                return builder.toString();
            } catch (IOException ex) {
                return "";
            }
        }

        /**
         * Set the progress text to make loading not seem as slow.
         * @param status
         */
        protected void onProgressUpdate(String... status) {
            mActivity.showLoading(status[0]);
        }
    }


}
