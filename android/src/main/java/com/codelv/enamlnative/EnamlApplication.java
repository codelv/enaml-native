package com.codelv.enamlnative;

import java.util.List;

/**
 * Created by jrm on 10/15/17.
 */

public interface EnamlApplication {

    /**
     * Packages installed
     * @return
     */
    List<EnamlPackage> getPackages();

    boolean showDebugMessages();

}
