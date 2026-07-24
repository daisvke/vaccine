from enum import Enum
from dataclasses import dataclass


"""
Colors
"""

RESET = "\033[0m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"


"""
Injection context
"""

@dataclass
class InjectionContext:
    prefix: str
    suffix: str
    name: str


"""
Max values
"""

HEIGH_NAME_LENGTH = 64
HEIGH_ELEMENT_COUNT = 1000


"""
Etc
"""

DIFFER_LENGTH_BOOL = 50
DIFFER_LENGTH_COL_COUNT = 100
DIFF_MARKER = "DF4456DdgZERZERAA768"