
use testdb;

CREATE DATABASE accounts;

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_holder VARCHAR(100),
    account_number VARCHAR(20) UNIQUE,
    password VARCHAR(100),       -- store hashed passwords ideally
    balance DECIMAL(12,2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from accounts;

CREATE DATABASE bank_accounts;

CREATE TABLE bank_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_holder VARCHAR(100),
    account_number VARCHAR(50) UNIQUE,
    password VARCHAR(100),
    balance DOUBLE DEFAULT 0
);

select * from bank_accounts;

