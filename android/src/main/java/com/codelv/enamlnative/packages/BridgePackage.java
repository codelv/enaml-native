package com.codelv.enamlnative.packages;

import com.codelv.enamlnative.EnamlActivity;
import com.codelv.enamlnative.EnamlPackage;
import com.codelv.enamlnative.Bridge;


/**
 * Created by jrm on 10/15/17.
 */
public class BridgePackage implements EnamlPackage {
    Bridge mBridge;
    EnamlActivity mActivity;

    @Override
    public void onCreate(EnamlActivity activity) {
        mActivity = activity;
        mBridge = new Bridge(activity);

        // Set the bridge
        activity.setBridge(mBridge);
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

    }

}