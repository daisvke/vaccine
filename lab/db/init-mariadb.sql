CREATE DATABASE IF NOT EXISTS VaccineLab;

USE VaccineLab;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(100)
);

INSERT INTO users (username, password)
VALUES
    ('admin', 'test'),
    ('root', 'rootpass');

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50)
);

INSERT INTO products (name)
VALUES
    ('Laptop'),
    ('Mouse');
