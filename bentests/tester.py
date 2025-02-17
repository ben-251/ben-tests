from typing import List, Type
from .utils import GREEN, CLEAR, YELLOW, RED, TestFail, TestPass, pluralise
from typing import Optional
from enum import Enum, auto
import re
import inspect


class TestResult(Enum):
	PASS = auto()
	FAIL = auto()


class SkippedTest(Exception): ...

class Test:
	def __init__(self,name):	
		is_snake_case =  name[:5] == "test_"  # assume camel otherwise
		name = self.split_name(name, is_snake_case)
		name = self.strip_test(name, is_snake_case)
		self.name = name.title()
	
	def strip_test(self, name, is_snake_case):
		return name[5:] if is_snake_case else name[4:]

	def split_name(self, name, is_snake_case):
		if is_snake_case:
			return name.replace("_"," ") # fine because dunder methods have already been excluded
		else:
			return re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
		
	def setResult(self, result:TestResult):
		self.result = result
	
	def setMessage(self, message:str):
		self.message = message

class testGroup:
	def __init__(self):
		self.tests:List[Test] = []
	
	def __getitem__(self,index):
		return self.tests[index]

	def __len__(self) -> int:
		return len(self.tests)

	def __iadd__(self, test:Test):
		self.tests.append(test)
		return self

	def __add__(self, test:Test):
		new_test = testGroup()
		new_test.tests.append(test)
		return new_test


def test_all(*args: type[testGroup],skip_passes=None, stats_amount:Optional[str]=None) -> None:
	'''
	Run all the tests within the specified test groups.

	If more than one test case is specified, it tests all groups
	.. code-block:: python
		bentests.test_all(ArithmeticTests, ExponentialTests)
	
	Stats Amount: The Volume of statistics to provide. "high", "low", and "none".
	if any other value is provided, "low" is assumed.
	

	'''
	#TODO: make high stat amount show all passing tests as well, to quickly tell which ones DID succeed
	if skip_passes is None:
		skip_passes = True
	if stats_amount is None or not stats_amount in ["low", "high", "none"]:
		stats_amount = "low"

	all_results = []

	if args is None:
		raise ValueError("No tests given")

	print("Starting tests...")
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
	if not stats_amount == "none":
		display_overall_stats(all_results, stats_amount)
 
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
	if cls is None:
		raise ValueError("class is none for some reason?!")

	test_group_instance: testGroup = cls()
	for method_name in method_list:
		try:
			new_result = getSingleTestResult(cls, method_name, skip_passes=skip_passes)
			test_group_instance += new_result
			display_single_result(test_group_instance[-1], skip_passes)
		except SkippedTest:
			continue
	return test_group_instance

def getSingleTestResult(cls, test_name, skip_passes = None):
	test_method = getattr(cls, test_name)
	current_test = Test(test_name)

	signature = inspect.signature(test_method)
	params = signature.parameters
	is_skipped = params["skip"].default is True if "skip" in params else False
	if is_skipped:
		raise SkippedTest()

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
	test_count = len(test_group)
	fail_count = sum([test.result == TestResult.FAIL for test in test_group.tests]) # bools are taken as 1 and 0

	if fail_count != 0:
		print(f"{RED}{fail_count}{CLEAR} Failing test{'s' if fail_count > 1 else ''} out of {test_count}.")
	elif test_count == 1:
		print(f"{GREEN}Test passed.{CLEAR}")
	elif test_count == 2:
		print(f"{GREEN}Both tests passed. {CLEAR}")
	else:
		print(f"{GREEN}All {test_count} Tests Passed.{CLEAR}")

def display_overall_stats(results:List[testGroup], stats_amount:str):
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
		display_message(f"{pluralise('Empty test group', skipped_count)} skipped.\n",colour=YELLOW, no_bullets=True)

	if not stats_amount == "low":
		display_message(f"{pluralise('Test',total_test_count)} run in {pluralise('Group', group_count)}:", no_bullets=True)

	if total_pass_count == total_test_count:
		display_message(f"All Tests Passed.", colour=GREEN, no_bullets=True)
		return
		# The other stats can be safely ignored if all tests have passed.

	display_message(f"{pluralise('test', total_pass_count)} passed.", colour=GREEN, no_bullets=False)
	display_message(f"{pluralise('test',total_fail_count)} failed.", colour = RED, no_bullets=False)

	if stats_amount == "low":
		return

	if passing_group_count == 0:
		display_message(f"All test groups had 1 or more fail(s).",colour=RED, no_bullets=True)
	else:
		display_message(f"{pluralise('test group', passing_group_count)} ran without any fails.", colour=GREEN, no_bullets=True)

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