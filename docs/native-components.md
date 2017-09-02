### Native Components

This is a short introduction into how enaml-native takes the components you define in your view code to the native widget that actually draws on the screen on Android or iOS. After reading this you should be able to add your own "native components" that can be used within your enaml-native views.

All components in enaml-native boil down to a single or collection of actual native widgets. What we are actually using in enaml-native is a proxy to a native widget (well a proxy to a proxy to be exact). Our enaml code is "Declarative" meaning we are just describing explicitly how the components should be created, organized, and interact with eachother. The actual implementation is abstracted out leaving it to be done however necessary.  

Enaml requires two parts in order to use a widget:

1. A component (or widget) declaration
2. A component (or proxy) implementation

#### Declaration

TODO


#### Implementation

TODO:



See the [enaml introduction](http://nucleic.github.io/enaml/docs/get_started/introduction.html) for a more detailed explaination of enaml.



### Adding your own Components

TODO
