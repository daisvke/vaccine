<?php

require "config-mariadb.php";

$id = $_POST["id"] ?? "";

$sql =
"SELECT *
FROM products
WHERE id=$id";

echo "<pre>";
echo "SQL:\n$sql\n\n";

$result = $conn->query($sql);

while ($row = $result->fetch_assoc()) {
    print_r($row);
}
