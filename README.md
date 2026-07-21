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
```sh
# Run docker
sudo docker run --rm -it -p 4280:80 vulnerables/web-dvwa

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
