CREATE DATABASE StockBrokerage;
USE StockBrokerage;

-- Create the 'investor' table
CREATE TABLE investor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL
);

-- Create the 'stock' table
CREATE TABLE stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stockname VARCHAR(100) NOT NULL,
    abbreviation VARCHAR(10) NOT NULL,
    currentprice DECIMAL(10, 2) NOT NULL
);

-- Create the 'bond' table
CREATE TABLE bond (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bondname VARCHAR(100) NOT NULL,
    abbreviation VARCHAR(10) NOT NULL,
    currentprice DECIMAL(10, 2) NOT NULL
);

-- Create the 'stocktransaction' table
CREATE TABLE stocktransaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    investorid INT NOT NULL,
    stockid INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (investorid) REFERENCES investor(id) ON DELETE CASCADE,
    FOREIGN KEY (stockid) REFERENCES stock(id) ON DELETE CASCADE
);

-- Create the 'bondtransaction' table
CREATE TABLE bondtransaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    investorid INT NOT NULL,
    bondid INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (investorid) REFERENCES investor(id) ON DELETE CASCADE,
    FOREIGN KEY (bondid) REFERENCES bond(id) ON DELETE CASCADE
);

-- Insert records into 'investor' table
INSERT INTO investor (firstname, lastname) 
VALUES 
    ('John', 'Doe'),
    ('Jane', 'Smith'),
    ('Michael', 'Johnson');

-- Insert records into 'stock' table
INSERT INTO stock (stockname, abbreviation, currentprice) 
VALUES 
    ('Apple Inc.', 'AAPL', 175.00),
    ('Tesla Inc.', 'TSLA', 800.50),
    ('Amazon.com', 'AMZN', 3300.75);

-- Insert records into 'bond' table
INSERT INTO bond (bondname, abbreviation, currentprice) 
VALUES 
    ('US Treasury 10-Year', 'UST10Y', 1000.00),
    ('Corporate Bond A', 'CBA', 900.50),
    ('Municipal Bond B', 'MBB', 850.25);

-- Insert records into 'stocktransaction' table
INSERT INTO stocktransaction (investorid, stockid, quantity) 
VALUES 
    (1, 1, 10),   -- John Doe buys 10 Apple stocks
    (2, 2, 5),    -- Jane Smith buys 5 Tesla stocks
    (3, 3, -3);   -- Michael Johnson sells 3 Amazon stocks

-- Insert records into 'bondtransaction' table
INSERT INTO bondtransaction (investorid, bondid, quantity) 
VALUES 
    (1, 1, 2),    -- John Doe buys 2 US Treasury 10-Year bonds
    (2, 2, 1),    -- Jane Smith buys 1 Corporate Bond A
    (3, 3, -1);   -- Michael Johnson sells 1 Municipal Bond B
