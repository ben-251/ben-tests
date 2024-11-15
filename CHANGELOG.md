# Changelog

This project adheres to [Semantic Versioning](https://semver.org).


## [2.1.0]

### Added
- Support for camelCase and snake_case in function names

### Removed
- `assertIsTrue` removed with no replacement.

### In Development
- diff feature


## [2.0.0]
### Changed
Function call structure.
```python
import bentests as bt
bt.assertEquals
```
Must now be called by
```python
from bentests import asserts
asserts.assertEquals

# OR

import bentests as bt
bt.asserts.assertEquals
```
See example.py for a detailed demonstration.

### Suggested
- a diff feature, to show where the failing test result differs from expected (using colour) for iterables
- support for both camel and snake case in test method names (e.g `testAddition` vs `test_addition`) 

### In Development



## [1.0.0]

### Changed

- Move assert methods from the base level to the `asserts` submodule
- Lighten red in failing and error messages

### Deprecated

- `assertIsTrue` will be removed with no replacement.


