#!/bin/bash

# Parameters' values must be valid ones if you want complete tests

TESTS=(
    # MariaDB
	"GET|http://localhost:8080/user.php?id=1"
    # "PATCH|http://localhost:8080/methods.php?username=admin"
    # "PUT|http://localhost:8080/methods.php?username=admin"
    # "DELETE|http://localhost:8080/methods.php?username=admin"
    # "GET|http://localhost:8080/search.php?username=admin&password=test"
    # "POST|http://localhost:8080/product.php?id=1"

    # Microsoft Server SQL
    # "GET|http://localhost:8080/ms-sql-search.php?username=admin"

    # SQLite
    # "GET|http://localhost:8080/sq-lite-search.php?username=admin"
)

for test in "${TESTS[@]}"
do
	# Feeds the value of $test into read,
	# split on `|` and read pieces into variables` METHOD` `URL` etc
    IFS='|' read -r METHOD URL USERNAME PASSWORD <<< "$test"

    echo -e "Testing: \033[33m$URL\033[0m"

    # Test -A with user.php which prints the received user agent
    CMD=(
        python3 main.py
        -X "$METHOD"
        "$URL"
        -A "Custom User-Agent"
        --debug
	)

    "${CMD[@]}"

    echo
done
