<?php

/* Unlike MariaDB, SQLite doesn't have an initialization container.
 * Create the database with:
 * docker compose exec web php /var/www/html/init-sqlite.php
 */

require "config/config-sqlite.php";

$conn->exec("
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
");

$conn->exec("
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
");

$conn->exec("
    INSERT INTO users (username, password)
    VALUES
        ('admin', 'test'),
        ('root', 'rootpass')
");

$conn->exec("
    INSERT INTO products (name)
    VALUES
        ('Laptop'),
        ('Mouse')
");

echo "SQLite database initialized.\n";
