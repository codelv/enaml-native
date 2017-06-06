package com.jventura.pybridge;

import org.json.JSONObject;
import org.json.JSONException;


public class PyBridge {

    /**
     * Initializes the Python interpreter.
     *
     * @param datapath the location of the extracted python files
     * @return error code
     */
    public static native int start(String datapath);

    /**
     * Stops the Python interpreter.
     *
     * @return error code
     */
    public static native int stop();

    /**
     * Sends a string payload to the Python interpreter.
     *
     * @param payload the payload string
     * @return a string with the result
     */
    public static native String call(String payload);

    /**
     * Sends a JSON payload to the Python interpreter.
     *
     * @param payload JSON payload
     * @return JSON response
     */
    public static JSONObject call(JSONObject payload) {
        String result = call(payload.toString());
        try {
            return new JSONObject(result);
        } catch (JSONException e) {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * Class
     */
    public static class PythonCallback implements Runnable {

        private long mCallbackId;

        public PythonCallback(long callbackId) {
            mCallbackId = callbackId;
        }

        @Override
        public void run() {
            try {
                JSONObject json = new JSONObject();
                json.put("method", "callback");
                JSONObject params = new JSONObject();
                params.put("callback_id",mCallbackId);
                json.putOpt("params",params);
                PyBridge.call(json);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    // Load library
    static {
        System.loadLibrary("pybridge");
        System.loadLibrary("jnius");
    }
}
