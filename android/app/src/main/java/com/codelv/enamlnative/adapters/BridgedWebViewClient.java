package com.codelv.enamlnative.adapters;

import android.graphics.Bitmap;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.webkit.WebViewClient;

/**
 * A web view client that allows all events to be observed by a listener.
 *
 * Created by jrm on 7/7/17.
 */
public class BridgedWebViewClient extends WebViewClient {
    protected WebViewListener mListener;
    protected WebView mWebView;
    protected final BridgedWebChromeClient mChromeClient = new BridgedWebChromeClient();

    public BridgedWebViewClient() {}

    public void setWebView(WebView view, WebViewListener listener) {
        mWebView = view;
        mListener = listener;
        mChromeClient.setWebViewListener(mListener);
        mWebView.setWebViewClient(this);
        mWebView.setWebChromeClient(mChromeClient);
    }

    /**
     * Enable javascript
     * @param enabled
     */
    public void setJavaScriptEnabled(boolean enabled) {
        mWebView.getSettings().setJavaScriptEnabled(enabled);
    }

    @Override
    public void onLoadResource(WebView view, String url) {
        if (mListener!=null) {
            mListener.onLoadResource(view, url);
        }
    }

    @Override
    public void onPageStarted(WebView view, String url, Bitmap favicon) {
        if (mListener!=null) {
            mListener.onPageStarted(view, url);
        }
    }

    @Override
    public void onPageFinished(WebView view, String url) {
        if (mListener!=null) {
            mListener.onPageFinished(view, url);
        }
    }

    @Override
    public void onScaleChanged(WebView view, float oldScale, float newScale) {
        if (mListener!=null) {
            mListener.onScaleChanged(view, oldScale, newScale);
        }
    }

    @Override
    public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
        if (mListener!=null) {
            mListener.onReceivedError(view, errorCode, description, failingUrl);
        }
    }

    public static class BridgedWebChromeClient extends WebChromeClient {
        protected WebViewListener mListener;

        public BridgedWebChromeClient() {}

        public void setWebViewListener(WebViewListener listener) {
            mListener = listener;
        }

        public void onProgressChanged(WebView view, int progress) {
            if (mListener !=null) {
                mListener.onProgressChanged(view, progress);
            }
        }

        public void onReceivedTitle(WebView view, String title) {
            if (mListener !=null) {
                mListener.onReceivedTitle(view, title);
            }
        }

    }


    interface WebViewListener {
        /**
         * Notify the host application that the WebView will load the resource specified by the given url.
         * @param view
         * @param url
         */
        void onLoadResource(WebView view, String url);

        /**
         * Notify the host application that a page has started loading.
         * @param view
         * @param url
         */
        void onPageStarted(WebView view, String url);

        /**
         * Notify the host application that a page has finished loading.
         * @param view
         * @param url
         */
        void onPageFinished(WebView view, String url);

        /**
         * Report web resource loading error to the host application.
         * @param view
         * @param request
         * @param error
         */
        void onReceivedError(WebView view, int errorCode, String description, String failingUrl);

        /**
         * Notify the host application that the scale applied to the WebView has changed.
         * @param view
         * @param oldScale
         * @param newScale
         */
        void onScaleChanged(WebView view, float oldScale, float newScale);

        /**
         * Tell the host application the current progress of loading a page.
         * @param view
         * @param progress
         */
        void onProgressChanged(WebView view, int progress);

        /**
         * Notify the host application of a change in the document title.
         * @param view
         * @param title
         */
        void onReceivedTitle(WebView view, String title);
    }


}
