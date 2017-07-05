package com.enaml.adapters;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentStatePagerAdapter;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import com.enaml.MainActivity;

import java.util.ArrayList;

/**
 * A
 *
 * Created by jrm on 6/30/17.
 */
public class BridgedFragmentStatePagerAdapter extends FragmentStatePagerAdapter {

    protected final ArrayList<Fragment> mFragments = new ArrayList<>();

    public BridgedFragmentStatePagerAdapter() {
        this(MainActivity.mActivity.getSupportFragmentManager());
    }

    public BridgedFragmentStatePagerAdapter(FragmentManager fm) {
        super(fm);
    }

    public void addFragment(Fragment fragment) {
        mFragments.add(fragment);
        notifyDataSetChanged();
    }

    public void removeFragment(Fragment fragment) {
        mFragments.remove(fragment);
        notifyDataSetChanged();
    }

    @Override
    public int getCount() {
        return mFragments.size();
    }

    @Override
    public Fragment getItem(int position) {
        return mFragments.get(position);
    }

    interface FragmentListener {
        View onCreateView();
        void onDestroyView();
    }

    public static class BridgedFragment extends Fragment {
        //public static final String VIEW_ID = "viewId";
        //protected final Bridge mBridge;
        protected FragmentListener mListener = null;

        public BridgedFragment() {}

        public void setFragmentListener(FragmentListener listener) {
            mListener = listener;
        }

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
