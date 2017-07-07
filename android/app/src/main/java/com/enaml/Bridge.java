package com.enaml;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.HandlerThread;
import android.os.Handler;
import android.view.KeyEvent;
import android.view.View;
import android.util.Log;

import org.msgpack.core.MessageBufferPacker;
import org.msgpack.core.MessagePack;
import org.msgpack.core.MessageUnpacker;
import org.msgpack.value.ArrayValue;
import org.msgpack.value.ExtensionValue;
import org.msgpack.value.FloatValue;
import org.msgpack.value.IntegerValue;
import org.msgpack.value.Value;

import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;


import java.lang.reflect.Proxy;
import java.util.HashMap;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.concurrent.atomic.AtomicInteger;

public class Bridge {

    public static final String TAG = "Bridge";

    public static final int IGNORE_RESULT = 0;

    public static final String CREATE = "c";
    public static final String METHOD = "m";
    public static final String FIELD = "f";
    public static final String DELETE = "d";
    public static final String RESULT = "r";
    public static final String SHOW = "s";
    public static final String ERROR = "e";

    final MainActivity mActivity;

    // Context
    final Context mContext;

    // Root view
    View mRootView;

    // Cache for constructors methods
    final HashMap<String,Constructor> mConstructorCache = new HashMap<String, Constructor>();

    // Cache for methods
    final HashMap<String,Method> mMethodCache = new HashMap<String, Method>();

    // Cache for fields
    final HashMap<String,Field> mFieldCache = new HashMap<String, Field>();

    // Cache for objects
    final ConcurrentHashMap<Integer,Object> mObjectCache = new ConcurrentHashMap<Integer, Object>();


    // Cache for results
    final ConcurrentHashMap<Integer,BridgeFuture<Object>> mResultCache = new ConcurrentHashMap<Integer, BridgeFuture<Object>>();
    private int mResultCount = 0;

    // Looper thread
    final ConcurrentLinkedQueue<Runnable> mTaskQueue = new ConcurrentLinkedQueue<>();
    final ConcurrentLinkedQueue<MessageBufferPacker> mEventList = new ConcurrentLinkedQueue<>();
    final HandlerThread mBridgeHandlerThread = new HandlerThread("bridge");
    final Handler mBridgeHandler;
    final AtomicInteger mEventCount = new AtomicInteger();
    final int mEventDelay = 3;

    public Bridge(Context context) {
        mContext = context;
        mActivity = MainActivity.mActivity;
        mObjectCache.put(-1, mContext);
        mBridgeHandlerThread.start();
        mBridgeHandler = new Handler(mBridgeHandlerThread.getLooper());
    }

    /**
     * Unpacks encoded bridge values. Each value is a tuple of type:
     *
     * ("arg.type.String", <value>)
     *
     * References are passed as ids/integers
     *
     */
    public class UnpackedValues {
        protected final Object[] mArgs;
        protected final Class[] mSpec;
        protected final String mName;

        public UnpackedValues(Value[] args) {
            // Unpack args
            mArgs = new Object[args.length];
            mSpec = new Class[args.length];
            String name = new String();

            // Decode each value
            for (int i=0; i<args.length; i++) {
                Value arg = args[i];
                ArrayValue argv = arg.asArrayValue();
                String argType = argv.get(0).asStringValue().asString();
                name += argType;
                try {
                    if (argType.equals("NoneType")) {
                        mSpec[i] = Void.TYPE;
                    } else if (argType.equals("int")) {
                        mSpec[i] = int.class;
                    } else if (argType.equals("boolean")) {
                        mSpec[i] = boolean.class;
                    } else if (argType.equals("float")) {
                        mSpec[i] = float.class;
                    } else if (argType.equals("long")) {
                        mSpec[i] = long.class;
                    } else if (argType.equals("double")) {
                        mSpec[i] = double.class;
                    } else {
                        mSpec[i] = Class.forName(argType);
                    }

                } catch (ClassNotFoundException e) {
                    mActivity.showErrorMessage(e);
                }

                Value v = argv.get(1);
                if (argType.equals("android.content.Context")) {
                    // Hack for android context
                    mArgs[i] = mContext;
                } else {
                    switch (v.getValueType()) {
                        case NIL:
                            mArgs[i] = null;
                            break;
                        case BOOLEAN:
                            mArgs[i] = v.asBooleanValue().getBoolean();
                            break;
                        case INTEGER:
                            IntegerValue iv = v.asIntegerValue();
                            if (mSpec[i].isInterface()) {
                                // If an int/long is passed for an interface... create a proxy
                                // for the interface and pass in the reference.
                                Class infClass = mSpec[i];
                                Object proxy = Proxy.newProxyInstance(
                                        infClass.getClassLoader(),
                                        new Class[]{infClass},
                                        new BridgeInvocationHandler(iv.toInt())
                                );
                                //mProxyCache.put(objId,proxy);
                                mArgs[i] = proxy;
                            } else if (iv.isInIntRange()) {
                                mArgs[i] = iv.toInt();
                            } else if (iv.isInLongRange()) {
                                mArgs[i] = iv.toLong();
                            } else {
                                mArgs[i] = iv.toBigInteger();
                            }
                            break;
                        case FLOAT:
                            FloatValue fv = v.asFloatValue();
                            if (argType.equals("float")) {
                                mArgs[i] = fv.toFloat();
                            } else {
                                mArgs[i] = fv.toDouble();
                            }
                            break;
                        case STRING:
                            if (argType.equals("android.graphics.Color")) {
                                // Hack for colors
                                mArgs[i] = Color.parseColor(v.asStringValue().asString());
                                mSpec[i] = int.class;
                            } else if (argType.equals("android.graphics.Typeface")) {
                                // Hack for fonts
                                mArgs[i] = Typeface.create(v.asStringValue().asString(), 0);
                            } else {
                                mArgs[i] = v.asStringValue().asString();
                            }
                            break;
                        case BINARY:
                            byte[] mb = v.asBinaryValue().asByteArray();
                            System.out.println("read binary: size=" + mb.length);
                            break;
                        case ARRAY:
                            ArrayValue a = v.asArrayValue();
                            // Use an array for passing references.
                            // Assumes the first element in the array is a pointer
                            // to the reference object we want.
                            for (Value e : a) {
                                mArgs[i] = mObjectCache.get(e.asIntegerValue().toInt());
                                break;
                            }
                            break;
                        case EXTENSION:
                            ExtensionValue ev = v.asExtensionValue();
                            byte extType = ev.getType();
                            byte[] extValue = ev.getData();
                            break;
                    }
                }
            }


            mName = name;
        }

        public Object[] getArgs() {
            return mArgs;
        }

        public Class[] getSpec() {
            return mSpec;
        }

        public String getName() {
            return mName;
        }
    }

    /**
     * Return the root view
     * @return
     */
    public View getRootView() {
        return mRootView;
    }

    /**
     * Return the view with the given id.
     * @return
     */
    public View getView(int objId) { return (View) mObjectCache.get(objId);}

    /**
     * Create a view with the given id.
     *
     * The first call will be set as the root node.
     *
     * @param className
     * @param objId
     */
    public void createObject(int objId, String className, Value[] args) {
        try {
            UnpackedValues uv = new UnpackedValues(args);
            String key = className + uv.getName();

            // Try to pull from cache
            if (!mConstructorCache.containsKey(key)) {
                Class objClass = Class.forName(className);
                mConstructorCache.put(className, objClass.getConstructor(uv.getSpec()));
            }

            // Create the instance
            Constructor constructor = mConstructorCache.get(className);
            Object obj = constructor.newInstance(uv.getArgs());

            // For views, set the id as well
            if (obj instanceof View) {
                View view = (View) obj;
                view.setId(objId);
                if (mRootView==null) {
                    mRootView = view;
                }
            }

            // Save to cache
            mObjectCache.put(objId, obj);
        } catch (InstantiationException e) {
            mActivity.showErrorMessage(e);
        } catch (IllegalAccessException e) {
            mActivity.showErrorMessage(e);
        } catch (InvocationTargetException e) {
            mActivity.showErrorMessage(e);
        } catch (ClassNotFoundException e) {
            mActivity.showErrorMessage(e);
        } catch (NoSuchMethodException e) {
            mActivity.showErrorMessage(e);
        }
    }

    /**
     * Call a method on the view with the given id.
     *
     * Uses lambdas (via retrolambda) to have as fast as direct use performance:
     * @see  https://github.com/Hervian/lambda-factory/
     *
     * @param objId
     * @param method
     * @param args
     */
    public void updateObject(int objId, int resultId, String method, Value[] args) {
        //Log.e(TAG,"id="+objId+" method="+method);
        Object obj = mObjectCache.get(objId);
        if (obj==null) {
            Log.e(TAG,"Error: Null object reference when updating id="+objId+" method="+method);
        }
        Class objClass = obj.getClass();

        // Decode args
        UnpackedValues uv = new UnpackedValues(args);
        String key = objClass.getName() + method+ uv.getName();

        // Cache the lambda methods
        if (!mMethodCache.containsKey(key)) {
            try {
                mMethodCache.put(key, objClass.getMethod(method, uv.getSpec()));
            } catch (NoSuchMethodException e) {
                Log.e(TAG,"Error getting method id="+objId+" method="+method, e);
                mActivity.showErrorMessage(e);
                return;
            } catch (Exception e) {
                Log.e(TAG,"Error getting method id="+objId+" method="+method, e);
                mActivity.showErrorMessage(e);
                return;
            }
        }

        // Get the lambda
        Method lambda = mMethodCache.get(key);
        try {
            Object result = lambda.invoke(obj, uv.getArgs());
            onResult(resultId, result);
        } catch (IllegalAccessException e) {
            Log.e(TAG,"Error invoking obj="+ obj +" id="+objId+" method="+method, e);
            mActivity.showErrorMessage(e);
        } catch (InvocationTargetException e) {
            Log.e(TAG,"Error invoking obj="+ obj +" id="+objId+" method="+method, e);
            mActivity.showErrorMessage(e);
        }
    }

    /**
     * Call a method on the view with the given id.
     *
     * Uses lambdas (via retrolambda) to have as fast as direct use performance:
     * @see  https://github.com/Hervian/lambda-factory/
     *
     * @param objId
     * @param method
     * @param args
     */
    public void updateObjectField(int objId, String field, Value[] args) {
        Object obj = mObjectCache.get(objId);
        if (obj==null) {
            Log.e(TAG,"Error: Null object reference when updating id="+objId+" field="+field);
        }
        Class objClass = obj.getClass();

        // Decode args
        UnpackedValues uv = new UnpackedValues(args);
        String key = objClass.getName() + field;

        // Cache the lambda methods
        if (!mFieldCache.containsKey(key)) {
            try {
                mFieldCache.put(key, objClass.getField(field));
            } catch (Exception e) {
                mActivity.showErrorMessage(e);
                return;
            }
        }

        // Get the lambda
        Field lambda = mFieldCache.get(key);
        try {
            lambda.set(obj, uv.getArgs()[0]);
        } catch (IllegalAccessException e) {
            mActivity.showErrorMessage(e);
        }
    }

    /**
     * Destroy the object by removing it from the cache.
     * @param objId
     */
    public void deleteObject(int objId) {
        // Log.d(TAG, "Delete object id="+objId);
        Object obj = mObjectCache.get(objId);
        if (obj !=null) {
            mObjectCache.remove(objId);
            //obj = null; Will GC handle this??
        }
    }

    /**
     * BridgeFuture access is always done in the main same thread,
     * so it's really simple...
     *
     * @param <T>
     */
    class BridgeFuture<T> implements Future<T> {
        private boolean mDone = false;
        private boolean mCancelled = false;
        private T mResult = null;

        @Override
        public boolean cancel(boolean mayInterruptIfRunning) {
            mCancelled = true;
            return true;
        }

        @Override
        public boolean isCancelled() {
            return mCancelled;
        }

        @Override
        public boolean isDone() {
            return mDone;
        }

        public void setResult(T result) {
            mResult = result;
            mDone = true;
        }

        @Override
        public T get() throws InterruptedException, ExecutionException {
            return (T) mResult;
        }

        @Override
        public T get(long timeout, TimeUnit unit) throws InterruptedException, ExecutionException, TimeoutException {
            return mResult;
        }
    }

    /**
     * InvocationHandler that dispatches the event over the bridge and
     * invokes the proper callback in Python.
     */
    class BridgeInvocationHandler implements InvocationHandler {
        private final int mPythonObjectPtr;

        public BridgeInvocationHandler(int ptr) {
            mPythonObjectPtr = ptr;
        }

        @Override
        public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
            int resultId = IGNORE_RESULT;
            if (!method.getReturnType().equals(Void.TYPE)) {
                mResultCount += 1;
                mResultCache.put(mResultCount, (new BridgeFuture<Object>()));
                resultId = mResultCount;
            }
            return onEvent(resultId, mPythonObjectPtr, method.getName(), args);
        }
    }

    /**
     * Set the result of a future. Note, don't do this in the UI thread or we'll get a deadlock.
     * @param objId
     * @param result
     */
    public void setResult(int objId, Value result) {
        BridgeFuture<Object> future = mResultCache.get(objId);
        UnpackedValues uv = new UnpackedValues(new Value[]{result});
        future.setResult(uv.getArgs()[0]);
    }

    /**
     * Sets the result of a future in python.
     * @param pythonObjectId
     * @param result
     */
    public void onResult(int pythonObjectId, Object result) {
        if (pythonObjectId==IGNORE_RESULT) {
            return;
        }
        // TODO: This should use the EventLoop implementation
        onEvent(IGNORE_RESULT, pythonObjectId, "set_result", new Object[]{result});
    }

    /**
     * Packs an event and sends it to python. The event is packed in the format:
     *
     * ("event",(returnId, pythonObjectId, "method", (args...)))
     * @param resultId: id of the future to set the result of. If 0, result shall be ignored.
     * @param pythonObjectId: ptr to object in python. Cast to object to get a reference
     * @param method: method name to invoke on the object
     * @param args: args to pass to the method
     * @return
     */
    public Object onEvent(int resultId, int pythonObjectId, String method, Object[] args) {
        MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
        try {
            packer.packArrayHeader(2);
            packer.packString("event");
            packer.packArrayHeader(4);
            packer.packInt(resultId);
            packer.packInt(pythonObjectId);
            packer.packString(method);
            if (args==null) {
                packer.packArrayHeader(0);
            } else {
                packer.packArrayHeader(args.length);
                for (Object arg : args) {
                    packer.packArrayHeader(2);
                    if (arg==null) {
                        // Discard this event??
                        Log.w(TAG,"Warning: Trying to send event '"+method+"' with a null argument!");
                        //return null;
                        packer.packString("void");
                        packer.packNil();
                        continue;
                    }
                    Class argClass = arg.getClass();
                    packer.packString(argClass.getCanonicalName());
                    if (argClass == int.class || arg instanceof Integer) {
                        packer.packInt((int) arg);
                    } else if (argClass == int.class || arg instanceof Boolean) {
                        packer.packBoolean((boolean) arg);
                    } else if (argClass == String.class) {
                        packer.packString((String) arg);
                    } else if (argClass == long.class || arg instanceof Long) {
                        packer.packLong((long) arg);
                    } else if (argClass == float.class || arg instanceof Float) {
                        packer.packFloat((float) arg);
                    } else if (argClass == double.class || arg instanceof Double) {
                        packer.packDouble((double) arg);
                    } else if (argClass == short.class || arg instanceof Short) {
                        packer.packShort((short) arg);
                    } else if (arg instanceof View) {
                        // This only works with ids's created in python
                        packer.packInt(((View) arg).getId());
                    } else if (arg instanceof KeyEvent) {
                        KeyEvent event = (KeyEvent) arg;
                        packer.packString(KeyEvent.keyCodeToString(event.getKeyCode()));
//                    } else if (arg instanceof MotionEvent) {
//                        MotionEvent event = (MotionEvent) arg;
//                        packer.packString(MotionEvent.actionToString(event.getAction()));
                    } else {
                        packer.packString(arg.toString());
                    }
                }
            }
            packer.close();
        } catch (IOException e) {
            mActivity.showErrorMessage(e);
        }

        // Send events to python
        sendEvent(packer);

        // If a result is requested, poll async until ready.
        if (resultId != IGNORE_RESULT) {
            try {
                Future<Object> future = mResultCache.get(resultId);
                while (!future.isDone()) {
                    // Process pending messages until done
                    // TODO: Busy loop, maybe block?
                    Runnable task = mTaskQueue.poll();
                    if (task != null) {
                        task.run();
                    }
                }
                Object result = future.get();
                mResultCache.remove(resultId);
                return result;
            } catch (InterruptedException e) {
                mActivity.showErrorMessage(e);
            } catch (ExecutionException e) {
                mActivity.showErrorMessage(e);
            }
        }

        return null;
    }


    /**
     * Interface for python to pass it's calls in a structured manner
     * for Java to actually call.
     *
     *
     * In python, using jnius
     *
     * class TextView(JavaProxyClass):
     *      __javaclass__ = `android.widgets.TextView`
     *
     * #: etc.. for other widgets
     *
     * v = LinearLayout()
     *
     * tv = TextView()
     * tv.setText("text")
     *
     * v.addView(tv)
     *
     * maps to:
     * [
     *  #: Argument of context is implied
     *  ("createView", ("android.widgets.LinearLayout",0x01)),
     *  ("createView", ("android.widgets.TextView",0x02)),
     *  ("updateView", (0x02,"setText","text")),
     *  ("updateView", (0x01,"addView",{"ref":0x01})
     * ]
     *
     * @warning This is called from the Python thread, NOT the UI thread!
     *
     * @param view
     */
    public void processEvents(byte[] data) {
        MessageUnpacker unpacker = MessagePack.newDefaultUnpacker(data);
        try {
            int eventCount = unpacker.unpackArrayHeader();
            for (int i=0; i<eventCount; i++) {
                int eventTuple = unpacker.unpackArrayHeader(); // Unpack event tuple
                String eventType = unpacker.unpackString(); // first value
                int paramCount = unpacker.unpackArrayHeader();

                switch (eventType) {
                    case CREATE:
                        int objId = unpacker.unpackInt();
                        String objClass = unpacker.unpackString();
                        int argCount = unpacker.unpackArrayHeader();
                        Value[] args = new Value[argCount];
                        for (int j=0; j<argCount; j++) {
                            Value v = unpacker.unpackValue();
                            args[j] = v;
                        }
                        mTaskQueue.add(()->{createObject(objId, objClass, args);});
                        break;

                    case METHOD:
                        objId = unpacker.unpackInt();
                        int resultId = unpacker.unpackInt();
                        String objMethod = unpacker.unpackString();
                        argCount = unpacker.unpackArrayHeader();
                        args = new Value[argCount];
                        for (int j=0; j<argCount; j++) {
                            Value v = unpacker.unpackValue();
                            args[j] = v;
                        }
                        mTaskQueue.add(()->{updateObject(objId, resultId, objMethod, args);});
                        break;
                    case FIELD:
                        objId = unpacker.unpackInt();
                        String objField = unpacker.unpackString();
                        argCount = unpacker.unpackArrayHeader();
                        args = new Value[argCount];
                        for (int j=0; j<argCount; j++) {
                            Value v = unpacker.unpackValue();
                            args[j] = v;
                        }
                        mTaskQueue.add(()->{updateObjectField(objId, objField, args);});
                        break;
                    case DELETE:
                        objId = unpacker.unpackInt();
                        mTaskQueue.add(()->{deleteObject(objId);});
                        break;

                    case RESULT:
                        objId = unpacker.unpackInt();
                        Value arg = unpacker.unpackValue();
                        mTaskQueue.add(()->{setResult(objId, arg);});
                        break;
                    case SHOW:
                        mTaskQueue.add(()->{mActivity.setView(getRootView());});
                        break;
                    case ERROR:
                        String errorMessage = unpacker.unpackString();
                        mTaskQueue.add(()->{mActivity.showErrorMessage(errorMessage);});
                        break;
                }
            }
        } catch (IOException e) {
            mActivity.showErrorMessage(e);
        }

        // TODO: if we're waiting on a future, this will create a deadlock,
        // how do i process them now??
        // TODO: WHY POST?
        mActivity.runOnUiThread(()->{
            long start = System.currentTimeMillis();
            Runnable task = mTaskQueue.poll();
            while (task != null) {
                task.run();
                task = mTaskQueue.poll();
            }
            Log.i(TAG, "Running tasks took ("+(System.currentTimeMillis()-start)+" ms)");
        });
    }

    /**
     * Post an event to the bridge handler thread.
     * When the delay expires, send the data to the app
     * event listener.
     */
    public void sendEvent(MessageBufferPacker event) {
        mEventCount.incrementAndGet();
        mEventList.add(event);
        // Send to bridge thread for processing
        mBridgeHandler.postDelayed(() -> {
            int delays = mEventCount.decrementAndGet();
            MainActivity.AppEventListener listener = mActivity.getAppEventListener();

            // If events stopped updating temporarily
            if (listener != null && delays == 0) {
                MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
                try {
                    // Events can be added during packing this so pull only what's here now.
                    int size = mEventList.size();
                    packer.packArrayHeader(size);
                    for (int i=0; i<size; i++){
                        MessageBufferPacker e = mEventList.remove();
                        packer.addPayload(e.toByteArray());
                    }
                } catch (IOException e) {
                    mActivity.showErrorMessage(e);
                }
                listener.onEvents(packer.toByteArray());
                //mEventList.clear();
            }
        }, mEventDelay);
    }

}