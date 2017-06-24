package com.enaml;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.view.View;
import android.view.ViewManager;
import android.util.Log;

import org.msgpack.value.ArrayValue;
import org.msgpack.value.ExtensionValue;
import org.msgpack.value.FloatValue;
import org.msgpack.value.IntegerValue;
import org.msgpack.value.Value;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;


import java.util.HashMap;

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
    final HashMap<Integer,View> mViewCache = new HashMap<Integer, View>();

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
     * Create a view with the given id.
     *
     * The first call will be set as the root node.
     *
     * @param className
     * @param viewId
     */
    public void createView(String className, int viewId) {
        try {
            //Log.i(TAG,"Create "+className+" id="+viewId);
            if (!mConstructorCache.containsKey(className)) {
                Class viewClass = Class.forName(className);
                mConstructorCache.put(className, viewClass.getConstructor(Context.class));
            }
            Constructor constructor = mConstructorCache.get(className);
            View view = (View) constructor.newInstance(mContext);
            view.setId(viewId);
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
    public void updateView(int viewId, String method, Value[] args) {
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
                        methodArgs[i] = mViewCache.get(iv.toInt());
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
            } catch (Throwable throwable) {
                throwable.printStackTrace();
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

        // Invoke it
        //lambda.invoke_for_void(args[0].asStringValue());
    }

    /**
     * Destroy the view by removing it from the widget tree.
     * @param viewId
     */
    public void destroyView(int viewId) {
        View view = mViewCache.get(viewId);
        ViewManager parent = (ViewManager) view.getParent();
        if (parent!=null) {
            parent.removeView(view);
        }
        mViewCache.remove(viewId);
    }


}