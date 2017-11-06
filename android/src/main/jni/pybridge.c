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

#define LOG(x) __android_log_write(ANDROID_LOG_INFO, "pybridge", (x))


/* --------------- */
/*   Android log   */
/* --------------- */
static JNIEnv* jenv;
static jclass mPythonInterpreter;
static jmethodID mPublishEvents;

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

static PyMethodDef NativeHooksMethods[] = {
    {"write", NativeHooks_write, METH_VARARGS, "Write to android log"},
    {"flush", NativeHooks_flush, METH_VARARGS, "Required for logging"},
    {"publish", NativeHooks_publish, METH_VARARGS, "Send events to the Java implementation"},
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

PyMODINIT_FUNC PyInit_NativeHooks(JNIEnv *env) {
    // Get and cache the method pointer
    jenv = env;
    mPythonInterpreter = (*env)->FindClass(env, "com/codelv/enamlnative/python/PythonInterpreter");
    mPublishEvents = (*env)->GetStaticMethodID(env, mPythonInterpreter, "publishEvents", "([B)V");
#if PY_MAJOR_VERSION >= 3
    PyObject* module= PyModule_Create(&NativeHooksModule);
#else
    PyObject* module = Py_InitModule("nativehooks", NativeHooksMethods);
#endif

    // Redirect stdout and stderr to this module
    PySys_SetObject("stdout", module);
    PySys_SetObject("stderr", module);
    //return module;
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
        (JNIEnv *env, jclass jc, jstring path, jstring jni_path){
    LOG("Initializing the Python interpreter");

    // Get the location of the python files
    const char *pypath = (*env)->GetStringUTFChars(env, path, NULL);
    const char *jnipath = (*env)->GetStringUTFChars(env, jni_path, NULL);
    LOG(pypath);
    LOG(jnipath);

    // Set JNI path
    setenv("PY_LIB_DIR", jnipath, 1);

    // Build paths for the Python interpreter
    char paths[512];
    // Remove extra paths, the smaller the search path the faster the import
    snprintf(paths, sizeof(paths),"%s", pypath);
#if PY_MAJOR_VERSION >= 3
    // Set Python paths
    wchar_t *wchar_paths = Py_DecodeLocale(paths, NULL);
    Py_SetPath(wchar_paths);
#else
    //PySys_SetPath(paths);
    Py_SetPath(paths); // works with crystax NOT normal python...
#endif

#if PY_MAJOR_VERSION >= 3
    // Initialize Python interpreter and logging
    PyImport_AppendInittab("nativehooks", PyInit_NativeHooks);
#endif
    Py_OptimizeFlag = 1;
    Py_Initialize();
    if (! PyEval_ThreadsInitialized()) {
        PyEval_InitThreads();
    }

    PyInit_NativeHooks(env);

    // Inject  bootstrap code to redirect python stdin/stdout
    // to the androidlog module
    // then add the custom import hook loader
    // and run main() from bootstrap.py
    int result = PyRun_SimpleString(
      "import os\n" \
      "import sys\n" \
      "import imp\n" \
      "class _AndroidExtensionImporter(object):\n" \
      "    extension_modules = {}\n" \
      "    def __init__(self):\n" \
      "        ext_type = 'dylib' if sys.platform == 'darwin' else 'so'\n" \
      "        prefix = '' if sys.platform == 'darwin' else 'lib.'\n" \
      "        start = 0 if sys.platform == 'darwin' else 1\n" \
      "        lib_dir = os.environ.get('PY_LIB_DIR','.')\n" \
      "        for lib in os.listdir(lib_dir):\n" \
      "            lib = lib.split('/')[-1]\n"\
      "            if lib.startswith(prefix) and lib.endswith(ext_type):\n"\
      "                mod = '.'.join(lib.split('.')[start:-1])  # Strip lib and so\n" \
      "                self.extension_modules[mod] = os.path.join(lib_dir, lib)\n" \
      "    def load_module(self, mod):\n" \
      "        try:\n" \
      "            return sys.modules[mod]\n" \
      "        except KeyError:\n" \
      "            pass\n" \
      "        lib = self.extension_modules[mod]\n" \
      "        m = imp.load_dynamic(mod, lib)\n" \
      "        sys.modules[mod] = m\n" \
      "        return m\n" \
      "    def find_module(self, mod, path=None):\n" \
      "        if mod in self.extension_modules:\n" \
      "            return self\n" \
      "        return None\n" \
      "sys.meta_path.append(_AndroidExtensionImporter()) \n" \
      "try:\n"\
      "    from main import main\n" \
      "    main()\n" \
      "except:\n"\
      "    import traceback\n" \
      "    traceback.print_exc()\n" \
    );
    /*





          */
    // Cleanup
    (*env)->ReleaseStringUTFChars(env, path, pypath);
    (*env)->ReleaseStringUTFChars(env, jni_path, jnipath);
#if PY_MAJOR_VERSION >= 3
    PyMem_RawFree(wchar_paths);
#endif
    return result;
}


JNIEXPORT jint JNICALL Java_com_codelv_enamlnative_python_PythonInterpreter_stop
  (JNIEnv *env, jclass jc) {
    LOG("Finalizing the Python interpreter");
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

    // Send the events
    PyObject_CallMethod(app, "on_events", "s#", buf, size);

    // Cleanup
    (*env)->ReleaseByteArrayElements(env, payload, buf, JNI_ABORT);
    Py_DECREF(app);
    Py_DECREF(AndroidApplication);
    Py_DECREF(module);

    // Release the thread. No Python API allowed beyond this point (in native code!).
    PyGILState_Release(state);

    return 0;
}
