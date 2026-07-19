# vaccine

User
 │
 ▼
CLI Parser
 │
 ▼
Target Analyzer
 │
 ▼
Injection Engine
 │
 ├── Boolean Tests
 │
 ├── Error Tests
 │
 └── Union Tests
 │
 ▼
Response Analyzer
 │
 ▼
DB Fingerprinter
 │
 ▼
Enumerator
 │
 ▼
Storage

---

vaccine/
│
├── main.py
│
├── core/
│   ├── scanner.py
│   ├── requester.py
│   ├── analyzer.py
│   └── storage.py
│
├── injections/
│   ├── boolean.py
│   ├── error.py
│   └── union.py
│
├── databases/
│   ├── mysql.py
│   ├── sqlite.py
│   └── fingerprint.py
│
├── models/
│   ├── target.py
│   ├── result.py
│   └── vulnerability.py
│
└── data/
    └── vaccine.json

## Websites
https://github.com/WebGoat/WebGoat
WARNING 1: While running this program your machine will be extremely vulnerable to attack. You should disconnect from the Internet while using this program.

docker run --rm -it -p 4280:80 vulnerables/web-dvwa
login: admin
password: password
create database

https://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet
