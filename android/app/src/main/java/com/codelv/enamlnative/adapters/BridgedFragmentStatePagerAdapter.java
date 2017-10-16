package com.codelv.enamlnative.adapters;

import android.os.Bundle;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentStatePagerAdapter;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import com.codelv.enamlnative.EnamlActivity;

import java.util.ArrayList;

/**
 * A fragment state adapter that takes a list of fragments with unpopulated views and
 * dispatches an event to request the view when it is shown (or next to a shown view).
 *
 * Created by jrm on 6/30/17.
 */
public class BridgedFragmentStatePagerAdapter extends FragmentStatePagerAdapter {
    public final String TAG = "PagerAdapter";

    protected final ArrayList<Fragment> mFragments = new ArrayList<>();
    protected final Handler mHandler = new Handler();

    public BridgedFragmentStatePagerAdapter() {
        this(EnamlActivity.mActivity.getSupportFragmentManager());
    }

    public BridgedFragmentStatePagerAdapter(FragmentManager fm) {
        super(fm);
    }

    public void addFragment(Fragment fragment) {
        mFragments.add(fragment);
        //notifyDataSetChanged();
    }

    public void removeFragment(Fragment fragment) {
        mFragments.remove(fragment);
        //notifyDataSetChanged();
    }

    /**
     * A safe notify

    @Override
    public void notifyDataSetChanged() {
        try{
            super.notifyDataSetChanged();
        } catch (IllegalStateException e) {
            // Try again later
            mHandler.post(()->{
               notifyDataSetChanged();
            });
        }
    }
     */

    @Override
    public int getCount() {
        return mFragments.size();
    }

    @Override
    public Fragment getItem(int position) {
        // So how does it know that this item is different?
        //Log.d(TAG,"getItem("+position+")");
        return mFragments.get(position);
    }

    @Override
    public String getPageTitle(int position) {
        return ((BridgedFragment) mFragments.get(position)).getTitle();
    }

    @Override
    public int getItemPosition(Object item) {
        BridgedFragment fragment = (BridgedFragment)item;
        int position = mFragments.indexOf(fragment);
        //Log.d(TAG,"getItemPosition("+fragment+") is "+position);
        if (position >= 0) {
            return position;
        } else {
            return POSITION_NONE;
        }
    }


    interface FragmentListener {
        View onCreateView();
        void onDestroyView();
    }

    public static class BridgedFragment extends Fragment {
        //public static final String VIEW_ID = "viewId";
        //protected final Bridge mBridge;
        protected int mId = 0;
        protected String mTitle = "";
        protected FragmentListener mListener = null;

        public BridgedFragment() {}

        public void setFragmentListener(FragmentListener listener) {
            mListener = listener;
        }

        public void setTitle(String title) { mTitle = title; }
        public String getTitle() { return mTitle; }

        @Override
        public View onCreateView(LayoutInflater inflater,
                                 ViewGroup container, Bundle savedInstanceState) {
            //int viewId = savedInstanceState.getInt(BridgedFragment.VIEW_ID);
            if (mListener != null) {
                View view =  mListener.onCreateView();
                return view;
            }
            return null;
            //return mBridge.getView(viewId);
        }

        @Override
        public void onDestroyView() {
            super.onDestroyView();
            if (mListener != null) {
                mListener.onDestroyView();
            }
        }

    }
}
