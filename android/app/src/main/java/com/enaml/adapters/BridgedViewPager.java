package com.enaml.adapters;

import android.content.Context;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.support.v4.view.ViewPager;

public class BridgedViewPager extends ViewPager {

    private boolean mEnabled = true;

    public BridgedViewPager(Context context) {
        super(context);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (this.mEnabled) {
            return super.onTouchEvent(event);
        }

        return false;
    }

    @Override
    public boolean onInterceptTouchEvent(MotionEvent event) {
        if (this.mEnabled) {
            return super.onInterceptTouchEvent(event);
        }

        return false;
    }

    public void setPagingEnabled(boolean enabled) {
        mEnabled = enabled;
    }
}