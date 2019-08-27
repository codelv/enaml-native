package com.codelv.enamlnative.adapters;

import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.Map;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Headers;
import okhttp3.Interceptor;
import okhttp3.MediaType;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.ResponseBody;
import okio.Buffer;
import okio.BufferedSource;
import okio.ForwardingSource;
import okio.Okio;
import okio.Source;

/**
 * Created by jrm on 7/20/17.
 */
public class BridgedAsyncHttpCallback implements Callback {

    private static final String TAG = "BridgeAsyncHttp";
    protected AsyncHttpResponseListener mListener;
    protected boolean mStream = false;
    protected long mBytesSent = 0;

    /**
     * Creates a new BridgedAsyncHttpCallback
     */
    public BridgedAsyncHttpCallback() {}

    /**
     * Set a listener that will be notified of all the events. If stream is true data
     * will be sent in chunks via onProgressData and NOT at the end. Otherwise data
     * will be sent in onSuccess or onFailure.
     * @param listener
     */
    public void setAsyncHttpResponseListener(AsyncHttpResponseListener listener, boolean stream) {
        mListener = listener;
        mStream = stream;
    }

    /**
     * Fired when the request is started, override to handle in your own code
     */
    public void onStart() {
        if (mListener!=null) {
            mListener.onStart();
        }
    }

    /**
     * Fired when the request progress, override to handle in your own code
     *
     * @param bytesWritten offset from start of file
     * @param totalSize    total size of file
     */
    public void onProgress(long bytesWritten, long totalSize) {
        if (mListener!=null) {
            mListener.onProgress((bytesWritten>0)?bytesWritten:mBytesSent, totalSize);
        }
    }

    /**
     * Fired when the request progress, override to handle in your own code
     *
     * @param responseData stream data
     */
    public void onProgressData(byte[] responseData) {
        mBytesSent += responseData.length;
        if (mListener!=null && mStream) {
            mListener.onProgressData(responseData);
        }
    }


    /**
     * Fired when a retry occurs, override to handle in your own code
     *
     * @param retryNo number of retry
     */
    public void onRetry(int retryNo) {
        if (mListener!=null) {
            mListener.onRetry(retryNo);
        }
    }

    public void onCancel() {
        if (mListener!=null) {
            mListener.onCancel();
        }
    }

    @Override
    public void onFailure(Call call, IOException e) {
        if (mListener!=null) {
            mListener.onFailure(0, null, null, e.getMessage());
            mListener.onFinish();
        }
    }

    @Override
    public void onResponse(Call call, Response response) throws IOException {
        if (mListener!=null) {
            String headerData = "";
            Headers headers = response.headers();
            ResponseBody body = response.body();
            mListener.onResponse(response.code(), headers.toMultimap(), (mStream)?null:body.bytes());

            if (mStream) {
                InputStream inputStream = null;
                try {
                    inputStream = body.byteStream();
                    long totalBytesRead = 0;
                    int chunkSize = 512*1024;
                    long contentLength = body.contentLength();

                    mListener.onProgress(0L, contentLength);
                    while (true) {
                        byte[] data = new byte[chunkSize];
                        int n = inputStream.read(data);
                        if (n == -1) {
                            break;
                        }
                        totalBytesRead += n;
                        if (n == chunkSize) {
                            onProgressData(data);
                        } else {
                            onProgressData(Arrays.copyOf(data, n));
                        }
                        if (call.isCanceled()) {
                            mListener.onCancel();
                            break;
                        }
                        // Dispatch progress
                        contentLength = body.contentLength();
                        onProgress(totalBytesRead, contentLength);
                    }
                    // Dispatch progress
                    onProgress(totalBytesRead, contentLength);
                } catch (IOException e) {
                    mListener.onFailure(response.code(), headers.toMultimap(),
                            null, e.getMessage());
                } finally {
                    if (inputStream != null) {
                        inputStream.close();
                    }
                    mListener.onFinish();
                }
            } else {
                mListener.onFinish();
            }
        }

    }


    /**
     * Interface for listening from Python
     */
    interface AsyncHttpResponseListener {
        void onStart();
        void onProgress(long bytesWritten, long totalSize);
        void onProgressData(byte[] responseBody);
        void onFinish();
        void onRetry(int retryNo);
        void onCancel();
        void onResponse(int statusCode, Map headers, byte[] responseBody);
        void onFailure(int statusCode, Map headers, byte[] responseBody, String error);
    }

}
