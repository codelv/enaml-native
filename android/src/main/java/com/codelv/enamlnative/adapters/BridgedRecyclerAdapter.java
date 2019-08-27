package com.codelv.enamlnative.adapters;

import androidx.recyclerview.widget.RecyclerView;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;

import java.util.ArrayList;

/**
 * Created by jrm on 5/3/18.
 */
public class BridgedRecyclerAdapter extends RecyclerView.Adapter<BridgedRecyclerAdapter.ViewHolder> {
    public static final String TAG = "BridgedRecyclerAdapter";
    int mCount;
    int mRecycleIndex = -1; // Incremented before first use
    RecyclerView mListView;
    BridgedListAdapterListener mListener;
    final ArrayList<View> mRecycleViews = new ArrayList<>();

    // Provide a reference to the views for each data item
    // Complex data items may need more than one view per item, and
    // you provide access to all the views for a data item in a view holder
    public static class ViewHolder extends RecyclerView.ViewHolder {
        // each data item is just a string in this case
        public View mView;
        public int mIndex;
        public ViewHolder(View v, int i) {
            super(v);
            mView = v;
            mIndex = i;
        }
    }

    public BridgedRecyclerAdapter(RecyclerView listView) {
        super();
        mListView = listView;
    }

    // Create new views (invoked by the layout manager)
    @Override
    public BridgedRecyclerAdapter.ViewHolder onCreateViewHolder(ViewGroup parent,
                                                                int viewType) {
        // create a new view
        mRecycleIndex += 1;
        if (mRecycleIndex==mRecycleViews.size()) {
            mRecycleIndex = 0;
        }
        View v = mRecycleViews.get(mRecycleIndex);
        ViewGroup vp = (ViewGroup) v.getParent();
        if (vp!=null) {
            vp.removeView(v);
        }
        FrameLayout frame = new FrameLayout(parent.getContext());
        frame.addView(v);
        return new ViewHolder(frame, mRecycleIndex);
    }


    // Replace the contents of a view (invoked by the layout manager)
    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
        mListener.onRecycleView(holder.mIndex, position);
    }

    public void setRecyleListener(BridgedListAdapterListener listener) {
        mListener = listener;
//        mListView.addOnScrollListener(new AbsListView.OnScrollListener() {
//            @Override
//            public void onScrollStateChanged(AbsListView view, int scrollState) {
//                if (mListener!=null) {
//                    mListener.onScrollStateChanged(view, scrollState);
//                }
//            }
//
//            @Override
//            public void onScroll(AbsListView view, int firstVisibleItem, int visibleItemCount, int totalItemCount) {
//                if (mListener!=null) {
//                    // Notify if # of visible items changed
//                    if (mVisibileCount!=visibleItemCount) {
//                        mListener.onVisibleCountChanged(visibleItemCount, totalItemCount);
//                    }
//                    mVisibileCount = visibleItemCount;
//                }
//            }
//        });
    }

    /**
     * Set the number of items this adapter has.
     */
    public void setItemCount(int count) {
        mCount = count;
    }

    @Override
    public int getItemCount() {
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


    interface BridgedListAdapterListener {
        void onRecycleView(int index, int position);
    }
}
