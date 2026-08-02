# vaccine

SQL injection (SQLi)

SELECT first_name, last_name
FROM users
WHERE id = <input>;

- Boolean SQLi: injects into the query's WHERE clause and infers information from different responses.
- UNION SQLi: appends another SELECT to return additional rows or values.
- Time SQLi: uses conditional delays.
- Error SQLi: relies on database error messages.

---
no login handling
---
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



Get databases
    |
    +-- skip information_schema/mysql/performance_schema/sys
    |
    +-- for each remaining database:
            |
            +-- get tables from information_schema.tables
            |       WHERE table_schema = <that database>
            |
            +-- get columns from information_schema.columns
                    WHERE table_schema = <that database>

## Websites
```sh
# Run docker
sudo docker run --rm -it -p 4280:80 vulnerables/web-dvwa

# If using WSL or VM

# Get WSL IP
hostname -I
> 192.168.47.192 172.17.0.1
192.168.47.192 is the WSL IP, the other is Docker's bridge gateway

Access with 192.168.47.192:4280 from host, from inside Docker use localhost:4280
```

- Enter these creds:
login: admin
password: password

- Click on button `create database` at the bottom of the page

---

https://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet
