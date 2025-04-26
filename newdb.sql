-- Drop existing database if exists
DROP DATABASE IF EXISTS MYBMS;
CREATE DATABASE IF NOT EXISTS MYBMS;

USE MYBMS;

-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    user_type ENUM('admin', 'staff', 'customer') NOT NULL
);

-- BRANCH TABLE
CREATE TABLE IF NOT EXISTS branch (
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    branch_address VARCHAR(255),
    branch_city VARCHAR(100),
    branch_state VARCHAR(100),
    branch_zip VARCHAR(10),
    branch_phone VARCHAR(20)
);

-- ACCOUNTS TABLE
CREATE TABLE IF NOT EXISTS accounts (
    account_number INT auto_increment PRIMARY KEY NOT NULL,
    username VARCHAR(50),
    account_type ENUM('Savings', 'Current') NOT NULL default 'Savings',
    balance DECIMAL(65, 2) NOT NULL default 1000,
    opened_date DATETIME not null DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Active', 'Closed', 'Suspended') NOT NULL default 'Active',
    branch_id INT not null,
    last_transaction_date DATETIME NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(10) NOT NULL,
    dob DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    email VARCHAR(100),
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
);

-- TRANSACTION HISTORY TABLE
CREATE TABLE IF NOT EXISTS transaction_history (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number INT NOT NULL,
    transaction_date DATE,
    transaction_time TIME,
    transaction_type ENUM('Deposit', 'Withdrawal', 'Transfer') NOT NULL,
    amount DECIMAL(65, 2) NOT NULL,
    balance_before DECIMAL(65, 2) NOT NULL,
    balance_after DECIMAL(65, 2) NOT NULL,
    target_account_number INT,
    description VARCHAR(255),
    FOREIGN KEY (account_number) REFERENCES accounts(account_number) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (target_account_number) REFERENCES accounts(account_number) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE interest_fee_management (
    interest_rate DECIMAL(5, 2) NOT NULL default 6.5,
    fee DECIMAL(10, 2) NOT NULL default 230,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


DELIMITER //

CREATE TRIGGER before_insert_transaction
BEFORE INSERT ON transaction_history
FOR EACH ROW
BEGIN
    IF NEW.transaction_date IS NULL THEN
        SET NEW.transaction_date = CURDATE();
    END IF;
    IF NEW.transaction_time IS NULL THEN
        SET NEW.transaction_time = CURTIME();
    END IF;
END;

//
DELIMITER ;

-- TRIGGER TO DELETE USER WHEN ACCOUNT IS DELETED
DELIMITER //
CREATE TRIGGER after_account_delete
AFTER DELETE ON accounts
FOR EACH ROW
BEGIN
    DELETE FROM users WHERE username = OLD.username;
END;
//
DELIMITER ;

-- STORED PROCEDURE TO UPDATE USERNAME
DELIMITER //
CREATE PROCEDURE UpdateUsername(IN old_username VARCHAR(50), IN new_username VARCHAR(50))
BEGIN
    -- Check if the new username exists in the users table
    IF EXISTS (SELECT 1 FROM users WHERE username = old_username) THEN
        -- Update username in the users table
        UPDATE users
        SET username = new_username
        WHERE username = old_username;
	ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'New username does not exist in users table';
    END IF;
END;
//
DELIMITER ;

-- TRIGGER TO UPDATE USERNAME IN USERS TABLE WHEN UPDATED IN ACCOUNTS TABLE
DELIMITER //
CREATE TRIGGER before_account_update
BEFORE UPDATE ON accounts
FOR EACH ROW
BEGIN
	CALL UpdateUsername(OLD.username, NEW.username);
END;
//
DELIMITER ;


