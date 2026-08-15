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
Heigh values
"""

HEIGH_ELEMENT_NAME_LENGTH = 64
HEIGH_COL_VALUE_LENGTH = 1024
HEIGH_ELEMENT_COUNT = 1000


"""
Skipped system schemas (which are )not user-created application databases).
"""

SYSTEM_DATABASES = {
    "information_schema",
    "mysql",
    "performance_schema",
    "sys",
}


"""
Etc
"""

DIFFER_LENGTH_BOOL = 50
DIFFER_LENGTH_COL_COUNT = 100
DIFF_MARKER = "DF4456DdgZERZERAA768"
