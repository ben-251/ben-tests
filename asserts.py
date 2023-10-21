from .constants import *
from .display import *
from typing import Any, Union
import contextlib

def assertEquals(actual:Any,expected: Any):
	'''Passes only if the actual value exactly matches the expected one.
	'''
	result = TestResult.PASS if actual == expected else TestResult.FAIL
	display_normal_message(result, actual, expected)
	 
class _AssertRaisesContext:
	'''	
		A context manager used to implement assertRaises* methods.		
	'''
	def __init__(self,expected_exception: BaseException, *args, **kwargs):
		self.expected_exception = expected_exception

	def __enter__(self):
		return self
	
	def __exit__(self,exc_type, exc_value, tb):
		result = TestResult.PASS if exc_type == self.expected_exception else TestResult.FAIL
		display_exception_message(result, exc_type, self.expected_exception)
		return exc_type is not None and issubclass(exc_type, self.expected_exception)  # suppress the exception if the exception is the requested one

def assertRaises(expected_exception: BaseException, *args, **kwargs): #-> _AssertRaisesContext[BaseException]
	'''
	Test fails unless an exception of class expected_exception is raised. If a different type of exception is raised, it will not be caught, and the test will exit with an error, just like it would for an unexpected exception.

	Used like this:
	.. code-block:: python
		with assertRaises(SomeException):
   			do_something()	
	'''
	return _AssertRaisesContext(expected_exception) #TODO: make anoother version that also that the exception message is correct

def test() -> str:
	return 1 # jedi should say something here




