drop database bank_management;
create database bank_management;
USE bank_management;

-- Create Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role ENUM('admin', 'staff', 'customer') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Customers Table
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create Accounts Table
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Create Support Requests Table
CREATE TABLE support_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    request_description TEXT NOT NULL,
    status ENUM('open', 'resolved') DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Create Transactions Table (optional)
-- This table can be used to track deposits, withdrawals, and transfers.
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_type ENUM('deposit', 'withdrawal', 'transfer') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);




-- User Table
-- CREATE TABLE users (
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     username VARCHAR(100) NOT NULL UNIQUE,
--     password_hash TEXT NOT NULL,
--     role ENUM('admin', 'staff', 'customer') NOT NULL
-- );


-- Customer Account Table
-- CREATE TABLE accounts (
--     account_id INT PRIMARY KEY AUTO_INCREMENT,
--     user_id INT,
--     account_number VARCHAR(20) UNIQUE,
--     balance DECIMAL(10, 2) DEFAULT 0,
--     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
-- );


-- Transactions Table
-- CREATE TABLE transactions (
--     transaction_id INT PRIMARY KEY AUTO_INCREMENT,
--     account_id INT,
--     transaction_type ENUM('deposit', 'withdrawal', 'transfer'),
--     amount DECIMAL(10, 2),
--     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
-- );


-- System Settings Table (for interest rates, transaction limits)
-- CREATE TABLE system_settings (
--     setting_id INT PRIMARY KEY AUTO_INCREMENT,
--     setting_name VARCHAR(100) UNIQUE,
--     setting_value DECIMAL(10, 2)
-- );
