<?php

$db_path = __DIR__ . "/data/VaccineLab.db";

$conn = new PDO("sqlite:" . $db_path);

$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);