from enum import Enum
from functools import singledispatchmethod
from typing import Any, Dict, Iterable, Tuple
import copy


class Printer:

	def __init__(self,max_depth:int=2,tab_count:int=1) -> None:
		self.max_depth = max_depth # in the future, I'll let this be picked by user during unit-testing
		self.TAB = " "*tab_count # this allows the option to have the user choose tab size

	def tabs(self, depth:int) -> str:
		'''
		generates custom tab character

		Parameters:
			depth (int): the current depth

		Returns:
			output_string (str): a string of spaces (or whatever the tab character is)
		'''
		return self.TAB * depth

	def tprint(self, value:Any, depth:int,end="",is_terminal=True): #TODO: make this take in a "type" avariable, probably type(value) <- orignal value before preparing for print, so that it can say "string" type: str.
		'''
		The print method, taking tabs into account.

		Parameters:
            value (Any): item to be printed
			max_depth (int): current depth (in terms of iterables, classes, etc)
			end (str): what to print at the end of the string
			is_terminal (bool): whether we are at the most-indented level of an iterable. 
			                    Counts as true if value is not an iterable, since individual items shouldn't be indented any extra.

        Returns:
            None

		'''
		# might be better to have this return a string, kinda like the way __str__ works, so that I can use it witout having to catch output. i'll think abt it
		printed_value = value
		if isinstance(printed_value, list) and not isinstance(printed_value, tuple):
			is_terminal = True
		if depth >= self.max_depth:
			value = "..." 
			is_terminal = True # overrides if at maximum allowed depth, since it's no longer treating it like an iterable
		print(
			f"{self.tabs(depth) if not is_terminal else ""}{value}",end=end
		)

	@singledispatchmethod
	def pretty_print(self, value:Any, depth:int=0,end=""):
		'''
		Prints a value nicely. Default is to print as expected.
		'''
		# if isinstance(value, Enum):
		# 	self.print_enum(self.)
		# elif _:
		# 	...
		output_value = value
		self.tprint(output_value, depth,end=end)

	@pretty_print.register
	def _(self, value:None, depth=0,end=""):
		self.tprint("<none>", depth,end=end)

	@pretty_print.register
	def _(self, value:str, depth=0,end=""):
		self.tprint(f'"{value}"', depth,end=end)

	@pretty_print.register
	def _(self, value:int, depth=0,end=""):
		self.tprint(value, depth,end=end)

	@pretty_print.register
	def _(self, value:float, depth=0,end=""):
		value_to_print = round(value, 4) #TODO: make this rounding value dependent on the error_margin
		self.tprint(value_to_print, depth,end=end)

	# @pretty_print.register
	# def _(self, value:Iterable,depth=1): # okay iterables don't work..
	# 	'''
	# 	generic iterables (if not a list or dict, etc)
	# 	'''
	# 	for element in copy.deepcopy(value): # deepcopying juuust in case
	# 		self.pretty_print(element, depth+1) # recursion go brrr (i'll see myself out...)

	def find_full_depth(self, iterable:Any) -> int:
		if isinstance(iterable,list) or isinstance(iterable,tuple):
			return 1 + max(self.find_full_depth(item) for item in iterable)
		else:
			return 0

	def print_iterable_inline(self, iterable, depth:int, brackets:str):
		open_bracket, close_bracket = brackets[0], brackets[1]
		print(f"{self.tabs(depth)}{open_bracket}",end="")
		for i, element in enumerate(iterable):
			if i != len(iterable) - 1:
				self.pretty_print(element, depth+1,end=", ")
			else:
				self.pretty_print(element, depth+1,end="")
		print(f"{close_bracket},")
	
	def print_iterable_indented(self, iterable, depth:int, brackets:str):
		open_bracket, close_bracket = brackets[0], brackets[1]
		print(f"{self.tabs(depth)}{open_bracket}",end="\n")
		for element in iterable:
			self.pretty_print(element, depth+1,end=",")
		print(f"{self.tabs(depth)}{close_bracket};")

	def pretty_print_iterable(self, iterable, depth:int, brackets="[]"):
		full_depth = self.find_full_depth(iterable)
		if depth >= full_depth or depth == 0: # might add extra reasons to do this soon
			self.print_iterable_inline(iterable, depth, brackets)
		else:
			self.print_iterable_indented(iterable, depth, brackets) 

	@pretty_print.register
	def _(self, iterable:tuple, depth=0,end=""):
		self.pretty_print_iterable(iterable,depth=depth,brackets="()")

	@pretty_print.register
	def _(self, iterable:list, depth=0,end=""):
		self.pretty_print_iterable(iterable,depth=depth,brackets="[]")

	@pretty_print.register
	def _(self, variable:Enum, depth=0,end=""):
		enum_type = variable.__class__.__name__
		output = f"{str(variable)} ({enum_type})"
		self.tprint(output, depth,end=end)
	
	@pretty_print.register
	def _(self, value:dict):
		pass

