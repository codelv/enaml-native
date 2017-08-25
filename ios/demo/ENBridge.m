//
//  ENBridge.m
//  Enaml native bridge implementation
//
//  Created by jrm on 7/14/17.
//  Copyright © 2017 frmdstryr. All rights reserved.
//

#import "ENBridge.h"
#import <Foundation/Foundation.h>
#import <MPMessagePack/MPMessagePack.h>
#import <UIKit/UIKit.h>
#include <Python/Python.h>
#import "UIColor+HexString.h"


@interface ENBridge ()

    @property AppDelegate* appDelegate;
    @property ViewController* viewController;

    @property NSMutableDictionary* objectCache;

    @property int resultCount;
    @property NSMutableDictionary* resultCache;

    @property int eventCallsPending;
    @property NSMutableArray* eventQueue;
    @property NSOperationQueue* taskQueue;

    -(void)runUntilCurrent;
    -(void)onResult:(NSNumber *)resuiltId withValue:(NSObject*) result;
    -(id)convertArg:(NSArray *)spec;

    + (UIColor *) colorWithHexString: (NSString *) hexString;

@end

@implementation ENBridge

    // Bridge commands
    static NSString* CREATE = @"c";
    static NSString* METHOD = @"m";
    static NSString* FIELD  = @"f";
    static NSString* DELETE = @"d";
    static NSString* RESULT = @"r";
    static NSString* ERROR  = @"e";

    static ENBridge *_instance;

    /**
     * Bridge is a singleton
     */
    + (void)initialize {
        static BOOL initialized = NO;
        if(!initialized) {
            initialized = YES;
            _instance = [[ENBridge alloc] init];
        }
    }
    /**
     * Use to retrive the single instance. Python uses this.
     */
    + (ENBridge *)instance {
        return _instance;
    }

    /**
     * Create initial variables
     */
    - (instancetype)init {
        self = [super init];
        if (self) {
            // Initialize self
            self.objectCache = [NSMutableDictionary new];
            self.resultCount = 0;
            self.resultCache = [NSMutableDictionary new];
            self.eventCallsPending = 0;
            self.eventQueue = [NSMutableArray new];
            self.taskQueue = [NSOperationQueue new];
        }
        return self;
    }



    /**
     * Set app delegate and store it in the cache with id = -1
     */
    -(void)setAppDelegate:(AppDelegate *)delegate {
        _appDelegate = delegate;
        [self.objectCache setObject:delegate forKey:@(-1)];
    }

    /**
     * Set view controller and store it in the cache with id = -2
     */
    -(void)setViewController:(ViewController *) controller {
        _viewController = controller;
        [self.objectCache setObject:controller forKey:@(-2)];
        [self.objectCache setObject:controller.view forKey:@(-3)];
    }

    -(id) getObject:(NSNumber *) objId{
        return self.objectCache[objId];
    }

    /**
     * Convert msgpack arg to correct format based on arg tuple from python
     */
    -(id)convertArg:(NSArray *)spec {
        NSString* argType = spec[0];
        
        // If a string is passed for a UIColor argument, convert it
        if ([argType isEqualToString:@"UIColor"] && [spec[1] isKindOfClass:[NSString class]]) {
            return [UIColor colorWithHexString: (NSString *) spec[1]];
        } else if ([argType isEqualToString:@"CGRect"] && [spec[1] isKindOfClass:[NSArray class]]) {
            return [NSValue valueWithCGRect:CGRectMake([(NSNumber *)spec[1][0] floatValue],
                              [(NSNumber *)spec[1][1] floatValue],
                              [(NSNumber *)spec[1][2] floatValue],
                              [(NSNumber *)spec[1][3] floatValue])];
        } else if ([argType isEqualToString:@"CGSize"] && [spec[1] isKindOfClass:[NSArray class]]) {
            return [NSValue valueWithCGSize:CGSizeMake([(NSNumber *)spec[1][0] floatValue],
                                                       [(NSNumber *)spec[1][1] floatValue])];
        // Extensions are passed as dictionaries
        } else if ([spec[1] isKindOfClass:[NSDictionary class]]) {
            NSDictionary* arg = spec[1];
            NSData* data = arg[@"data"];
            const int* refNumber = data.bytes;
            NSNumber* objId = [NSNumber numberWithInt:*refNumber];
            return self.objectCache[objId];
        }
        return spec[1];
    }

    /**
     * Create an object over the bridge
     */
    - (void)createObject:(NSNumber *)objId withType:(NSString *)className withArgs:(NSArray *)args {
        NSLog(@"Creating %@ with id %@",className,objId);
        NSObject * obj = [[NSClassFromString(className) alloc] init];//initWithFrame:CGRectMake(0, 0, 100, 100)];
        [self.objectCache setObject:obj forKey:objId];
    }

    /**
     * Update an object by calling a method and returning the value (if needed).
     * 
     * Parameters
     * ----------------
     *  objId: reference id to use as key in the cache
     *  returnId: id of python object to return the result to
     *  method: method to invoke
     *  args: list of tuples containing the type and value
     *
     */
    - (void)updateObject:(NSNumber *)objId andReturn:(NSNumber *)returnId usingMethod:(NSString *)method withArgs:(NSArray *)args {
        NSLog(@"Updating id=%@ using method %@ with args %@",objId,method,args);
        
        // Get the object from the cache
        NSObject *obj = self.objectCache[objId];
        
        if (!obj) {
            NSLog(@"Warning: Null object when referencing id=%@", objId);
            return;
        }
        
        SEL selector = NSSelectorFromString(method);
        
        // Get signature
        NSMethodSignature *signature = [[obj class] instanceMethodSignatureForSelector:selector];
        if (!signature) {
            NSLog(@"Null signature for %@",method);
        }
        
        // Get method
        NSInvocation* lambda = [NSInvocation invocationWithMethodSignature:signature];
        
        // Set target
        [lambda setTarget:obj];
        [lambda setSelector:selector];
        
        // Set args
        int i = 2;
        for (NSArray* arg in args) {
            NSObject* val = [self convertArg:arg];
            [lambda setArgument:&val atIndex:i];
            i++;
        }
        
        // Call it
        [lambda invoke];
        
        if (returnId.intValue) {
            //[self onResult:resultId withValue:result];
            NSObject* result;
            [lambda getReturnValue: &result];
            [self onResult:returnId withValue:result];
        }
    }

    /**
     * Update an object by setting a property value
     */
    - (void)updateObject:(NSNumber *)objId usingField:(NSString *)field withValue:(NSObject *)value {
        
        NSLog(@"Setting id=%@ using field %@ with args %@",objId,field,value);
        
        // Get the object from the cache
        NSObject *obj = self.objectCache[objId];
        
        if (!obj) {
            NSLog(@"Warning: Null object when referencing id=%@", objId);
            return;
        }
        
        // Parse arg
        NSObject* val = [self convertArg:value];
        [obj setValue:val forKey:field];

    }

    /**
     * Remove an object from the cache so it can be deallocated
     */
    - (void)deleteObject:(NSNumber *)objId {
        [self.objectCache removeObjectForKey:objId];
    }

    - (void)setResult:(NSNumber *)objId withValue:(NSObject *)result {
        //[self.resultCache s]
    }

    - (void)onResult:(NSNumber *)resultId withValue:(NSObject*) result {
    
    }

    - (void)sendEvent:(NSDictionary *)event {
        self.eventCallsPending += 1;
        [self.eventQueue addObject:event];
        
        // In 3ms dispatch
        dispatch_time_t delay = dispatch_time(DISPATCH_TIME_NOW, NSEC_PER_MSEC*3.0);
        dispatch_after(delay, dispatch_get_main_queue(), ^{
            self.eventCallsPending -= 1;
            if (self.eventCallsPending==0) {
                NSError *error = nil;
                NSData *data = [MPMessagePackWriter writeObject:self.eventQueue error:&error];
                [self sendEventsToPython: data];
            }
        });
    }

    /**
     * Called from python thread. Sends encoded msgpack data.
     */
    - (void)processEvents:(char *)bytes length:(int)len {
        // Read data
        NSData* data = [NSData dataWithBytesNoCopy:(void *)bytes
                               length:len freeWhenDone:NO];
        
        // Parse it
        NSError* error;
        NSArray* events = [MPMessagePackReader readData:data error:&error];
        
        if (error) {
            [self.viewController showError:error];
        }
        // Houston we have Data
        //NSLog(@"%@",events);
        for (NSArray* event in events) {
            //NSLog(@"Event %@",event);
            // Pull cmd and args
            NSString* cmd = event[0];
            NSArray* args = event[1];
            
            if ([cmd isEqualToString:CREATE]) {
                // Run on UI thread
                [[NSOperationQueue mainQueue] addOperationWithBlock:^{
                    [self createObject: (NSNumber *) args[0]
                              withType: (NSString*) args[1]
                              withArgs: [args subarrayWithRange:(NSRange) {[args count]-2,2}]];

                }];
                
            } else if ([cmd isEqualToString:METHOD]) {
                [[NSOperationQueue mainQueue] addOperationWithBlock:^{

                    [self updateObject:  (NSNumber *)args[0]
                      andReturn: (NSNumber *) args[1]
                      usingMethod: (NSString*) args[2]
                      withArgs: args[3]];
                    
                }];
                
            } else if ([cmd isEqualToString:FIELD]) {
                
                [[NSOperationQueue mainQueue] addOperationWithBlock:^{

                    [self updateObject: (NSNumber *) args[0]
                      usingField: (NSString*) args[1]
                      withValue: args[2][0]];
                    
                }];
                
            } else if ([cmd isEqualToString:DELETE]) {
                [[NSOperationQueue mainQueue] addOperationWithBlock:^{

                    [self deleteObject: (NSNumber *) args[0]];
                }];
                
            } else if ([cmd isEqualToString:RESULT]) {
                
                [[NSOperationQueue mainQueue] addOperationWithBlock:^{

                    [self setResult: (NSNumber *) args[0]
                      withValue: args[2]];
                }];
            } else if ([cmd isEqualToString:ERROR]) {
                // TODO...
                NSLog(@"%@", args);
            }
        }
    }

    /**
     * Run all pending tasks
     */
    -(void)runUntilCurrent {
        //for (NSOperation task in self.taskQueue) {
        //    task();
        //}
        //[self.taskQueue clear];
    }

    /**
     * Send data to python using the Python C-API. This will
     * retreive an instance of IPhoneApplication and invoke `onEvents`
     * with the data.
     */
    -(void)sendEventsToPython:(NSData *)data {
        // Import the module
        PyObject* module = PyImport_ImportModule("enamlnative.ios.app");
        
        // Get the class
        PyObject* IPhoneApplication = PyObject_GetAttrString(module, "IPhoneApplication");
        
        //PyObject* instance = PyObject_GetAttrString(IPhoneApplication, "instance");
        
        // Invoke it
        PyObject* app = PyObject_CallMethod(IPhoneApplication, "instance", "");
        
        if (app) {
            // Send msgpack data
            PyObject_CallMethod(app, "on_events", "s", data.bytes);
        }
        
        // Cleanup
        Py_XDECREF(module);
        Py_XDECREF(IPhoneApplication);
        //Py_XDECREF(instance);
        Py_XDECREF(app);
    }


@end
