<?php

require "config/config-mssql.php";

$username = $_GET["username"] ?? "";

$sql = "
SELECT id, username, password
FROM users
WHERE username = '$username'
";

echo "<pre>";
echo "SQL:\n$sql\n\n";

$stmt = sqlsrv_query($conn, $sql);

if ($stmt === false) {
    print_r(sqlsrv_errors());
    exit;
}

while ($row = sqlsrv_fetch_array($stmt, SQLSRV_FETCH_ASSOC)) {
    print_r($row);
}
