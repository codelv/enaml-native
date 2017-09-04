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


+ (ENBridge *)instance;

- (void) setAppDelegate:(AppDelegate *) delegate;
- (void) setViewController:(ViewController *) controller;

- (id) getObject:(NSNumber *) objId;
- (void) createObject:(NSNumber *)objId withType:(NSString *) className usingConstructor:(NSString*) constructor withArgs:(NSArray *) args;
- (void) updateObject:(NSNumber *)objId andReturn:(NSNumber *)returnId usingMethod:(NSString *) method withArgs:(NSArray *) args;
- (void) updateObject:(NSNumber *)objId usingField: (NSString *) field withValue: (NSObject *) value;
- (void) deleteObject:(NSNumber *)objId;

- (void) setResult:(NSNumber *)objId withValue:(NSObject *) result;

- (void) sendEvent:(NSDictionary *) event;
- (void) processEvents:(char *) data length:(int) len;

- (void) sendEventsToPython:(NSData *) data;

- (void) addTarget:(UIControl *)control forControlEvents:(UIControlEvents) controlEvents
         andCallback:(NSNumber*) pythonId usingMethod:(NSString*)method withValues:(NSArray*) keys;

@end

#endif /* Bridge_h */
