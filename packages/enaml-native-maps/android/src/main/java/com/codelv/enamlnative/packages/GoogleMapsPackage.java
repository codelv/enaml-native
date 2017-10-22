package com.codelv.enamlnative.packages;

import com.codelv.enamlnative.EnamlActivity;
import com.codelv.enamlnative.EnamlPackage;
import com.codelv.enamlnative.Bridge;
import com.google.android.gms.maps.model.CameraPosition;
import com.google.android.gms.maps.model.Circle;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.Polygon;
import com.google.android.gms.maps.model.Polyline;

/**
 * Created by jrm on 10/15/17.
 */

public class GoogleMapsPackage implements EnamlPackage {

    EnamlActivity mActivity;

    @Override
    public void onCreate(EnamlActivity activity) {
        mActivity = activity;
    }

    /**
     * Add special bridge packers required by map components
     */
    @Override
    public void onStart() {
        Bridge bridge = mActivity.getBridge();

        bridge.addPacker(LatLng.class,(packer, id, object)->{
            LatLng pos = (LatLng) object;
            packer.packArrayHeader(2);
            // Pack a tuple of (lat,lng)
            packer.packDouble(pos.latitude);
            packer.packDouble(pos.longitude);
        });

        bridge.addPacker(Marker.class,(packer, id, object)->{
            Marker marker = (Marker) object;
            packer.packArrayHeader(2);
            // Pack a tuple of (id, (lat,lng))
            try {
                packer.packInt((int) marker.getTag());
            } catch (Exception e) {
                packer.packInt(id); // Required for factory return values
            }
            packer.packArrayHeader(2);
            LatLng pos = marker.getPosition();
            packer.packDouble(pos.latitude);
            packer.packDouble(pos.longitude);
        });

        bridge.addPacker(new Class[]{Circle.class, Polygon.class, Polyline.class},(packer, id, object)-> {
            Class type = object.getClass();
            int objId = id;

            try {
                if (type == Circle.class) {
                    objId = (int) ((Circle) object).getTag();
                } else if (type == Polygon.class) {
                    objId = (int) ((Polygon) object).getTag();
                } else if (type == Polyline.class) {
                    objId = (int) ((Polyline) object).getTag();
                }
                packer.packInt(objId);
            } catch (Exception e) {
                packer.packInt(id); // Required for factory return values
            }
        });

        bridge.addPacker(CameraPosition.class,(packer, id, object)->{
            CameraPosition cameraPosition = (CameraPosition) object;
            packer.packArrayHeader(4);
            // Pack a tuple of ((lat,lng), zoom, tilt, bearing)
            packer.packArrayHeader(2);
            LatLng pos = cameraPosition.target;
            packer.packDouble(pos.latitude);
            packer.packDouble(pos.longitude);
            packer.packFloat(cameraPosition.zoom);
            packer.packFloat(cameraPosition.tilt);
            packer.packFloat(cameraPosition.bearing);
        });
    }

    @Override
    public void onResume() {

    }

    @Override
    public void onPause() {

    }

    @Override
    public void onStop() {

    }

    @Override
    public void onDestroy() {

    }
}
