### Components

Usage examples of every component should go here.  At some point editable examples should be added. 

### ActivityIndicator

Displays a circular loading indicator.


    :::python

    from enamlnative.widgets.api import *

    enamldef ContentView(LinearLayout):
      #: Normal size
      ActivityIndicator:
        pass

      #: Small
      ActivityIndicator:
        style = "small"

      #: Large
      ActivityIndicator:
        style = "large"
  
