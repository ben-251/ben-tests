import colorama
import sys
import pprint
from io import StringIO
from enum import Enum, auto
from typing import Any, Callable, Iterable
from contextlib import redirect_stdout
from functools import singledispatchmethod
from bentests.display import Printer


CLEAR = colorama.Style.RESET_ALL
GREEN = colour = colorama.Fore.GREEN
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW

class Colour:
	Fore: str
	Back: str

	def __init__(self,name):
		self.Fore = ""
		self.Back = ""
		self.Name = name
	
	def SetFore(self,r: int,g:int, b:int):
		'''
		Assigns the foreground colour of the text to the rgb value provided
		'''
		self.Fore = f'\x1b[38;2;{r};{g};{b}m'

	def SetBack(self,r: int,g:int, b:int):
		'''
		Assigns the background colour of the text to the rgb value provided
		'''
		self.Back =  f'\x1b[48;2;{r};{g};{b}m'
	
	def __str__(self):
		return self.Fore + self.Back
	
GREEN, YELLOW, RED =  [Colour(name) for name in ["green","yellow","red"]]
GREEN.SetFore(147, 250, 102)
YELLOW.SetFore(255, 211, 96)
RED.SetFore(252, 95, 108)

class AssertType(Enum):
	EQUALS = auto()
	ALMOST_EQUALS = auto()
	RAISES = auto()
	DEFAULT = auto()

printer = Printer()

def catch_output(func:Callable, *args, **kwargs):
	buffer = StringIO()
	with redirect_stdout(buffer):
		func(*args, **kwargs)
	return buffer.getvalue()

def catch_pretty_output(value):
	custom_pprint = True
	if custom_pprint:
		output = catch_output(printer.pretty_print, value)
	else:
		output = catch_output(pprint.pprint, value, underscore_numbers=True)
	return output

class TestFail(Exception):
	def __init__(self, actual, expected):
		self.actual = actual
		self.expected = expected
	
	def __str__(self) -> str:
		# print the error message. will then be overriden for raises errors
		return f"{RED}{' '*4}Failed.{CLEAR}"

class EqualsFailError(TestFail):
	def __init__(self,actual, expected):
		super().__init__(actual, expected)

	def __str__(self):
		actual_output = catch_pretty_output(self.actual)
		expected_output = catch_pretty_output(self.expected)
		
		return f"{RED}{' '*4}Failed. \n\tResult:   {actual_output}\n\tExpected: {expected_output}{CLEAR}"
	
	def convert_to_string(self, variable):
		if isinstance(variable, str):
			return f"\"{variable}{RED}\""
		else:
			return f"{str(variable)}{RED}"

class AlmostEqualFailError(EqualsFailError): # this could cause issues when i say isinstance and stuff.
	def __init__(self, actual, expected, error_margin):
		super().__init__(actual, expected)
		self.error_margin = error_margin
	
	def __str__(self):
		actual_rounded = round(self.actual, self.error_margin)
		expected_rounded = round(self.expected, self.error_margin)
		actual_output = catch_pretty_output(actual_rounded)
		expected_output = catch_pretty_output(expected_rounded)
		return f"{RED}{' '*4}Failed. \n\tResult:   {actual_output}\n\tExpected: {expected_output}{CLEAR}"

class RaisesFailError(TestFail):
	def __init__(self,actual, expected):
		super().__init__(actual, expected)
	
	def __str__(self):
		if self.actual is None:
			return f"{RED}{' '*4}Did not raise {self.expected.__name__}.{CLEAR}"
		else:
			return f"{RED}{' '*4}Raises {self.actual.__name__}.{CLEAR}"


class NotRaisesFailError(TestFail):
	def __init__(self,actual, avoiding_exception):
		self.actual = actual
		self.avoiding_exception = avoiding_exception
	
	def __str__(self):
		return f"{RED}{' '*4}Raised {self.avoiding_exception.__name__}.{CLEAR}"

class IsNotTrueError(TestFail):
	def __init__(self, statement:str, result: Any):
		self.statement = statement
		self.result = result
	
	def __str__(self):
		return f"{RED}{' '*4}\"{self.statement}\" is not true."

class TestPass():
	def __init__(self):
		pass

	def __str__(self):
		return f"{GREEN}{' '*4}Ok.{CLEAR}"

class TestSkip():
	'''
	To match with the form of `TestPass`. Used when individual tests are skipped.
	'''
	def __init__(self):
		pass

	def __str__(self):
		return f"{YELLOW}{' '*4}Skipped.{CLEAR}"

def pluralise(word,count):
	'''
	Basic pluraliser. Adds s to words that are greater than 1 in quantity.
	Complex pluralisation to come.
	'''
	description = f"{count} {word}"
	return description if count == 1 else description + "s"