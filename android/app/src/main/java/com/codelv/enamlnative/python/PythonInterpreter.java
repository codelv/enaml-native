package com.codelv.enamlnative.python;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by jrm on 10/16/17.
 */

public class PythonInterpreter {

    static PythonInterpreter mInstance;
    final List<EventListener> mEventListeners = new ArrayList<EventListener>();

    /**
     * Singleton
     */
    protected PythonInterpreter() {
        mInstance = this;
    }

    public static PythonInterpreter instance() {
        if (mInstance==null) {
            new PythonInterpreter();
        }
        return mInstance;
    }

    /**
     * Initializes the Python interpreter.
     *
     * @param pythonPath the location of the extracted python files
     * @param nativePath the location of native libraries
     * @return error code
     */
    public static native int start(String pythonPath, String nativePath);

    /**
     * Sends bridge encoded event data to the python bridge implementation
     *
     * @param data Bridge encoded data
     * @return Bridge encoded response data
     */
    public static native int sendEvents(byte[] data);

    /**
     * Stops the Python interpreter.
     *
     * @return error code
     */
    public static native int stop();

    /**
     * Add a listener to events in python
     * @param listener
     */
    public static void addEventListener(EventListener listener) {
        PythonInterpreter interpreter = PythonInterpreter.instance();
        interpreter.getEventListeners().add(listener);
    }


    /**
     * Add a listener to events in python
     * @param listener
     */
    public static void removeEventListener(EventListener listener) {
        PythonInterpreter interpreter = PythonInterpreter.instance();
        interpreter.getEventListeners().remove(listener);
    }

    /**
     * Get the event listeners
     * @return
     */
    public List<EventListener> getEventListeners() {
        return mEventListeners;
    }

    /**
     * The python implementation uses this to publish events to java.
     * @param data
     */
    public static void publishEvents(byte[] data) {
        PythonInterpreter interpreter = PythonInterpreter.instance();
        for(EventListener listener:interpreter.getEventListeners()) {
            listener.onEvents(data);
        }
    }

    public interface EventListener {
        /**
         * Receives bridge encoded event data from the python bridge implementation
         * @param data
         */
        void onEvents(byte[] data);
    }

    // Load library
    static {
        System.loadLibrary("pybridge");
    }
}
