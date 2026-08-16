<?php

require "config/config-sqlite.php";

$username = $_GET["username"] ?? "";

$sql =
"SELECT id, username, password
FROM users
WHERE username = '$username'";

echo "<pre>";
echo "SQL:\n$sql\n\n";

$result = $conn->query($sql);

while ($row = $result->fetch(PDO::FETCH_ASSOC)) {
    print_r($row);
}
