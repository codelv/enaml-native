/**
    This file defines the JNI implementation of the Bridge class.

    It implements the native methods of the class and makes sure that
    all the prints and errors from the Python interpreter is redirected
    to the Android log. This is specially useful as it allows us to
    debug the Python code running on the Android device using logcat.

*/

#include <Python.h>
#include <jni.h>
#include <android/log.h>
#include <string.h>
#include <dirent.h>

/* --------------- */
/*   Android log   */
/* --------------- */
static JNIEnv* jenv;
static jclass mPythonInterpreter;
static jmethodID mPublishEvents;
static PyObject* mExtensions;
static PyObject* mImpLoadDynamic;
static PyObject* mNativehooksModule;
static int pfd[2];
static pthread_t mLogThread;
static const char *tag = "pybridge";
#define LOG(x) __android_log_write(ANDROID_LOG_INFO, tag, (x))

/**
 * Pipe to catch output from stdout and log it
 */
static void *thread_func(void* x) {
    ssize_t rdsz;
    char buf[128];
    while((rdsz = read(pfd[0], buf, sizeof buf - 1)) > 0) {
        if(buf[rdsz - 1] == '\n') --rdsz;
        buf[rdsz] = 0;  /* add null-terminator */
        __android_log_write(ANDROID_LOG_DEBUG, tag, buf);
    }
    return 0;
}

/**
 * Create a pipe and spawn a thread to catch output from nkd libraries
 * and send it to androids log.
 *
 * Thanks to https://codelab.wordpress.com/2014/11/03/how-to-use-standard-output-streams-for-logging-in-android-apps/
 */
int start_logger() {
    /* make stdout line-buffered and stderr unbuffered */
    setvbuf(stdout, 0, _IOLBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);

    /* create the pipe and redirect stdout and stderr */
    pipe(pfd);
    dup2(pfd[1], 1);
    dup2(pfd[1], 2);

    /* spawn the logging thread */
    if(pthread_create(&mLogThread, 0, thread_func, 0) == -1)
        return -1;
    pthread_detach(mLogThread);
    return 0;
}


/**
 * Call our hook into java. From python use it via
 *  import nativehooks
 *  nativehooks.publish(data)
 *
 * This sends data to the java's PythonInterpreter.publishEvents for handling.
 */
static PyObject *NativeHooks_publish(PyObject *self, PyObject *args) {
    Py_ssize_t count;
    const char* data;
    if (!PyArg_ParseTuple(args, "s#", &data, &count)) {
        return NULL;
    }
    jbyteArray buf = (*jenv)->NewByteArray(jenv, count);
    (*jenv)->SetByteArrayRegion(jenv,buf, 0, count, data);
    (*jenv)->CallStaticVoidMethod(jenv, mPythonInterpreter, mPublishEvents, buf);

    // Cleanup
    (*jenv)->DeleteLocalRef(jenv, buf);

    Py_RETURN_NONE;
}

/**
 * Log API
 */
static PyObject *NativeHooks_write(PyObject *self, PyObject *args) {
    char *str;
    if (!PyArg_ParseTuple(args, "s", &str)) {
        return NULL;
    }
    LOG(str);
    Py_RETURN_NONE;
}

static PyObject *NativeHooks_flush(PyObject *self, PyObject *args) {
    Py_RETURN_NONE;
}


/**
 * ExtensionImporter API
 */
static PyObject *NativeHooks_load_module(PyObject *self, PyObject *args) {
    PyObject *mod;
    if (!PyArg_ParseTuple(args, "O", &mod)) {
        return NULL;
    }
    PyObject* sys_modules = PyImport_GetModuleDict();
    if (PyDict_Contains(sys_modules, mod)) {
        return PyDict_GetItem(sys_modules, mod);
    }
#if PY_MAJOR_VERSION >= 3
    // Create an ExtensionFileLoader instance
    PyObject *loader = PyObject_CallFunction(mImpLoadDynamic, "OO", mod, PyDict_GetItem(mExtensions, mod));
    PyObject *result =  PyObject_CallMethod(loader, "load_module", NULL);
    Py_XDECREF(loader);
    return result;
#else
    return PyObject_CallFunction(mImpLoadDynamic, "OO", mod, PyDict_GetItem(mExtensions, mod));
#endif
}

static PyObject *NativeHooks_find_module(PyObject *self, PyObject *args) {
    PyObject *mod = NULL;
    PyObject *path = NULL;
    if (!PyArg_ParseTuple(args, "OO", &mod, &path)) {
        return NULL;
    }
    if (PyDict_Contains(mExtensions, mod)) {
        Py_INCREF(mNativehooksModule);
        return mNativehooksModule;
    }
    Py_RETURN_NONE;
}

static PyMethodDef NativeHooksMethods[] = {
    {"write", NativeHooks_write, METH_VARARGS, "Write to android log"},
    {"flush", NativeHooks_flush, METH_VARARGS, "Required for logging"},
    {"publish", NativeHooks_publish, METH_VARARGS, "Send events to the Java implementation"},
    {"load_module", NativeHooks_load_module, METH_VARARGS, "Load an extension"},
    {"find_module", NativeHooks_find_module, METH_VARARGS, "Find an extension"},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef NativeHooksModule = {
    PyModuleDef_HEAD_INIT,
    "nativehooks",        /* m_name */
    "Android native hooks",   /* m_doc */
    -1,                  /* m_size */
    NativeHooksMethods    /* m_methods */
};

#endif

PyMODINIT_FUNC PyInit_NativeHooks() {
    LOG("Init native hooks");
    mPythonInterpreter = (*jenv)->FindClass(jenv, "com/codelv/enamlnative/python/PythonInterpreter");
    mPublishEvents = (*jenv)->GetStaticMethodID(jenv, mPythonInterpreter, "publishEvents", "([B)V");
#if PY_MAJOR_VERSION >= 3
    mNativehooksModule = PyModule_Create(&NativeHooksModule);
#else
    mNativehooksModule = Py_InitModule("nativehooks", NativeHooksMethods);
#endif

    // Redirect stdout and stderr to this module
    PySys_SetObject("stdout", mNativehooksModule);
    PySys_SetObject("stderr", mNativehooksModule);

#if PY_MAJOR_VERSION >= 3
    PyObject* imp =  PyImport_ImportModule("importlib.machinery");
    mImpLoadDynamic = PyObject_GetAttrString(imp, "ExtensionFileLoader");
#else
    // Get load dynamic
    PyObject* imp =  PyImport_ImportModule("imp");
    mImpLoadDynamic = PyObject_GetAttrString(imp, "load_dynamic");
#endif

    // Build extension dict
    mExtensions = PyDict_New();
    if (mExtensions!=NULL) {
        char* lib_dir = getenv("PY_LIB_DIR");
        int nlib = strlen(lib_dir);
        int n;
        DIR *dir;
        char mod[256];// lib. .so+'\0'
        char path[256];
        struct dirent *ent;
        if ((dir = opendir(lib_dir)) != NULL) {
            // print all the files and directories within directory
            while ((ent = readdir(dir)) != NULL) {
                // If startswith lib. strip mod
                if (ent->d_type == DT_REG && strncmp("lib.", ent->d_name, 4) == 0) {
                    n = strlen(ent->d_name);
                    strncpy(mod, ent->d_name+4, n-7);
                    mod[n-7] = '\0';
                    strcpy(path, lib_dir);
                    strcat(path, "/");
                    strcat(path, ent->d_name);
                    path[nlib+n+1] = '\0';
                    PyDict_SetItem(mExtensions, Py_BuildValue("s", mod), Py_BuildValue("s", path));
                }
            }
            closedir(dir);
        } else {
          /* could not open directory */
          LOG("Python extension dir is invalid");
        }
    }

    // Add to meta path
    Py_INCREF(mNativehooksModule);

    PyObject* meta_path = PySys_GetObject("meta_path");
    PyObject* result = PyObject_CallMethod(meta_path, "append", "O", mNativehooksModule);

    Py_XDECREF(result);
    Py_XDECREF(imp);

#if PY_MAJOR_VERSION >= 3
    return mNativehooksModule;
#endif
}

/* ------------------ */
/*   Native methods   */
/* ------------------ */

/**
    This function configures the location of the standard library,
    initializes the interpreter and sets up the python log redirect.
    It runs a file called bootstrap.py before returning, so make sure
    that you configure all your python code on that file.

    Note: the function must receives a string with the location of the
    python files extracted from the assets folder.

*/
JNIEXPORT jint JNICALL Java_com_codelv_enamlnative_python_PythonInterpreter_start
        (JNIEnv *env, jclass jc, jstring assets_path, jstring cache_path, jstring jni_path){
    LOG("Initializing the Python interpreter");
    // Save the env
    jenv = env;

    // This forwards NDK stdout output to logcat
    start_logger();

    // Get the location of the python files
    const char *assetspath = (*env)->GetStringUTFChars(env, assets_path, NULL);
    const char *cachepath = (*env)->GetStringUTFChars(env, cache_path, NULL);
    const char *jnipath = (*env)->GetStringUTFChars(env, jni_path, NULL);
    LOG(cachepath);
    LOG(assetspath);
    LOG(jnipath);

    // Build paths for the Python interpreter
    char paths[512];
    // Remove extra paths, the smaller the search path the faster the import
    snprintf(paths, sizeof(paths),"%s:%s/site-packages", cachepath, cachepath);

    // Set JNI path
    setenv("ASSETS", assetspath, 1);
    setenv("PYTHONPATH", paths, 1);
    setenv("TMP", cachepath, 1);
    setenv("PY_LIB_DIR", jnipath, 1);


#if PY_MAJOR_VERSION >= 3
    // Initialize Python interpreter and logging
    PyImport_AppendInittab("nativehooks", PyInit_NativeHooks);
#endif
    //Py_OptimizeFlag = 1;
    Py_NoSiteFlag = 1;
    Py_Initialize();


#if PY_MAJOR_VERSION < 3
    if (! PyEval_ThreadsInitialized()) {
        PyEval_InitThreads();
    }

    PyInit_NativeHooks();
#endif

    // Inject  bootstrap code to redirect python stdin/stdout
    // to the androidlog module
    // then add the custom import hook loader
    // and run main() from bootstrap.py
    int result = PyRun_SimpleString(
        "try:\n"\
        "    import nativehooks\n"\
        "    import sys\n"\
        "    if sys.version_info.major > 2:\n"\
        "       from importlib import reload\n"\
        "    print('Launching main.py...')\n"\
        "    from main import main\n" \
        "    main()\n" \
        "except Exception as e:\n"\
        "    try:\n"\
        "        import traceback\n"\
        "        traceback.print_exc()\n"\
        "    except:\n"\
        "        print(e)\n" \
    );

    // Cleanup
    (*env)->ReleaseStringUTFChars(env, assets_path, assetspath);
    (*env)->ReleaseStringUTFChars(env, cache_path, cachepath);
    (*env)->ReleaseStringUTFChars(env, jni_path, jnipath);
    return result;
}


JNIEXPORT jint JNICALL Java_com_codelv_enamlnative_python_PythonInterpreter_stop
  (JNIEnv *env, jclass jc) {
    LOG("Finalizing the Python interpreter");
    Py_XDECREF(mNativehooksModule);
    Py_XDECREF(mExtensions);
    Py_Finalize();
    return 0;
}


/**
 *  Sends a bridge encoded buffer to the android application's on_events method.
 */
JNIEXPORT int JNICALL Java_com_codelv_enamlnative_python_PythonInterpreter_sendEvents
        (JNIEnv *env, jclass jc, jbyteArray payload) {
    PyGILState_STATE state = PyGILState_Ensure();

    // Import module
    PyObject* module = PyImport_ImportModule("enamlnative.android.app");

    // Get android app
    PyObject* AndroidApplication = PyObject_GetAttrString(module, "AndroidApplication");

    // Get a reference to the app instance
    PyObject* app = PyObject_CallMethod(AndroidApplication, "instance", "");

    // Read array
    jsize size = (*env)->GetArrayLength(env, payload);
    jbyte* buf = (*env)->GetByteArrayElements(env, payload, NULL);

    if (buf==NULL) {
      PyErr_NoMemory();
      PyGILState_Release(state);
      return -1;
    }


#if PY_MAJOR_VERSION >= 3
    const char* sig="y#";
#else
    const char* sig="s#";
#endif

    // Send the events
    PyObject* result = PyObject_CallMethod(app, "on_events", sig, buf, size);

    // Cleanup
    (*env)->ReleaseByteArrayElements(env, payload, buf, JNI_ABORT);
    Py_DECREF(result);
    Py_DECREF(app);
    Py_DECREF(AndroidApplication);
    Py_DECREF(module);

    // Release the thread. No Python API allowed beyond this point (in native code!).
    PyGILState_Release(state);

    return 0;
}
