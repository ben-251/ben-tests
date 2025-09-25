# Changelog

This project adheres to [Semantic Versioning](https://semver.org).
## [2.4.7]
## Fixed
- Colour resets now to allow for coloured values to print without being affected by test result colours

## [2.4.6]
### Improved
- Enum's now print according to `__str__` 

## [2.4.5]
### Improved
- Added custom pretty print!

## [2.4.4]
### Improved
- Output of failing tests now passes through pretty print for a cleaner look.

### In Development
- Nested Test Groups
- diff feature


## [2.4.3]
### Improved 
- Autosuggestion for `stats_amount` will now show the options of "high", "low", and "none"

## [2.4.2]
### Changed
- Default behaviour is now to show all test results, even passes.

## [2.4.1]
### Improved
- Refactored the test-skip feature
- Added more detailed test-skip statistics

## [2.4.0]
### Added
- Option to disable individual tests via the "skip" keyword.

### In Development
- Recognition of individual skips in the final display: "3 test(s) force-skipped"

## [2.3.3]
### Fixed
- `assertRaises` no longer re-raises the error when an unexpected one is raised. Instead it displays "raised {unexpected error name}"

## [2.3.2]
### Fixed
- almostEqual only working for values of the same type (preventing the use of mpmath)
### Improved
- used allclose instead of manual closeness to allow for more accurate measure of closeness

## [2.3.1]
- changed almostEquals so that it can check any iterables of numbers, not just numpy arrays.


## [2.2.0]

### CHanged 
- changed function display to split words in function names to avoid bias of snake and camel (e.g "addNumbersTwice" -> "add-numbers-twice")

### In Development
- diff feature


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


