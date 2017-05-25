/**
    This file defines the JNI implementation of the PyBridge class.

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

static PyObject *androidlog(PyObject *self, PyObject *args)
{
    char *str;
    if (!PyArg_ParseTuple(args, "s", &str))
        return NULL;

    LOG(str);
    Py_RETURN_NONE;
}


static PyMethodDef AndroidlogMethods[] = {
    {"log", androidlog, METH_VARARGS, "Logs to Android stdout"},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef AndroidlogModule = {
    PyModuleDef_HEAD_INIT,
    "androidlog",        /* m_name */
    "Log for Android",   /* m_doc */
    -1,                  /* m_size */
    AndroidlogMethods    /* m_methods */
};


PyMODINIT_FUNC PyInit_androidlog(void)
{
    return PyModule_Create(&AndroidlogModule);
}
#else
PyMODINIT_FUNC PyInit_androidlog(void)
{
  (void)Py_InitModule("androidlog", AndroidlogMethods);
}
#endif

void setAndroidLog()
{
    // Inject  bootstrap code to redirect python stdin/stdout
    // to the androidlog module
    PyRun_SimpleString(
            "import sys\n" \
            "import androidlog\n" \
            "class LogFile(object):\n" \
            "    def __init__(self):\n" \
            "        self.buffer = ''\n" \
            "    def write(self, s):\n" \
            "        s = self.buffer + s\n" \
            "        lines = s.split(\"\\n\")\n" \
            "        for l in lines[:-1]:\n" \
            "            androidlog.log(l)\n" \
            "        self.buffer = lines[-1]\n" \
            "    def flush(self):\n" \
            "        return\n" \
            "sys.stdout = sys.stderr = LogFile()\n"
    );
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
JNIEXPORT jint JNICALL Java_com_jventura_pybridge_PyBridge_start
        (JNIEnv *env, jclass jc, jstring path)
{
    LOG("Initializing the Python interpreter");

    // Get the location of the python files
    const char *pypath = (*env)->GetStringUTFChars(env, path, NULL);
    LOG(pypath);

    // Build paths for the Python interpreter
    char paths[512];
    snprintf(paths, sizeof(paths), "%s:%s/stdlib.zip:%s/modules:%s/site-packages",
                                    pypath, pypath,pypath, pypath);
#if PY_MAJOR_VERSION >= 3
    // Set Python paths
    wchar_t *wchar_paths = Py_DecodeLocale(paths, NULL);
    Py_SetPath(wchar_paths);
#else
    Py_SetPath(paths);
#endif

#if PY_MAJOR_VERSION >= 3
    // Initialize Python interpreter and logging
    PyImport_AppendInittab("androidlog", PyInit_androidlog);
#endif
    Py_OptimizeFlag = 1;
    Py_Initialize();
    setAndroidLog();

    // Bootstrap
    PyRun_SimpleString("import bootstrap");

    // Cleanup
    (*env)->ReleaseStringUTFChars(env, path, pypath);
#if PY_MAJOR_VERSION >= 3
    PyMem_RawFree(wchar_paths);
#endif
    return 0;
}


JNIEXPORT jint JNICALL Java_com_jventura_pybridge_PyBridge_stop
        (JNIEnv *env, jclass jc)
{
    LOG("Finalizing the Python interpreter");
    Py_Finalize();
    return 0;
}


/**
    This function is responsible for receiving a payload string
    and sending it to the router function defined in the bootstrap.py
    file.

*/
JNIEXPORT jstring JNICALL Java_com_jventura_pybridge_PyBridge_call
        (JNIEnv *env, jclass jc, jstring payload)
{
    LOG("Call into Python interpreter");

    // Get the payload string
    jboolean iscopy;
    const char *payload_utf = (*env)->GetStringUTFChars(env, payload, &iscopy);

    // Import module
    PyObject* myModuleString = PyUnicode_FromString((char*)"bootstrap");
    PyObject* myModule = PyImport_Import(myModuleString);

    // Get reference to the router function
    PyObject* myFunction = PyObject_GetAttrString(myModule, (char*)"router");
    PyObject* args = PyTuple_Pack(1, PyUnicode_FromString(payload_utf));

    // Call function and get the resulting string
    PyObject* myResult = PyObject_CallObject(myFunction, args);
#if PY_MAJOR_VERSION >= 3
    char *myResultChar = PyUnicode_AsUTF8(myResult);
#else
    char *myResultChar = PyString_AsString(myResult);
#endif

    // Store the result on a java.lang.String object
    jstring result = (*env)->NewStringUTF(env, myResultChar);

    // Cleanup
    (*env)->ReleaseStringUTFChars(env, payload, payload_utf);
    Py_DECREF(myModuleString);
    Py_DECREF(myModule);
    Py_DECREF(myFunction);
    Py_DECREF(args);
    Py_DECREF(myResult);
    return result;
}
