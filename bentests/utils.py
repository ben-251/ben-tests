import colorama
from enum import Enum, auto
from typing import Any

CLEAR = colorama.Style.RESET_ALL
GREEN = colour = colorama.Fore.GREEN
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW

class Colour:
	Fore: str
	Back: str

	def __init__(self,name):
		# defined here to avoid issues with values being set for all colours
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
RED.SetFore(255, 56, 73)


class AssertType(Enum):
	EQUALS = auto()
	ALMOST_EQUALS = auto()
	RAISES = auto()
	DEFAULT = auto()

class TestFail(Exception):
	def __init__(self, actual, expected):
		self.actual = actual
		self.expected = expected
	
	def __str__(self) -> str:
		#print the error message. will then be overriden for raises errors
		return f"{RED}{' '*4}Failed.{CLEAR}"

class EqualsFailError(TestFail):
	def __init__(self,actual, expected):
		super().__init__(actual, expected)
	
	def __str__(self):
		actual_output = self.convert_to_string(self.actual)
		expected_output = self.convert_to_string(self.expected)
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
		actual_output = self.convert_to_string(round(self.actual, self.error_margin))
		expected_output = self.convert_to_string(round(self.expected, self.error_margin))
		return f"{RED}{' '*4}Failed. \n\tResult:   {actual_output}\n\tExpected: {expected_output}{CLEAR}"

class RaisesFailError(TestFail):
	def __init__(self,actual, expected):
		super().__init__(actual, expected)
	
	def __str__(self):
		if self.actual is None:
			return f"{RED}{' '*4}Did not raise {self.expected.__name__}.{CLEAR}"
		else:
			raise self.actual # ehhhhh quite a messyy way

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

def pluralise(word,count):
	description = f"{count} {word}"
	return description if count == 1 else description + "s"