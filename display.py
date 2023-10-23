from .constants import *
from typing import Any, Type

def get_colour(state: TestResult):
	if state == TestResult.FAIL:
		return RED
	elif state == TestResult.PASS:
		return GREEN
	
def clearColour():
	print(CLEAR)

def display_normal_message(state: TestResult, actual: Any, expected: Any):
	colour = get_colour(state)
	if state == TestResult.PASS:
		print(f"{' '*4}{colour}Ok.",end = "")
		clearColour()
	else:
		print(f"{' '*4}{colour}Failed. \n\tResult: {actual}\n\tExpected: {expected}")
		clearColour()

def display_exception_message(state: TestResult, actual_exception: Type[Exception] | None, expected_exception: Type[Exception]):
	colour = get_colour(state)

	if state == TestResult.PASS:
		print(f"{' '*4}{colour}Ok.", end="")
		clearColour()
	else:
		print(f"{' '*4}{colour}Did not raise {expected_exception.__name__}.")
		clearColour()