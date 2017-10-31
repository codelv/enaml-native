package com.codelv.enamlnative;

/**
 * The core interface that allows external packages to hook into the main application.
 */
public interface EnamlPackage {

    // Lifecycle events
    void onCreate(EnamlActivity activity);
    void onStart();
    void onResume();
    void onPause();
    void onStop();
    void onDestroy();

}
