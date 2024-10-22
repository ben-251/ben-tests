# Ben-tests
Unit-testing Framework

## Installation
```bash
pip install bentests@git+https://github.com/ben-251/ben-tests.git
```

## Updating
```bash
pip install --upgrade --force-reinstall bentests@git+https://github.com/ben-251/ben-tests.git
```

## How to use
Import as with any library:
```python
import bentests as b
```

Group tests with classes:
```python
class FloatTests(b.testGroup):
	def testAlmostRight(self):
		b.assertAlmostEquals(1.0001,1,error_margin=3)

class ArithmeticTests(b.testGroup):
	def testSubtraction(self):
		b.assertEquals(1,2-1)
	
	def testZeroDivision(self):
		with b.assertRaises(ZeroDivisionError):
			v = 1/0 
```

Run tests in their groups:
```python
b.test_all(FloatTests, ArithmeticTests, stats_amount="high")
```

Example Output:
```
Starting tests..

Running tests in "FloatTests":
Test passed.

Running tests in "ArithmeticTests":
Both tests passed. 

Tests Complete.
3 Tests run in 2 Groups:
All Tests Passed.
```