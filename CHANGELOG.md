# Changelog

This project adheres to [Semantic Versioning](https://semver.org).

## [2.0.0]

### Added

### Changed
Function call structure. NOT BACKWARD COMPATIBLE
This was accidentally referred to as a **deprecation** in the previous version, when the change was already implemented. 
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
### Deprecated


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

