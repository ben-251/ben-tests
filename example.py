import bentests as b

class ArithmeticTests(b.testCase):
	def testEquals(self):
		b.assertEquals(1,2-1)
		b.assertEquals(1,0) # Should Fail

	def testZeroDivision(self):
		with b.assertRaises(ZeroDivisionError):
			v = 1/0

		with b.assertRaises(ValueError):
			v = 1 # Should Fail

class ExponentialTests(b.testCase):
	def testSquares(self):
		b.assertEquals(4,2**2)
	
	def testCubes(self):
		b.assertEquals(125,5**3)

b.test_all(ExponentialTests, ArithmeticTests)