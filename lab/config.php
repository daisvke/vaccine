<?php

$conn = new mysqli(
    "db",
    "root",
    "root",
    "sqli_lab"
);

if ($conn->connect_error) {
    die($conn->connect_error);
}

$conn->set_charset("utf8");
