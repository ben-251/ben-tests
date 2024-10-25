"""
Python self-made TDD framework.

This module contains classes that form can be used for testing a variety of functionalities,
for example assertEqual, assertRaises, etc.

Start all test methods with "test"

Example usage:
    import bentests as bt

	def testAdd():
		bt.assertEqual((1 + 2), 3)
		bt.assertEqual(0 + 1, 1)
	def testMultiply():
		bt.assertEqual((0 * 10), 0)
		bt.assertEqual((5 * 8), 40)
	def testZeroDivision():
		with bt.assertRaises(ZeroDivisionError):
			var = 1/0

    if __name__ == '__main__':
        bentests.main()
"""
from .tester import testGroup, test_all
# from .asserts import *