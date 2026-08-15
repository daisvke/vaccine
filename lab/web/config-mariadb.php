<?php

$conn = new mysqli(
    "mariadb",
    "lab",
    "lab",
    "VaccineLab"
);

if ($conn->connect_error) {
    die("MariaDB connection failed: " . $conn->connect_error);
}