import bentests as b

class FloatTests(b.testGroup):
	def testAlmostRight(self):
		b.assertAlmostEquals(1.0001,1,error_margin=3)

class ArithmeticTests(b.testGroup):
	def testSubtraction(self):
		b.assertEquals(1,2-1)
	
	def testZeroDivision(self):
		with b.assertRaises(ZeroDivisionError):
			v = 1/0 


b.test_all(FloatTests, ArithmeticTests, stats_amount="high")


