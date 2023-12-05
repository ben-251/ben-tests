import bentests as b

class FloatTests(b.testGroup):
	def testAlmostRight(self):
		b.assertAlmostEquals(1.0001,1,error_margin=3)

class ArithmeticTests(b.testGroup):
	def testSubtraction(self):
		b.assertEquals(1,2-1)
	
	def testIncorrectSubtraction(self):
		b.assertEquals(1,1-1) # Fails.

	def testZeroDivision(self):
		with b.assertRaises(ZeroDivisionError):
			v = 1/0 # type: ignore

	def testRaisedException(self):
		with b.assertRaises(ZeroDivisionError):
			raise ZeroDivisionError("Zero")

	def testValueError(self):
		with b.assertRaises(ValueError):
			v = 1 # Fails.

class ExponentialTests(b.testGroup):
	def testSquares(self):
		b.assertEquals(4,2**2)
	
	def testCubes(self):
		b.assertEquals(125,5**3)
	
class AllFailingTests(b.testGroup):
	def testAddition(self):
		b.assertEquals(1,1+1)

	def testNotRaiseFail(self):
		with b.assertNotRaises(ZeroDivisionError):
			v = 1/0

	def testNotRaiseSuccess(self):
		with b.assertNotRaises(ZeroDivisionError):
			v = 1
class EmptyTests(b.testGroup):
	...

b.test_all(FloatTests, ExponentialTests, ArithmeticTests, EmptyTests, AllFailingTests)