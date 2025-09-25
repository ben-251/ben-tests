'''
A file to test the display printer
'''
import sys
import os

sys.path.insert(0, os.path.abspath("."))

import importlib
import bentests.display

importlib.reload(bentests.display)

from bentests.display import Printer

class Animal:
	color:str
	height:int

printer = Printer(max_depth=4)

tests = [
	None,
	"hi",
	#2,
	[1,2,3,4],
	(1,2,3,4),
	[[(1,),(2,),(3,)],[(1,2),(2,3),(1,3)],[(1,2,3)]],
	Animal()
]


for test in tests:
	printer.pretty_print(test)
	print()