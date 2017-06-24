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
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;


import java.lang.reflect.Proxy;
import java.util.HashMap;
import java.util.Objects;

public class UiManager {

    public static final String TAG = "UiManager";

    // Context
    Context mContext;

    // Root view
    View mRootView;

    // Cache for constructors methods
    final HashMap<String,Constructor> mConstructorCache = new HashMap<String, Constructor>();

    // Cache for methods
    final HashMap<String,Method> mMethodCache = new HashMap<String, Method>();

    // Cache for views
    final HashMap<Long,View> mViewCache = new HashMap<Long, View>();
    //final HashMap<Long,Object> mProxyCache = new HashMap<Long, Object>();

    public UiManager(Context context) {
        mContext = context;
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
    public View getView(int viewId) { return mViewCache.get(viewId);}

    /**
     * Create a view with the given id.
     *
     * The first call will be set as the root node.
     *
     * @param className
     * @param viewId
     */
    public void createView(String className, long viewId) {
        try {
            //Log.i(TAG,"Create "+className+" id="+viewId);
            if (!mConstructorCache.containsKey(className)) {
                Class viewClass = Class.forName(className);
                mConstructorCache.put(className, viewClass.getConstructor(Context.class));
            }
            Constructor constructor = mConstructorCache.get(className);
            View view = (View) constructor.newInstance(mContext);
            mViewCache.put(viewId, view);
            if (mRootView==null) {
                mRootView = view;
            }
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
     * @param viewId
     * @param method
     * @param args
     */
    public void updateView(long viewId, String method, Value[] args) {
        //Log.i(TAG,"Update id="+viewId+" method="+method);
        View view = mViewCache.get(viewId);
        Class viewClass = view.getClass();
        String key = viewClass.getName() + method;


        // Unpack args
        Object[] methodArgs = new Object[args.length];
        Class[] methodSpec = new Class[args.length];

        //
        for (int i=0; i<args.length; i++) {
            Value arg = args[i];
            ArrayValue argv = arg.asArrayValue();
            String argType = argv.get(0).asStringValue().asString();
            try {
                if (argType.equals("int")) {
                    methodSpec[i] = int.class;
                } else if (argType.equals("boolean")) {
                    methodSpec[i] = boolean.class;
                } else if (argType.equals("float")) {
                    methodSpec[i] = float.class;
                } else if (argType.equals("long")) {
                    methodSpec[i] = long.class;
                } else if (argType.equals("double")) {
                    methodSpec[i] = double.class;
                } else {
                    methodSpec[i] = Class.forName(argType);
                }

            } catch (ClassNotFoundException e) {
                e.printStackTrace();
                return;
            }

            Value v = argv.get(1);

            switch (v.getValueType()) {
                case NIL:
                    methodArgs[i] = null;
                    break;
                case BOOLEAN:
                    methodArgs[i] = v.asBooleanValue().getBoolean();
                    break;
                case INTEGER:
                    IntegerValue iv = v.asIntegerValue();
                    // Hack for passing references
                    if (argType.equals("android.view.View")) {
                        methodArgs[i] = mViewCache.get(iv.toLong());
                    } else if (methodSpec[i].isInterface()) {
                        // If an int/long is passed for an interface... create a proxy
                        // for the interface and pass in the reference.
                        Class infClass = methodSpec[i];
                        Object proxy = Proxy.newProxyInstance(
                            infClass.getClassLoader(),
                            new Class[]{infClass},
                            new BridgeInvocationHandler(iv.toLong())
                        );
                        //mProxyCache.put(viewId,proxy);
                        methodArgs[i] = proxy;
                    } else if (iv.isInIntRange()) {
                        methodArgs[i] = iv.toInt();
                    }
                    else if (iv.isInLongRange()) {
                        methodArgs[i] = iv.toLong();
                    } else {
                        methodArgs[i] = iv.toBigInteger();
                    }
                    break;
                case FLOAT:
                    FloatValue fv = v.asFloatValue();
                    if (argType.equals("float")) {
                        methodArgs[i] = fv.toFloat();
                    } else {
                        methodArgs[i] =  fv.toDouble();
                    }
                    break;
                case STRING:
                    if (argType.equals("android.graphics.Color")) {
                        // Hack for colors
                        methodArgs[i] = Color.parseColor(v.asStringValue().asString());
                        methodSpec[i] = int.class;
                    } else if (argType.equals("android.graphics.Typeface")) {
                        // Hack for fonts
                        methodArgs[i] = Typeface.create(v.asStringValue().asString(),0);
                    } else {
                        methodArgs[i] = v.asStringValue().asString();
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
            key += argType; // Append signature to key
        }

        // Cache the lambda methods
        if (!mMethodCache.containsKey(key)) {
            try {
                Method viewClassMethod = null;
                viewClassMethod = viewClass.getMethod(method, methodSpec);
                mMethodCache.put(key, viewClassMethod);
            } catch (NoSuchMethodException e) {
                e.printStackTrace();
                return;
            } catch (Throwable throwable) {
                throwable.printStackTrace();
                return;
            }
        }

        // Get the lambda
        Method lambda = mMethodCache.get(key);
        try {
            lambda.invoke(view, methodArgs);
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        }

    }
    /*
    public void connectView(int viewId, String method, Value[] args) {
        View view = mViewCache.get(viewId);
        Class viewClass = view.getClass();
        ArrayValue argv = args[0].asArrayValue();
        try {
            Class infClass = Class.forName(argv.get(0).asStringValue().asString());
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
            return;
        }
        Object o = Proxy.newProxyInstance(infClass.getClassLoader(), new Class[]{infClass},
            (Object proxy, Method proxyMethod, Object[] proxyArgs) -> {
                MessageBufferPacker packer = MessagePack.newDefaultBufferPacker();
                return null;
        });

    }
    */

    /**
     * Destroy the view by removing it from the widget tree.
     * @param viewId
     */
    public void destroyView(long viewId) {
        View view = mViewCache.get(viewId);
        ViewManager parent = (ViewManager) view.getParent();
        if (parent!=null) {
            parent.removeView(view);
        }
        mViewCache.remove(viewId);
    }

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
     * ("eventName",(pythonObjectId,"method", (args...)))
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
            packer.packString("viewEvent");
            packer.packArrayHeader(3);
            packer.packLong(pythonObjectId);
            packer.packString(method.getName());
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
            packer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Send events to python
        activity.sendEvent(packer);
        return null;
    }

}