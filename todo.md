
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

pretty print where possible? (pretty print added now, but still need to fix the indentation, since every line needs to be extra indented)

for enums, I want to have pp(enum_instance) call enum_instance.__str__(), so maybe pprinting is not best

for all objects, I want to list properties if in full detail mode, so like
```bash
Expected:

```

# Bugs
- it currently can't compare something as simple as a list of numpy arrays, since the type check only checks if the elements are np arrays, then assumes no np otherwise
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

