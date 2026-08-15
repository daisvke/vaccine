#!/bin/bash

TESTS=(
	# "GET|http://localhost:8080/user.php?id=1"
    "GET|http://localhost:8080/search.php?username=admin"
    # "POST|http://localhost:8080/product.php?id=1"

	# "GET|http://192.168.56.102/index.php?page=member&id=1&Submit=Submit"
	# "GET|http://192.168.56.102/?page=searchimg&id=1&Submit=Submit"

    # "GET|https://juice-shop.herokuapp.com/#/search?q=xxx"
)

for test in "${TESTS[@]}"
do
	# Feeds the value of $test into read,
	# split on `|` and read pieces into variables` METHOD` `URL` etc
    IFS='|' read -r METHOD URL USERNAME PASSWORD <<< "$test"

    echo -e "Testing: \033[33m$URL\033[0m"

    CMD=(
        python3 main.py
        -X "$METHOD"
        "$URL"
        --debug
	)

    "${CMD[@]}"

    echo
done
