package com.codelv.enamlnative.adapters;

import android.content.Context;
import android.os.Handler;
import android.view.MotionEvent;
import android.support.v4.view.ViewPager;

public class BridgedViewPager extends ViewPager {

    private boolean mEnabled = true;

    protected final Handler mHandler = new Handler();

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

    /**
     * Avoids "FragmenatManager is already executing transactions"
     * @param item
     */
    public void setCurrentItem(int item) {
        mHandler.post(()->{super.setCurrentItem(item);});
    }
}