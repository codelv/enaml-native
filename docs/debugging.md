
Currently there is no `live` debugger where you can breakpoint and step through code like in react-native. There are a few helpful things you can do to make life easier though.

### Development server

With the development server you can save changes to your source code and it will reload it on the fly. You can use this to print out whatever you need to see. To enable this:

1. set `app.dev="<dev server ip>"`
2. set `app.reload_view` to a function reloads your modules and sets the `app.view`
3. finally start the dev server by running  `./enaml-native start` in your project folder.

You will see:

    
    $ ./enaml-native start
    Entering into src
    Watching /home/jrm/Workspace/Apps/TestBible/src
    Tornado Dev server started on 8888
    Client connected!



and in the device log


    07-22 12:22:39.542 /app I/pybridge: Dev server connecting ws://192.168.34.103:8888/dev...
    07-22 12:22:39.687 /app I/pybridge: Dev server connected

A youtube video of reloading is here:

[Live Reloading](https://youtu.be/CbxVc_vNiNk)


### Debugging the bridge 

One of the great things about using the bridge is being able to get a complete trace of everything that was happening.  To enable this set `app.debug = True` and rebuild the app. It will generate a nice trace of all bridge methods and callbacks. 



    07-22 12:01:55.014 /app I/pybridge: ======== Py <-- Native ======
    07-22 12:01:55.015 /app I/pybridge: ['event', [0, 111, 'onPageScrollStateChanged', [['java.lang.Integer', 2]]]]
    07-22 12:01:55.015 /app I/pybridge: ['event', [0, 111, 'onPageSelected', [['java.lang.Integer', 0]]]]
    07-22 12:01:55.015 /app I/pybridge: ['event', [0, 114, 'onTabUnselected', [['android.support.design.widget.TabLayout.Tab', 'android.support.design.widget.TabLayout$Tab@6c6e5d4']]]]
    07-22 12:01:55.015 /app I/pybridge: ['event', [45, 804, 'onCreateView', []]]
    07-22 12:01:55.015 /app I/pybridge: ===========================
    07-22 12:01:55.046 /app I/pybridge: ======== Py --> Native ======
    07-22 12:01:55.047 /app I/pybridge: ('c', (838, u'android.widget.ScrollView', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-22 12:01:55.047 /app I/pybridge: ('c', (839, u'android.widget.LinearLayout', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-22 12:01:55.047 /app I/pybridge: ('m', (839, 0, 'setOrientation', [('int', 1)]))
    07-22 12:01:55.048 /app I/pybridge: ('c', (840, u'android.support.v7.widget.CardView', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-22 12:01:55.048 /app I/pybridge: ('m', (840, 0, 'setPadding', [('int', 60), ('int', 60), ('int', 60), ('int', 60)]))
    07-22 12:01:55.048 /app I/pybridge: ('c', (841, u'android.view.ViewGroup$MarginLayoutParams', [('int', -1), ('int', -1)]))
    07-22 12:01:55.048 /app I/pybridge: ('m', (840, 0, 'setLayoutParams', [('android.view.ViewGroup$LayoutParams', ExtType(code=1, data='\xcd\x03I'))]))
    07-22 12:01:55.049 /app I/pybridge: ('m', (841, 0, 'setMargins', [('int', 30), ('int', 30), ('int', 30), ('int', 30)]))
    07-22 12:01:55.049 /app I/pybridge: ('m', (840, 0, 'setContentPadding', [('int', 30), ('int', 30), ('int', 30), ('int', 30)]))
    07-22 12:01:55.049 /app I/pybridge: ('c', (842, u'android.widget.LinearLayout', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-22 12:01:55.049 /app I/pybridge: ('m', (842, 0, 'setOrientation', [('int', 1)]))
    07-22 12:01:55.049 /app I/pybridge: ('c', (843, u'android.widget.TextView', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-22 12:01:55.049 /app I/pybridge: ('m', (843, 0, 'setTextKeepState', [('java.lang.CharSequence', u'Chapter - 1')]))
    07-22 12:01:55.049 /app I/pybridge: ('m', (843, 0, 'setTypeface', [('android.graphics.Typeface', u'sans-serif-condensed-light'), ('int', 0)]))
    07-22 12:01:55.049 /app I/pybridge: ('m', (843, 0, 'setTextSize', [('float', 18.0)]))
    07-22 12:01:55.050 /app I/pybridge: ('c', (844, u'android.widget.TextView', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-22 12:01:55.050 /app I/pybridge: ('m', (844, 0, 'setTextKeepState', [('java.lang.CharSequence', u"1. These are the words which Moses said to all Israel on the far side of Jordan, in the waste land in the Arabah opposite Suph, between Paran on the one side, and Tophel, Laban, Hazeroth, and Dizahab on the other.   2. It is eleven days' journey from Horeb by the way of Mount Seir to Kadesh-barnea.   3. Now in the fortieth year, on the first day of the eleventh month, Moses gave to the children of Israel all the orders which the Lord had given him for them;   4. After he had overcome Sihon, king of the Amorites, ruling in Heshbon, and Og, king of Bashan, ruling in Ashtaroth, at Edrei:   5. On the far side of Jordan in the land of Moab, Moses gave the people this law, saying,   6. The Lord our God said to us in Horeb, You have been long enough in this mountain:   7. Make a move now, and go on your way into the hill-country of the Amorites and the places near it, in the Arabah and the hill-country and in the lowlands and in the South and by the seaside, all the land of the Canaanites, and Lebanon, as far as the great river, the river Euphrates.   8. See, all the land is before you: go in and take for yourselves the land which the Lord gave by an oath to your fathers, Abraham, Isaac, and Jacob, and to their seed after them.   9. At that time I said to you, I am not able to undertake the care of you by myself;   10. The Lord your God has given you increase, and now you are like the stars of heaven in number.   11. May the Lord, the God of your fathers, make you a thousand times greater in number than you are, and give you his blessing as he has said!   12. How is it possible for me by myself to be responsible for you, and undertake the weight of all your troubles and your arguments?   13. Take for yourselves men who are wise, far-seeing, and respected among you, from your tribes, and I will make them rulers over you.   14. And you made answer and said to me, It is good for us to do as you say.   15. So I took the heads of your tribes, wise men and respected, and made them rulers over you, captains of thousands and captains of hundreds and captains of fifties and captains of tens, and overseers of your tribes.   16. And at that time I gave orders to your judges, saying, Let all questions between your brothers come before you for hearing, and give decisions uprightly between a man and his brother or one from another nation who is with him.   17. In judging, do not let a man's position have any weight with you; give hearing equally to small and great; have no fear of any man, for it is God who is judge: and any cause in which you are not able to give a decision, you are to put before me and I will give it a hearing.   18. And at that time I gave you all the orders which you were to do.   19. Then we went on from Horeb, through all that great and cruel waste which you saw, on our way to the hill-country of the Amorites, as the Lord gave us orders; and we came to Kadesh-barnea.   20. And I said to you, You have come to the hill-country of the Amorites, which the Lord our God is giving us.   21. See now, the Lord your God has put the land into your hands: go up and take it, as the Lord, the God of your fathers, has said to you; have no fear and do not be troubled.   22. And you came near to me, every one of you, and said, Let us send men before us to go through the land with care and give us an account of the way we are to go and the towns to which we will come.   23. And what you said seemed good to me, and I took twelve men from among you, one from every tribe;   24. And they went up into the hill-country and came to the valley of Eshcol, and saw what was there.   25. And taking in their hands some of the fruit of the land, they came down again to us, and gave us their account, saying, It is a good land which the Lord our God is giving us.   26. But going against the order of the Lord your God, you would not go up:   27. And you made an angry outcry in your tents, and said, In his hate for us the Lord has taken us out of the l
    07-22 12:01:55.050 /app I/pybridge: ('m', (844, 0, 'setTypeface', [('android.graphics.Typeface', u''), ('int', 0)]))
    07-22 12:01:55.050 /app I/pybridge: ('m', (844, 0, 'setTextSize', [('float', 14.0)]))
    07-22 12:01:55.051 /app I/pybridge: ('m', (844, 0, 'setLineSpacing', [('float', 0), ('float', 2)]))
    07-22 12:01:55.051 /app I/pybridge: ('m', (842, 0, 'addView', [('android.view.View', ExtType(code=1, data='\xcd\x03K')), ('int', 0)]))
    07-22 12:01:55.051 /app I/pybridge: ('m', (842, 0, 'addView', [('android.view.View', ExtType(code=1, data='\xcd\x03L')), ('int', 1)]))
    07-22 12:01:55.051 /app I/pybridge: ('m', (840, 0, 'addView', [('android.view.View', ExtType(code=1, data='\xcd\x03J')), ('int', 0)]))
    07-22 12:01:55.051 /app I/pybridge: ('m', (839, 0, 'addView', [('android.view.View', ExtType(code=1, data='\xcd\x03H')), ('int', 0)]))
    07-22 12:01:55.051 /app I/pybridge: ('m', (838, 0, 'addView', [('android.view.View', ExtType(code=1, data='\xcd\x03G')), ('int', 0)]))
    07-22 12:01:55.051 /app I/pybridge: ('r', (45, ('android.view.View', ExtType(code=1, data='\xcd\x03F'))))
    07-22 12:01:55.051 /app I/pybridge: ===========================
    07-22 12:01:55.087 /app I/pybridge: ======== Py <-- Native ======
    07-22 12:01:55.087 /app I/pybridge: ['event', [46, 805, 'onCreateView', []]]
    07-22 12:01:55.087 /app I/pybridge: ===========================

