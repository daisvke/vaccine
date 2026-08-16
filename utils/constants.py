from dataclasses import dataclass

"""
Colors
"""

RESET = "\033[0m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
BOLD = "\033[1m"

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
Fingerprints of database engines
"""


@dataclass(frozen=True)
class DatabaseFingerprint:
    schema: str
    version: str
    sleep: str | None
    char: str | None


fingerprints = {
    "sqlite": DatabaseFingerprint(
        schema="sqlite_master",
        version="sqlite_version()",
        sleep=None,
        char="unicode(substr({expression},{digit},1))",
    ),
    "mysql_mariadb": DatabaseFingerprint(
        schema="information_schema",
        version="VERSION()",
        sleep="SLEEP({seconds})",  # Usage: `fingerprint.sleep.format(seconds=1)`
        char="ASCII(SUBSTRING({expression},{digit},1))",
    ),
    "mariadb": DatabaseFingerprint(
        schema="information_schema",
        version="VERSION()",
        sleep="SLEEP({seconds})",
        char="ASCII(SUBSTRING({expression},{digit},1))",
    ),
    "mssql": DatabaseFingerprint(
        schema="sys.tables",
        version="@@VERSION",
        sleep=None,
        char="ASCII(SUBSTRING({expression},{digit},1))",
    ),
}


"""
Etc
"""

DIFFER_LENGTH_BOOL = 50
DIFFER_LENGTH_COL_COUNT = 100
DIFF_MARKER = "DF4456DdgZERZERAA768"
