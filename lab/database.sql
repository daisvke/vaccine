CREATE DATABASE IF NOT EXISTS sqli_lab;

USE sqli_lab;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(255)
);

INSERT INTO users(username,password)
VALUES
('root','3bf1114a986ba87ed28fc1b5884fc2f8'),
('admin','3bf1114a986ba87ed28fc1b5884fc2f8'),
('alice','alice123');

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price INT
);

INSERT INTO products(name,price)
VALUES
('Keyboard',50),
('Mouse',20),
('Laptop',1200);
