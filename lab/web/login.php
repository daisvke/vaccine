<?php

require "config/config-mariadb.php";

$username = $_POST["username"] ?? "";
$password = $_POST["password"] ?? "";

$sql =
"SELECT *
FROM users
WHERE username='$username'
AND password='$password'";

echo "<pre>";
echo "SQL:\n$sql\n\n";

$result = $conn->query($sql);

if ($result->num_rows) {
    echo "Login successful\n\n";

    while ($row = $result->fetch_assoc()) {
        print_r($row);
    }
}
else {
    echo "Invalid credentials";
}
