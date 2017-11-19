package com.codelv.enamlnative.adapters;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/**
 * A BroadcastReceiver that delegates to a listener.
 *
 * Created by jrm on 11/18/17.
 */
public class BridgeBroadcastReceiver extends BroadcastReceiver {
    Receiver mDelegate;

    public BridgeBroadcastReceiver() {
        super();
    }

    public void setReceiver(Receiver listener) {
        mDelegate = listener;
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        mDelegate.onReceive(context, intent);
    }

    interface Receiver {
        void onReceive(Context context, Intent intent);
    }

}
