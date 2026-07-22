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
Etc
"""

differ_length_bool = 50
differ_length_col_count = 100
diff_marker = "DF4456DdgZERZERAA768"