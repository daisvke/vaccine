# vaccine

no login handling

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
