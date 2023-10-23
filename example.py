import bentests as b

class ArithmeticTests(b.testCase):
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
			v = 1 # Should Fail # type: ignore

class ExponentialTests(b.testCase):
	def testSquares(self):
		b.assertEquals(4,2**2)
	
	def testCubes(self):
		b.assertEquals(125,5**3)
	
	def testNestedExperiment(self):
		# I'm not sure what i expect to happen here this is just for fun :)
		with b.assertRaises(ZeroDivisionError):
			b.assertEquals(1/0, 1/0)

b.test_all(ExponentialTests, ArithmeticTests)