<?php

require "config-mariadb.php";

if ($_SERVER["REQUEST_METHOD"] !== "PATCH"
    && $_SERVER["REQUEST_METHOD"] !== "PUT"
    && $_SERVER["REQUEST_METHOD"] !== "DELETE"
) {
    http_response_code(405);
    exit("PATCH, PUT, or DELETE required");
}

parse_str(file_get_contents("php://input"), $data);

$username = $data["username"] ?? "";

$sql =
"SELECT id,username,password
FROM users
WHERE username = '$username'";

echo "<pre>";
echo "SQL:\n$sql\n\n";

$result = $conn->query($sql);

if ($result) {
    while ($row = $result->fetch_assoc()) {
        print_r($row);
    }
}
