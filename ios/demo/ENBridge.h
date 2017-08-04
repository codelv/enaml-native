//
//  ENBridge.h
//  Enaml native bridge.
//
//  Created by jrm on 7/14/17.
//  Copyright © 2017 frmdstryr. All rights reserved.
//
#import "AppDelegate.h"
#import "ViewController.h"
#import <Foundation/Foundation.h>

#ifndef ENBridge_h
#define ENBridge_h

@interface ENBridge : NSObject

@property AppDelegate* appDelegate;
@property ViewController* viewController;

+ (ENBridge *)instance;
- (void)createObject:(int)objId withType:(NSString *) className withArgs:(NSArray *) args;
- (void)updateObject:(int)objId andReturn:(int)returnId usingMethod:(NSString *) method withArgs:(NSArray *) args;
- (void)updateObject:(int)objId usingField: (NSString *) field withValue: (NSObject *) value;
- (void)deleteObject:(int)objId;

- (void)setResult:(int)objId withValue:(NSObject *) result;

- (void)sendEvent:(NSDictionary *) event;
- (void)processEvents:(char *) data length:(int) len;

- (void)sendEventsToPython:(NSData *) data;


@end

#endif /* Bridge_h */
