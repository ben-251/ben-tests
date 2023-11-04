import bentests as b

class ArithmeticTests(b.testGroup):
	def testSubtraction(self):
		b.assertEquals(1,2-1)
	
	def testWrong(self):
		b.assertEquals(1,0) # Should Fail

	def testZeroDivision(self):
		with b.assertRaises(ZeroDivisionError):
			v = 1/0 # type: ignore

	def testRaisedException(self):
		with b.assertRaises(ZeroDivisionError):
			raise ZeroDivisionError("Zero")

	def testValueError(self):
		with b.assertRaises(ValueError):
			v = 1 # Should Fail

class ExponentialTests(b.testGroup):
	def testSquares(self):
		b.assertEquals(4,2**2)
	
	def testCubes(self):
		b.assertEquals(125,5**3)
	
	def testNestedExperiment(self):
		# ooh just realised that happens because the zero division will stop it from getting to assert equals. this makes me want to make a assertNotRaises now
		with b.assertRaises(ZeroDivisionError):
			b.assertEquals(1, 1/0)

class AllFailingTests(b.testGroup):
	def testAddition(self):
		b.assertEquals(1,1+1)


class EmptyTests(b.testGroup):
	...

b.test_all(ExponentialTests, ArithmeticTests, EmptyTests)