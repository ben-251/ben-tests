from .constants import *
from .display import *
from typing import Any
import numpy as np
from .response import Response

def assertEquals(actual:Any,expected: Any):
	'''Passes only if the actual value exactly matches the expected one.
	'''
	if type(actual) == np.ndarray and type(expected) == np.ndarray:
		result = TestResult.PASS if np.array_equal(actual, expected) else TestResult.FAIL
	else: 
		try:
			result = TestResult.PASS if actual == expected else TestResult.FAIL
		except ValueError:
			result = TestResult.FAIL
	EqualsMessageDisplayer(result, actual, expected)

def assertAlmostEquals(actual:Any, expected: Any, error_margin:int|None = None) -> None:
	'''
	Passes if the elements are within a range of each other.
	For example:

	.. code-block:: python
	assertAlmostEquals(0.100000001, 0.1) # passes

	If matrices are input, then the error margin is irrelevant
	'''
	#TODO: rename error_margin to better capture the idea of freedom, as in, you can be loose up to n digits
	if error_margin is None:
		error_margin = 7

	if type(actual) == np.ndarray and type(expected) == np.ndarray:
		result = TestResult.PASS if np.allclose(actual, expected) else TestResult.FAIL

	elif not isinstance(actual, float) and not isinstance(actual, int):
		result = TestResult.FAIL
	elif not round(actual-expected,error_margin) == 0:
		result = TestResult.FAIL
	else:
		result = TestResult.PASS
	EqualsMessageDisplayer(result, actual, expected)
		
class _AssertRaisesContext:
	'''	
		A context manager used to implement assertRaises* methods.		
	'''
	def __init__(self,expected_exception: type[Exception]) -> None:
		self.expected_exception = expected_exception

	def __enter__(self):
		return self
	
	def __exit__(self,exc_type: type | None, exc_value: Any, tb: Any) -> bool: 
		result = TestResult.PASS if exc_type == self.expected_exception else TestResult.FAIL
		ExceptionMessageDisplayer(result, exc_type, self.expected_exception)
		return exc_type is not None and issubclass(exc_type, self.expected_exception)  # suppress the exception if the exception is the requested one 

def assertRaises(expected_exception: type[Exception]): 
	'''
	Test fails unless an exception of class expected_exception is raised. If a different type of exception is raised, it will not be caught, and the test will exit with an error, just like it would for an unexpected exception.

	Used like this:
	.. code-block:: python
		with assertRaises(SomeException):
   			do_something()	
	'''
	return _AssertRaisesContext(expected_exception) #TODO: make anoother version that also that the exception message is correct