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
#include <Python/Python.h>


@interface ENBridge ()

    @property NSMutableDictionary* objectCache;

    @property int resultCount;
    @property NSMutableDictionary* resultCache;

    @property int eventCallsPending;
    @property NSMutableArray* eventQueue;
    @property NSOperationQueue* taskQueue;

    -(void)runUntilCurrent;
    -(void)onResult:(int)resuiltId withValue:(NSObject*) result;

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
     * Create an object over the bridge
     */
    - (void)createObject:(int)objId withType:(NSString *)className withArgs:(NSArray *)args {
        NSLog(@"Creating %@ with id %i",className,objId);
        NSObject * obj = [NSClassFromString(className) new];
        [self.objectCache setObject:obj forKey:[NSNumber numberWithInt:objId]];
    }

    /**
     * Update an object by calling a method and returning the value (if needed)
     */
    - (void)updateObject:(int)objId andReturn:(int)returnId usingMethod:(NSString *)method withArgs:(NSArray *)args {
        NSObject *obj = self.objectCache[[NSNumber numberWithInt:objId]];
        
        // Get signature
        NSMethodSignature *signature = [NSMutableArray instanceMethodSignatureForSelector:NSSelectorFromString(method)];
        
        // Get method
        NSInvocation* lambda = [NSInvocation invocationWithMethodSignature:signature];
        
        // Set target
        [lambda setTarget:obj];
        
        // Call it
        // How do i get the return value?
        [lambda invoke];
        if (returnId) {
            //[self onResult:resultId withValue:result];
        }
    }

    /**
     * Update an object by setting a property value
     */
    - (void)updateObject:(int)objId usingField:(NSString *)field withValue:(NSObject *)value {
    
    }

    /**
     * Remove an object from the cache so it can be deallocated
     */
    - (void)deleteObject:(int)objId {
        [self.objectCache removeObjectForKey:[NSNumber numberWithInt:objId]];
    }

    - (void)setResult:(int)objId withValue:(NSObject *)result {
        //[self.resultCache s]
    }

    - (void)onResult:(int)resultId withValue:(NSObject*) result {
    
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
        NSData* data = [NSData dataWithBytesNoCopy:(const void *)bytes
                               length:len freeWhenDone:NO];
        
        // Parse it
        NSError* error;
        NSArray* events = [MPMessagePackReader readData:data error:&error];
        
        // Houston we have Data
        //NSLog(@"%@",events);
        for (NSArray* event in events) {
            NSLog(@"Event %@",event);
            // Pull cmd and args
            NSString* cmd = event[0];
            NSArray* args = event[1];
            
            if ([cmd isEqualToString:CREATE]) {
                [self createObject: (int) args[0]
                      withType: (NSString*) args[1]
                          withArgs: [args subarrayWithRange:(NSRange) {[args count]-2,2}]];
                
            } else if ([cmd isEqualToString:METHOD]) {
                [self updateObject: (int) args[0]
                      andReturn: (int) args[1]
                      usingMethod: (NSString*) args[2]
                      withArgs: [args subarrayWithRange:(NSRange){[args count]-3,3}]];
                
            } else if ([cmd isEqualToString:FIELD]) {
                [self updateObject: (int) args[0]
                      usingField: (NSString*) args[1]
                      withValue: args[2]];
                
            } else if ([cmd isEqualToString:DELETE]) {
                [self deleteObject: (int) args[0]];
                
            } else if ([cmd isEqualToString:RESULT]) {
                [self setResult: (int) args[0]
                      withValue: args[2]];
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
