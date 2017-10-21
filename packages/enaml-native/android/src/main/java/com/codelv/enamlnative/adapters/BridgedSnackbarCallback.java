package com.codelv.enamlnative.adapters;

import android.support.design.widget.Snackbar;

/**
 * Add a listener interface to a Snackbar Callbacks
 */
public class BridgedSnackbarCallback extends Snackbar.Callback {
    protected SnackbarListener mListener;

    public void setListener(SnackbarListener listener) {
        mListener = listener;
    }

    @Override
    public void onDismissed(Snackbar transientBottomBar, int event) {
        if (mListener != null) {
            mListener.onDismissed(transientBottomBar, event);
        }
        super.onDismissed(transientBottomBar, event);
    }

    @Override
    public void onShown(Snackbar sb) {
        if (mListener != null) {
            mListener.onShown(sb);
        }
        super.onShown(sb);
    }

    interface SnackbarListener {
        public void onDismissed(Snackbar transientBottomBar, int event);
        public void onShown(Snackbar sb);
    }
}
