-- Create database for Stock Portfolio API
CREATE DATABASE IF NOT EXISTS stock_portfolio
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Show all databases
SHOW DATABASES;

-- Use the created database
USE stock_portfolio;

-- Show message
SELECT 'Database stock_portfolio created successfully!' AS message;