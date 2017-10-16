package com.codelv.enamlnative.adapters;

import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.BaseAdapter;
import android.widget.ListView;

import java.util.ArrayList;

/**
 * Created by jrm on 7/11/17.
 */

public class BridgedListAdapter extends BaseAdapter {
    public static final String TAG = "BridgedListAdapter";
    int mCount;
    int mRecycleIndex = -1; // Incremented before first use
    int mVisibileCount = 0;
    ListView mListView;
    BridgedListAdapterListener mListener;
    final ArrayList<View> mRecycleViews = new ArrayList<>();

    public BridgedListAdapter() {super();}

    public void setListView(ListView listView, BridgedListAdapterListener listener) {
        mListView = listView;
        mListener = listener;
        mListView.setOnScrollListener(new AbsListView.OnScrollListener() {
            @Override
            public void onScrollStateChanged(AbsListView view, int scrollState) {
                if (mListener!=null) {
                    mListener.onScrollStateChanged(view, scrollState);
                }
            }

            @Override
            public void onScroll(AbsListView view, int firstVisibleItem, int visibleItemCount, int totalItemCount) {
                if (mListener!=null) {
                    // Notify if # of visible items changed
                    if (mVisibileCount!=visibleItemCount) {
                        mListener.onVisibleCountChanged(visibleItemCount, totalItemCount);
                    }
                    mVisibileCount = visibleItemCount;
                }
            }
        });
    }

    /**
     * Set the number of items this adapter has.
     */
    public void setCount(int count) {
        mCount = count;
    }

    @Override
    public int getCount() {
        return mCount;
    }

    /**
     * Set the views that this adapter will cycle through.
     * @param views
     */
    public void setRecycleViews(View... views) {
        for (View view: views) {
            mRecycleViews.add(view);
        }
    }

    public void addRecyleView(View view) {
        mRecycleViews.add(view);
    }

    public void removeRecycleView(View view) {
        mRecycleViews.remove(view);
    }

    public void clearRecycleViews() {
        mRecycleViews.clear();
    }

    @Override
    public Object getItem(int position) {
        return null;
    }

    @Override
    public long getItemId(int position) {
        return 0;
    }

    public View getView(int position, View convertView, ViewGroup parent) {
        mRecycleIndex = (mRecycleIndex+1)%mRecycleViews.size();
        if (mListener!=null) {
            //Log.d(TAG,"onRecycleView(index: "+mRecycleIndex+", position: "+position+")");
            mListener.onRecycleView(mRecycleIndex, position);
        }
        return mRecycleViews.get(mRecycleIndex);
    }


    interface BridgedListAdapterListener {
        void onVisibleCountChanged(int count, int total);
        void onRecycleView(int index, int position);
        void onScrollStateChanged(View view, int scrollState);
    }
}
