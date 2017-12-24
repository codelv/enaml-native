package com.codelv.enamlnative.adapters;

import java.io.IOException;
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
public class BridgedAsyncHttpCallback implements Callback, Interceptor{

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
     * Wraps the response body to retain the loopj api so we can stream callback data
     * to python and also show progress.
     */
    @Override
    public Response intercept(Chain chain) throws IOException {
        Response originalResponse = chain.proceed(chain.request());
        return originalResponse.newBuilder()
                .body(new ProgressResponseBody(originalResponse.body()))
                .build();
    }

    private class ProgressResponseBody extends ResponseBody {

        private final ResponseBody mResponseBody;
        private BufferedSource mBufferedSource;

        ProgressResponseBody(ResponseBody responseBody) {
            mResponseBody = responseBody;
            onStart();
        }

        @Override
        public MediaType contentType() {
            return mResponseBody.contentType();
        }

        @Override
        public long contentLength() {
            return mResponseBody.contentLength();
        }

        @Override
        public BufferedSource source() {
            if (mBufferedSource == null) {
                mBufferedSource = Okio.buffer(source(mResponseBody.source()));
            }
            return mBufferedSource;
        }

        /**
         * Wraps the source and dispatches the data read
         * @param source
         * @return
         */
        private Source source(Source source) {
            return new ForwardingSource(source) {
                long totalBytesRead = 0L;

                @Override
                public long read(Buffer sink, long byteCount) throws IOException {
                    long bytesRead;
                    if (mStream) {
                        byte[] responseData = sink.readByteArray(byteCount);
                        onProgressData(responseData);
                        bytesRead = responseData.length;
                    } else {
                        bytesRead = super.read(sink, byteCount);
                    }

                    // read() returns the number of bytes read, or -1 if this source is exhausted.
                    totalBytesRead += bytesRead != -1 ? bytesRead : 0;

                    // Dispatch progress
                    onProgress(totalBytesRead, mResponseBody.contentLength());

                    return bytesRead;
                }
            };
        }
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
     * @param responseBody stream data
     */
    public void onProgressData(byte[] responseBody) {
        mBytesSent += responseBody.length;
        if (mListener!=null && mStream) {
            mListener.onProgressData(responseBody);
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
            mListener.onSuccess(response.code(), headers.toMultimap(),
                    (mStream)?null:response.body().bytes());
            mListener.onFinish();
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
        void onSuccess(int statusCode, Map headers, byte[] responseBody);
        void onFailure(int statusCode, Map headers, byte[] responseBody, String error);
    }

}
