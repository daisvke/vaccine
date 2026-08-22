<?php

require "config/config-mariadb.php";

// Check the User-Agent
echo 'User-Agent: ' . ($_SERVER['HTTP_USER_AGENT'] ?? 'no user agent');

$id = $_GET["id"];

$sql =
"SELECT id,username,password
FROM users
WHERE id = $id";

echo "<pre>";
echo "SQL:\n$sql\n\n";

$result = $conn->query($sql);

while ($row = $result->fetch_assoc()) {
    print_r($row);
}
