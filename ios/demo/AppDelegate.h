//
//  AppDelegate.h
//  Demo2
//
//  Created by jrm on 7/14/17.
//  Copyright © 2017 frmdstryr. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface AppDelegate : UIResponder <UIApplicationDelegate>

@property (strong, nonatomic) UIWindow *window;

-(int)startPython:(UIApplication *)application;
-(void)stopPython:(UIApplication *)application;

@end

