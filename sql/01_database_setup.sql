
-- ============================================================
-- PROJECT: TELECOM CUSTOMER CHURN ANALYTICS
-- FILE: 01_database_setup.sql
-- PURPOSE: Create database and customer table
-- ============================================================

-- 1. Create database
CREATE DATABASE IF NOT EXISTS telecom_churn_analytics;

-- 2. Select database
USE telecom_churn_analytics;

-- 3. Create customers table
-- This structure documents the cleaned dataset schema.
-- IF NOT EXISTS prevents replacing an existing imported table.

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    gender VARCHAR(10),
    senior_citizen VARCHAR(3),
    partner VARCHAR(5),
    dependents VARCHAR(5),
    tenure INT,
    phoneservice VARCHAR(5),
    multiplelines VARCHAR(30),
    internetservice VARCHAR(30),
    onlinesecurity VARCHAR(30),
    onlinebackup VARCHAR(30),
    deviceprotection VARCHAR(30),
    techsupport VARCHAR(30),
    streamingtv VARCHAR(30),
    streamingmovies VARCHAR(30),
    contract VARCHAR(30),
    paperlessbilling VARCHAR(5),
    paymentmethod VARCHAR(50),
    monthlycharges DECIMAL(10,2),
    totalcharges DECIMAL(10,2),
    churn VARCHAR(5)
);

-- 4. Verify selected database
SELECT DATABASE() AS current_database;

-- 5. Verify customer table
SHOW TABLES;

-- 6. Verify table structure
DESCRIBE customers;

-- 7. Verify imported records
SELECT COUNT(*) AS total_customers
FROM customers;
