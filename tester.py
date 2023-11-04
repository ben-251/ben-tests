from typing import ClassVar, List, Type
from .asserts import *
from .constants import GREEN, CLEAR

class TestResult(Enum):
	PASS = auto()
	FAIL = auto()

class testGroup:
	__name__ = "Default"

	def __init__(self):
		self.tests:List[Test] = []


class Test:
	def __init__(self,name):
		self.name = name[4:]
	
	def setResult(self, result:TestResult):
		self.result = result
	
	def setMessage(self, message:str):
		self.message = message

def test_all(*args: type[testGroup],skip_passes=None, display_statistics=None) -> None:
	'''
	Run all the tests within the specified test case.

	If more than one test case is specified, test all the tests in each test cases
	.. code-block:: python
		bentests.test_all(ArithmeticTests, ExponentialTests)
	'''
	if skip_passes is None:
		skip_passes = True
	if display_statistics is None:
		display_statistics = True

	all_results = []
	print("Starting tests..")
	for test_group in args:
		methods = getMethodNames(test_group)
		if methods:
			print(f"\nRunning tests in \"{test_group.__name__}\":") 
			results:testGroup = getTestResults(test_group, methods, skip_passes=skip_passes)
			displayStats(results)
			all_results.append(results)
		else:
			print(f"{YELLOW}\nNo tests found in \"{test_group.__name__}\".{CLEAR}")
			all_results.append(None)
	print("\nTests Complete.")
	if display_statistics:
		display_overall_stats(all_results)
 
def getTestResults(cls: Type[testGroup], method_list, skip_passes=None):
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
	test_group_instance = cls()
	for method_name in method_list:
		new_result = getSingleTestResult(cls, method_name, skip_passes=skip_passes)
		test_group_instance.tests.append(new_result)
		display_single_result(test_group_instance.tests[-1], skip_passes)
	return test_group_instance

def getSingleTestResult(cls, test_name, skip_passes = None):
	test_method = getattr(cls, test_name)
	current_test = Test(test_name)
	try:
		test_method(cls)
	except TestFail as fail_message:
		current_test.setResult(TestResult.FAIL)
		current_test.setMessage(str(fail_message))
	else:
		current_test.setResult(TestResult.PASS)
		current_test.setMessage(str(TestPass()))
	return current_test

def display_single_result(test:Test, skip_passes):
	if test.result == TestResult.PASS:
		if not skip_passes:
			print(f"• {test.name}:")
			print(test.message, end="\n\n")
	else:
		print(f"• {test.name}:")
		print(test.message, end = "\n\n")

def displayStats(test_group:testGroup):
	test_count = len(test_group.tests)
	fail_count = sum([test.result == TestResult.FAIL for test in test_group.tests]) # bools are taken as 1 and 0

	if fail_count == 0:
		if test_count == 1:
			print(f"{GREEN} Test Passed.{CLEAR}")
		else:
			print(f"{GREEN}All {test_count} Tests Passed.{CLEAR}")
	else:
		print(f"{RED}{fail_count}{CLEAR} Failing test{'s' if fail_count > 1 else ''} out of {test_count}.")

def display_overall_stats(results:List[testGroup]):
	skipped_count = 0
	total_pass_count = 0
	passing_group_count = 0
	total_test_count = 0

	for result in results:
		if result is None:
			skipped_count += 1
		else:
			if all([test.result == TestResult.PASS for test in result.tests]):
				passing_group_count += 1
			for test in result.tests:
				total_test_count += 1
				if test.result == TestResult.PASS:
					total_pass_count += 1
	total_fail_count = total_test_count-total_pass_count

	print(f"{total_test_count} Test{'' if total_test_count == 1 else 's'} run.")
	if skipped_count > 0:	
		print(f"{YELLOW}{skipped_count} Empty Test group{'s' if skipped_count > 1 else ''} skipped.{CLEAR}")

	if total_pass_count == total_test_count:
		print(f"{GREEN}All Tests Passed")
		return # we don't care about the other stats if we've passed all

	print(f"{GREEN}{total_pass_count} Test{'s' if total_pass_count > 1 else ''} passed{CLEAR}, {RED}{total_fail_count} Test{'s' if total_fail_count > 1 else ''} failed.{CLEAR}")
	if passing_group_count == 0:
		print(f"{RED}No Test Groups ran without any fails.{CLEAR}")
	else:
		print(f"{GREEN}{passing_group_count} Test Group{'s' if passing_group_count > 1 else ''} ran without any fails.{CLEAR}")

	if total_pass_count == 0 and not total_test_count <= 1:
		print(f"\n{RED}BTW, don't you find it concerning that NONE of your {total_test_count} tests passed?")

def getMethodNames(cls: type[testGroup]) -> List[str]:
	method_list: List[str] = []
	for attribute in dir(cls):
		attribute_value = getattr(cls, attribute)
		if callable(attribute_value):
			if not attribute.startswith('__') and not attribute.endswith('__'):
				method_list.append(attribute)
	return method_list
