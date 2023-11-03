import colorama
from enum import Enum, auto

CLEAR = colorama.Style.RESET_ALL
GREEN = colour = colorama.Fore.GREEN
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN

class TestResult(Enum):
	PASS = auto()
	FAIL = auto()

class AssertType(Enum):
	EQUALS = auto()
	ALMOST_EQUALS = auto()
	RAISES = auto()
	DEFAULT = auto()