package com.enaml;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Build;
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
import java.lang.reflect.Array;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;


import java.lang.reflect.Proxy;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.concurrent.atomic.AtomicInteger;

import static org.msgpack.core.MessagePack.newDefaultUnpacker;

public class Bridge {

    public static final String TAG = "Bridge";

    // Result handling
    public static final int TYPE_REF = 1;
    public static final int IGNORE_RESULT = 0;

    // Bridge commands
    public static final String CREATE = "c";
    public static final String PROXY = "p";
    public static final String METHOD = "m";
    public static final String STATIC_METHOD = "sm";
    public static final String FIELD = "f";
    public static final String DELETE = "d";
    public static final String RESULT = "r";
    public static final String ERROR = "e";

    final MainActivity mActivity;

    final Bridge mBridge;

    // Context
    final Context mContext;

    // Cache for constructors methods
    final HashMap<Integer,Constructor> mConstructorCache = new HashMap<Integer, Constructor>();

    // Cache for methods
    final HashMap<Integer,Method> mMethodCache = new HashMap<Integer, Method>();

    // Cache for fields
    final HashMap<Integer,Field> mFieldCache = new HashMap<Integer, Field>();

    // Cache for Classes
    final HashMap<String,Class> mClassCache = new HashMap<String, Class>();

    final HashMap<Integer, Class[]> mClassSpecCache = new HashMap<Integer, Class[]>();

    final HashMap<Class,HashMap<Integer,Object>> mReflectionCache = new HashMap<>();

    // Cache for objects
    final ConcurrentHashMap<Integer,Object> mObjectCache = new ConcurrentHashMap<Integer, Object>();

    // Cache for results
    final ConcurrentHashMap<Integer,BridgeFuture<Object>> mResultCache = new ConcurrentHashMap<Integer, BridgeFuture<Object>>();
    // For generating IDs
    private int mResultCount = 0;

    // Looper thread
    final LinkedBlockingQueue<Runnable> mTaskQueue = new LinkedBlockingQueue<>();
    final ConcurrentLinkedQueue<MessageBufferPacker> mEventList = new ConcurrentLinkedQueue<>();
    final HandlerThread mBridgeHandlerThread = new HandlerThread("bridge");
    final Handler mBridgeHandler;
    final AtomicInteger mEventCount = new AtomicInteger();
    final int mEventDelay = 1;

    public Bridge(Context context) {
        mBridge = this;
        mContext = context;
        mActivity = MainActivity.mActivity;
        mObjectCache.put(-1, mContext);
        mBridgeHandlerThread.start();
        mBridgeHandler = new Handler(mBridgeHandlerThread.getLooper());
    }

    /**
     * Get the class for the given name (including primitive types)
     * @param name
     * @return
     * @throws ClassNotFoundException
     */
    public Class getClass(String name) throws ClassNotFoundException {
        Class cls = mClassCache.get(name);
        if (cls==null) {
            if (name.equals("NoneType")) {
                cls = Void.TYPE;
            } else if (name.equals("int")) {
                cls = int.class;
            } else if (name.equals("boolean") || name.equals("bool")) {
                cls = boolean.class;
            } else if (name.equals("float")) {
                cls = float.class;
            } else if (name.equals("long")) {
                cls = long.class;
            } else if (name.equals("double")) {
                cls = double.class;
            } else {
                cls = Class.forName(name);
            }
            mClassCache.put(name,cls);
        }
        return cls;
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

        public class UnpackedValue {
            public final Class cls;
            public final Object arg;
            public UnpackedValue(Class cls, Object arg) {
                this.cls = cls;
                this.arg = arg;
            }
        }

        public UnpackedValues(int cacheId, Value[] args) throws ClassNotFoundException, IOException {
            // Unpack args
            mArgs = new Object[args.length];

            Class[] spec = mClassSpecCache.get(cacheId);
            boolean newSpec = cacheId==0 || spec==null;
            if (newSpec) {
                spec = new Class[args.length];
                mClassSpecCache.put(cacheId,spec);
            }

            // Decode each value
            for (int i=0; i<args.length; i++) {
                // Every arg is a tuple of (String type ,Value arg)
                ArrayValue argv = args[i].asArrayValue();

                // Get the argument value
                Value type = argv.get(0);
                Value v = argv.get(1);
                if (newSpec) {
                    // Get the argument type
                    spec[i] = mBridge.getClass(type.asStringValue().asString());
                }

                // Determine the class
                UnpackedValue uv = unpackValue(spec[i], type, v);
                if (newSpec) {
                    spec[i] = uv.cls;
                }
                mArgs[i] = uv.arg;
            }

            mSpec = spec;
        }

        /**
         * Parse the value based on the given type
         * @param spec
         * @param type (may be null)
         * @param v
         */
        protected UnpackedValue unpackValue(Class spec, Value type, Value v) throws IOException {
            Object arg = null;
            switch (v.getValueType()) {
                case NIL:
                    break;

                case BOOLEAN:
                    arg = v.asBooleanValue().getBoolean();
                    break;

                case INTEGER:
                    IntegerValue iv = v.asIntegerValue();
                    if (spec.isInterface()) {
                        // If an int/long is passed for an interface... create a proxy
                        // for the interface and pass in the reference.
                        Class infClass = spec;
                        Object proxy = Proxy.newProxyInstance(
                                infClass.getClassLoader(),
                                new Class[]{infClass},
                                new BridgeInvocationHandler(iv.toInt())
                        );
                        //mProxyCache.put(objId,proxy);
                        arg = proxy;
                    } else if (iv.isInIntRange()) {
                        arg = iv.toInt();
                    } else if (iv.isInLongRange()) {
                        arg = iv.toLong();
                    } else {
                        arg = iv.toBigInteger();
                    }
                    break;

                case FLOAT:
                    FloatValue fv = v.asFloatValue();
                    if (spec==float.class || spec == Float.TYPE) {
                        arg = fv.toFloat();
                    } else {
                        arg = fv.toDouble();
                    }
                    break;

                case STRING:
                    String argType = (type==null)?"":type.asStringValue().asString();
                    if (argType.equals("android.graphics.Color")) {
                        // Hack for colors
                        spec = int.class; // Umm?
                        String color = v.asStringValue().asString();
                        // Add support for #RGB and #ARGB
                        if (color.length()==4) {
                            // #RGB
                            color = String.format("#%c%c%c%c%c%c",
                                    color.charAt(1),color.charAt(1), // R
                                    color.charAt(2),color.charAt(2), // G
                                    color.charAt(3),color.charAt(3)); // B
                        } else if (color.length()==5) {
                            // #ARGB
                            color = String.format("#%c%c%c%c%c%c%c%c",
                                    color.charAt(1),color.charAt(1), // A
                                    color.charAt(2),color.charAt(2), // R
                                    color.charAt(3),color.charAt(3), // G
                                    color.charAt(4),color.charAt(4)); // B
                        }
                        arg = Color.parseColor(color);
                    } else if (argType.equals("android.R")) {
                        // Hack for resources such as
                        // @drawable/icon_name
                        // @string/bla
                        // @layout/etc
                        // Strip off the @ and split by path
                        String sv = v.asStringValue().asString();
                        String[] res = sv.substring(1).split("/");
                        assert res.length == 2: "Resources must match @<type>/<name>, got '"+sv+"'!";
                        int resId = mActivity.getResources().getIdentifier(
                                res[1], res[0], "android"
                        );
                        if (resId==0) {
                            resId = mActivity.getResources().getIdentifier(
                                    res[1], res[0], mActivity.getPackageName()
                            );
                        }
                        Log.d(TAG,"Replacing resource `"+sv+"` with id "+resId);
                        spec = int.class;
                        arg = resId;
                    } else if (spec==Typeface.class) {
                        // Hack for fonts
                        arg = Typeface.create(v.asStringValue().asString(), 0);
                    } else {
                        arg = v.asStringValue().asString();
                    }
                    break;

                case BINARY:
                    arg = v.asBinaryValue().asByteArray();
                    break;

                case ARRAY:
                    ArrayValue a = v.asArrayValue();
                    // Use an array for passing references.
                    // Assumes the first element in the array is a pointer
                    // to the reference object we want.
                    if (spec.isInstance(Collection.class)) {
                        ArrayList list = new ArrayList<>();
                        for (int i=0; i<a.size(); i++) {
                            UnpackedValue uv = unpackValue(Object.class, null, a.get(i));
                            list.add(uv.arg);
                        }
                        arg = list;
                    } else {
                        // Primitive array?
                        Class arrayType = spec.getComponentType();
                        assert arrayType != null : "Array values must have an array arg type matching the JNI syntax" +
                                ". Ex '[Ljava.lang.String' or `[I` ";
                        arg = Array.newInstance(arrayType, a.size());
                        for (int i = 0; i < a.size(); i++) {
                            UnpackedValue uv = unpackValue(arrayType, null, a.get(i));
                            Array.set(arg, i, uv.arg);
                        }
                    }
                    break;

                case EXTENSION:
                    // Currenly only extension is JavaBridgeObjects
                    ExtensionValue ev = v.asExtensionValue();
                    int extType = (int) ev.getType();
                    if (extType==TYPE_REF) {
                        MessageUnpacker ref = MessagePack.newDefaultUnpacker(ev.getData());
                        arg = mObjectCache.get(ref.unpackInt());
                    }
            }
            return new UnpackedValue(spec, arg);
        }

        public Object[] getArgs() {
            return mArgs;
        }

        public Class[] getSpec() {
            return mSpec;
        }

    }


    /**
     * Define the "spec" for a construtor, method, or field invocation and save it in the cache
     * to speed up runtime operation.
     * @param cacheId
     * @param type
     * @param args
     */
    public void defineSpec(int cacheId, String type, Value[] args) {

    }

    /**
     * Create a view with the given id.
     *
     * The first call will be set as the root node.
     *
     * @param className
     * @param objId
     */
    public void createObject(int objId, int cacheId, String className, Value[] args) {
        //Log.d(TAG,"Create object id="+objId+" cacheId="+cacheId+" class="+className);
        try {
            UnpackedValues uv = new UnpackedValues(cacheId, args);
            //String key = className + uv.getName();

            // Try to pull from cache
            Constructor constructor = mConstructorCache.get(cacheId);
            if (constructor==null) {
                Class objClass = mBridge.getClass(className);
                constructor = objClass.getConstructor(uv.getSpec());
                mConstructorCache.put(cacheId, constructor);
            }

            // Create the instance
            Object obj = constructor.newInstance(uv.getArgs());

            assert obj!=null: "Failed to create id="+objId+" type="+className;

            // For views, set the id as well
            if (obj instanceof View) {
                View view = (View) obj;
                view.setId(objId);
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
        } catch (AssertionError e) {
            mActivity.showErrorMessage(e.getMessage());
        } catch (IOException e) {
            mActivity.showErrorMessage(e);
        }
    }

    /**
     * Create a proxy for the given interface that directs it's calls to the object
     * with the given refId.
     * @param objId
     * @param interfaceName
     * @param refId
     */
    public void createProxy(int objId, String interfaceName, int refId) {
        try {
            Class infClass = mBridge.getClass(interfaceName);
            Object proxy = Proxy.newProxyInstance(
                    infClass.getClassLoader(),
                    new Class[]{infClass},
                    new BridgeInvocationHandler(refId)
            );
            mObjectCache.put(objId,proxy);
        } catch (ClassNotFoundException e) {
            mActivity.showErrorMessage(e);
        }
    }

    /**
     * Call a static method on the class with the given name.
     *
     * @param className: Class name to invoke the method on
     * @param resultId: Serves two purposes,
     *                  1. ID that result should be stored as
     *                  2. and ID of the Future in python that can be used to retrieve the result
     * @param method: Method to invoke on the given object
     * @param args: Args to pass to the object
     */
    public void invokeStatic(String className, int resultId, int cacheId, String method, Value[] args) {
        try {
            Class objClass = mBridge.getClass(className);

            // Decode args
            UnpackedValues uv = new UnpackedValues(cacheId, args);

            // Cache the lambda methods
            Method lambda = mMethodCache.get(cacheId);
            if (lambda==null) {
                try {
                    lambda = objClass.getMethod(method, uv.getSpec());
                    mMethodCache.put(cacheId, lambda);
                } catch (NoSuchMethodException e) {
                    Log.e(TAG,"Error getting method of class="+className+" method="+method, e);
                    mActivity.showErrorMessage(e);
                    return;
                } catch (Exception e) {
                    Log.e(TAG,"Error getting method of class="+className+" method="+method, e);
                    mActivity.showErrorMessage(e);
                    return;
                }
            }


            // Get the lambda
            Object result = lambda.invoke(objClass, uv.getArgs());
            onResult(resultId, result);
        } catch (IllegalAccessException e) {
            Log.e(TAG,"Error invoking class method="+method+" of class="+className, e);
            mActivity.showErrorMessage(e);
        } catch (InvocationTargetException e) {
            Log.e(TAG,"Error invoking class method="+method+" of class="+className, e);
            mActivity.showErrorMessage(e);
        } catch (ClassNotFoundException e) {
            mActivity.showErrorMessage(e);
        } catch (IOException e) {
            mActivity.showErrorMessage(e);
        }
    }

    /**
     * Call a method on the view with the given id.
     *
     * @param objId: ID of object to invoke the method on
     * @param resultId: Serves two purposes,
     *                  1. ID that result should be stored as
     *                  2. and ID of the Future in python that can be used to retrieve the result
     * @param method: Method to invoke on the given object
     * @param args: Args to pass to the object
     */
    public void updateObject(int objId, int resultId, int cacheId, String method, Value[] args) {
        //Log.d(TAG,"Update object  obid="+objId+" method="+method);
        Object obj = mObjectCache.get(objId);
        if (obj==null) {
            mActivity.showErrorMessage(
                    "Error: Null object reference when updating id="+objId+" method="+method);
            return;
        }

        try {
            // Decode args
            UnpackedValues uv = new UnpackedValues(cacheId, args);
            //String key = objClass.getName() + method+ uv.getName();

            Class objClass = obj.getClass();
            HashMap<Integer,Object> reflectionCache = mReflectionCache.get(objClass);
            if (reflectionCache==null) {
                reflectionCache = new HashMap<>();
                mReflectionCache.put(objClass, reflectionCache);

            }

            // Cache the lambda methods
            Method lambda = (Method) reflectionCache.get(cacheId);
            if (lambda==null) {
                try {
                    // Must use the declaring class method OR we get IllegalArgumentExceptions
                    // ex. Expected receiver of type x, but got y
                    lambda = objClass.getMethod(method, uv.getSpec());
                    lambda.setAccessible(true);
                    reflectionCache.put(cacheId, lambda);
                } catch (NoSuchMethodException e) {
                    Log.e(TAG,"Error getting method id="+objId+" method="+method+" on object="+obj, e);
                    mActivity.showErrorMessage(e);
                    return;
                } catch (Exception e) {
                    Log.e(TAG,"Error getting method id="+objId+" method="+method+" on object="+obj, e);
                    mActivity.showErrorMessage(e);
                    return;
                }
            }


            // Get the lambda
            Object result = lambda.invoke(obj, uv.getArgs());
            onResult(resultId, result);
        } catch (IllegalAccessException e) {
            Log.e(TAG,"Error invoking obj="+ obj +" id="+objId+" method="+method, e);
            mActivity.showErrorMessage(e);
        } catch (InvocationTargetException e) {
            Log.e(TAG,"Error invoking obj="+ obj +" id="+objId+" method="+method, e);
            mActivity.showErrorMessage(e);
        } catch (ClassNotFoundException e) {
            mActivity.showErrorMessage(e);
        } catch (IOException e) {
            mActivity.showErrorMessage(e);
        }
    }

    /**
     * Call a method on the view with the given id.
     *
     * @param objId
     * @param field
     * @param args
     */
    public void updateObjectField(int objId, int cacheId, String field, Value[] args) {
        Object obj = mObjectCache.get(objId);
        if (obj==null) {
            mActivity.showErrorMessage(
                    "Error: Null object reference when updating id="+objId+" field="+field);
            return;
        }

        try {
            // Decode args
            UnpackedValues uv = new UnpackedValues(cacheId, args);


            // This is pretty stupid but we have to get the method of EACH class that uses it
            // for some stupid reason it can't
            Class objClass = obj.getClass();
            HashMap<Integer,Object> reflectionCache = mReflectionCache.get(objClass);
            if (reflectionCache==null) {
                reflectionCache = new HashMap<>();
                mReflectionCache.put(objClass, reflectionCache);

            }

            // Cache the lambda methods
            Field lambda = (Field) reflectionCache.get(cacheId);
            if (lambda==null) {
                try {
                    lambda = objClass.getField(field);
                    lambda.setAccessible(true);
                    reflectionCache.put(cacheId, lambda);
                } catch (Exception e) {
                    mActivity.showErrorMessage(e);
                    return;
                }
            }

            // Get the lambda
            lambda.set(obj, uv.getArgs()[0]);
        } catch (IllegalAccessException e) {
            mActivity.showErrorMessage(e);
        } catch (ClassNotFoundException e ) {
            mActivity.showErrorMessage(e);
        } catch (IOException e) {
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
     * Set the result of a future.
     * @param objId
     * @param result
     */
    public void setResult(int objId, Value result) {
        try {
            BridgeFuture<Object> future = mResultCache.get(objId);
            UnpackedValues uv = new UnpackedValues(0, new Value[]{result});
            future.setResult(uv.getArgs()[0]);
        } catch (ClassNotFoundException e) {
            mActivity.showErrorMessage(e);
        } catch (IOException e) {
            mActivity.showErrorMessage(e);
        }
    }

    /**
     * If the pythonObjectId!=IGNORE_RESULT, this sets the result of a future in python and
     * stores the result locally within the object cache if it is not a primitive type.
     * @param pythonObjectId
     * @param result
     */
    public void onResult(int pythonObjectId, Object result) {
        if (pythonObjectId==IGNORE_RESULT) {
            return;
        }

        if (!isPackableResult(result)) {
            // Store the result with the given ID, the python implementation
            // guarantees that the ID is unique and will not overwrite an existing object
            mObjectCache.put(pythonObjectId, result);
        }

        // Send the result to python
        // TODO: This should use the EventLoop implementation, currently assumes a tornado Future
        onEvent(IGNORE_RESULT, pythonObjectId, "set_result", new Object[]{result});
    }

    /**
     * A very crude way of determining if the result is of a primitive type or if a reference
     * needs created.  Results that can be sent via msgpack do not need to have a reference created.
     * @param result
     * @return
     */
    protected boolean isPackableResult(Object result) {
        Class resultType = result.getClass();
        if (resultType == int.class || result instanceof Integer) {
            return true;
        } else if (resultType == boolean.class || result instanceof Boolean) {
            return true;
        } else if (result instanceof String) {
            return true;
        } else if (resultType == long.class || result instanceof Long) {
            return true;
        } else if (resultType == float.class || result instanceof Float) {
            return true;
        } else if (resultType == double.class || result instanceof Double) {
            return true;
        } else if (resultType == short.class || result instanceof Short) {
            return true;
        }
        return false;
    }

    /**
     * Packs an event and sends it to python. The event is packed in the format:
     *
     * ("event",(returnId, pythonObjectId, "method", (args...)))
     * @param resultId: Id of the Future in Java to return the result to.
     *                  If resultId==IGNORE_RESULT, python shall not send a result back.
     * @param pythonObjectId: ptr to object in python object cache.
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

                    // TODO: There has to be a better way than this...
                    if (argClass == int.class || arg instanceof Integer) {
                        packer.packInt((int) arg);
                    } else if (argClass == int[].class) {
                        int[] argList = (int[]) arg;
                        packer.packArrayHeader(argList.length);
                        for (int v:argList) {
                            packer.packInt(v);
                        }
                    } else if (argClass == boolean.class || arg instanceof Boolean) {
                        packer.packBoolean((boolean) arg);
                    } else if (argClass == boolean[].class) {
                        boolean[] argList = (boolean[]) arg;
                        packer.packArrayHeader(argList.length);
                        for (boolean v:argList) {
                            packer.packBoolean(v);
                        }
                    } else if (argClass == String.class) {
                        packer.packString((String) arg);
                    } else if (argClass == String[].class) {
                        String[] argList = (String[]) arg;
                        packer.packArrayHeader(argList.length);
                        for (String v:argList) {
                            packer.packString(v);
                        }
                    } else if (argClass == long.class || arg instanceof Long) {
                        packer.packLong((long) arg);
                    } else if (argClass == long[].class) {
                        long[] argList = (long[]) arg;
                        packer.packArrayHeader(argList.length);
                        for (long v:argList) {
                            packer.packLong(v);
                        }
                    } else if (argClass == float.class || arg instanceof Float) {
                        packer.packFloat((float) arg);
                    } else if (argClass == float[].class) {
                        float[] argList = (float[]) arg;
                        packer.packArrayHeader(argList.length);
                        for (float v:argList) {
                            packer.packFloat(v);
                        }
                    } else if (argClass == double.class || arg instanceof Double) {
                        packer.packDouble((double) arg);
                    } else if (argClass == double[].class) {
                        double[] argList = (double[]) arg;
                        packer.packArrayHeader(argList.length);
                        for (double v:argList) {
                            packer.packDouble(v);
                        }
                    } else if (argClass == short.class || arg instanceof Short) {
                        packer.packShort((short) arg);
                    } else if (argClass == short[].class) {
                        short[] argList = (short[]) arg;
                        packer.packArrayHeader(argList.length);
                        for (short v:argList) {
                            packer.packShort(v);
                        }
                    } else if (argClass == byte[].class) {
                        byte[] bytes = (byte[]) arg;
                        packer.packBinaryHeader(bytes.length);
                        packer.addPayload(bytes);
                    } else if (arg instanceof View) {
                        // This only works with ids's created in python
                        packer.packInt(((View) arg).getId());
                    } else if (arg instanceof KeyEvent) {
                        KeyEvent event = (KeyEvent) arg;
                        packer.packString(KeyEvent.keyCodeToString(event.getKeyCode()));
//                    } else if (arg instanceof MotionEvent) {
//                        MotionEvent event = (MotionEvent) arg;
//                        packer.packString(MotionEvent.actionToString(event.getAction()));
                    } else if (pythonObjectId!=IGNORE_RESULT && method.equals("set_result")) {
                        // If it was packable, it should already be packed
                        packer.packInt(pythonObjectId);
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
                runUntilDone(future);
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
     * Run UI tasks until the future is completed. This MUST be called in the UI thread.
     * @param future: Future to wait for.
     */
    public void runUntilDone(Future future) {
        long start = System.currentTimeMillis();
        int i = 0;
        while (!future.isDone()) {
            // Process pending messages until done
            try {
                // TODO: Busy loop, maybe block?
                Runnable task = mTaskQueue.take();
                task.run();
                i++;
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        }
        if (i>0) {
            Log.i(TAG, "runUntilDone took (" + (System.currentTimeMillis() - start) + " ms) to run (" + i + ") tasks");
        }
    }

    /**
     * Run UI tasks until the queue is empty.
     * This MUST only be called in the UI thread.
     */
    public void runUntilCurrent() {
        long start = System.currentTimeMillis();
        Runnable task = mTaskQueue.poll();
        int i = 0;
        while (task != null) {
            task.run();
            task = mTaskQueue.poll();
            i++;
        }
        if (i>0) {
            Log.i(TAG, "runUntilCurrent took (" + (System.currentTimeMillis() - start) + " ms) to run ("+ i + ") tasks");
        }
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
        mBridgeHandler.post(()->{
            long start = System.currentTimeMillis();
            MessageUnpacker unpacker = newDefaultUnpacker(data);
            try {
                int eventCount = unpacker.unpackArrayHeader();
                for (int i=0; i<eventCount; i++) {
                    int eventTuple = unpacker.unpackArrayHeader(); // Unpack event tuple
                    String eventType = unpacker.unpackString(); // first value
                    int paramCount = unpacker.unpackArrayHeader();

                    switch (eventType) {
                        case CREATE:
                            int objId = unpacker.unpackInt();
                            int cacheId = unpacker.unpackInt();
                            String objClass = unpacker.unpackString();
                            int argCount = unpacker.unpackArrayHeader();
                            Value[] args = new Value[argCount];
                            for (int j=0; j<argCount; j++) {
                                Value v = unpacker.unpackValue();
                                args[j] = v;
                            }
                            mTaskQueue.add(()->{createObject(objId, cacheId, objClass, args);});
                            break;

                        case PROXY:
                            objId = unpacker.unpackInt();
                            objClass = unpacker.unpackString();
                            int refId = unpacker.unpackInt();
                            mTaskQueue.add(()->{createProxy(objId, objClass, refId);});
                            break;

                        case METHOD:
                            objId = unpacker.unpackInt();
                            int resultId = unpacker.unpackInt();
                            cacheId = unpacker.unpackInt();
                            String objMethod = unpacker.unpackString();
                            argCount = unpacker.unpackArrayHeader();
                            args = new Value[argCount];
                            for (int j=0; j<argCount; j++) {
                                Value v = unpacker.unpackValue();
                                args[j] = v;
                            }
                            mTaskQueue.add(()->{updateObject(objId, resultId, cacheId, objMethod, args);});
                            break;
                        case STATIC_METHOD:
                            objClass = unpacker.unpackString();
                            resultId = unpacker.unpackInt();
                            cacheId = unpacker.unpackInt();
                            objMethod = unpacker.unpackString();
                            argCount = unpacker.unpackArrayHeader();
                            args = new Value[argCount];
                            for (int j=0; j<argCount; j++) {
                                Value v = unpacker.unpackValue();
                                args[j] = v;
                            }
                            mTaskQueue.add(()->{invokeStatic(objClass, resultId, cacheId, objMethod, args);});
                            break;

                        case FIELD:
                            objId = unpacker.unpackInt();
                            cacheId = unpacker.unpackInt();
                            String objField = unpacker.unpackString();
                            argCount = unpacker.unpackArrayHeader();
                            args = new Value[argCount];
                            for (int j=0; j<argCount; j++) {
                                Value v = unpacker.unpackValue();
                                args[j] = v;
                            }
                            mTaskQueue.add(()->{updateObjectField(objId, cacheId, objField, args);});
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

                        case ERROR:
                            String errorMessage = unpacker.unpackString();
                            mTaskQueue.add(()->{mActivity.showErrorMessage(errorMessage);});
                            break;
                    }
                }
            } catch (IOException e) {
                mActivity.runOnUiThread(()->{
                    mActivity.showErrorMessage(e);
                });
            }

            // Process requested tasks
            mActivity.runOnUiThread(()->{
                runUntilCurrent();
            });
            Log.i(TAG, "processEvents took (" + (System.currentTimeMillis() - start) + " ms) to run");
        });
    }

    /**
     * Post an event to the bridge handler thread.
     * When the delay expires, send the data to the app
     * event listener (which goes to Python).
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
            }
        }, mEventDelay);
    }

    /**
     * Return build info
     * @return
     */
    public byte[] getBuildInfo() {
        MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
        try {
            packer.packMapHeader(20);
            
            packer.packString("BOARD");
            packer.packString(Build.BOARD);
            packer.packString("BOOTLOADER");
            packer.packString(Build.BOOTLOADER);
            packer.packString("BOARD");
            packer.packString(Build.BOARD);
            packer.packString("BOOTLOADER");
            packer.packString(Build.BOOTLOADER);
            packer.packString("BRAND");
            packer.packString(Build.BRAND);
            packer.packString("DEVICE");
            packer.packString(Build.DEVICE);
            packer.packString("DISPLAY");
            packer.packString(Build.DISPLAY);
            packer.packString("FINGERPRINT");
            packer.packString(Build.FINGERPRINT);
            packer.packString("HARDWARE");
            packer.packString(Build.HARDWARE);
            packer.packString("HOST");
            packer.packString(Build.HOST);
            packer.packString("ID");
            packer.packString(Build.ID);
            packer.packString("MANUFACTURER");
            packer.packString(Build.MANUFACTURER);
            packer.packString("MODEL");
            packer.packString(Build.MODEL);
            packer.packString("PRODUCT");
            packer.packString(Build.PRODUCT);
            packer.packString("SERIAL");
            packer.packString(Build.SERIAL);
            packer.packString("USER");
            packer.packString(Build.USER);
            packer.packString("SDK_INT");
            packer.packString(""+Build.VERSION.SDK_INT);
            packer.packString("BASE_OS");
            packer.packString(Build.VERSION.BASE_OS);
            packer.packString("RELEASE");
            packer.packString(Build.VERSION.RELEASE);
            packer.packString("CODENAME");
            packer.packString(Build.VERSION.CODENAME);


            return packer.toByteArray();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }
}
