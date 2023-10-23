from .constants import *
from typing import Any, Type

class MessageDisplayer:
	def __init__(self, state, actual, expected):
		self.state = state
		self.actual = actual
		self.expected = expected
	
	def display_message(self):
		if self.state == TestResult.PASS:
			self.display_pass_message()
		else:
			self.display_fail_message()

	def display_pass_message(self):
		self.setColour(GREEN)
		print(f"{' '*4}Ok.")
		self.clearColour()
	
	def display_fail_message(self):
		self.setColour(RED)
		print(f"{' '*4}Failed.")
		self.clearColour()
	
	def clearColour(self):
		print(CLEAR, end="")

	def setColour(self, colour):
		print(colour, end = "")

class ExceptionMessageDisplayer(MessageDisplayer):
	def __init__(self, state, actual_exception: Type[Exception] | None, expected_exception: Type[Exception]):
		super().__init__(state, actual_exception, expected_exception)

	def display_message(self):
		return super().display_message()

	def display_pass_message(self):
		return super().display_pass_message() 
	
	def display_fail_message(self):
		self.setColour(RED)
		print(f"{' '*4}Did not raise {self.expected.__name__}.")
		self.clearColour()

class EqualsMessageDisplayer(MessageDisplayer):
	def __init__(self, state, actual: Any, expected: Any):
		super().__init__(state, actual, expected)
	
	def display_fail_message(self):
		self.setColour(RED)
		if isinstance(self.actual, str):
			actual_output = f"\"{self.actual}\""
		else:
			actual_output = str(self.actual) # possibly unncessary

		if isinstance(self.expected, str):
			expected_output = f"\"{self.expected}\""
		else:
			expected_output = str(self.expected)

		print(f"{' '*4}Failed. \n\tResult: {actual_output}\n\tExpected: {expected_output}")
		self.clearColour()