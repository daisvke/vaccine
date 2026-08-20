# Vaccine

SQL injection (SQLi) detection and database enumeration tool written in Python.

Vaccine is a command-line tool designed to detect common SQL injection techniques and, where supported, enumerate database metadata and display the resulting database structure.

> **Disclaimer:** Vaccine is intended for authorized security testing, educational labs, and CTF environments. Only use it against systems you own or have explicit permission to test.

---

## TO DO
- do get_boolean in bool+time
- make more complex DBs
- Video

---

## Usage

Clone the repository and install the project's Python dependencies:

```sh
git clone <repository-url>
cd vaccine
```

Then run the CLI according to the project's entry point.

Usage:

```
main.py [-h] [-V VIEW] [-X {GET,POST,PATCH,PUT,DELETE}] [-o OUTPUT] [-D] [-A AGENT] [url]

positional arguments:
  url                   Target URL with its parameters.All methods need its data given in the form of valid parameters and values.Example: http://localhost:8080/user.php?id=1

options:
  -h, --help            show this help message and exit
  -V, --view VIEW       View the formatted results with the given result ID
  -X, --method {GET,POST,PATCH,PUT,DELETE}
                        HTTP method
  -o, --output OUTPUT   Output file
  -D, --debug           Enable debug mode
  -A, --agent AGENT     Custom User-Agent
```

---

## SQL Injection (SQLi)

Example vulnerable query:

```sql
SELECT first_name, last_name
FROM users
WHERE id = <input>;
```

Vaccine supports several SQL injection techniques:

* **Boolean-based SQLi**: injects a true/false condition into the query and infers information from differences in the application's responses.
* **UNION-based SQLi**: uses `UNION SELECT` to retrieve additional data when the original query is compatible with a UNION query.
* **Time-based SQLi**: uses conditional database delays and infers information from differences in response times.
* **Error-based SQLi**: relies on database error messages returned by the application to detect injection and identify the database engine.

---

## Current limitations

* No authentication/login handling.
* Designed for GET, POST, PUT, PATCH, and DELETE parameters.
* Database enumeration currently relies on MySQL/MariaDB-compatible `information_schema` metadata.
* Time-based detection is sensitive to network and server latency.
* Enumeration capabilities depend on the privileges available to the database user.

---

## Architecture

```text
User
 │
 ▼
CLI Parser
 │
 ▼
Injection Engine
 |     │
 |     ├── Error Test ─────┐
 |     |                   | ──▶ Target Analyser (detect context, column count)
 |     ├── Union Test ─────┘
 |     |
 |     ├── Boolean Test
 |     |
 |     └── Time Test
 │
 ▼
Response Analyzer
 │
 ▼
DB Fingerprinter ──┐
 |                 |   Union
 |                 ▼     |
 |          Injection Engine ────▶ Get databases
 |                 |                     |
 |              ┌── ──┐                  +-- get tables from information_schema.tables
 |              |     |                  |       WHERE table_schema = <that database>
 |            Bool  Time                 |
 |                                       +-- get columns from information_schema.columns
 |                                               WHERE table_schema = <that database>
 ▼
Table Display of the Database
 │
 ▼
Storage (JSON)
```

---

## Detection workflow

Vaccine first extracts the parameters supplied to the target endpoint and tests each parameter individually.

For a detected injection point, the tool attempts to determine the SQL context, for example whether the parameter is inserted into a quoted or unquoted expression.

The detected context is then used by subsequent injection tests.

For UNION-based injection, Vaccine determines the number of columns expected by the original query before attempting further enumeration.

When the required injection technique is available, Vaccine can enumerate database metadata using MySQL/MariaDB's `information_schema`.

### Blind extraction with Boolean and Time-based SQLi

When the application does not directly return the value being queried, Vaccine can infer it one character at a time using blind SQL injection.

For each character, the tool converts the character to its ASCII numeric value and uses a binary search over the printable ASCII range (32 to 126). Instead of testing every possible character, it asks questions such as whether the ASCII value is greater than the current midpoint.

For example, if the character is `A`, its ASCII value is `65`. The search can test progressively smaller ranges:

```text
32 ─────────────────────────────── 126
                  │
                > 79 ?  → false
        32 ───────────── 79
                  │
                > 55 ?  → true
                  │
                ...
                  │
                  65
```

With **Boolean-based SQLi**, the result of each comparison is inferred from a difference in the HTTP response. A true condition produces one observable response, while a false condition produces another. Binary search uses that true/false result to select the next half of the ASCII range.

With **Time-based SQLi**, the same binary-search algorithm is used, but the true/false result is communicated through response time instead of response content. A condition can trigger a database delay when true and avoid the delay when false. A significantly slower response therefore represents `true`, while a normal response represents `false`.

The process is repeated for every character position until the complete value has been reconstructed.

---

## Database enumeration

When database enumeration is possible, Vaccine can retrieve:

```text
Databases
   │
   ├── Tables
   │      │
   │      └── Columns
   │             │
   │             ├── Data type
   │             ├── Character maximum length
   │             └── Values
```

System schemas such as the following are skipped during normal database enumeration:

```text
information_schema
mysql
performance_schema
sys
```

Table and column metadata is retrieved from:

```sql
information_schema.tables
```

and:

```sql
information_schema.columns
```

---

## JSON output

Results can be stored in JSON for later inspection.

The database dump follows a structure similar to:

```json
{
  "database_name": {
    "table_name": {
      "column_name": {
        "data_types": [],
        "character_maximum_lengths": [],
        "values": []
      }
    }
  }
}
```

---

# Testing

For testing, it is recommended to use intentionally vulnerable applications in an isolated environment.

## Local lab

The project includes an intentionally vulnerable SQL injection lab in [`lab/`](lab/).

Build and start it from the project root:

```sh
cd lab
docker compose up --build
```

The lab is available at:

```text
http://localhost:8080
```

Open `http://localhost:8080/` to access the test page. It provides vulnerable parameters for testing different SQL injection contexts and techniques.

To stop the lab:

```sh
docker compose down
```

The lab is intended for local development and testing. Do not expose it to untrusted networks.

## DVWA

One option is **Damn Vulnerable Web Application (DVWA)**.

Start DVWA with Docker:

```sh
sudo docker run --rm -it -p 4280:80 vulnerables/web-dvwa
```

Then access:

```text
http://localhost:4280
```

If Docker is running inside WSL or a VM and the application needs to be accessed from the host, find the WSL/VM IP:

```sh
hostname -I
```

Example:

```text
192.168.47.192 172.17.0.1
```

The first address is the WSL/VM address in this example; the second is typically Docker's bridge gateway.

From the host, the application can then be accessed using:

```text
http://192.168.47.192:4280
```

From the Docker/WSL environment itself:

```text
http://localhost:4280
```

### DVWA setup

Default credentials:

```text
Login:    admin
Password: password
```

After logging in, complete the initial DVWA setup and create the database using the **Create / Reset Database** button.

> Keep vulnerable applications such as DVWA isolated from networks and systems you do not control.


## Tester

The project also includes a simple Bash script (`test.sh`) for running multiple test targets against Vaccine.

Run it with:

```sh
chmod +x tester.sh
./tester.sh
```

Add or uncomment entries in `TESTS` to test different endpoints and HTTP methods.

---

## SQL Injection reference

The following reference is useful when developing and testing MySQL/MariaDB SQL injection functionality:

[MySQL SQL Injection Cheat Sheet — Pentestmonkey](https://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet?utm_source=chatgpt.com)

---

## Legal notice

Vaccine is a security-testing tool. Do not use it against systems without authorization.

The author is not responsible for damage, data loss, service disruption, or unauthorized access resulting from misuse of this software.


sudo docker compose -f docker-compose.mssql.yml exec mssql \
  /opt/mssql-tools18/bin/sqlcmd \
  -S localhost \
  -U sa \
  -P 'VaccineLab123!' \
  -C \
  -d VaccineLab \
  -Q "SELECT id, username, password FROM users WHERE username = 'admin' UNION SELECT TOP 1 schema_name, NULL, NULL FROM information_schema.schemata"
