#include <Python.h>
#include <freerdp/codec/progressive.h>
#include <freerdp/codec/region.h>


static void progressive_context_free_wrapper(PyObject * self) {
	progressive_context_free((PROGRESSIVE_CONTEXT*)PyCapsule_GetPointer(self, "progressive_context"));
}

static PyObject* progressive_context_new_wrapper(PyObject *self, PyObject *args) {
	int compressor = 0;
	if (!PyArg_ParseTuple(args, "p", &compressor)) {
        return NULL;
    }
    
    return PyCapsule_New(progressive_context_new(FALSE), "progressive_context", progressive_context_free_wrapper);
}

static PyObject* progressive_create_surface_context_wrapper(PyObject *self, PyObject *args) {
	uint32_t id, width, height;
	PyObject* context;
	if (!PyArg_ParseTuple(args, "OIII", &context, &id, &width, &height)) {
        return NULL;
    }
    
    progressive_create_surface_context((PROGRESSIVE_CONTEXT*)PyCapsule_GetPointer(context, "progressive_context"), id, width, height);
    return Py_None;
}

static PyObject* progressive_decompress_wrapper(PyObject *self, PyObject *args) {
    uint32_t width, height, step;
    uint8_t* input_data;
    uint8_t* output_data;
    PyObject* context;
    int input_data_size = 0, output_data_size = 0;
    
    if (!PyArg_ParseTuple(args, "OIIIy#y#", &context, &width, &height, &step, &input_data, &input_data_size, &output_data, &output_data_size)) {
        return NULL;
    }
    
    PROGRESSIVE_CONTEXT* progressive = (PROGRESSIVE_CONTEXT*)PyCapsule_GetPointer(context, "progressive_context");
        
    int status = progressive_decompress(progressive, input_data, (size_t)input_data_size, output_data, PIXEL_FORMAT_XRGB32, step, 0, 0, NULL, 0);
    
    return Py_BuildValue("I", status);
}

// Exported methods are collected in a table
PyMethodDef method_table[] = {
	{"progressive_context_new", (PyCFunction) progressive_context_new_wrapper, METH_VARARGS, "Create a progressive context"},
    {"progressive_create_surface_context", (PyCFunction) progressive_create_surface_context_wrapper, METH_VARARGS, "Create a surface context"},
    {"progressive_decompress", (PyCFunction) progressive_decompress_wrapper, METH_VARARGS, "Decompress image with Calista Progressive algorithm"},
    {NULL, NULL, 0, NULL} // Sentinel value ending the table
};

// A struct contains the definition of a module
PyModuleDef progressive_module = {
    PyModuleDef_HEAD_INIT,
    "progressive", // Module name
    "This is the module docstring",
    -1,   // Optional size of the module state memory
    method_table,
    NULL, // Optional slot definitions
    NULL, // Optional traversal function
    NULL, // Optional clear function
    NULL  // Optional module deallocation function
};

// The module init function
PyMODINIT_FUNC PyInit_progressive(void) {
    return PyModule_Create(&progressive_module);
}
