from typing import ClassVar, List, Type
from .asserts import *
from .utils import GREEN, CLEAR

class TestResult(Enum):
	PASS = auto()
	FAIL = auto()

class testGroup:
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
			results = getTestResults(test_group, methods, skip_passes=skip_passes)
			displayStats(results)
			all_results.append(results)
		else:
			print(f"{YELLOW}\nNo tests found in \"{test_group.__name__}\".{CLEAR}")
			all_results.append(None)
	print("\nTests Complete.")
	if display_statistics:
		display_overall_stats(all_results)
 
def getTestResults(cls: Type[testGroup], method_list, skip_passes=None) -> testGroup:
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
			print(test.message)
	else:
		print(f"• {test.name}:")
		print(test.message)

def displayStats(test_group:testGroup):
	test_count = len(test_group.tests)
	fail_count = sum([test.result == TestResult.FAIL for test in test_group.tests]) # bools are taken as 1 and 0

	if fail_count != 0:
		print(f"{RED}{fail_count}{CLEAR} Failing test{'s' if fail_count > 1 else ''} out of {test_count}.")
	elif test_count == 1:
		print(f"{GREEN}Test Passed.{CLEAR}")
	else:
		print(f"{GREEN}All {test_count} Tests Passed.{CLEAR}")

def display_overall_stats(results:List[testGroup]):
	skipped_count = 0
	total_pass_count = 0
	passing_group_count = 0
	total_test_count = 0
	group_count = len(results)

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

	if skipped_count > 0:
		display_message(f"{pluralise('Empty test group', skipped_count)} skipped.",colour=YELLOW)

	display_message(f"{pluralise('Test',total_test_count)} run in {pluralise('Group', group_count)}:")

	if total_pass_count == total_test_count:
		display_message(f"\tAll Tests Passed.", colour=GREEN)
		return # we don't care about the other stats if we've passed all

	display_message(f"{pluralise('test', total_pass_count)} passed.", colour=GREEN)
	display_message(f"{pluralise('test',total_fail_count)} failed.", colour = RED)
	if passing_group_count == 0:
		display_message(f"No Test Groups ran without any fails.",colour=RED)
	else:
		display_message(f"{pluralise('test group', passing_group_count)} ran without any fails.", colour=GREEN)

def getMethodNames(cls: type[testGroup]) -> List[str]:
	method_list = []
	for attribute_name in dir(cls):
		attribute = getattr(cls, attribute_name)
		is_callable = callable(attribute)
		is_magic_method = attribute_name.startswith('__') and attribute_name.endswith('__')
		if is_callable and not is_magic_method:
			method_list.append(attribute_name)
	return method_list

def display_message(message, colour=None,no_bullets = None):
	if colour is None:
		colour = ""
	bullet = "" if no_bullets else "• "
	print(f"{bullet}{colour}{message}{CLEAR}")