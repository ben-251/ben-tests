from .constants import *
from .display import *
from typing import Any

def assertEquals(actual:Any,expected: Any) -> None:
	'''Passes only if the actual value exactly matches the expected one.
	'''
	#TODO: Add support for numpy arrays. could be in this method or could make another. probably this one
	result = TestResult.PASS if actual == expected else TestResult.FAIL
	EqualsMessageDisplayer(result, actual, expected).display_message()
	 
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
		ExceptionMessageDisplayer(result, exc_type, self.expected_exception).display_message()
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





