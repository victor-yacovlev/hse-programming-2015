#include <stdio.h>
#include <vector>

extern "C" {
#include <Python.h>
}

using namespace std;

static PyObject * diods_res(PyObject* module, PyObject* args)
{          
	PyObject * input = PyTuple_GetItem(args, 0);
	int size = PyObject_Length(input);
	vector<vector<double>> table(size, vector<double>(size));
	for (int i=0; i<size; i++)
		{
			PyObject * py_row = PyList_GetItem(input, i);
			for(int j=0; j<size; j++)
				{ 
					PyObject * elem = PyList_GetItem(py_row, j);
					table[i][j] = PyFloat_AsDouble(elem);
				}
		}
	for (int k=0; k<size; k++)
		for (int i=0; i<size; i++)
			for(int j=0; j<size; j++)
				{
					if (table[i][j] == 0 ||  table[k][j] == 0 && table[i][k] == 0)
						table[i][j]=0;
					else
						table[i][j] = 1.0/(1.0/table[i][j] + 1.0/(table[i][k] + table[k][j]));		
				}
	PyObject * output = PyList_New(size);
	for (int i = 0; i < size; i++)
		{
			PyObject * py_row = PyList_New(size);
			PyList_SetItem(output, i, py_row);
				for (int j = 0; j < size; j++)
					{
						PyObject* elem = PyFloat_FromDouble(table[i][j]);
						PyList_SetItem(py_row, j, elem);
					}
		}
	return output;
}

PyMODINIT_FUNC PyInit_diods()
{
	static PyMethodDef ModuleMethods[] = {
		{ "diods_res", diods_res, METH_VARARGS, "diods_res" },
		{ NULL, NULL, 0, NULL }
	};
	static PyModuleDef ModuleDef = {
		PyModuleDef_HEAD_INIT,
		"calculation_between_diods",
		"resistence_between_diods)",
		-1, ModuleMethods,
		NULL, NULL, NULL, NULL
	};
	PyObject * module = PyModule_Create(&ModuleDef);
	return module;
}
	
