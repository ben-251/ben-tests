from typing import Any
import colorama

clear = colorama.Style.RESET_ALL
green = colour = colorama.Fore.GREEN
red = colorama.Fore.RED
cyan = colorama.Fore.CYAN


def get_colour(state):
	if state == "fail":
		return red
	elif state == "pass":
		return green
	
def display_message(state, actual, expected):
	colour = get_colour(state)
	if state == "pass":
		print(f"{colour}Ok.{clear}")
		...
	else:
		print(f"{colour}Failed. \nResult:\n{actual}\nExpected:\n{expected}{clear}")

def assertEquals(actual:Any,expected: Any):
	'''Passes only if both of the values are identical'''
	return actual == expected

def assertRaises(action, expected_exception: Exception):
	'''
		Fails test if the input exception is not raised.
		Sample use
		def testZeroDivision():
			with assert_raises(ZeroDivisionError):
				var = 1/0				
	'''
	try:
		action()
	except expected_exception:
		return True
	return False
