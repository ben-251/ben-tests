'''
A file to test the module before committing/pushing. Differs to example.py because that is primarily for end-users  
'''
from enum import Enum, auto
import sys
import os

# Add the parent directory of bentests to sys.path
sys.path.insert(0, os.path.abspath("."))

import importlib
import bentests.asserts
import bentests.tester

# Manually reload to reflect changes
importlib.reload(bentests.tester)
importlib.reload(bentests.asserts) 

from bentests.tester import testGroup, test_all
import bentests.asserts as asserts

class FloatTests(testGroup):
	def test_almost_right(self):
		asserts.assertAlmostEquals(1.00134758374583475,1,error_margin=3)

	def test_almost_almost_right(self):
		asserts.assertAlmostEquals(1.01478735475453453,1,error_margin=3)

class ArithmeticTests(testGroup):
	def testSubtraction(self):
		asserts.assertEquals(1,2-1)
	
	def test_incorrect_subtraction(self):
		asserts.assertEquals(1,1-1) # Fails.

	def testZeroDivision(self):
		with asserts.assertRaises(ZeroDivisionError):
			v = 1/0 # type: ignore

	def testRaisedException(self):
		with asserts.assertRaises(ZeroDivisionError):
			raise ZeroDivisionError("Zero")

	def testValueError(self):
		with asserts.assertRaises(ValueError):
			v = 1 # Fails.

class ExponentialTests(testGroup):
	def testSquares(self):
		asserts.assertEquals(4,2**2)
	
	def testCubes(self):
		asserts.assertEquals(125,5**3)
	
class MiscTests(testGroup):
	def testAdditionFail(self):
		asserts.assertEquals(1,1+1)

	def testNotRaiseFail(self):
		with asserts.assertNotRaises(ZeroDivisionError):
			v = 1/0

	def testNotRaiseSuccess(self):
		with asserts.assertNotRaises(ZeroDivisionError):
			v = 1
	
	def testNotSkipped(self, skip=False):
		asserts.assertEquals("1", 1)

	def testSkipped(self, skip=True):
		print("uh oh, still running!")
		asserts.assertEquals("1", 1)

class FancyOutputTests(testGroup):
	def testEnumList(self):
		class AnimalType(Enum):
			Dog = 0
			Cat = 1
		
		answer = []
		for i in range(4):
			answer.append(AnimalType(i%2))
		
		asserts.assertEquals([AnimalType.Dog, AnimalType.Dog, AnimalType.Cat], answer)


class EmptyTests(testGroup):
	...

test_all(FloatTests, ArithmeticTests, ExponentialTests, EmptyTests, MiscTests, FancyOutputTests)
