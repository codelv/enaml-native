package com.enaml;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.view.View;
import android.view.ViewManager;
import android.util.Log;
import android.widget.CheckBox;

import org.msgpack.core.MessageBufferPacker;
import org.msgpack.core.MessagePack;
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

public class Bridge {

    public static final String TAG = "Bridge";

    // Context
    Context mContext;

    // Root view
    View mRootView;

    // Cache for constructors methods
    final HashMap<String,Constructor> mConstructorCache = new HashMap<String, Constructor>();

    // Cache for methods
    final HashMap<String,Method> mMethodCache = new HashMap<String, Method>();

    // Cache for fieldss
    final HashMap<String,Field> mFieldCache = new HashMap<String, Field>();

    // Cache for objects
    final HashMap<Integer,Object> mObjectCache = new HashMap<Integer, Object>();


    public Bridge(Context context) {
        mContext = context;
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
                    if (argType.equals("int")) {
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
                    e.printStackTrace();
                }

                Value v = argv.get(1);

                switch (v.getValueType()) {
                    case NIL:
                        mArgs[i] = null;
                        break;
                    case BOOLEAN:
                        mArgs[i] = v.asBooleanValue().getBoolean();
                        break;
                    case INTEGER:
                        IntegerValue iv = v.asIntegerValue();
                        if (argType.equals("android.content.Context")) {
                            // Hack for android context
                            mArgs[i] = mContext;
                        } else if (
                                // TODO: There should be a generic way for doing this
                                argType.equals("android.view.ViewGroup$LayoutParams") ||
                                argType.equals("android.view.View") ||
                                argType.equals("android.widget.SpinnerAdapter")
                                ) {
                            // Hack for passing references. Assumes that if you pass
                            // an int for a type that is not an int,
                            // we want to reference an object
                            mArgs[i] = mObjectCache.get(iv.toInt());
//                            if (mArgs[i]==null) {
//                                Log.e(TAG, "Failed to dereference id="+iv.toInt()+" for type="+argType);
//                            } else {
//                                Log.i(TAG, "Converted id=" + iv.toInt() + " type="+argType+" to=" + mArgs[i].toString());
//                            }
                        } else if (mSpec[i].isInterface()) {
                            // If an int/long is passed for an interface... create a proxy
                            // for the interface and pass in the reference.
                            Class infClass = mSpec[i];
                            Object proxy = Proxy.newProxyInstance(
                                    infClass.getClassLoader(),
                                    new Class[]{infClass},
                                    new BridgeInvocationHandler(iv.toLong())
                            );
                            //mProxyCache.put(objId,proxy);
                            mArgs[i] = proxy;
                        } else if (iv.isInIntRange()) {
                            mArgs[i] = iv.toInt();
                        }
                        else if (iv.isInLongRange()) {
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
                            mArgs[i] =  fv.toDouble();
                        }
                        break;
                    case STRING:
                        if (argType.equals("android.graphics.Color")) {
                            // Hack for colors
                            mArgs[i] = Color.parseColor(v.asStringValue().asString());
                            mSpec[i] = int.class;
                        } else if (argType.equals("android.graphics.Typeface")) {
                            // Hack for fonts
                            mArgs[i] = Typeface.create(v.asStringValue().asString(),0);
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
                        for (Value e : a) {
                            System.out.println("read array element: " + e);
                        }
                        break;
                    case EXTENSION:
                        ExtensionValue ev = v.asExtensionValue();
                        byte extType = ev.getType();
                        byte[] extValue = ev.getData();
                        break;
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
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
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
    public void updateObject(int objId, String method, Value[] args) {
        Object obj = mObjectCache.get(objId);
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
                return;
            } catch (Throwable e) {
                Log.e(TAG,"Error getting method id="+objId+" method="+method, e);
                return;
            }
        }

        // Get the lambda
        Method lambda = mMethodCache.get(key);
        try {
            lambda.invoke(obj, uv.getArgs());
        } catch (IllegalAccessException e) {
            Log.e(TAG,"Error invoking id="+objId+" method="+method, e);
        } catch (InvocationTargetException e) {
            Log.e(TAG,"Error invoking id="+objId+" method="+method, e);
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
        //Log.i(TAG,"Update id="+objId+" method="+method);
        Object obj = mObjectCache.get(objId);
        Class objClass = obj.getClass();

        // Decode args
        UnpackedValues uv = new UnpackedValues(args);
        String key = objClass.getName() + field;

        // Cache the lambda methods
        if (!mFieldCache.containsKey(key)) {
            try {
                mFieldCache.put(key, objClass.getField(field));
            } catch (Throwable throwable) {
                throwable.printStackTrace();
                return;
            }
        }

        // Get the lambda
        Field lambda = mFieldCache.get(key);
        try {
            lambda.set(obj, uv.getArgs()[0]);
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
    }

    /**
     * Destroy the object by removing it from the cache.
     * @param objId
     */
    public void deleteObject(int objId) {
        Object obj = mObjectCache.get(objId);
        if (obj !=null) {
            mObjectCache.remove(objId);
            obj = null;
        }
    }

    /**
     * InvocationHandler that dispatches the event over the bridge and
     * invokes the proper callback in Python.
     */
    class BridgeInvocationHandler implements InvocationHandler {
        private final long mPythonObjectPtr;

        public BridgeInvocationHandler(long ptr) {
            mPythonObjectPtr = ptr;
        }

        @Override
        public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
            return onEvent(mPythonObjectPtr, proxy, method, args);
        }
    }

    /**
     * Packs an event and sends it to python. The event is packed in the format:
     *
     * ("event",(pythonObjectId,"method", (args...)))
     *
     * @param pythonObjectId
     * @param proxy
     * @param method
     * @param args
     * @return
     */
    public Object onEvent(long pythonObjectId, Object proxy, Method method, Object[] args) {
        MainActivity activity = MainActivity.mActivity;
        MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
        try {
            packer.packArrayHeader(2);
            packer.packString("event");
            packer.packArrayHeader(3);
            packer.packLong(pythonObjectId);
            packer.packString(method.getName());
            if (args==null) {
                packer.packArrayHeader(0);
            } else {
                packer.packArrayHeader(args.length);
                for (Object arg : args) {
                    packer.packArrayHeader(2);
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
                        packer.packInt(((View) arg).getId());
                    } else {
                        packer.packString(arg.toString());
                    }
                }
            }
            packer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Send events to python
        activity.sendEvent(packer);
        return null;
    }

}