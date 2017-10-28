package com.codelv.enamlnative.packages;

import com.codelv.enamlnative.EnamlActivity;
import com.codelv.enamlnative.EnamlPackage;
import com.codelv.enamlnative.Bridge;

/**
 * Created by jrm on 10/15/17.
 */

public class ChartsPackage implements EnamlPackage {

    EnamlActivity mActivity;

    @Override
    public void onCreate(EnamlActivity activity) {
        mActivity = activity;
    }

    /**
     * Add special bridge packers required by map components
     */
    @Override
    public void onStart() {
        Bridge bridge = mActivity.getBridge();
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
