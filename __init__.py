"""
Python self-made TDD framework.

This module contains classes that form can be used for testing a variety of functionalities,
for example assertEqual, assertRaises, etc.

Example usage:
    import bentests as bt

	def testAdd():
		bt.assertEqual((1 + 2), 3)
		bt.assertEqual(0 + 1, 1)
	def testMultiply():
		bt.assertEqual((0 * 10), 0)
		bt.assertEqual((5 * 8), 40)
	def testZeroDivision():
		with bt.assertRaises(ZeroDivisionError):
			var = 1/0

    if __name__ == '__main__':
        bentests.main()
"""
import inspect
from .asserts import *

class testCase: ...

def test_all(*args):
	'''
	Run all the tests within the specified test case.

	If more than one test case is specified, test all the tests in each test cases
	.. code-block:: python
		bentests.test_all(ArithmeticTests, ExponentialTests)
	'''
	for test_case in args:
		print(f"\nRunning tests in \"{test_case.__name__}\":")
		test_all_methods_in_(test_case)
 
def test_all_methods_in_(test_case):
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
	method_list = []
	# attribute is a string representing the attribute name
	for attribute in dir(test_case):
		# Get the attribute value
		attribute_value = getattr(test_case, attribute)
		# Check that it is callable
		if callable(attribute_value):
			# Filter all dunder (__ prefix) methods
			if not attribute.startswith('__') and not attribute.endswith('__'):
				method_list.append(attribute)
	
	test_group = test_case()
	for method_name in method_list:
		method = getattr(test_group, method_name)
		method()