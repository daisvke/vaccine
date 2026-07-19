#!/bin/bash

TESTS=(
#	"GET|http://192.168.56.101/index.php?page=member&id=1&Submit=Submit"
	"GET|http://192.168.56.101/?page=searchimg&id=1&Submit=Submit"
	"GET|http://localhost:4280/vulnerabilities/sqli/?id=1&Submit=Submit|http://localhost:4280/login.php|admin|password"
)

for test in "${TESTS[@]}"
do
	# Feeds the value of $test into read,
	# split on `|` and read pieces into variables` METHOD` `URL` etc
    IFS='|' read -r METHOD URL LOGIN_URL USERNAME PASSWORD <<< "$test"

    echo -e "Testing: \033[33m$URL\033[0m"

    CMD=(
        python3 main.py
        -X "$METHOD"
        "$URL"
        --debug
	)

    if [ -n "$LOGIN_URL" ]; then
        CMD+=(
            --login-url "$LOGIN_URL"
            --username "$USERNAME"
            --password "$PASSWORD"
        )
    fi

    "${CMD[@]}"

    echo
done
