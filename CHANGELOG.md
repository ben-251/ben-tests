# Changelog

This project adheres to [Semantic Versioning](https://semver.org).

## [1.0.1]

### Added

### Changed

### Deprecated
importing asserts directly. for example:
```python
import bentests as bt
bt.assertEquals
```
will be replaced by
```python
from bentests import asserts
asserts.assertEquals

# OR

import bentests as bt
bt.asserts.assertEquals
```
This is to restrict how much of the module is call-able.

### Removed

### Fixed

### Changed

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

### Fixed

### Changed

