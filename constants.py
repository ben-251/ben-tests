import colorama
from enum import Enum, auto

CLEAR = colorama.Style.RESET_ALL
GREEN = colour = colorama.Fore.GREEN
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN

class TestResult(Enum):
	PASS = auto()
	FAIL = auto()

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

class RaisesFailError(TestFail):
	def __init__(self,actual, expected):
		super().__init__(actual, expected)
	
	def __str__(self):
		return f"{RED}{' '*4}Did not raise {self.expected.__name__}.{CLEAR}"		