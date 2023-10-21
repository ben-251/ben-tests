from .constants import *

def get_colour(state):
	if state == TestResult.FAIL:
		return RED_
	elif state == TestResult.PASS:
		return GREEN_
	
def clearColour():
	print(CLEAR)

def display_normal_message(state, actual, expected):
	colour = get_colour(state)
	if state == TestResult.PASS:
		print(f"{colour}Ok.",end = "")
		clearColour()
	else:
		print(f"{colour}Failed. \n\tResult: {actual}\n\tExpected: {expected}")
		clearColour()

def display_exception_message(state, actual_exception, expected_exception):
	colour = get_colour(state)

	if state == TestResult.PASS:
		print(f"{colour}Ok.", end="")
		clearColour()
	else:
		print(f"{colour}Did not raise {expected_exception.__name__}.")
		clearColour()