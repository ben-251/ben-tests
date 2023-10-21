import colorama
from enum import Enum, auto

CLEAR = colorama.Style.RESET_ALL
GREEN_ = colour = colorama.Fore.GREEN
RED_ = colorama.Fore.RED
CYAN_ = colorama.Fore.CYAN

class TestResult(Enum):
	PASS = auto()
	FAIL = auto()

