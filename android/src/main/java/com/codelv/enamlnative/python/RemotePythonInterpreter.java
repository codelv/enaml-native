package com.codelv.enamlnative.python;

import com.codelv.enamlnative.BuildConfig;

import java.util.concurrent.TimeUnit;

import okhttp3.WebSocket;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.WebSocketListener;
import okio.ByteString;

/**
 * Uses websockets send and receive bridge events to python running
 * remotely (ie not on Android)..
 * You must have the the enaml-native dev server running locally.
 *
 * Created by jrm on 12/16/17.
 */
public class RemotePythonInterpreter extends PythonInterpreter {
    static boolean mDone = false;
    static OkHttpClient mClient;
    static DevClient mDevClient;
    static WebSocket mWebsocket;
    static RemotePythonInterpreter mInstance;

    /**
     * Singleton
     */
    protected RemotePythonInterpreter() {
        mInstance = this;
    }

    public static RemotePythonInterpreter instance() {
        if (mInstance==null) {
            new RemotePythonInterpreter();
        }
        return mInstance;
    }

    /**
     * Initializes the Python interpreter.
     *
     * @param pythonPath the location of the extracted python files
     * @param nativePath the location of native libraries
     * @return error code
     */
    public static int start(String pythonPath, String nativePath) {
        OkHttpClient mClient = new OkHttpClient.Builder()
                .readTimeout(0,  TimeUnit.MILLISECONDS)
                .build();
        Request request = new Request.Builder()
                .url(BuildConfig.DEV_SERVER)
                .build();
        mDevClient = new DevClient();
        mClient.newWebSocket(request, mDevClient);
        try {
            // Block indefinitely
            while (!mDone) {
                Thread.sleep(1000);
            }
            return 0;
        } catch (InterruptedException e) {
            e.printStackTrace();
            return -1;
        }
    }

    /**
     * Sends bridge encoded event data to the python bridge implementation
     *
     * @param data Bridge encoded data
     * @return Bridge encoded response data
     */
    public static int sendEvents(byte[] data) {
        if (mWebsocket != null) {
            mWebsocket.send(ByteString.of(data));
        }
        return 0;
    }

    /**
     * Stops the Python interpreter.
     *
     * @return error code
     */
    public static int stop() {
        // Trigger shutdown of the dispatcher's executor so this process can exit cleanly.
        mDone = true;
        mClient.dispatcher().executorService().shutdown();
        return 0;
    }


    static class DevClient extends WebSocketListener {
        @Override
        public void onOpen(WebSocket webSocket, Response response) {
            // Tell the enaml-native dev server this is the android app
            mWebsocket = webSocket;
        }

        @Override
        public void onMessage(WebSocket webSocket, String text) {
            // This should never happen
        }

        @Override
        public void onMessage(WebSocket webSocket, ByteString bytes) {
            publishEvents(bytes.toByteArray());
        }

        @Override
        public void onClosing(WebSocket webSocket, int code, String reason) {
            webSocket.close(1000, null);
            mWebsocket = null;
        }

        @Override
        public void onFailure(WebSocket webSocket, Throwable t, Response response) {
            t.printStackTrace();
            mWebsocket = null;
        }
    }
}
