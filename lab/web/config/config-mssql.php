<?php

$serverName = "mssql,1433";

$connectionOptions = [
    "Database" => "VaccineLab",
    "Uid" => "sa",
    "PWD" => "VaccineLab123!",
    "TrustServerCertificate" => true,
];

$conn = sqlsrv_connect($serverName, $connectionOptions);

if ($conn === false) {
    echo "<pre>";
    print_r(sqlsrv_errors());
    echo "</pre>";
    exit;
}