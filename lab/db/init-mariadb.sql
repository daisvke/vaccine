/*
    STRING      => CHAR, VARCHAR, TEXT
    INTEGER     => TINYINT, SMALLINT, MEDIUMINT, INT, BIGINT
    BOOLEAN     => BOOLEAN
    UNSUPPORTED => FLOAT, DECIMAL
*/

CREATE DATABASE IF NOT EXISTS VaccineLab;

USE VaccineLab;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(100),

    -- Boolean
    is_admin BOOLEAN,

    -- Integer types
    small_number SMALLINT,
    medium_number MEDIUMINT,
    big_number BIGINT,
    tiny_number TINYINT,

    -- String types
    fixed_text CHAR(10),
    short_text VARCHAR(100),
    long_text TEXT,

    -- Numeric type
    float_value FLOAT
);

INSERT INTO users (
    username,
    password,
    is_admin,
    small_number,
    medium_number,
    big_number,
    tiny_number,
    fixed_text,
    short_text,
    long_text,
    float_value
)
VALUES
(
    'admin',
    'test',
    TRUE,
    100,
    100000,
    9000000000,
    10,
    'admin',
    'Administrator',
    'Administrator account',
    1.5
),
(
    'root',
    'rootpass',
    FALSE,
    200,
    200000,
    8000000000,
    20,
    'root',
    'Root User',
    'Root account',
    3.14159
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),

    -- Boolean
    is_available BOOLEAN,

    -- Integer types
    stock TINYINT,
    warehouse_stock SMALLINT,
    total_stock BIGINT,

    -- String types
    sku CHAR(10),
    description TEXT,

    -- Numeric types
    price DECIMAL(10, 2)
);

INSERT INTO products (
    name,
    is_available,
    stock,
    warehouse_stock,
    total_stock,
    sku,
    description,
    price
)
VALUES
(
    'Laptop',
    TRUE,
    10,
    100,
    10000,
    'LAPTOP001',
    'High-performance laptop',
    1299.99
),
(
    'Mouse',
    TRUE,
    50,
    500,
    50000,
    'MOUSE0001',
    'Wireless mouse',
    29.99
);
