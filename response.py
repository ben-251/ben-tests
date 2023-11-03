from typing import Any
from .constants import AssertType, TestResult
from dataclasses import dataclass

@dataclass
class Response():
	assertType: AssertType
	actual: Any
	expected: Any
	result: TestResult
	