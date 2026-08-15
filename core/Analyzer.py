from core.Requester import HttpResponse
from utils.Logger import Logger

DATABASE_ERRORS = {
    "Microsoft SQL Server": [
        "unclosed quotation mark",
        "microsoft sql server",
        "sql server",
    ],
    "MariaDB": ["mariadb"],
    "MySQL": ["you have an error in your sql syntax", "mysql"],
    "SQLite": ["sqlite", "sqlite3::"],
    "Oracle": ["ora-", "oracle error"],
}


class Analyzer:
    def responses_differ(self, r1: HttpResponse, r2: HttpResponse, diff: int) -> bool:
        # Logger.debug(r1.body)
        # Logger.debug(r2.body)
        # Logger.debug(f"Diff: {len(r1.body)},  {len(r2.body)}, {diff}")

        if r1.status != r2.status:
            return True

        return abs(len(r1.body) - len(r2.body)) > diff

    def detect_database(self, response_body: str) -> str:
        body = response_body.lower()

        for database, signatures in DATABASE_ERRORS.items():
            for signature in signatures:
                if signature in body:
                    return database

        return "Unknown"

    def has_sql_error(self, response: HttpResponse):
        errors = [
            "unrecognized token",
            "ora-",

            # mysql/mariadb
            "in your sql syntax",
            "mariadb",
            "mysqli_sql_exception",
            "unknown column",
            "different number of columns",

            "syntax error",
            "unterminated quoted string",
            "unclosed quotation mark",

            # pdo sqlite
            "pdoexception",
            "general error",
            "no such function",
            "number of result columns",
        ]

        body = response.body.lower()
        # 		Logger.debug(f"body: {body}")
        return any(e in body for e in errors)

    def is_delayed(
        self,
        normal: HttpResponse,
        delayed: HttpResponse,
        sleep: float = 1.0,
    ) -> bool:
        delay = delayed.elapsed - normal.elapsed

        Logger.debug(
            f"Response time: normal={normal.elapsed:.3f}s, "
            f"test={delayed.elapsed:.3f}s, "
            f"difference={delay:.3f}s"
        )

        return delay >= sleep * 0.8
