from .utils import IsNotTrueError, EqualsFailError, RaisesFailError, NotRaisesFailError
from typing import Any, Optional
from collections.abc import Iterable
from numbers import Number
import numpy as np
import math



def assertEquals(actual:Any,expected: Any):
	'''Passes only if the actual value exactly matches the expected one.
	'''
	if type(actual) == np.ndarray and type(expected) == np.ndarray:
		if not np.array_equal(actual, expected):
			raise EqualsFailError(actual, expected)
	elif actual != expected:
			raise EqualsFailError(actual, expected)

def is_iterable_of_numbers(obj):
    # Check if the object is iterable but not a string
    if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        # Check if all elements are instances of Number
        return all(isinstance(item, Number) for item in obj)
    return False

def is_almost_equal(actual, expected, error_margin):
	diff = actual-expected
	rounded =  round(diff, error_margin)
	return rounded == 0

def is_almost_equal_iter(actual, expected, rel_tolerance, abs_tolerance):
	for actual_el, expected_el in zip(actual, expected):
		if not math.isclose(actual_el, expected_el, rel_tol=rel_tolerance, abs_tol=abs_tolerance):
			return False
	return True

def assertAlmostEquals(actual:Any, expected: Any, error_margin:Optional[int] = None) -> None:
	'''
	Passes if the elements are within a range of each other.
	For example:

	.. code-block:: python
	assertAlmostEquals(0.100000001, 0.1) # passes

	If matrices are input, then the error margin is irrelevant
	'''
	if error_margin is None:
		error_margin = 8
	rel_tolerance = 10 ** -error_margin
	abs_tolerance = 10 ** -math.ceil(error_margin/2)

	if type(actual) == np.ndarray and type(expected) == np.ndarray:
		if not np.allclose(actual, expected):
			raise EqualsFailError(actual, expected)
	elif is_iterable_of_numbers(actual):
		if not is_almost_equal_iter(actual, expected, rel_tolerance, abs_tolerance):
			raise EqualsFailError(actual, expected)
	elif not isinstance(actual, float) and not isinstance(actual, int):
		raise EqualsFailError(actual, expected)
	elif not math.isclose(actual, expected, rel_tol=rel_tolerance, abs_tol=abs_tolerance):
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


class _AssertNotRaisesContext:
	'''	
		A context manager used to implement assertNotRaises* methods.		
	'''
	def __init__(self,avoiding_exception: type[Exception]) -> None:
		self.avoiding_exception = avoiding_exception

	def __enter__(self):
		return self
	
	def __exit__(self,exc_type: type | None, exc_value: Any, tb: Any) -> bool: 
		if exc_type == self.avoiding_exception:
			raise NotRaisesFailError(exc_type, self.avoiding_exception)
		return exc_type is not None and issubclass(exc_type, self.avoiding_exception)  # supress the exception so we can debug normally

def assertNotRaises(avoiding_exception: type[Exception]): 
	'''
	Test fails if an exception of class expected_exception is raised.
	If a different type of exception is raised, it will not be caught, and the test will exit with an error, 
	just like it would for an unexpected exception. Might change to surpress, but for now that's bad.

	Used like this:
	.. code-block:: python
		with assertNotRaises(SomeException):
   			do_something()	
	'''
	return _AssertNotRaisesContext(avoiding_exception)