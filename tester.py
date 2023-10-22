from typing import List
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
		print(f"\nRunning tests in \"{test_case.__name__}\":") 
		_test_all_methods_in_(test_case)
	print("Tests Complete.")
 
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
	method_list: List[str] = []
	for attribute in dir(test_case):
		attribute_value = getattr(test_case, attribute)
		if callable(attribute_value):
			if not attribute.startswith('__') and not attribute.endswith('__'):
				method_list.append(attribute)
	
	test_group = test_case()
	for method_name in method_list:
		method = getattr(test_group, method_name)
		method()