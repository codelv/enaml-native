//
//  ViewController.m
//  demo
//
//  Created by jrm on 7/27/17.
//  Copyright © 2017 frmdstryr. All rights reserved.
//
#import <UIKit/UIKit.h>
#import "ViewController.h"
#import "ENBridge.h"
#import <YogaKit/UIView+Yoga.h>

@interface ViewController ()

@property ENBridge* bridge;

@end

@implementation ViewController

- (void) displayView:(UIView *)view {
    
    // Hide loading
    NSArray *viewsToRemove = [self.view subviews];
    for (UIView *v in viewsToRemove) {
        [v removeFromSuperview];
    }
    
    // Copy frame from root
    view.frame = self.view.window.frame;
    view.yoga.isEnabled = YES;
    view.yoga.width = YGPointValue(self.view.frame.size.width);
    view.yoga.height = YGPointValue(self.view.frame.size.height);
    [view.yoga applyLayoutPreservingOrigin:YES];
    
    // Add new view
    [self.view addSubview:view];
}

- (void) showError:(NSString *)message {
    NSLog(@"%@", message);
}

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    self.bridge = [ENBridge instance];
    [self.bridge setViewController:self];
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


@end
