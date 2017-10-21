package com.codelv.enamlnative.demo;

import android.app.Application;

import com.codelv.enamlnative.EnamlApplication;
import com.codelv.enamlnative.EnamlPackage;
import com.codelv.enamlnative.packages.BridgePackage;
import com.codelv.enamlnative.packages.GoogleMapsPackage;
import com.codelv.enamlnative.packages.IconifyPackage;
import com.codelv.enamlnative.packages.PythonPackage;

import java.util.Arrays;
import java.util.List;

/**
 * Created by jrm on 10/15/17.
 */

public class MainApplication extends Application implements EnamlApplication {
    @Override
    public List<EnamlPackage> getPackages() {
        return Arrays.<EnamlPackage>asList(
                new BridgePackage(),
                new PythonPackage(),
                new IconifyPackage(),
                new GoogleMapsPackage()
        );
    }

    @Override
    public boolean showDebugMessages() {
        return BuildConfig.DEBUG;
    }
}
