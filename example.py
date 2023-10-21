import bentests as b

def testEquals():
	b.assertEquals(1,2-1)
	b.assertEquals(1,0)

def testZeroDivision():
	with b.assertRaises(ZeroDivisionError):
		v = 1/0

	with b.assertRaises(ValueError):
		v = 1


testEquals()
testZeroDivision()