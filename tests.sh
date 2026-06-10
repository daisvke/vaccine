#!/bin/bash

TESTS=(
	"GET|http://192.168.56.101/index.php?page=member&id=1&Submit=Submit#"
    "POST|http://192.168.56.101/index.php?page=searchimg"
)

for test in "${TESTS[@]}"
do
	# Feeds the value of $test into read,
	# split on `|` and read pieces into variables` METHOD` `URL`
    IFS='|' read -r METHOD URL <<< "$test"

    echo -e "Testing: \033[33m$URL\033[0m"

    python3 main.py \
        -X "$METHOD" \
        "$URL" \
		--debug

    echo
done
