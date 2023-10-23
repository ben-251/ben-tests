from typing import ClassVar, List
from .asserts import *

class testCase:
	__name__ = "Default"

def test_all(*args: type[testCase]) -> None:
	'''
	Run all the tests within the specified test case.

	If more than one test case is specified, test all the tests in each test cases
	.. code-block:: python
		bentests.test_all(ArithmeticTests, ExponentialTests)
	'''
	for test_case in args:
		methods = getMethodNames(test_case)
		if methods:
			print(f"\nRunning tests in \"{test_case.__name__}\":") 
			_test_all_methods_in_(test_case)
		else:
			print(f"\nNo tests found in \"{test_case.__name__}\".")
	print("\nTests Complete.")
 
def _test_all_methods_in_(test_case: type[testCase]) -> None:
	'''
	Run all the tests within the specified test group:
	.. code-block:: python
		class ArithmeticTests(bentests.testCase):
			def testAddition():
				bentests.assertEquals(1,0+1)
			def testSubtraction():
				bentests.assertEquals(1,2-1)
		bentests.test_all(ArithmeticTests)
	'''
	#TODO: make failing tests say which tests failed. 
	method_list = getMethodNames(test_case)
	test_group = test_case()
	for method_name in method_list:
		print(f"- testing {method_name[4:]}") # remove "test"
		method = getattr(test_group, method_name)
		method()

def getMethodNames(cls: Type[testCase]) -> List[str]:
	method_list: List[str] = []
	for attribute in dir(cls):
		attribute_value = getattr(cls, attribute)
		if callable(attribute_value):
			if not attribute.startswith('__') and not attribute.endswith('__'):
				method_list.append(attribute)
	return method_list