use mybms;

-- INSERT INTO USERS TABLE
-- INSERT INTO users (username, password, user_type) VALUES
-- ('admin', 'admin', 'admin');


-- alter table branch auto_increment = 301 ;

-- INSERT INTO BRANCH TABLE
-- INSERT INTO branch (branch_name, branch_address, branch_city, branch_state, branch_zip, branch_phone) VALUES
-- ('Anand Branch', 'Amul Road, Anand - 388001', 'Anand', 'Gujarat', '388001', '9999999999'),
-- ('V.V. Nagar Branch', 'A.V. Road, Anand - 388001', 'V.V. Nagar', 'Gujarat', '388120', '8888888888'),
-- ('Gamdi Branch', 'Gamdi, Anand - 388001', 'Gamdi', 'Gujarat', '388002', '7777777777'),
-- ('Karamsad Branch', 'Karamsad Road, Karamsad - 388122', 'Karamsad', 'Gujarat', '388122', '6666666666');

-- alter table accounts auto_increment = 10001 ;

-- INSERT INTO ACCOUNTS TABLE
-- INSERT INTO accounts (username, balance, branch_id, first_name, middle_name, last_name, address, phone_number, dob, gender, email) VALUES
-- ('john'  , 'Savings', 1000.50, 'Active', 302, 'John'  , 'A', 'Doe' , '123 Main St'   , '5551234567', '1985-06-15', 'Male'  , 'johndoe@gmail.com'),
-- ('jane'  , 'Savings', 2500.75, 'Active', 303, 'Jane'  , 'B', 'Smith', '456 Elm St'   , '5552345678', '1990-09-20', 'Female', 'janesmith@gmail.com'),
-- ('om'    , 'Current', 500.00 , 'Active', 302, 'Om'    , 'J', 'Patel', '123 Main St'  , '5551234567', '1985-06-15', 'Male'  , 'ome@gmail.com'),
-- ('ap'    , 'Savings', 1200.30, 'Active', 303, 'Aayush', 'A', 'Patel', '789 Maple Ave', '5553456789', '1980-12-01', 'Male'  , 'apr@gmail.com');
-- ('hkp' , 1200.30, 303, 'hjh', 'A', 'Patel', '543 Kaple Avete', '2121212121', '1960-12-21', 'Female'  , 'tetr@gmail.com');

-- INSERT INTO TRANSACTION HISTORY TABLE
-- INSERT INTO transaction_history (account_number, transaction_type, amount, balance_before, balance_after, target_account_number, description) VALUES
-- (10005, 'Deposit', 500.00, 500.50, 1000.50, NULL, 'Initial deposit'),
-- (10006, 'Withdrawal', 200.00, 2700.75, 2500.75, NULL, 'ATM withdrawal'),
-- (10007, 'Transfer', 100.00, 600.00, 500.00, 10006, 'Transfer to another account'),
-- (10008, 'Deposit', 1200.30, 0.00, 1200.30, NULL, 'Account opening deposit');

-- select * from users;
-- select * from branch;
-- select * from accounts;
-- select * from transaction_history;

-- DELETE FROM accounts
-- WHERE account_number = 'ACC10003';

-- UPDATE accounts
-- SET username = 'harsh'
-- WHERE account_number = 'ACC10001';

-- DELETE FROM users
-- WHERE username = 'staff';


-- ALTER TABLE accounts
-- ADD COLUMN interest_rate DECIMAL(5, 2) DEFAULT 0.00,
-- ADD COLUMN fee DECIMAL(10, 2) DEFAULT 0.00;

-- alter table accounts auto_increment = 10001 ;




-- delete from accounts where account_number=10010;

-- UPDATE accounts SET first_name = "Chandubhai", middle_name = "Manibhai", last_name = "Patel", phone_number = 1234512345, 
-- email = "chandubhai@gmail.com", address = "Gamdi, anand", account_type = "Current", username = "chandu"
-- WHERE account_number = 10011;
                
select * from users;
select * from branch;
select * from accounts;
select * from transaction_history;
select * from interest_fee_management;
