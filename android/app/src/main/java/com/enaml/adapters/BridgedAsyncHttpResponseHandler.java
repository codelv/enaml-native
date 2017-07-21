package com.enaml.adapters;

import com.loopj.android.http.AsyncHttpResponseHandler;
import cz.msebera.android.httpclient.Header;

/**
 * Created by jrm on 7/20/17.
 */
public class BridgedAsyncHttpResponseHandler extends AsyncHttpResponseHandler {

    protected AsyncHttpResponseListener mListener;
    protected boolean mStream = false;

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
            mListener.onProgress(bytesWritten, totalSize);
        }
    }

    /**
     * Fired when the request progress, override to handle in your own code
     *
     * @param responseBody stream data
     */
    public void onProgressData(byte[] responseBody) {
        if (mListener!=null && mStream) {
            mListener.onProgressData(responseBody);
        }
    }

    /**
     * Fired in all cases when the request is finished, after both success and failure, override to
     * handle in your own code
     */
    public void onFinish() {
        if (mListener!=null) {
            mListener.onFinish();
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


    /**
     * Fired when a request returns successfully, override to handle in your own code
     *
     * @param statusCode   the status code of the response
     * @param headers      return headers, if any
     * @param responseBody the body of the HTTP response from the server
     */
    @Override
    public void onSuccess(int statusCode, Header[] headers, byte[] responseBody) {
        if (mListener!=null) {
            mListener.onSuccess(statusCode, headers, (mStream)?null:responseBody);
        }

    }

    /**
     * Fired when a request fails to complete, override to handle in your own code
     *
     * @param statusCode   return HTTP status code
     * @param headers      return headers, if any
     * @param responseBody the response body, if any
     * @param error        the underlying cause of the failure
     */
    @Override
    public void onFailure(int statusCode, Header[] headers, byte[] responseBody, Throwable error) {
        if (mListener!=null) {
            mListener.onFailure(statusCode, headers, (mStream)?null:responseBody, error);
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
        void onSuccess(int statusCode, Header[] headers, byte[] responseBody);
        void onFailure(int statusCode, Header[] headers, byte[] responseBody, Throwable error);
    }

}
