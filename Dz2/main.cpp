#include <vector>

extern "C" {
#include <Python.h>
}


namespace matrixes {	
	typedef std::vector<double>  row_t;
	typedef std::vector<row_t>   matrix_t;

	static matrix_t algo(const matrix_t &a)
	{
		matrix_t result;
		result.resize(a.size());
		size_t n = a.size();
		
		for (size_t i=0; i<n; ++i) 
		{
			result[i].resize(n);
			for (size_t j=0; j<n; ++j) 
			{
				result[i][j]=a[i][j];				
			}
		}
		/*
		printf("\nN  = %d\n",n);
		for (size_t i=0; i<n; ++i) 
		{
			for (size_t j=0; j<n; ++j) 
			{
				printf("%10f",result[i][j]);				
			}
			printf("\n");
		}
		*/
		
		for (size_t k=0; k<n; k++)
			for (size_t i=0; i<n; i++) 
				for (size_t j=0; j<n; j++) 
					if (result[i][k]+result[k][j] != 0)
						if ((1/result[i][j]+1/(result[i][k]+result[k][j])) != 0)
						{
							result[i][j] = 1/(1/result[i][j]+1/(result[i][k]+result[k][j]));
						}
						
						
		/*				
		printf("\n-----------After CALCULATION--------------\n");
		for (size_t i=0; i<n; ++i) 
		{
			for (size_t j=0; j<n; ++j) 
			{
				printf("%20f",result[i][j]);				
			}
			printf("\n");
		}
		*/
		
		return result;
	}
}

static matrixes::matrix_t pyobject_to_cxx(PyObject * py_matrix)
{
	matrixes::matrix_t result;
	result.resize(PyObject_Length(py_matrix));
	for (size_t i=0; i<result.size(); ++i) {
		PyObject * py_row = PyList_GetItem(py_matrix, i);
		matrixes::row_t & row = result[i];
		row.resize(PyObject_Length(py_row));
		for (size_t j=0; j<row.size(); ++j) {
			PyObject * py_elem = PyList_GetItem(py_row, j);
			const double elem = PyFloat_AsDouble(py_elem);
			row[j] = elem;
		}
	}
	return result;
}

static PyObject * cxx_to_pyobject(const matrixes::matrix_t &matrix)
{
	PyObject * result = PyList_New(matrix.size());
	for (size_t i=0; i<matrix.size(); ++i) {
		const matrixes::row_t & row = matrix[i];
		PyObject * py_row = PyList_New(row.size());
		PyList_SetItem(result, i, py_row);
		for (size_t j=0; j<row.size(); ++j) {
			const double elem = row[j];
			PyObject * py_elem = PyFloat_FromDouble(elem);
			PyList_SetItem(py_row, j, py_elem);
		}
	}
	return result;
}

static PyObject * fast_resist(PyObject * module, PyObject * args)
{
	PyObject * py_a = PyTuple_GetItem(args, 0);

	/* Convert to C++ structure */
	const matrixes::matrix_t a = pyobject_to_cxx(py_a);

	/* Perform calculations */
	const matrixes::matrix_t result = matrixes::algo(a);

	/* Convert back to Python object */
	PyObject * py_result = cxx_to_pyobject(result);
	return py_result;
}

PyMODINIT_FUNC PyInit_my_module()
{
	static PyMethodDef ModuleMethods[] = {
		{ "fast_algo", fast_resist, METH_VARARGS, "Fast_algo_resists" },
		{ NULL, NULL, 0, NULL }
	};
	static PyModuleDef ModuleDef = {
		PyModuleDef_HEAD_INIT,
		"matrixes",
		"Fast calculation resistances on c++",
		-1, ModuleMethods, 
		NULL, NULL, NULL, NULL
	};
	PyObject * module = PyModule_Create(&ModuleDef);
	return module;
}
