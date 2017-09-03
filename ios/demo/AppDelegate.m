//
//  AppDelegate.m
//  Demo2
//
//  Created by jrm on 7/14/17.
//  Copyright © 2017 frmdstryr. All rights reserved.
//

#import "AppDelegate.h"
#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>
#include <Python/Python.h>
#include <dlfcn.h>
#include "ENBridge.h"

@interface AppDelegate ()

@end

@implementation AppDelegate


ENBridge* bridge;


- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    // Override point for customization after application launch.
    
    // Bring up the bridge
    bridge = [ENBridge instance];
    bridge.appDelegate = self;
        
    // Start python
    [self performSelectorInBackground:@selector(startPython:) withObject:application];
    return YES;
}


- (void)applicationWillResignActive:(UIApplication *)application {
    // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
    // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
    
    
}


- (void)applicationDidEnterBackground:(UIApplication *)application {
    // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
    // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    
}


- (void)applicationWillEnterForeground:(UIApplication *)application {
    // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
}


- (void)applicationDidBecomeActive:(UIApplication *)application {
    // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
}


- (void)applicationWillTerminate:(UIApplication *)application {
    // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    [self stopPython:application];
}

- (int)startPython:(UIApplication *)application {
    NSLog(@"Starting python thread");
    int argc = 1; // Needed for some stupid reason
    char *argv[argc]; // Needed for some stupid reason
    int ret = 0;
    NSString *tmp_path;
    NSString *libs_path;
    NSString *python_home;
    NSString *python_path;
    char *wpython_home;
    const char* main_script;
    
    NSString * resourcePath = [[NSBundle mainBundle] resourcePath];
    
    // Special environment to avoid writing bytecode because
    // the process will not have write attribute on the device.
    putenv("PYTHONDONTWRITEBYTECODE=1");
    
    // Set the home for the Python interpreter
    python_home = [NSString stringWithFormat:@"%@/Python/stdlib", resourcePath, nil];
    NSLog(@"PythonHome is: %@", python_home);
    wpython_home = strdup([python_home UTF8String]);
    Py_SetPythonHome(wpython_home);
    
    // Set the PYTHONPATH
    python_path = [NSString stringWithFormat:@"PYTHONPATH=%@/Python:%@/Python/site-packages:%@/Python/stdlib",
                   resourcePath, resourcePath, resourcePath, nil];
    NSLog(@"PYTHONPATH is: %@", python_path);
    putenv((char *)[python_path UTF8String]);
    
    // iOS provides a specific directory for temp files.
    tmp_path = [NSString stringWithFormat:@"TMP=%@", NSTemporaryDirectory(), nil];
    putenv((char *)[tmp_path UTF8String]);
    
    // Set library Loader path
    libs_path = [NSString stringWithFormat:@"PY_LIB_DIR=%@/Libs", resourcePath, nil];
    putenv((char *)[libs_path UTF8String]);
    
    NSLog(@"Initializing Python runtime");
    Py_Initialize();
    
    // Set the name of the main script
    NSString *mainScript = [NSString stringWithFormat:@"Python/main", nil];
    main_script = [[[NSBundle mainBundle] pathForResource:mainScript ofType:@"py"] cStringUsingEncoding:NSUTF8StringEncoding];
    
    if (main_script == NULL) {
        NSLog(@"Unable to locate python main module file");
        return -1;
    }
    
    // Construct argv for the interpreter
    //python_argv = PyMem_Malloc(sizeof(char *) * argc);
    //
    //python_argv[0] = strdup(main_script);
    //for (i = 1; i < argc; i++) {
    //    python_argv[i] = argv[i];
    //}
    
    
    //PySys_SetArgv(argc, python_argv);
    
    // If other modules are using threads, we need to initialize them.
    PyEval_InitThreads();
    
    // Start the main.py script
    NSLog(@"Running %s", main_script);
        
    @try {
        FILE* fd = fopen(main_script, "r");
        if (fd == NULL) {
            ret = 1;
            NSLog(@"Unable to open main.py, abort.");
        } else {
            ret = PyRun_SimpleString(
                "from main import main\n" \
                "main()"
            );
            //ret = PyRun_SimpleFileEx(fd, main_script, 1);
            if (ret != 0) {
                NSLog(@"Python quit abnormally!");
            } else {
                NSLog(@"Python quit properly!");
            }
            
        }
    }
    @catch (NSException *exception) {
        NSLog(@"Python runtime error: %@", [exception reason]);
    }
    @finally {
        Py_Finalize();
    }
    PyMem_Free(wpython_home);
    return ret;
    
}

/**
 * Send event to stop python and wait for it to quit
 */
- (void)stopPython:(UIApplication *)application {
}


@end
