from .constants import *
from typing import Any
import numpy as np

def assertEquals(actual:Any,expected: Any):
	'''Passes only if the actual value exactly matches the expected one.
	'''
	if type(actual) == np.ndarray and type(expected) == np.ndarray:
		if not np.array_equal(actual, expected):
			raise EqualsFailError(actual, expected)
	elif actual != expected:
			raise EqualsFailError(actual, expected)

def assertAlmostEquals(actual:Any, expected: Any, error_margin:int|None = None) -> None:
	'''
	Passes if the elements are within a range of each other.
	For example:

	.. code-block:: python
	assertAlmostEquals(0.100000001, 0.1) # passes

	If matrices are input, then the error margin is irrelevant
	'''
	if error_margin is None:
		error_margin = 7

	if type(actual) == np.ndarray and type(expected) == np.ndarray:
		if not np.allclose(actual, expected):
			raise EqualsFailError(actual, expected)

	elif not isinstance(actual, float) and not isinstance(actual, int):
		raise EqualsFailError(actual, expected)
	elif not round(actual- expected,error_margin) == 0:
		raise EqualsFailError(actual, expected)

class _AssertRaisesContext:
	'''	
		A context manager used to implement assertRaises* methods.		
	'''
	def __init__(self,expected_exception: type[Exception]) -> None:
		self.expected_exception = expected_exception

	def __enter__(self):
		return self
	
	def __exit__(self,exc_type: type | None, exc_value: Any, tb: Any) -> bool: 
		if exc_type != self.expected_exception:
			raise RaisesFailError(exc_type, self.expected_exception) # wait but this unsupresses 
		return exc_type is not None and issubclass(exc_type, self.expected_exception)  # does it reach here anymore?

def assertRaises(expected_exception: type[Exception]): 
	'''
	Test fails unless an exception of class expected_exception is raised. If a different type of exception is raised, it will not be caught, and the test will exit with an error, just like it would for an unexpected exception.

	Used like this:
	.. code-block:: python
		with assertRaises(SomeException):
   			do_something()	
	'''
	return _AssertRaisesContext(expected_exception)