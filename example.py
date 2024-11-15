from bentests import testGroup, test_all, asserts

class FloatTests(testGroup):
	def testAlmostRight(self):
		asserts.assertAlmostEquals(1.0001,1,error_margin=3)

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

class EmptyTests(testGroup):
	...

#b.test_all(FloatTests, ExponentialTests, ArithmeticTests, EmptyTests, MiscTests, stats_amount="high")
test_all(ArithmeticTests, ExponentialTests, EmptyTests, MiscTests)