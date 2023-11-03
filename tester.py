from typing import ClassVar, List, Type
from .asserts import *
from .constants import GREEN, CLEAR

class testCase:
	__name__ = "Default"

def test_all(*args: type[testCase],skip_passes=None) -> None:
	'''
	Run all the tests within the specified test case.

	If more than one test case is specified, test all the tests in each test cases
	.. code-block:: python
		bentests.test_all(ArithmeticTests, ExponentialTests)
	'''
	if skip_passes is None:
		skip_passes = True

	for test_case in args:
		methods = getMethodNames(test_case)
		if methods:
			print(f"\nRunning tests in \"{test_case.__name__}\":") 
			_test_all_methods_in_(test_case, skip_passes)
		else:
			print(f"\nNo tests found in \"{test_case.__name__}\".")
	print("\nTests Complete.")
 
def _test_all_methods_in_(test_case: type[testCase], skip_passes: bool) -> None:
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
	method_list = getMethodNames(test_case)
	test_group = test_case()
	fail_count = getFailCount(method_list, test_group,skip_passes=skip_passes)
	test_count = len(method_list)
	displayStats(fail_count, test_count)

def getFailCount(method_list,test_group,skip_passes=None):
	fail_count = 0
	for method_name in method_list:
		method = getattr(test_group, method_name)
		try:
			method()
		except TestFail as e:
			print(f"- {method_name[4:]}:") # remove "test"
			print(e)
			fail_count += 1
		else:
			if not skip_passes:
				print(f"{method_name[4:]}: ")
				print(f"{GREEN}{' '*4}Ok.{CLEAR}")
	return fail_count

def displayStats(fail_count, test_count):
	if fail_count == 0:
		if test_count == 1:
			print(f"{GREEN} Test Passed.{CLEAR}")
		else:
			print(f"{GREEN}All {test_count} Tests Passed.{CLEAR}")
	else:
		print(f"\n{RED}{fail_count}{CLEAR} Failing test{'s' if fail_count > 1 else ''} out of {test_count}.")

def getMethodNames(cls: type[testCase]) -> List[str]:
	method_list: List[str] = []
	for attribute in dir(cls):
		attribute_value = getattr(cls, attribute)
		if callable(attribute_value):
			if not attribute.startswith('__') and not attribute.endswith('__'):
				method_list.append(attribute)
	return method_list