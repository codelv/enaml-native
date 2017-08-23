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

- (void) displayView:(UIView *)view {
    //self.view.backgroundColor = [UIColor redColor];
    /*UILabel *fromLabel = [[UILabel alloc]initWithFrame:CGRectMake(91, 15, 200, 20)];
    fromLabel.text = @"CRAP";
    fromLabel.textColor = [UIColor blackColor];
    //fromLabel.textAlignment = NSTextAlignmentLeft;
     */
    //[self.view addSubview:[self.bridge getObject:@1]];
    //[self.view addSubview:fromLabel];
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
