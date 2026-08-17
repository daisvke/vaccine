<?php

$dbDir = __DIR__ . "/../data";

if (!is_dir($dbDir) && !mkdir($dbDir, 0775, true)) {
    throw new RuntimeException("Unable to create SQLite database directory");
}

$dbFile = $dbDir . "/VaccineLab.db";

$conn = new PDO("sqlite:" . $dbFile);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
