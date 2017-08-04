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

@interface ViewController ()

@property ENBridge* bridge;

@end

@implementation ViewController

- (void) showView:(UIView *)view {
    [self.view]
}

- (void) showError:(NSString *)message {
    NSLog(@"%@", message);
}

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    self.bridge = [ENBridge instance];
    self.bridge.viewController = self;
    
    UIButton *button = [UIButton buttonWithType:UIButtonTypeCustom];
    button.backgroundColor = [UIColor blueColor];
    [button setTitle:@"Show View" forState:UIControlStateNormal];
    button.frame = CGRectMake(80.0, 210.0, 160.0, 40.0);
    [self.view addSubview:button];
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


@end
