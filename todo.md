
# Improvements/New Features
somehow allow nested tests, to be able to do something like this:
```python
class MovementTests(bt.testGroup):
	<subclass> LinearMovementTests(self):
		def test_simple_line(self): ...
		def test_tricky_line(self): ...
	<subclass> ParabolicMotionTests(self):
		def test_default_curve(self): ...
```

pretty print where possible?

# Bugs

- Doesn't actually do the errors if its not expected. for example:
```python
	def testWrongErrorType(self):
		with b.assertRaises(ValueError):
			v = 1**4/0
```
that should ideally still raise the valueerror as expected. the only work around i've come up with is this:

```python
	...
	def __str__(self):
		if self.actual is None:
			return f"{RED}{' '*4}Did not raise {self.expected.__name__}.{CLEAR}"
		else:
			raise self.actual
```
which is quite messy

