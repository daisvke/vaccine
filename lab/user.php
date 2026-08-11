<?php

require "config.php";

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
